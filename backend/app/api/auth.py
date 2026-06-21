from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str = "EMPLOYEE"


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/auth/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Bu email zaten kayıtlı."
        )

    user = User(
        email=request.email,
        password=hash_password(request.password),
        role=request.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "id": user.id,
        "email": user.email,
        "role": user.role
    }


@router.post("/auth/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email veya şifre hatalı."
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Email veya şifre hatalı."
        )

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
