"""Password hashing and JWT token utilities."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import jwt

from app.core.config import settings
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


def hash_password(password: str) -> str:
    args = [password]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_hash_password__mutmut_orig, x_hash_password__mutmut_mutants, args, kwargs, None)


def x_hash_password__mutmut_orig(password: str) -> str:
    """Hash a plain-text password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def x_hash_password__mutmut_1(password: str) -> str:
    """Hash a plain-text password."""
    return bcrypt.hashpw(None, bcrypt.gensalt()).decode()


def x_hash_password__mutmut_2(password: str) -> str:
    """Hash a plain-text password."""
    return bcrypt.hashpw(password.encode(), None).decode()


def x_hash_password__mutmut_3(password: str) -> str:
    """Hash a plain-text password."""
    return bcrypt.hashpw(bcrypt.gensalt()).decode()


def x_hash_password__mutmut_4(password: str) -> str:
    """Hash a plain-text password."""
    return bcrypt.hashpw(password.encode(), ).decode()

x_hash_password__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_hash_password__mutmut_1': x_hash_password__mutmut_1, 
    'x_hash_password__mutmut_2': x_hash_password__mutmut_2, 
    'x_hash_password__mutmut_3': x_hash_password__mutmut_3, 
    'x_hash_password__mutmut_4': x_hash_password__mutmut_4
}
x_hash_password__mutmut_orig.__name__ = 'x_hash_password'


def verify_password(plain_password: str, hashed_password: str) -> bool:
    args = [plain_password, hashed_password]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_verify_password__mutmut_orig, x_verify_password__mutmut_mutants, args, kwargs, None)


def x_verify_password__mutmut_orig(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def x_verify_password__mutmut_1(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""
    return bcrypt.checkpw(None, hashed_password.encode())


def x_verify_password__mutmut_2(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""
    return bcrypt.checkpw(plain_password.encode(), None)


def x_verify_password__mutmut_3(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""
    return bcrypt.checkpw(hashed_password.encode())


def x_verify_password__mutmut_4(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""
    return bcrypt.checkpw(plain_password.encode(), )

x_verify_password__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_verify_password__mutmut_1': x_verify_password__mutmut_1, 
    'x_verify_password__mutmut_2': x_verify_password__mutmut_2, 
    'x_verify_password__mutmut_3': x_verify_password__mutmut_3, 
    'x_verify_password__mutmut_4': x_verify_password__mutmut_4
}
x_verify_password__mutmut_orig.__name__ = 'x_verify_password'


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    args = [data, expires_delta]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_create_access_token__mutmut_orig, x_create_access_token__mutmut_mutants, args, kwargs, None)


def x_create_access_token__mutmut_orig(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_1(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = None
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_2(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = None
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_3(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) - (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_4(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(None) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_5(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta and timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_6(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=None)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_7(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = None
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_8(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["XXexpXX"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_9(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["EXP"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_10(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(None, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_11(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, None, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_12(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=None)


def x_create_access_token__mutmut_13(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_14(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, algorithm=settings.jwt_algorithm)


def x_create_access_token__mutmut_15(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, )

x_create_access_token__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_create_access_token__mutmut_1': x_create_access_token__mutmut_1, 
    'x_create_access_token__mutmut_2': x_create_access_token__mutmut_2, 
    'x_create_access_token__mutmut_3': x_create_access_token__mutmut_3, 
    'x_create_access_token__mutmut_4': x_create_access_token__mutmut_4, 
    'x_create_access_token__mutmut_5': x_create_access_token__mutmut_5, 
    'x_create_access_token__mutmut_6': x_create_access_token__mutmut_6, 
    'x_create_access_token__mutmut_7': x_create_access_token__mutmut_7, 
    'x_create_access_token__mutmut_8': x_create_access_token__mutmut_8, 
    'x_create_access_token__mutmut_9': x_create_access_token__mutmut_9, 
    'x_create_access_token__mutmut_10': x_create_access_token__mutmut_10, 
    'x_create_access_token__mutmut_11': x_create_access_token__mutmut_11, 
    'x_create_access_token__mutmut_12': x_create_access_token__mutmut_12, 
    'x_create_access_token__mutmut_13': x_create_access_token__mutmut_13, 
    'x_create_access_token__mutmut_14': x_create_access_token__mutmut_14, 
    'x_create_access_token__mutmut_15': x_create_access_token__mutmut_15
}
x_create_access_token__mutmut_orig.__name__ = 'x_create_access_token'


def decode_token(token: str) -> dict:
    args = [token]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_decode_token__mutmut_orig, x_decode_token__mutmut_mutants, args, kwargs, None)


def x_decode_token__mutmut_orig(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def x_decode_token__mutmut_1(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(None, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def x_decode_token__mutmut_2(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, None, algorithms=[settings.jwt_algorithm])


def x_decode_token__mutmut_3(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=None)


def x_decode_token__mutmut_4(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def x_decode_token__mutmut_5(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, algorithms=[settings.jwt_algorithm])


def x_decode_token__mutmut_6(token: str) -> dict:
    """Decode and verify a JWT token. Raises JWTError on failure."""
    return jwt.decode(token, settings.jwt_secret_key, )

x_decode_token__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_decode_token__mutmut_1': x_decode_token__mutmut_1, 
    'x_decode_token__mutmut_2': x_decode_token__mutmut_2, 
    'x_decode_token__mutmut_3': x_decode_token__mutmut_3, 
    'x_decode_token__mutmut_4': x_decode_token__mutmut_4, 
    'x_decode_token__mutmut_5': x_decode_token__mutmut_5, 
    'x_decode_token__mutmut_6': x_decode_token__mutmut_6
}
x_decode_token__mutmut_orig.__name__ = 'x_decode_token'
