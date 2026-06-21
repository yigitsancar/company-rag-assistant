from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import require_admin
from app.db.database import get_db
from app.models.user import User


router = APIRouter()


class UpdateRoleRequest(BaseModel):
    role: str


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    users = db.query(User).order_by(User.id.asc()).all()

    return [
        {
            "id": item.id,
            "email": item.email,
            "role": item.role
        }
        for item in users
    ]


@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    request: UpdateRoleRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    allowed_roles = ["ADMIN", "MANAGER", "EMPLOYEE"]

    if request.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz rol."
        )

    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="Kullanıcı bulunamadı."
        )

    target_user.role = request.role
    db.commit()
    db.refresh(target_user)

    return {
        "message": "User role updated successfully",
        "id": target_user.id,
        "email": target_user.email,
        "role": target_user.role
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="Kullanıcı bulunamadı."
        )

    if target_user.email == user.get("sub"):
        raise HTTPException(
            status_code=400,
            detail="Kendi hesabını silemezsin."
        )

    db.delete(target_user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }
