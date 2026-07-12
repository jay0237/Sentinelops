from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.auth_deps import get_current_user
from app.config.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import create_access_token
from app.utils.security import hash_password, verify_password

router = APIRouter()


@router.post("/register")
def register_user(
	user: UserCreate,
	db: Session = Depends(get_db)
):

	existing_user = db.query(User).filter(
		(User.email == user.email) | (User.username == user.username)
	).first()

	if existing_user:
		raise HTTPException(status_code=409, detail="User already exists")

	new_user = User(
		username=user.username,
		email=user.email,
		password=hash_password(user.password)
	)

	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return {
		"message": "User registered successfully",
		"user_id": new_user.id
	}


@router.post("/login")
def login_user(
	form_data: OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db)
):

	existing_user = db.query(User).filter(
		User.email == form_data.username
	).first()

	if not existing_user:
		raise HTTPException(status_code=401, detail="Invalid email or password")

	password_valid = verify_password(
		form_data.password,
		existing_user.password
	)

	if not password_valid:
		raise HTTPException(status_code=401, detail="Invalid email or password")

	access_token = create_access_token(
		data={
			"user_id": existing_user.id,
			"email": existing_user.email
		}
	)

	return {
		"access_token": access_token,
		"token_type": "bearer"
	}


@router.get("/profile")
def get_profile(
	current_user: User = Depends(get_current_user)
):
	return {
		"id": current_user.id,
		"username": current_user.username,
		"email": current_user.email
	}
