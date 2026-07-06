from app.security.engine import scan as engine_scan
from .models import ScanResult


class Sentinel:

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key

    def scan(self, text: str):

        result = engine_scan(text)

        return ScanResult(
            safe=result["safe"],
            severity=result["severity"],
            category=result["category"],
            reason=result["reason"],
            risk_score=result["risk_score"],
            original_prompt=result["original_prompt"],
            sanitized_prompt=result["sanitized_prompt"],
        )