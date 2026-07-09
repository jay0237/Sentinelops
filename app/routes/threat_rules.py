from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.security.rule_loader import load_rules
from app.security.redaction import redact_pii
from app.security.risk_score import calculate_risk

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

    @router.delete("/{rule_id}")
    def delete_rule(rule_id: int, db: Session = Depends(get_db)):

        rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()

        if not rule:
            return {"message": "Rule not found"}

            db.delete(rule)
            db.commit()

            return{
                "message" : "Rule Deleted Successfully"

            }

    @router.put("/{rule_id}")
    def update_rule( rule_id: int, rule: ThreatRuleCreate, db: Session = Depends(get_db)):

        db_rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()

        if not db_rule:
            return {"message": "Rule not found"}

            db_rule.keyword = rule.keyword
            db_rule.category = rule.category
            db_rule.severity = rule.severity
            db_rule.reason = rule.reason
            db_rule.is_active = rule.is_active

            db.commit()
            db.refresh(db_rule)

            return db_rule