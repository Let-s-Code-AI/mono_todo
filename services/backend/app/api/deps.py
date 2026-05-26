"""Shared FastAPI dependencies."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session

from app.core.security import decode_token
from app.db.models import User
from app.db.repository import TaskRepository, UserRepository
from app.db.session import get_session
from app.services.ai_priority_service import (
    AIPriorityService,
    MockAIPriorityService,
    OpenAIPriorityService,
)
from app.services.task_service import TaskService
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    """Dependency to get task repository."""
    return TaskRepository(session)


def get_ai_service() -> AIPriorityService:
    """Dependency to get AI priority service."""
    if settings.openai_api_key:
        return OpenAIPriorityService(settings.openai_api_key)
    return MockAIPriorityService()


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(repository, session, ai_service)
