from sqlalchemy.orm import Session

from app.security.rule_loader import load_rules
from app.security.redaction import redact_pii
from app.security.risk_score import calculate_risk
from app.security.severity import SEVERITY_ORDER


def scan_threat(text: str, db: Session):
    # Keep original prompt
    original_text = text

    # Redact sensitive information
    redacted_text = redact_pii(text)

    # Convert to lowercase for case-insensitive matching
    text = redacted_text.lower()

    # Load active rules from database
    rules = load_rules(db)

    # Store every matched rule
    matches = []

    for rule in rules:
        if rule.keyword.lower() in text:
            matches.append(rule)

    # No threats detected
    if not matches:
        return {
            "safe": True,
            "severity": "low",
            "reason": "No Threat Detected",
            "category": "None",
            "risk_score": 0,
            "original_text": original_text,
            "sanitized_text": redacted_text,
            "matched_rules": []
        }

    # Pick the highest severity rule
    highest = max(
        matches,
        key=lambda rule: SEVERITY_ORDER[rule.severity.lower()]
    )

    # Return full analysis
    return {
        "safe": False,
        "severity": highest.severity,
        "reason": highest.reason,
        "category": highest.category,
        "risk_score": calculate_risk(highest.severity),
        "original_text": original_text,
        "sanitized_text": redacted_text,
        "matched_rules": [
            {
                "keyword": rule.keyword,
                "category": rule.category,
                "severity": rule.severity,
                "reason": rule.reason,
            }
            for rule in matches
        ]
    }


# Backward compatibility
analyze_text = scan_threat