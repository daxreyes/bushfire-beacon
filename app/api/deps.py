from typing import Generator, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from loguru import logger

from app import crud, models, schemas
from app.config import settings
from app.database import SessionLocal

SSE_CLIENTS = set()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api{settings.API_V1_STR}/login/access-token", auto_error=False
)
cookie_sec = APIKeyCookie(name="session", auto_error=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
    session: str = Depends(cookie_sec),
) -> models.User:
    has_valid_token = False

    if not (token or session):
        logger.error(f"no token {token} or session {session}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = schemas.TokenPayload(**payload)
            has_valid_token = True
        except (jwt.JWTError, ValidationError) as e:
            # logger.info(f"token {token}, payload {payload}")
            logger.error(f"invalid jwt token in headers: {e}")

    if not has_valid_token and session:
        try:
            payload = jwt.decode(session, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = schemas.TokenPayload(**payload)
            has_valid_token = True
        except (jwt.JWTError, ValidationError) as e:
            # logger.info(f"token {token}, payload {payload}")
            logger.error(f"invalid jwt token in session: {e}")

    if not has_valid_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    logger.info(f"token is valid {token_data}")
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    logger.debug(
        f"is_superuser: {crud.user.is_superuser(current_user)} is_active: {crud.user.is_active(current_user)}"
    )
    if not (crud.user.is_superuser(current_user) or crud.user.is_active(current_user)):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return current_user


async def sse_notify(event: str, data: Any):
    for client in SSE_CLIENTS:
        await client.put({"event": event, "data": data})
