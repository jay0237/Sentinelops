from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.prompt_log import PromptLog

router = APIRouter()


@router.get("/admin/stats")
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
        "total_logs": total_logs,
        "blocked_logs": blocked_logs,
        "safe_logs": safe_logs,
        "high_threats": high_threats
    }
