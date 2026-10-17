"""Shared FastAPI dependencies for authentication."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session

from app.core.security import decode_token
from app.db.models import User
from app.db.repository import UserRepository
from app.db.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_from_token(token: str, session: Session) -> Optional[User]:
    """Resolve the user encoded in a JWT; None when the token is invalid or the user is gone."""
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None
    return UserRepository(session).get_by_id(user_id)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    user = get_user_from_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
