from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.config.database import engine
from app.config.base import Base
from app.config.deps import get_db

from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.user import UserCreate
from app.config.auth_deps import get_current_user
from app.middleware.guard import scan_prompt
from app.models.prompt_log import PromptLog
from sqlalchemy import func
from app.utils.pii_scanner import detect_pii
from app.utils.injection_detector import detect_prompt_injection

from app.config.api_key import verify_api_key

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest
from prometheus_client import Histogram

app = FastAPI()

REQUEST_COUNT = Counter(
    "sentinelops_api_requests_total",
    "Total API Requests"
)

SAFE_PROMPT_COUNT = Counter(
    "sentinelops_safe_prompts_total",
    "Total safe prompts"
)

BLOCKED_PROMPT_COUNT = Counter(
    "sentinelops_blocked_prompts_total",
    "Total blocked prompts"
)

HIGH_THREAT_COUNT = Counter(
    "sentinelops_high_threat_total",
    "Total high threat prompts"
)

REQUEST_DURATION = Histogram(
    "sentinelops_request_duration_seconds",
    "Duration of API requests in seconds"
)


limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

from app.utils.security import (
    hash_password,
    verify_password
)

from app.utils.auth import create_access_token

SAFE_PROMPT_COUNT = Counter(
        "sentinelops_safe_prompt_total",
        "Total safe prompts"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "SentinelOps API is Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelOps API",
        "version": "1.0.0"
    }


@app.get("/db-check")
def db_check():

    try:
        connection = engine.connect()
        connection.close()

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


from fastapi.security import OAuth2PasswordRequestForm


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        return {
            "error": "Invalid email or password"
        }

    password_valid = verify_password(
        form_data.password,
        existing_user.password
    )

    if not password_valid:
        return {
            "error": "Invalid email or password"
        }

    access_token = create_access_token(
        data={
            "user_id": existing_user.id,
            "email": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

import time

@app.post("/scan")
@limiter.limit("5/minute")
def scan_ai_prompt(
    request: Request,
    prompt: dict,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    start_time = time.time()

    REQUEST_COUNT.inc()

    text = prompt.get("text", "")

    result = scan_prompt(text)

    print(f"Scan result: {result}")
    result = scan_prompt(text)

    if result["safe"]:
        SAFE_PROMPT_COUNT.inc()
    else:
        BLOCKED_PROMPT_COUNT.inc()

    if result["threat_level"] == "high":
        HIGH_THREAT_COUNT.inc()
    
    log = PromptLog(
        prompt=text,
        status="safe" if result["safe"] else "blocked",
        reason=result["reason"]
    )

    db.add(log)
    db.commit()

    REQUEST_DURATION.observe(
        time.time() - start_time
    )

    return result

@app.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db)
):
    total_prompts = db.query(PromptLog).count()

    safe_prompts = db.query(PromptLog).filter(
        PromptLog.status == "safe"
    ).count()

    blocked_prompts = db.query(PromptLog).filter(
        PromptLog.status == "blocked"
    ).count()

    high_threats = blocked_prompts

    return {
        "total_prompts": total_prompts,
        "safe_prompts": safe_prompts,
        "blocked_prompts": blocked_prompts,
        "high_threats": high_threats
    }

@app.get("/logs")
def get_logs(
    status: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(PromptLog)
    if status:
        query = query.filter(
            PromptLog.status == status
        )

    logs = query.all()

    return logs


@app.get("/export-injection")
def export_logs(
    db: Session = Depends(get_db)
):
    logs = db.query(PromptLog).all()

    exported_logs = []

    for log in logs:

        exported_logs.append({
            "id": log.id,
            "prompt": log.prompt,
            "status": log.status,
            "reason": log.reason
        })

    return {
        "logs": exported_logs
    }

@app.post("/detect-pii")
def detect_pii_endpoint(data: dict):

    result = detect_pii(data["text"])

    return {
        "pii_detected": result
    }


@app.post("/detect-injection")
def detect_injection(data: dict):

    result = detect_prompt_injection(
        data["text"]
        )

    return result

@app.get("/admin/stats")
def admin_stats(
    db: Session = Depends(get_db)
):

    total_logs = db.query(PromptLog).count()

    blocked_logs = db.query(PromptLog).filter(
        PromptLog.status == "blocked"
    ).count()

    safe_logs = db.query(PromptLog).filter(
        PromptLog.status == "safe"
    ).count()

    high_threats = db.query(PromptLog).filter(
        PromptLog.reason.contains("bypass")
    ).count()

    return {
        "total_logs" : total_logs,
        "blocked_logs" : blocked_logs,
        "safe_logs" : safe_logs,
        "high_threats" : high_threats
    }

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )