from app.security.rules import RULES

def scan_threat(text):
    text = text.lower():

    for rule in RULES:

        if rule in RULES:

            return {
                "safe": False,
                "category": rule["severity"],
                "reason": rule["reason"]
                "category": rule["category"]
            }

            return {
                "safe": True,
                "severity": "low",
                "reason": "No Threat Detected",
                "category": "None"
            }