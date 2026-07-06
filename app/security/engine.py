from app.security.redaction import redact_pii
from app.security.threat_engine import scan_threat
from app.security.risk_score import calculate_risk


def scan(text: str):

    sanitized = redact_pii(tex)t

    threat = scan_threat(sanitized)

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