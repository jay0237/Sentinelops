from app.security.redaction import redact_pii

def scan(text: str):
    
    sanitized = redact_pii (text)

    print(sanitized)