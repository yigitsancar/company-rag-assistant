from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from app.core.config import settings


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Geçersiz token."
        )


def require_admin(
    user: dict = Depends(get_current_user)
):
    if user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin yetkisi gerekli."
        )

    return user


def require_manager_or_admin(
    user: dict = Depends(get_current_user)
):
    if user.get("role") not in ["ADMIN", "MANAGER"]:
        raise HTTPException(
            status_code=403,
            detail="Manager veya admin yetkisi gerekli."
        )

    return user
