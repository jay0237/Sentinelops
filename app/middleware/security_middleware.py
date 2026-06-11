from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        print(
            f"[SentinelOps] Request received: "
            f"{request.method} {request.url.path}"
        )

        response = await call_next(request)

        return response