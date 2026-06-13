from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.config.database import engine
from app.config.base import Base
from app.config.deps import get_db

from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware

from app.security_rules import RULES
from app.schemas.user import UserCreate
from app.config.auth_deps import get_current_user
from app.middleware.guard import scan_prompt
from app.models.prompt_log import PromptLog
from sqlalchemy import func
from app.utils.pii_scanner import detect_pii
from app.utils.injection_detector import detect_prompt_injection

from app.config.api_key import verify_api_key
from app.middleware.security_middleware import SecurityMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest
from prometheus_client import Histogram
from fastapi import UploadFile, File 
from app.models.api_key import ApiKey
import secrets

app = FastAPI()

app.add_middleware(SecurityMiddleware)

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

    text = prompt.get("text", "").lower()
    result = None

    for rule in RULES:
        if rule["keyword"] in text.lower():
            result = {
                "safe": False,
                "threat_level": rule["severity"],
                "reason": rule["reason"]
            }
            break

    if result is None:
        if "bypass authentication" in text:
            result = {
                "safe": False,
                "threat_level": "high",
                "reason": "Authentication Bypass"
            }

        elif "ignore previous instructions" in text:
            result = {
                "safe": False,
                "threat_level": "medium",
                "reason": "Prompt Injection"
            }

        else:
            result = {
                "safe": True,
                "threat_level": "low",
                "reason": "Prompt is Safe"
            }

    if result["safe"]:
        SAFE_PROMPT_COUNT.inc()
    else:
        BLOCKED_PROMPT_COUNT.inc()

    if result["threat_level"] in ["high", "critical"]:
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
    limit: int = 20,
    status: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(PromptLog)

    if status:
        query = query.filter(
            PromptLog.status == status
        )

    logs = (
        query
        .order_by(PromptLog.id.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": log.id,
            "prompt": log.prompt,
            "status": log.status,
            "reason": log.reason
        }
        for log in logs
    ]
    

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

@app.get("/health")
def health_check():
    return {
        "status" : "healthy",
        "services": "Sentinelops",
        "database": "connected"
    }

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total = db.query(PromptLog).count()

    safe = db.query(PromptLog).filter(
        PromptLog.status == "safe"
    ).count()

    blocked = db.query(PromptLog).filter(
        PromptLog.status == "blocked"
    ).count()

    high_threat = db.query(PromptLog).filter(
        PromptLog.reason != "Prompt is Safe"
    ).count()

    return {
        "total_prompts": total,
        "safe": safe,
        "blocked": blocked,
        "high_threat": high_threat
    }


@app.post("/scan-file")
async def scan_file(
    file: UploadFile = File(...)
):

    content = await file.read()

    text = content.decode("utf-8", errors="ignore")

    result = scan_prompt(text)

    return {
        "filename": file.filename,
        "result": result,
        "scan_result": result
    }

@app.get("/threat-summary")
def threat_summary( db: Session = Depends (get_db)):

    return {
        "low": db.query(PromptLog).filter(
            PromptLog.reason == "Prompt is Safe"
        
        ).count(),

        "high": db.query(PromptLog).filter(
            PromptLog.reason.contains("Authentication")

        ).count(),

        "critical": db.query(PromptLog).filter(
            PromptLog.reason.contains("Malware")
        ).count()
    }

@app.get("/threat-categories")
def threat_categories(
    db: Session = Depends(get_db)
):

    malware = db.query(PromptLog).filter(
    PromptLog.reason.contains("Malware")
    ).count()

    prompt_injection = db.query(PromptLog).filter(
    PromptLog.reason.contains("Prompt Injection")
    ).count()

    access_control = db.query(PromptLog).filter(
    PromptLog.reason.contains("Access Control")
    ).count()

    return {
    "malware": malware,
    "prompt_injection": prompt_injection,
    "access_control": access_control
}

@app.post("/generate-api-key")
def generate_api_key(
    owner: str,
    db: Session = Depends(get_db)
):

