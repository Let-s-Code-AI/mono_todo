"""Database models for the TODO application."""

from datetime import date, datetime, timezone
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel
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


class Priority(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Status(str, Enum):
    """Task status values."""

    TODO = "todo"
    DONE = "done"


class User(SQLModel, table=True):
    """User database model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Category(SQLModel, table=True):
    """Task category database model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)
    color: Optional[str] = Field(default=None, max_length=20)


class Task(SQLModel, table=True):
    """Task database model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    priority_reason: Optional[str] = Field(default=None, max_length=500)
    status: Status = Field(default=Status.TODO)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", index=True)
    tags: Optional[List] = Field(default=None, sa_column=Column(JSON))
    ai_override: bool = Field(default=False)
    due_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskHistory(SQLModel, table=True):
    """Task change history tracking."""

    __tablename__ = "taskhistory"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    user_id: int = Field(foreign_key="user.id")
    field_name: str = Field(max_length=100)
    old_value: Optional[str] = Field(default=None, max_length=1000)
    new_value: Optional[str] = Field(default=None, max_length=1000)
    changed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskComment(SQLModel, table=True):
    """Task comments for discussion and notes."""

    __tablename__ = "taskcomment"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    user_id: int = Field(foreign_key="user.id")
    content: str = Field(max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
