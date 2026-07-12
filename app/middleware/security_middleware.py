from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import json
import re

from app.models.prompt_log import PromptLog
from app.config.database import SessionLocal
from app.security.rule_loader import load_rules


class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":

            try:
                body = await request.body()

                if body:
                    data = json.loads(body)
                    text = str(data.get("text", "")).lower()

                    if text:
                        db = SessionLocal()

                        try:
                            rules = load_rules(db)

                            for rule in rules:
                                rule_type = (rule.rule_type or "keyword").lower()

                                if rule_type == "regex":
                                    pattern = rule.pattern or rule.keyword

                                    try:
                                        matched = bool(
                                            re.search(pattern, text, re.IGNORECASE)
                                        )
                                    except re.error:
                                        matched = False
                                else:
                                    matched = rule.keyword.lower() in text

                                if matched:
                                    log = PromptLog(
                                        prompt=text,
                                        status="blocked",
                                        reason=rule.reason,
                                        severity=rule.severity,
                                        category=rule.category,
                                    )

                                    db.add(log)
                                    db.commit()

                                    return JSONResponse(
                                        status_code=403,
                                        content={
                                            "blocked": True,
                                            "category": rule.category,
                                            "reason": rule.reason,
                                            "severity": rule.severity,
                                        },
                                    )
                        finally:
                            db.close()

            except Exception as e:
                _ = e

        response = await call_next(request)

        return response