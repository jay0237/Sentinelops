from app.security.redaction import redact_pii
from app.security.threat_engine import scan_threat
from app.security.risk_score import calculate_risk

def scan(text: str):
    
    sanitized = redact_pii (text)

    threat = scan_threat(sanitized)

    return{
        "safe": threat["safe"],
        "original_prompt":text,
        "sanitized_prompt": sanitized,
        "serverity":threat[ "serverity"],
        "category":threat["category"],
        "reason":threat["reason"],
        "risk_score": 0
    }