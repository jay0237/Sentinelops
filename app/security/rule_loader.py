from sqlalchemy.orm import Session
from app.models.threat_rule import ThreatRule

def load_rules(db: Session):
    rules = db.query(ThreatRule).filter(ThreatRule.is_active.is_(True)).all()
    return rules