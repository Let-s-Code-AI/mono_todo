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
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    args = [token, session]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_current_user__mutmut_orig, x_get_current_user__mutmut_mutants, args, kwargs, None)


def x_get_current_user__mutmut_orig(
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


def x_get_current_user__mutmut_1(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = None
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_2(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=None,
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


def x_get_current_user__mutmut_3(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=None,
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


def x_get_current_user__mutmut_4(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers=None,
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


def x_get_current_user__mutmut_5(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
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


def x_get_current_user__mutmut_6(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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


def x_get_current_user__mutmut_7(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
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


def x_get_current_user__mutmut_8(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="XXInvalid or expired tokenXX",
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


def x_get_current_user__mutmut_9(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid or expired token",
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


def x_get_current_user__mutmut_10(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="INVALID OR EXPIRED TOKEN",
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


def x_get_current_user__mutmut_11(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"XXWWW-AuthenticateXX": "Bearer"},
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


def x_get_current_user__mutmut_12(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"www-authenticate": "Bearer"},
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


def x_get_current_user__mutmut_13(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-AUTHENTICATE": "Bearer"},
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


def x_get_current_user__mutmut_14(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "XXBearerXX"},
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


def x_get_current_user__mutmut_15(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "bearer"},
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


def x_get_current_user__mutmut_16(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    """Extract and validate the current user from a JWT bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "BEARER"},
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


def x_get_current_user__mutmut_17(
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
        payload = None
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_18(
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
        payload = decode_token(None)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_19(
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
        user_id = None
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_20(
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
        user_id = int(None)
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_21(
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
        user_id = int(payload["XXsubXX"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_22(
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
        user_id = int(payload["SUB"])
    except (JWTError, KeyError, ValueError):
        raise credentials_error

    user = UserRepository(session).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_23(
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

    user = None
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_24(
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

    user = UserRepository(session).get_by_id(None)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_25(
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

    user = UserRepository(None).get_by_id(user_id)
    if not user:
        raise credentials_error
    return user


def x_get_current_user__mutmut_26(
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
    if user:
        raise credentials_error
    return user

x_get_current_user__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_current_user__mutmut_1': x_get_current_user__mutmut_1, 
    'x_get_current_user__mutmut_2': x_get_current_user__mutmut_2, 
    'x_get_current_user__mutmut_3': x_get_current_user__mutmut_3, 
    'x_get_current_user__mutmut_4': x_get_current_user__mutmut_4, 
    'x_get_current_user__mutmut_5': x_get_current_user__mutmut_5, 
    'x_get_current_user__mutmut_6': x_get_current_user__mutmut_6, 
    'x_get_current_user__mutmut_7': x_get_current_user__mutmut_7, 
    'x_get_current_user__mutmut_8': x_get_current_user__mutmut_8, 
    'x_get_current_user__mutmut_9': x_get_current_user__mutmut_9, 
    'x_get_current_user__mutmut_10': x_get_current_user__mutmut_10, 
    'x_get_current_user__mutmut_11': x_get_current_user__mutmut_11, 
    'x_get_current_user__mutmut_12': x_get_current_user__mutmut_12, 
    'x_get_current_user__mutmut_13': x_get_current_user__mutmut_13, 
    'x_get_current_user__mutmut_14': x_get_current_user__mutmut_14, 
    'x_get_current_user__mutmut_15': x_get_current_user__mutmut_15, 
    'x_get_current_user__mutmut_16': x_get_current_user__mutmut_16, 
    'x_get_current_user__mutmut_17': x_get_current_user__mutmut_17, 
    'x_get_current_user__mutmut_18': x_get_current_user__mutmut_18, 
    'x_get_current_user__mutmut_19': x_get_current_user__mutmut_19, 
    'x_get_current_user__mutmut_20': x_get_current_user__mutmut_20, 
    'x_get_current_user__mutmut_21': x_get_current_user__mutmut_21, 
    'x_get_current_user__mutmut_22': x_get_current_user__mutmut_22, 
    'x_get_current_user__mutmut_23': x_get_current_user__mutmut_23, 
    'x_get_current_user__mutmut_24': x_get_current_user__mutmut_24, 
    'x_get_current_user__mutmut_25': x_get_current_user__mutmut_25, 
    'x_get_current_user__mutmut_26': x_get_current_user__mutmut_26
}
x_get_current_user__mutmut_orig.__name__ = 'x_get_current_user'


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    args = [current_user]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_current_admin_user__mutmut_orig, x_get_current_admin_user__mutmut_mutants, args, kwargs, None)


def x_get_current_admin_user__mutmut_orig(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def x_get_current_admin_user__mutmut_1(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def x_get_current_admin_user__mutmut_2(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=None,
            detail="Admin access required",
        )
    return current_user


def x_get_current_admin_user__mutmut_3(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=None,
        )
    return current_user


def x_get_current_admin_user__mutmut_4(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            detail="Admin access required",
        )
    return current_user


def x_get_current_admin_user__mutmut_5(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            )
    return current_user


def x_get_current_admin_user__mutmut_6(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="XXAdmin access requiredXX",
        )
    return current_user


def x_get_current_admin_user__mutmut_7(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin access required",
        )
    return current_user


def x_get_current_admin_user__mutmut_8(current_user: User = Depends(get_current_user)) -> User:
    """Require the current user to be an admin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ADMIN ACCESS REQUIRED",
        )
    return current_user

x_get_current_admin_user__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_current_admin_user__mutmut_1': x_get_current_admin_user__mutmut_1, 
    'x_get_current_admin_user__mutmut_2': x_get_current_admin_user__mutmut_2, 
    'x_get_current_admin_user__mutmut_3': x_get_current_admin_user__mutmut_3, 
    'x_get_current_admin_user__mutmut_4': x_get_current_admin_user__mutmut_4, 
    'x_get_current_admin_user__mutmut_5': x_get_current_admin_user__mutmut_5, 
    'x_get_current_admin_user__mutmut_6': x_get_current_admin_user__mutmut_6, 
    'x_get_current_admin_user__mutmut_7': x_get_current_admin_user__mutmut_7, 
    'x_get_current_admin_user__mutmut_8': x_get_current_admin_user__mutmut_8
}
x_get_current_admin_user__mutmut_orig.__name__ = 'x_get_current_admin_user'


def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    args = [session]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_task_repository__mutmut_orig, x_get_task_repository__mutmut_mutants, args, kwargs, None)


def x_get_task_repository__mutmut_orig(session: Session = Depends(get_session)) -> TaskRepository:
    """Dependency to get task repository."""
    return TaskRepository(session)


def x_get_task_repository__mutmut_1(session: Session = Depends(get_session)) -> TaskRepository:
    """Dependency to get task repository."""
    return TaskRepository(None)

x_get_task_repository__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_task_repository__mutmut_1': x_get_task_repository__mutmut_1
}
x_get_task_repository__mutmut_orig.__name__ = 'x_get_task_repository'


def get_ai_service() -> AIPriorityService:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_ai_service__mutmut_orig, x_get_ai_service__mutmut_mutants, args, kwargs, None)


def x_get_ai_service__mutmut_orig() -> AIPriorityService:
    """Dependency to get AI priority service."""
    if settings.openai_api_key:
        return OpenAIPriorityService(settings.openai_api_key)
    return MockAIPriorityService()


def x_get_ai_service__mutmut_1() -> AIPriorityService:
    """Dependency to get AI priority service."""
    if settings.openai_api_key:
        return OpenAIPriorityService(None)
    return MockAIPriorityService()

x_get_ai_service__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_ai_service__mutmut_1': x_get_ai_service__mutmut_1
}
x_get_ai_service__mutmut_orig.__name__ = 'x_get_ai_service'


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    args = [repository, session, ai_service]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_task_service__mutmut_orig, x_get_task_service__mutmut_mutants, args, kwargs, None)


def x_get_task_service__mutmut_orig(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(repository, session, ai_service)


def x_get_task_service__mutmut_1(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(None, session, ai_service)


def x_get_task_service__mutmut_2(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(repository, None, ai_service)


def x_get_task_service__mutmut_3(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(repository, session, None)


def x_get_task_service__mutmut_4(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(session, ai_service)


def x_get_task_service__mutmut_5(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(repository, ai_service)


def x_get_task_service__mutmut_6(
    repository: TaskRepository = Depends(get_task_repository),
    session: Session = Depends(get_session),
    ai_service: AIPriorityService = Depends(get_ai_service),
) -> TaskService:
    """Dependency to get task service."""
    return TaskService(repository, session, )

x_get_task_service__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_task_service__mutmut_1': x_get_task_service__mutmut_1, 
    'x_get_task_service__mutmut_2': x_get_task_service__mutmut_2, 
    'x_get_task_service__mutmut_3': x_get_task_service__mutmut_3, 
    'x_get_task_service__mutmut_4': x_get_task_service__mutmut_4, 
    'x_get_task_service__mutmut_5': x_get_task_service__mutmut_5, 
    'x_get_task_service__mutmut_6': x_get_task_service__mutmut_6
}
x_get_task_service__mutmut_orig.__name__ = 'x_get_task_service'
