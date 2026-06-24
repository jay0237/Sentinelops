from app.security.rules import RULES

def scan_threat(text):

    text = text.lower()

    for rule in RULES:

        if rule["keyword"] in text:

            return {
                "safe": False,
                "severity": rule["severity"],
                "reason": rule["reason"],
                "category": rule["category"],
                "risk_score": calculate_risk(rule["severity"])
            }

    return {
        "safe": True,
        "severity": "low",
        "reason": "No Threat Detected",
        "category": "None",
        "risk_score": 0
    }
    