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

@router.post("/", response_model=ThreatRuleResponse)
def create_rule( rule: ThreatRuleCreate, db: Session = Depends(get_db)):
    db_rule = ThreatRule(
        keyword=rule.keyword,
        category=rule.category,
        severity=rule.severity,
        reason=rule.reason,
        is_active=rule.is_active
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule