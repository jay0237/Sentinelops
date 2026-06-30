import re

EMAIL_REGEX= r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PHONE_REGEX =  r"\b\d{10}\b"

def redact_pii(text):

    text = re.sub(EMAIL_REGEX,
    "[EMAIL_REDACTED]",
    text
    )

    text = re.sub(
        PHONE_REGEX,
        "[PHONE_REDACTED]",
        text
    )

    return text