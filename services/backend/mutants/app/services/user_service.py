"""Business logic layer for user operations."""

from typing import Optional

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.db.repository import UserRepository
from app.schemas.auth import Token, UserCreate
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


class UserService:
    """Service layer for user registration and authentication."""

    def __init__(self, repository: UserRepository) -> None:
        args = [repository]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserServiceǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁUserServiceǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁUserServiceǁ__init____mutmut_orig(self, repository: UserRepository) -> None:
        self.repository = repository

    def xǁUserServiceǁ__init____mutmut_1(self, repository: UserRepository) -> None:
        self.repository = None
    
    xǁUserServiceǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserServiceǁ__init____mutmut_1': xǁUserServiceǁ__init____mutmut_1
    }
    xǁUserServiceǁ__init____mutmut_orig.__name__ = 'xǁUserServiceǁ__init__'

    def register(self, user_data: UserCreate) -> Optional[User]:
        args = [user_data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserServiceǁregister__mutmut_orig'), object.__getattribute__(self, 'xǁUserServiceǁregister__mutmut_mutants'), args, kwargs, self)

    def xǁUserServiceǁregister__mutmut_orig(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            User(email=user_data.email, hashed_password=hash_password(user_data.password))
        )

    def xǁUserServiceǁregister__mutmut_1(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(None):
            return None
        return self.repository.create(
            User(email=user_data.email, hashed_password=hash_password(user_data.password))
        )

    def xǁUserServiceǁregister__mutmut_2(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            None
        )

    def xǁUserServiceǁregister__mutmut_3(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            User(email=None, hashed_password=hash_password(user_data.password))
        )

    def xǁUserServiceǁregister__mutmut_4(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            User(email=user_data.email, hashed_password=None)
        )

    def xǁUserServiceǁregister__mutmut_5(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            User(hashed_password=hash_password(user_data.password))
        )

    def xǁUserServiceǁregister__mutmut_6(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            User(email=user_data.email, )
        )

    def xǁUserServiceǁregister__mutmut_7(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user. Returns None if the email is already taken."""
        if self.repository.get_by_email(user_data.email):
            return None
        return self.repository.create(
            User(email=user_data.email, hashed_password=hash_password(None))
        )
    
    xǁUserServiceǁregister__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserServiceǁregister__mutmut_1': xǁUserServiceǁregister__mutmut_1, 
        'xǁUserServiceǁregister__mutmut_2': xǁUserServiceǁregister__mutmut_2, 
        'xǁUserServiceǁregister__mutmut_3': xǁUserServiceǁregister__mutmut_3, 
        'xǁUserServiceǁregister__mutmut_4': xǁUserServiceǁregister__mutmut_4, 
        'xǁUserServiceǁregister__mutmut_5': xǁUserServiceǁregister__mutmut_5, 
        'xǁUserServiceǁregister__mutmut_6': xǁUserServiceǁregister__mutmut_6, 
        'xǁUserServiceǁregister__mutmut_7': xǁUserServiceǁregister__mutmut_7
    }
    xǁUserServiceǁregister__mutmut_orig.__name__ = 'xǁUserServiceǁregister'

    def authenticate(self, email: str, password: str) -> Optional[Token]:
        args = [email, password]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUserServiceǁauthenticate__mutmut_orig'), object.__getattribute__(self, 'xǁUserServiceǁauthenticate__mutmut_mutants'), args, kwargs, self)

    def xǁUserServiceǁauthenticate__mutmut_orig(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_1(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = None
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_2(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(None)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_3(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user and not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_4(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_5(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_6(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(None, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_7(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, None):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_8(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_9(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, ):
            return None
        return Token(access_token=create_access_token({"sub": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_10(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=None)

    def xǁUserServiceǁauthenticate__mutmut_11(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token(None))

    def xǁUserServiceǁauthenticate__mutmut_12(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"XXsubXX": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_13(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"SUB": str(user.id)}))

    def xǁUserServiceǁauthenticate__mutmut_14(self, email: str, password: str) -> Optional[Token]:
        """Verify credentials and return a JWT token, or None if invalid."""
        user = self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return Token(access_token=create_access_token({"sub": str(None)}))
    
    xǁUserServiceǁauthenticate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUserServiceǁauthenticate__mutmut_1': xǁUserServiceǁauthenticate__mutmut_1, 
        'xǁUserServiceǁauthenticate__mutmut_2': xǁUserServiceǁauthenticate__mutmut_2, 
        'xǁUserServiceǁauthenticate__mutmut_3': xǁUserServiceǁauthenticate__mutmut_3, 
        'xǁUserServiceǁauthenticate__mutmut_4': xǁUserServiceǁauthenticate__mutmut_4, 
        'xǁUserServiceǁauthenticate__mutmut_5': xǁUserServiceǁauthenticate__mutmut_5, 
        'xǁUserServiceǁauthenticate__mutmut_6': xǁUserServiceǁauthenticate__mutmut_6, 
        'xǁUserServiceǁauthenticate__mutmut_7': xǁUserServiceǁauthenticate__mutmut_7, 
        'xǁUserServiceǁauthenticate__mutmut_8': xǁUserServiceǁauthenticate__mutmut_8, 
        'xǁUserServiceǁauthenticate__mutmut_9': xǁUserServiceǁauthenticate__mutmut_9, 
        'xǁUserServiceǁauthenticate__mutmut_10': xǁUserServiceǁauthenticate__mutmut_10, 
        'xǁUserServiceǁauthenticate__mutmut_11': xǁUserServiceǁauthenticate__mutmut_11, 
        'xǁUserServiceǁauthenticate__mutmut_12': xǁUserServiceǁauthenticate__mutmut_12, 
        'xǁUserServiceǁauthenticate__mutmut_13': xǁUserServiceǁauthenticate__mutmut_13, 
        'xǁUserServiceǁauthenticate__mutmut_14': xǁUserServiceǁauthenticate__mutmut_14
    }
    xǁUserServiceǁauthenticate__mutmut_orig.__name__ = 'xǁUserServiceǁauthenticate'
