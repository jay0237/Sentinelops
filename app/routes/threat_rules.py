from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.threat_rule import ThreatRule
from app.schemas.threat_rule import ThreatRuleCreate, ThreatRuleResponse

router = APIRouter(prefix="/rules", tags=["Threat Rules"])


def _handle_db_error(db: Session, exc: Exception) -> None:
    db.rollback()
    raise HTTPException(status_code=503, detail="Database operation failed") from exc


@router.post("/", response_model=ThreatRuleResponse)
def create_rule(rule: ThreatRuleCreate, db: Session = Depends(get_db)):
    db_rule = ThreatRule(**rule.model_dump())

    try:
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
    except SQLAlchemyError as exc:
        _handle_db_error(db, exc)

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

    for field, value in rule.model_dump().items():
        setattr(db_rule, field, value)

    try:
        db.commit()
        db.refresh(db_rule)
    except SQLAlchemyError as exc:
        _handle_db_error(db, exc)

    return db_rule


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    try:
        db.delete(rule)
        db.commit()
    except SQLAlchemyError as exc:
        _handle_db_error(db, exc)

    return {"message": "Rule deleted successfully"}


@router.patch("/{rule_id}/toggle", response_model=ThreatRuleResponse)
def toggle_rule_active(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(ThreatRule).filter(ThreatRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    rule.is_active = not rule.is_active

    try:
        db.commit()
        db.refresh(rule)
    except SQLAlchemyError as exc:
        _handle_db_error(db, exc)

    return rule
