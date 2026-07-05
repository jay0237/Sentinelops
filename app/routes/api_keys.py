import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.api_key import ApiKey

router = APIRouter()


@router.post("/generate-api-key")
def generate_api_key(
    owner: str,
    db: Session = Depends(get_db)
):

    new_key = secrets.token_urlsafe(32)

    api_key = ApiKey(
        key=new_key,
        owner=owner
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "api_key": new_key,
        "owner": owner
    }
