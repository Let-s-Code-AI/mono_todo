"""Pydantic schemas for task API requests and responses."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.db.models import Priority, Status
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


class CategoryCreate(BaseModel):
    """Schema for creating a new category."""

    name: str = Field(max_length=100, description="Category name")
    color: Optional[str] = Field(default=None, max_length=20, description="Hex color code")


class CategoryResponse(BaseModel):
    """Schema for category API responses."""

    id: int
    name: str
    color: Optional[str] = None

    model_config = {"from_attributes": True}


class TagCreate(BaseModel):
    """Schema for adding a tag to a task."""

    name: str = Field(max_length=100, description="Tag name")


class TaskBase(BaseModel):
    """Base task schema with common fields."""

    title: str = Field(max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description",
    )
    priority: Priority = Field(default=Priority.MEDIUM, description="Task priority level")
    status: Status = Field(default=Status.TODO, description="Task status")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    category_id: Optional[int] = None
    tags: list[str] = []
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[Priority] = None
    priority_reason: Optional[str] = Field(default=None, max_length=500)
    status: Optional[Status] = None
    category_id: Optional[int] = None
    due_date: Optional[date] = None


class TaskResponse(TaskBase):
    """Schema for task API responses."""

    id: int
    priority_reason: Optional[str] = None
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    tags: list[str] = []
    ai_override: bool = False

    model_config = {"from_attributes": True}

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v: object) -> list[str]:
        return v if v is not None else []


class PriorityAnalysisRequest(BaseModel):
    """Request schema for standalone priority analysis endpoint."""

    title: str = Field(max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description",
    )


class PriorityAnalysisResponse(BaseModel):
    """Response schema for standalone priority analysis endpoint."""

    priority: Priority = Field(description="Suggested task priority level")
    priority_reason: str = Field(description="Reason for the suggested priority")


class TaskHistoryResponse(BaseModel):
    """Schema for task change history entries."""

    id: int
    task_id: int
    user_id: int
    user_email: str
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    changed_at: datetime

    model_config = {"from_attributes": True}


class TaskCommentCreate(BaseModel):
    """Schema for creating a new comment."""

    content: str = Field(max_length=2000, description="Comment text")


class TaskCommentResponse(BaseModel):
    """Schema for comment API responses."""

    id: int
    task_id: int
    user_id: int
    user_email: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
