from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.deps import get_db
from app.models.user import User

from app.utils.auth import (
    oauth2_scheme,
    verify_access_token
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = verify_access_token(token)

        user_id = payload.get("user_id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication"
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )