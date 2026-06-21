from jose import jwt, JWTError
from fastapi import Header, HTTPException, Depends

from app.core.config import settings


def get_current_user(
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token gerekli."
        )

    try:
        token = authorization.replace(
            "Bearer ",
            ""
        )

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

def require_admin(user=Depends(get_current_user)):
    if user["role"] != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin yetkisi gerekli."
        )

    return user
