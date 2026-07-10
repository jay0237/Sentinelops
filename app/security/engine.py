from app.security.redaction import redact_pii
from app.security.threat_engine import scan_threat
from app.security.risk_score import calculate_risk

from sqlalchemy.orm import Session

def scan(text: str, db: Session):

    sanitized = redact_pii(text)

    threat = scan_threat(sanitized, db)

    score = calculate_risk(threat["severity"])

    return {
        "safe": threat["safe"],
        "original_prompt": text,
        "sanitized_prompt": sanitized,
        "category": threat["category"],
        "severity": threat["severity"],
        "reason": threat["reason"],
        "risk_score": score
    }