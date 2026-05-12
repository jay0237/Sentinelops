from fastapi import FastAPI
from app.config.database import engine
from app.config.base import Base
from app.models.user import User

app = FastAPI()

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