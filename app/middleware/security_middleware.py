from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.security.rules import RULES
import json

from app.models.prompt_log import PromptLog
from app.config.database import SessionLocal


class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        print(
            f"[SentinelOps] Request received: "
            f"{request.method} {request.url.path}"
        )

        if request.method == "POST":

            try:
                body = await request.body()

                data = json.loads(body)

                text = data.get(
                    "text",
                    ""
                ).lower()

                for rule in RULES:

                    if rule["keyword"] in text:

                        db = SessionLocal()

                        log = PromptLog(
                            prompt=text,
                            status="blocked",
                            reason=rule["reason"],
                            severity=rule["severity"]
                        )

                        db.add(log)
                        db.commit()
                        db.close()

                        return JSONResponse(
                            status_code=403,
                            content={
                                "blocked": True,
                                "category": rule["category"],
                                "reason": rule["reason"],
                                "severity": rule["severity"]
                            }
                        )

            except Exception as e:
                print(f"Middleware Error: {e}")

        response = await call_next(request)

        return response