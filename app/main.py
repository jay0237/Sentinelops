from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.config.database import engine
from app.config.base import Base
from app.config.deps import get_db

from app.models.user import User

from app.schemas.user import UserCreate
from app.config.auth_deps import get_current_user
from app.middleware.guard import scan_prompt
from app.models.prompt_log import PromptLog
from sqlalchemy import func
from app.utils.pii_scanner import detect_pii
from app.utils.injection_detector import detect_prompt_injection


from app.utils.security import (
    hash_password,
    verify_password
)

from app.utils.auth import create_access_token


app = FastAPI()

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


@app.post("/scan")
def scan_ai_prompt(
    prompt: dict,
    db: Session = Depends(get_db)
):

    result = scan_prompt(prompt["text"])

    log = PromptLog(
        prompt=prompt["text"],
        status="safe" if result["safe"] else "blocked",
        reason=result["reason"]
    )

    db.add(log)
    db.commit()

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

    return {
        "total_prompts": total_prompts,
        "safe_prompts": safe_prompts,
        "blocked_prompts": blocked_prompts,
        "high_threats": high_threats,
        "security_score": (
            safe_prompts / total_prompts *100
            if total_prompts > 0 else 100
        )
    }

@app.get("/logs")
def get_logs(
    db: Session = Depends(get_db)
):

    logs = db.query(PromptLog).all()

    return logs

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
                   