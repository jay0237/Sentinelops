from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.prompt_log import PromptLog

router = APIRouter()


@router.get("/analytics")
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

    malware_count = db.query(PromptLog).filter(
        PromptLog.reason == "Malware Detected"
    ).count()

    injection_count = db.query(PromptLog).filter(
        PromptLog.reason == "Prompt Injection"
    ).count()

    auth_bypass_count = db.query(PromptLog).filter(
        PromptLog.reason == "Authentication Bypass"
    ).count()

    return {
        "total_prompts": total_prompts,
        "safe_prompts": safe_prompts,
        "blocked_prompts": blocked_prompts,
        "high_threats": high_threats,
        "malware_count": malware_count,
        "injection_count": injection_count,
        "auth_bypass_count": auth_bypass_count
    }


@router.get("/logs")
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


@router.get("/export-injection")
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


@router.get("/stats")
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


@router.get("/threat-history")
def threat_history(db: Session = Depends(get_db)):
    logs = db.query(PromptLog).all()

    history = []

    for log in logs:
        history.append({
            "id": log.id,
            "prompt": log.prompt,
            "status": log.status,
            "reason": log.reason,
            "severity": log.severity,
            "category": log.category
        })

    return history


@router.get("/threat-summary")
def threat_summary(db: Session = Depends(get_db)):

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


@router.get("/threat-categories")
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


@router.get("/threat-summary-by-category")
def threat_summary_by_category(db: Session = Depends(get_db)):

    malware = db.query(PromptLog).filter(
        PromptLog.category == "Malware"
    ).count()

    injection = db.query(PromptLog).filter(
        PromptLog.category == "Prompt Injection"
    ).count()

    auth_bypass = db.query(PromptLog).filter(
        PromptLog.category == "Authentication Bypass"
    ).count()

    return {
        "malware": malware,
        "prompt_injection": injection,
        "authentication_bypass": auth_bypass
    }
