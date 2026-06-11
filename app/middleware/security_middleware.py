from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.response import JSONResponse
from app.security.rules import RULES
import json

class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        print(
            f"[SentinelOps] Request received: "
            f"{request.method} {request.url.path}"
        )

        if request.method == "POST":

            body = await request.body()

            data = json.loads(body)
            text = data.get("text", "").lower()

            for rule in RULES:

                if rule["keyword"] in text:

                    return JSONResponse(
                        status_code=403,
                        content={
                            "blocked": True,
                            "reason": rule["reason"],
                            "severity": rule["severity"]
                        }
                    )

                    except :
                        pass
                        
        response = await call_next(request)

        return response