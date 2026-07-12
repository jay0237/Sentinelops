from app.security.redaction import redact_pii
from app.security.threat_engine import scan_threat

from sqlalchemy.orm import Session

def scan(text: str, db: Session):
    sanitized = redact_pii(text)

    return scan_threat(sanitized, db, original_text=text)