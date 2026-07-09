from sqlalchemy.orm import Session

from app.security.rule_loader import load_rules
from app.security.redaction import redact_pii
from app.security.risk_score import calculate_risk

def analyze_text(text: str, db: Session):

    original_text = text

    redacted_text = redact_pii(text)

    text = redacted_text.lower()


    rules = load_rules(db)

    for rule in rules:

        if rule.keyword in text:

            return {
                "safe": False,
                "severity": rule.severity,
                "reason": rule.reason,
                "category": rule.category,
                "risk_score": calculate_risk(rule.severity),
                "original_text": original_text,
                "sanitized_text": redacted_text
            }

    return {
    "safe": False,
    "severity": rule.severity,
    "reason": rule.reason,
    "category": rule.category,
    "risk_score": calculate_risk(rule.severity),
    "original_text": original_text,
    "sanitized_text": redacted_text
}
    