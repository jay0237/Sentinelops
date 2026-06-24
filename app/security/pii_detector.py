import re

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

PHONE_REGEX = r"\b\d{10}\b"

def detect_pii(text):

    finding = []

    if re.search(EMAIL_REGEX, text):
        finding.append("email")

    if re.search(PHONE_REGEX, text):
        finding.append("phone")

    return finding