from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.threat_rule import ThreatRule
from app.schemas.threat_rule (
        ThreardRuleCreate,
        ThreatRuleResponse,
)

router  = APIRouter(prefix=/"rules", tags=["Threat Rules"])

def get_db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()
