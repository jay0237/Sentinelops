from app.security.rules import RULES
from app.security.redaction import redact_pii

def scan_threat(text):

    original_text = text

    redacted_text = redact_pii(text)

    text = redacted_text.lower()

    text = text.lower()

    for rule in RULES:

        if rule["keyword"] in text:

            return {
                "safe": False,
                "severity": rule["severity"],
                "reason": rule["reason"],
                "category": rule["category"],
                "risk_score": calculate_risk(rule["severity"]),
                "original_text": original_text,
                "sanitized_text": redacted_text
            }

    return {
        "safe": True,
        "severity": "low",
        "reason": "No Threat Detected",
        "category": "None",
        "risk_score": 0,
        "original_text": original_text,
        "sanitized_text": redacted_text
    }
    