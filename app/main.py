from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.config.database import engine
from app.config.base import Base
from app.models.user import User

from app.schemas.user import UserCreate
from app.config.deps import get_db

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


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }