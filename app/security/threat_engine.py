from app.security.rules import RULES

def scan_threat(text):
    text = text.lower():

    for rule in RULES:

        if rule in RULES:

            return {
                "safe": False,
                "category": rule["severity"],
            }