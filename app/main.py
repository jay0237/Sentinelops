from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest

from app.config.base import Base
from app.config.database import engine
from app.core.observability import limiter
from app.middleware.security_middleware import SecurityMiddleware
from slowapi.middleware import SlowAPIMiddleware
from app.models.threat_rule import ThreatRule
from app.routes.admin import router as admin_router
from app.routes.analytics import router as analytics_router
from app.routes.api_keys import router as api_keys_router
from app.routes.auth import router as auth_router
from app.routes.scan import router as scan_router

app = FastAPI()

app.add_middleware(SecurityMiddleware)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "SentinelOps API is Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelOps API",
        "version": "1.0.0"
    }


@app.get("/db-check")
def db_check():

    try:
        connection = engine.connect()
        connection.close()

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )


app.include_router(auth_router)
app.include_router(scan_router)
app.include_router(analytics_router)
app.include_router(admin_router)
app.include_router(api_keys_router)
