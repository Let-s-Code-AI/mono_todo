"""Authentication endpoints: register and login."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.db.repository import UserRepository
from app.db.session import get_session
from app.schemas.auth import Token, UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])
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


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    args = [session]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_user_service__mutmut_orig, x_get_user_service__mutmut_mutants, args, kwargs, None)


def x_get_user_service__mutmut_orig(session: Session = Depends(get_session)) -> UserService:
    """Dependency to get user service."""
    return UserService(UserRepository(session))


def x_get_user_service__mutmut_1(session: Session = Depends(get_session)) -> UserService:
    """Dependency to get user service."""
    return UserService(None)


def x_get_user_service__mutmut_2(session: Session = Depends(get_session)) -> UserService:
    """Dependency to get user service."""
    return UserService(UserRepository(None))

x_get_user_service__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_user_service__mutmut_1': x_get_user_service__mutmut_1, 
    'x_get_user_service__mutmut_2': x_get_user_service__mutmut_2
}
x_get_user_service__mutmut_orig.__name__ = 'x_get_user_service'


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Register a new user account.

    Args:
        user_data: Email and password for the new account.

    Returns:
        Created user (without password).

    Raises:
        HTTPException: 400 if email is already taken.
    """
    user = service.register(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
) -> Token:
    """
    Authenticate and receive a JWT access token.

    Args:
        form_data: OAuth2 form with username (email) and password.

    Returns:
        Bearer JWT token.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    token = service.authenticate(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token
