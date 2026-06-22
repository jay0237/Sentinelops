from app.security.rules import RULES

def scan_threat(text):

    text = text.lower()

    for rule in RULES:

        if rule["keyword"] in text:

            return {
                "safe": False,
                "severity": rule["severity"],
                "reason": rule["reason"],
                "category": rule["category"]
            }

    return {
        "safe": True,
        "severity": "low",
        "reason": "No Threat Detected",
        "category": "None"
    }