from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.threat_rule import ThreatRule
from app.schemas.threat_rule import ThreatRuleCreate, ThreatRuleResponse

router = APIRouter(prefix="/rules", tags=["Threat Rules"])


@router.post("/", response_model=ThreatRuleResponse)
def create_rule(rule: ThreatRuleCreate, db: Session = Depends(get_db)):
    db_rule = ThreatRule(
        keyword=rule.keyword,
        category=rule.category,
        severity=rule.severity,
        reason=rule.reason,
        is_active=rule.is_active,
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.get("/", response_model=list[ThreatRuleResponse])
def list_rules(db: Session = Depends(get_db)):
    return db.query(ThreatRule).order_by(ThreatRule.id.desc()).all()


@router.get("/{rule_id}", response_model=ThreatRuleResponse)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.put("/{rule_id}", response_model=ThreatRuleResponse)
def update_rule(rule_id: int, rule: ThreatRuleCreate, db: Session = Depends(get_db)):
    db_rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db_rule.keyword = rule.keyword
    db_rule.category = rule.category
    db_rule.severity = rule.severity
    db_rule.reason = rule.reason
    db_rule.is_active = rule.is_active

    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted successfully"}


@router.patch("/{rule_id}/toggle", response_model=ThreatRuleResponse)
def toggle_rule_active(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    rule.is_active = not rule.is_active
    db.commit()
    db.refresh(rule)
    return rule
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.threat_rule import ThreatRule
from app.schemas.threat_rule import ThreatRuleCreate, ThreatRuleResponse

router = APIRouter(prefix="/rules", tags=["Threat Rules"])


@router.post("/", response_model=ThreatRuleResponse)
def create_rule(rule: ThreatRuleCreate, db: Session = Depends(get_db)):
    db_rule = ThreatRule(
        keyword=rule.keyword,
        category=rule.category,
        severity=rule.severity,
        reason=rule.reason,
        is_active=rule.is_active,
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()

    return {"message": "Rule deleted successfully"}


@router.put("/{rule_id}", response_model=ThreatRuleResponse)
def update_rule(
    rule_id: int,
    rule: ThreatRuleCreate,
    db: Session = Depends(get_db),
):
    db_rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()

    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db_rule.keyword = rule.keyword
    db_rule.category = rule.category
    db_rule.severity = rule.severity
    db_rule.reason = rule.reason
    db_rule.is_active = rule.is_active

    db.commit()
    db.refresh(db_rule)

    return db_rule


@router.patch("/{rule_id}/toggle", response_model=ThreatRuleResponse)
def toggle_rule_active(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()

    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    rule.is_active = not rule.is_active
    db.commit()
    db.refresh(rule)

    return rule
