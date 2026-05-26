"""Business logic layer for task operations."""

import json
from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.db.models import Priority, Status, Task
from app.db.repository import (
    TaskCommentRepository,
    TaskHistoryRepository,
    TaskRepository,
    UserRepository,
)
from app.schemas.task import (
    CategoryResponse,
    TaskCommentResponse,
    TaskCreate,
    TaskHistoryResponse,
    TaskResponse,
    TaskUpdate,
)
from app.services.ai_priority_service import AIPriorityService, MockAIPriorityService
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


class TaskService:
    """Service layer for task business logic."""

    def __init__(
        self,
        repository: TaskRepository,
        session: Session,
        ai_service: Optional[AIPriorityService] = None,
    ) -> None:
        args = [repository, session, ai_service]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁ__init____mutmut_orig(
        self,
        repository: TaskRepository,
        session: Session,
        ai_service: Optional[AIPriorityService] = None,
    ) -> None:
        """Initialize task service with repository, session, and optional AI service."""
        self.repository = repository
        self.session = session
        self.ai_service = ai_service or MockAIPriorityService()

    def xǁTaskServiceǁ__init____mutmut_1(
        self,
        repository: TaskRepository,
        session: Session,
        ai_service: Optional[AIPriorityService] = None,
    ) -> None:
        """Initialize task service with repository, session, and optional AI service."""
        self.repository = None
        self.session = session
        self.ai_service = ai_service or MockAIPriorityService()

    def xǁTaskServiceǁ__init____mutmut_2(
        self,
        repository: TaskRepository,
        session: Session,
        ai_service: Optional[AIPriorityService] = None,
    ) -> None:
        """Initialize task service with repository, session, and optional AI service."""
        self.repository = repository
        self.session = None
        self.ai_service = ai_service or MockAIPriorityService()

    def xǁTaskServiceǁ__init____mutmut_3(
        self,
        repository: TaskRepository,
        session: Session,
        ai_service: Optional[AIPriorityService] = None,
    ) -> None:
        """Initialize task service with repository, session, and optional AI service."""
        self.repository = repository
        self.session = session
        self.ai_service = None

    def xǁTaskServiceǁ__init____mutmut_4(
        self,
        repository: TaskRepository,
        session: Session,
        ai_service: Optional[AIPriorityService] = None,
    ) -> None:
        """Initialize task service with repository, session, and optional AI service."""
        self.repository = repository
        self.session = session
        self.ai_service = ai_service and MockAIPriorityService()
    
    xǁTaskServiceǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁ__init____mutmut_1': xǁTaskServiceǁ__init____mutmut_1, 
        'xǁTaskServiceǁ__init____mutmut_2': xǁTaskServiceǁ__init____mutmut_2, 
        'xǁTaskServiceǁ__init____mutmut_3': xǁTaskServiceǁ__init____mutmut_3, 
        'xǁTaskServiceǁ__init____mutmut_4': xǁTaskServiceǁ__init____mutmut_4
    }
    xǁTaskServiceǁ__init____mutmut_orig.__name__ = 'xǁTaskServiceǁ__init__'

    def to_response(self, task: Task) -> TaskResponse:
        args = [task]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁto_response__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁto_response__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁto_response__mutmut_orig(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_1(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = ""
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_2(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = None
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_3(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(None)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_4(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = None
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_5(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(None)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_6(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = None
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_7(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(None)
        return response.model_copy(update={"category": category})

    def xǁTaskServiceǁto_response__mutmut_8(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update=None)

    def xǁTaskServiceǁto_response__mutmut_9(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"XXcategoryXX": category})

    def xǁTaskServiceǁto_response__mutmut_10(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"CATEGORY": category})
    
    xǁTaskServiceǁto_response__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁto_response__mutmut_1': xǁTaskServiceǁto_response__mutmut_1, 
        'xǁTaskServiceǁto_response__mutmut_2': xǁTaskServiceǁto_response__mutmut_2, 
        'xǁTaskServiceǁto_response__mutmut_3': xǁTaskServiceǁto_response__mutmut_3, 
        'xǁTaskServiceǁto_response__mutmut_4': xǁTaskServiceǁto_response__mutmut_4, 
        'xǁTaskServiceǁto_response__mutmut_5': xǁTaskServiceǁto_response__mutmut_5, 
        'xǁTaskServiceǁto_response__mutmut_6': xǁTaskServiceǁto_response__mutmut_6, 
        'xǁTaskServiceǁto_response__mutmut_7': xǁTaskServiceǁto_response__mutmut_7, 
        'xǁTaskServiceǁto_response__mutmut_8': xǁTaskServiceǁto_response__mutmut_8, 
        'xǁTaskServiceǁto_response__mutmut_9': xǁTaskServiceǁto_response__mutmut_9, 
        'xǁTaskServiceǁto_response__mutmut_10': xǁTaskServiceǁto_response__mutmut_10
    }
    xǁTaskServiceǁto_response__mutmut_orig.__name__ = 'xǁTaskServiceǁto_response'

    def _resolve_category_name_or_404(self, category_id: Optional[int]) -> Optional[str]:
        args = [category_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_orig(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_1(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is not None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_2(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = None
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_3(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(None)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_4(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_5(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=None, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_6(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail=None)
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_7(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_8(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, )
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_9(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=405, detail="Category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_10(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="XXCategory not foundXX")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_11(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="category not found")
        return category.name

    def xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_12(self, category_id: Optional[int]) -> Optional[str]:
        """Resolve category name from ID, raising 404 when category does not exist."""
        if category_id is None:
            return None

        category = self.repository.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="CATEGORY NOT FOUND")
        return category.name
    
    xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_1': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_1, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_2': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_2, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_3': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_3, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_4': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_4, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_5': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_5, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_6': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_6, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_7': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_7, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_8': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_8, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_9': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_9, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_10': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_10, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_11': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_11, 
        'xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_12': xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_12
    }
    xǁTaskServiceǁ_resolve_category_name_or_404__mutmut_orig.__name__ = 'xǁTaskServiceǁ_resolve_category_name_or_404'

    async def create_task(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        args = [task_data, use_ai_priority, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁcreate_task__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁcreate_task__mutmut_mutants'), args, kwargs, self)

    async def xǁTaskServiceǁcreate_task__mutmut_orig(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_1(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = True,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_2(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = None
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_3(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = None

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_4(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(None)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_5(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_6(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_7(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = None

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_8(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            None, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_9(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, None, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_10(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=None, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_11(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=None
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_12(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_13(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_14(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_15(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_16(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority != Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_17(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = None
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_18(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = None
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_19(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority == Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_20(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = None
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_21(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = None

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_22(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = True

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_23(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = None

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_24(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=None,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_25(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=None,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_26(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=None,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_27(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=None,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_28(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=None,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_29(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=None,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_30(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=None,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_31(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=None,
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_32(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=None,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_33(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=None,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_34(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_35(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_36(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_37(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_38(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_39(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_40(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_41(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_42(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            due_date=task_data.due_date,
        )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_43(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            )

        return self.repository.create(task)

    async def xǁTaskServiceǁcreate_task__mutmut_44(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user

        Returns:
            Created task
        """
        user_priority = task_data.priority
        category_name = self._resolve_category_name_or_404(task_data.category_id)

        # Pass category hint and due_date to AI only when use_ai_priority is True
        cat_hint = category_name if use_ai_priority else None
        due_hint = task_data.due_date if use_ai_priority else None
        ai_priority, priority_reason = await self.ai_service.suggest_priority(
            task_data.title, task_data.description, category_name=cat_hint, due_date=due_hint
        )

        # AI overrides to HIGH when it detects urgency (category-aware or keyword-based)
        if ai_priority == Priority.HIGH:
            priority = Priority.HIGH
            ai_override = user_priority != Priority.HIGH
        else:
            priority = user_priority
            ai_override = False

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=priority,
            priority_reason=priority_reason,
            status=task_data.status,
            owner_id=owner_id,
            category_id=task_data.category_id,
            tags=task_data.tags if task_data.tags else [],
            ai_override=ai_override,
            due_date=task_data.due_date,
        )

        return self.repository.create(None)
    
    xǁTaskServiceǁcreate_task__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁcreate_task__mutmut_1': xǁTaskServiceǁcreate_task__mutmut_1, 
        'xǁTaskServiceǁcreate_task__mutmut_2': xǁTaskServiceǁcreate_task__mutmut_2, 
        'xǁTaskServiceǁcreate_task__mutmut_3': xǁTaskServiceǁcreate_task__mutmut_3, 
        'xǁTaskServiceǁcreate_task__mutmut_4': xǁTaskServiceǁcreate_task__mutmut_4, 
        'xǁTaskServiceǁcreate_task__mutmut_5': xǁTaskServiceǁcreate_task__mutmut_5, 
        'xǁTaskServiceǁcreate_task__mutmut_6': xǁTaskServiceǁcreate_task__mutmut_6, 
        'xǁTaskServiceǁcreate_task__mutmut_7': xǁTaskServiceǁcreate_task__mutmut_7, 
        'xǁTaskServiceǁcreate_task__mutmut_8': xǁTaskServiceǁcreate_task__mutmut_8, 
        'xǁTaskServiceǁcreate_task__mutmut_9': xǁTaskServiceǁcreate_task__mutmut_9, 
        'xǁTaskServiceǁcreate_task__mutmut_10': xǁTaskServiceǁcreate_task__mutmut_10, 
        'xǁTaskServiceǁcreate_task__mutmut_11': xǁTaskServiceǁcreate_task__mutmut_11, 
        'xǁTaskServiceǁcreate_task__mutmut_12': xǁTaskServiceǁcreate_task__mutmut_12, 
        'xǁTaskServiceǁcreate_task__mutmut_13': xǁTaskServiceǁcreate_task__mutmut_13, 
        'xǁTaskServiceǁcreate_task__mutmut_14': xǁTaskServiceǁcreate_task__mutmut_14, 
        'xǁTaskServiceǁcreate_task__mutmut_15': xǁTaskServiceǁcreate_task__mutmut_15, 
        'xǁTaskServiceǁcreate_task__mutmut_16': xǁTaskServiceǁcreate_task__mutmut_16, 
        'xǁTaskServiceǁcreate_task__mutmut_17': xǁTaskServiceǁcreate_task__mutmut_17, 
        'xǁTaskServiceǁcreate_task__mutmut_18': xǁTaskServiceǁcreate_task__mutmut_18, 
        'xǁTaskServiceǁcreate_task__mutmut_19': xǁTaskServiceǁcreate_task__mutmut_19, 
        'xǁTaskServiceǁcreate_task__mutmut_20': xǁTaskServiceǁcreate_task__mutmut_20, 
        'xǁTaskServiceǁcreate_task__mutmut_21': xǁTaskServiceǁcreate_task__mutmut_21, 
        'xǁTaskServiceǁcreate_task__mutmut_22': xǁTaskServiceǁcreate_task__mutmut_22, 
        'xǁTaskServiceǁcreate_task__mutmut_23': xǁTaskServiceǁcreate_task__mutmut_23, 
        'xǁTaskServiceǁcreate_task__mutmut_24': xǁTaskServiceǁcreate_task__mutmut_24, 
        'xǁTaskServiceǁcreate_task__mutmut_25': xǁTaskServiceǁcreate_task__mutmut_25, 
        'xǁTaskServiceǁcreate_task__mutmut_26': xǁTaskServiceǁcreate_task__mutmut_26, 
        'xǁTaskServiceǁcreate_task__mutmut_27': xǁTaskServiceǁcreate_task__mutmut_27, 
        'xǁTaskServiceǁcreate_task__mutmut_28': xǁTaskServiceǁcreate_task__mutmut_28, 
        'xǁTaskServiceǁcreate_task__mutmut_29': xǁTaskServiceǁcreate_task__mutmut_29, 
        'xǁTaskServiceǁcreate_task__mutmut_30': xǁTaskServiceǁcreate_task__mutmut_30, 
        'xǁTaskServiceǁcreate_task__mutmut_31': xǁTaskServiceǁcreate_task__mutmut_31, 
        'xǁTaskServiceǁcreate_task__mutmut_32': xǁTaskServiceǁcreate_task__mutmut_32, 
        'xǁTaskServiceǁcreate_task__mutmut_33': xǁTaskServiceǁcreate_task__mutmut_33, 
        'xǁTaskServiceǁcreate_task__mutmut_34': xǁTaskServiceǁcreate_task__mutmut_34, 
        'xǁTaskServiceǁcreate_task__mutmut_35': xǁTaskServiceǁcreate_task__mutmut_35, 
        'xǁTaskServiceǁcreate_task__mutmut_36': xǁTaskServiceǁcreate_task__mutmut_36, 
        'xǁTaskServiceǁcreate_task__mutmut_37': xǁTaskServiceǁcreate_task__mutmut_37, 
        'xǁTaskServiceǁcreate_task__mutmut_38': xǁTaskServiceǁcreate_task__mutmut_38, 
        'xǁTaskServiceǁcreate_task__mutmut_39': xǁTaskServiceǁcreate_task__mutmut_39, 
        'xǁTaskServiceǁcreate_task__mutmut_40': xǁTaskServiceǁcreate_task__mutmut_40, 
        'xǁTaskServiceǁcreate_task__mutmut_41': xǁTaskServiceǁcreate_task__mutmut_41, 
        'xǁTaskServiceǁcreate_task__mutmut_42': xǁTaskServiceǁcreate_task__mutmut_42, 
        'xǁTaskServiceǁcreate_task__mutmut_43': xǁTaskServiceǁcreate_task__mutmut_43, 
        'xǁTaskServiceǁcreate_task__mutmut_44': xǁTaskServiceǁcreate_task__mutmut_44
    }
    xǁTaskServiceǁcreate_task__mutmut_orig.__name__ = 'xǁTaskServiceǁcreate_task'

    def get_task(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁget_task__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁget_task__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁget_task__mutmut_orig(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """
        Get a task by ID, scoped to owner if provided.

        Args:
            task_id: Task identifier
            owner_id: If set, only return the task if it belongs to this user

        Returns:
            Task if found and accessible, None otherwise
        """
        return self.repository.get_by_id(task_id, owner_id=owner_id)

    def xǁTaskServiceǁget_task__mutmut_1(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """
        Get a task by ID, scoped to owner if provided.

        Args:
            task_id: Task identifier
            owner_id: If set, only return the task if it belongs to this user

        Returns:
            Task if found and accessible, None otherwise
        """
        return self.repository.get_by_id(None, owner_id=owner_id)

    def xǁTaskServiceǁget_task__mutmut_2(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """
        Get a task by ID, scoped to owner if provided.

        Args:
            task_id: Task identifier
            owner_id: If set, only return the task if it belongs to this user

        Returns:
            Task if found and accessible, None otherwise
        """
        return self.repository.get_by_id(task_id, owner_id=None)

    def xǁTaskServiceǁget_task__mutmut_3(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """
        Get a task by ID, scoped to owner if provided.

        Args:
            task_id: Task identifier
            owner_id: If set, only return the task if it belongs to this user

        Returns:
            Task if found and accessible, None otherwise
        """
        return self.repository.get_by_id(owner_id=owner_id)

    def xǁTaskServiceǁget_task__mutmut_4(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """
        Get a task by ID, scoped to owner if provided.

        Args:
            task_id: Task identifier
            owner_id: If set, only return the task if it belongs to this user

        Returns:
            Task if found and accessible, None otherwise
        """
        return self.repository.get_by_id(task_id, )
    
    xǁTaskServiceǁget_task__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁget_task__mutmut_1': xǁTaskServiceǁget_task__mutmut_1, 
        'xǁTaskServiceǁget_task__mutmut_2': xǁTaskServiceǁget_task__mutmut_2, 
        'xǁTaskServiceǁget_task__mutmut_3': xǁTaskServiceǁget_task__mutmut_3, 
        'xǁTaskServiceǁget_task__mutmut_4': xǁTaskServiceǁget_task__mutmut_4
    }
    xǁTaskServiceǁget_task__mutmut_orig.__name__ = 'xǁTaskServiceǁget_task'

    def get_tasks(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        args = [status, priority, skip, limit, owner_id, category_id, tag, overdue]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁget_tasks__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁget_tasks__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁget_tasks__mutmut_orig(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_1(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 1,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_2(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 101,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_3(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = True,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_4(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=None,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_5(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=None,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_6(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=None,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_7(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=None,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_8(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=None,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_9(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=None,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_10(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=None,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_11(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=None,
        )

    def xǁTaskServiceǁget_tasks__mutmut_12(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_13(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_14(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_15(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_16(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            category_id=category_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_17(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            tag=tag,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_18(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            overdue=overdue,
        )

    def xǁTaskServiceǁget_tasks__mutmut_19(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        category_id: Optional[int] = None,
        tag: Optional[str] = None,
        overdue: bool = False,
    ) -> list[Task]:
        """
        Get tasks with optional filtering, scoped to owner if provided.

        Args:
            status: Optional status filter
            priority: Optional priority filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            owner_id: If set, only return tasks belonging to this user
            category_id: Optional category filter
            tag: Optional tag filter
            overdue: If True, return only tasks past their due_date and not done

        Returns:
            List of tasks
        """
        return self.repository.get_all(
            status=status,
            priority=priority,
            skip=skip,
            limit=limit,
            owner_id=owner_id,
            category_id=category_id,
            tag=tag,
            )
    
    xǁTaskServiceǁget_tasks__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁget_tasks__mutmut_1': xǁTaskServiceǁget_tasks__mutmut_1, 
        'xǁTaskServiceǁget_tasks__mutmut_2': xǁTaskServiceǁget_tasks__mutmut_2, 
        'xǁTaskServiceǁget_tasks__mutmut_3': xǁTaskServiceǁget_tasks__mutmut_3, 
        'xǁTaskServiceǁget_tasks__mutmut_4': xǁTaskServiceǁget_tasks__mutmut_4, 
        'xǁTaskServiceǁget_tasks__mutmut_5': xǁTaskServiceǁget_tasks__mutmut_5, 
        'xǁTaskServiceǁget_tasks__mutmut_6': xǁTaskServiceǁget_tasks__mutmut_6, 
        'xǁTaskServiceǁget_tasks__mutmut_7': xǁTaskServiceǁget_tasks__mutmut_7, 
        'xǁTaskServiceǁget_tasks__mutmut_8': xǁTaskServiceǁget_tasks__mutmut_8, 
        'xǁTaskServiceǁget_tasks__mutmut_9': xǁTaskServiceǁget_tasks__mutmut_9, 
        'xǁTaskServiceǁget_tasks__mutmut_10': xǁTaskServiceǁget_tasks__mutmut_10, 
        'xǁTaskServiceǁget_tasks__mutmut_11': xǁTaskServiceǁget_tasks__mutmut_11, 
        'xǁTaskServiceǁget_tasks__mutmut_12': xǁTaskServiceǁget_tasks__mutmut_12, 
        'xǁTaskServiceǁget_tasks__mutmut_13': xǁTaskServiceǁget_tasks__mutmut_13, 
        'xǁTaskServiceǁget_tasks__mutmut_14': xǁTaskServiceǁget_tasks__mutmut_14, 
        'xǁTaskServiceǁget_tasks__mutmut_15': xǁTaskServiceǁget_tasks__mutmut_15, 
        'xǁTaskServiceǁget_tasks__mutmut_16': xǁTaskServiceǁget_tasks__mutmut_16, 
        'xǁTaskServiceǁget_tasks__mutmut_17': xǁTaskServiceǁget_tasks__mutmut_17, 
        'xǁTaskServiceǁget_tasks__mutmut_18': xǁTaskServiceǁget_tasks__mutmut_18, 
        'xǁTaskServiceǁget_tasks__mutmut_19': xǁTaskServiceǁget_tasks__mutmut_19
    }
    xǁTaskServiceǁget_tasks__mutmut_orig.__name__ = 'xǁTaskServiceǁget_tasks'

    def get_upcoming_tasks(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        args = [days, owner_id, skip, limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁget_upcoming_tasks__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁget_upcoming_tasks__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_orig(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_1(
        self,
        days: int = 8,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_2(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 1,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_3(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 101,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_4(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=None, owner_id=owner_id, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_5(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=None, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_6(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=None, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_7(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=skip, limit=None)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_8(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(owner_id=owner_id, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_9(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, skip=skip, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_10(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, limit=limit)

    def xǁTaskServiceǁget_upcoming_tasks__mutmut_11(
        self,
        days: int = 7,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """
        Get tasks due within the next `days` days.

        Args:
            days: Number of days to look ahead
            owner_id: If set, only return tasks belonging to this user
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of upcoming tasks
        """
        return self.repository.get_upcoming(days=days, owner_id=owner_id, skip=skip, )
    
    xǁTaskServiceǁget_upcoming_tasks__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁget_upcoming_tasks__mutmut_1': xǁTaskServiceǁget_upcoming_tasks__mutmut_1, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_2': xǁTaskServiceǁget_upcoming_tasks__mutmut_2, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_3': xǁTaskServiceǁget_upcoming_tasks__mutmut_3, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_4': xǁTaskServiceǁget_upcoming_tasks__mutmut_4, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_5': xǁTaskServiceǁget_upcoming_tasks__mutmut_5, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_6': xǁTaskServiceǁget_upcoming_tasks__mutmut_6, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_7': xǁTaskServiceǁget_upcoming_tasks__mutmut_7, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_8': xǁTaskServiceǁget_upcoming_tasks__mutmut_8, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_9': xǁTaskServiceǁget_upcoming_tasks__mutmut_9, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_10': xǁTaskServiceǁget_upcoming_tasks__mutmut_10, 
        'xǁTaskServiceǁget_upcoming_tasks__mutmut_11': xǁTaskServiceǁget_upcoming_tasks__mutmut_11
    }
    xǁTaskServiceǁget_upcoming_tasks__mutmut_orig.__name__ = 'xǁTaskServiceǁget_upcoming_tasks'

    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        args = [task_id, task_data, owner_id, user_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁupdate_task__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁupdate_task__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁupdate_task__mutmut_orig(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_1(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = None
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_2(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_3(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_4(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_5(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_6(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_7(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = None
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_8(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=None)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_9(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=False)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_10(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "XXcategory_idXX" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_11(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "CATEGORY_ID" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_12(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" not in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_13(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(None)

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_14(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["XXcategory_idXX"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_15(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["CATEGORY_ID"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_16(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = None
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_17(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(None)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_18(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = None

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_19(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "XXtitleXX",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_20(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "TITLE",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_21(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "XXdescriptionXX",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_22(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "DESCRIPTION",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_23(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "XXpriorityXX",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_24(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "PRIORITY",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_25(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "XXstatusXX",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_26(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "STATUS",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_27(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "XXdue_dateXX",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_28(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "DUE_DATE",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_29(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "XXcategory_idXX",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_30(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "CATEGORY_ID",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_31(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "XXtagsXX",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_32(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "TAGS",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_33(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields or user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_34(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field not in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_35(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = None
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_36(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(None, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_37(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, None)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_38(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_39(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, )
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_40(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = None
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_41(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = None
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_42(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(None) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_43(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field != "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_44(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "XXtagsXX" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_45(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "TAGS" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_46(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(None)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_47(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = None
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_48(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(None) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_49(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field != "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_50(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "XXtagsXX" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_51(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "TAGS" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_52(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(None)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_53(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str == new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_54(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(None, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_55(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, None, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_56(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, None, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_57(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, None, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_58(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, None)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_59(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_60(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_61(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_62(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, new_str)
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_63(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, )
            setattr(task, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_64(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(None, field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_65(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, None, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_66(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, None)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_67(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(field, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_68(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, value)

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_69(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, )

        return self.repository.update(task)

    def xǁTaskServiceǁupdate_task__mutmut_70(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            user_id: ID of the user making the change (for history tracking)

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            self._resolve_category_name_or_404(update_data["category_id"])

        history_repo = TaskHistoryRepository(self.session)
        tracked_fields = {
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "category_id",
            "tags",
        }

        for field, value in update_data.items():
            if field in tracked_fields and user_id:
                old_value = getattr(task, field)
                new_value = value
                old_str = json.dumps(old_value) if field == "tags" else str(old_value)
                new_str = json.dumps(new_value) if field == "tags" else str(new_value)
                if old_str != new_str:
                    history_repo.create(task_id, user_id, field, old_str, new_str)
            setattr(task, field, value)

        return self.repository.update(None)
    
    xǁTaskServiceǁupdate_task__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁupdate_task__mutmut_1': xǁTaskServiceǁupdate_task__mutmut_1, 
        'xǁTaskServiceǁupdate_task__mutmut_2': xǁTaskServiceǁupdate_task__mutmut_2, 
        'xǁTaskServiceǁupdate_task__mutmut_3': xǁTaskServiceǁupdate_task__mutmut_3, 
        'xǁTaskServiceǁupdate_task__mutmut_4': xǁTaskServiceǁupdate_task__mutmut_4, 
        'xǁTaskServiceǁupdate_task__mutmut_5': xǁTaskServiceǁupdate_task__mutmut_5, 
        'xǁTaskServiceǁupdate_task__mutmut_6': xǁTaskServiceǁupdate_task__mutmut_6, 
        'xǁTaskServiceǁupdate_task__mutmut_7': xǁTaskServiceǁupdate_task__mutmut_7, 
        'xǁTaskServiceǁupdate_task__mutmut_8': xǁTaskServiceǁupdate_task__mutmut_8, 
        'xǁTaskServiceǁupdate_task__mutmut_9': xǁTaskServiceǁupdate_task__mutmut_9, 
        'xǁTaskServiceǁupdate_task__mutmut_10': xǁTaskServiceǁupdate_task__mutmut_10, 
        'xǁTaskServiceǁupdate_task__mutmut_11': xǁTaskServiceǁupdate_task__mutmut_11, 
        'xǁTaskServiceǁupdate_task__mutmut_12': xǁTaskServiceǁupdate_task__mutmut_12, 
        'xǁTaskServiceǁupdate_task__mutmut_13': xǁTaskServiceǁupdate_task__mutmut_13, 
        'xǁTaskServiceǁupdate_task__mutmut_14': xǁTaskServiceǁupdate_task__mutmut_14, 
        'xǁTaskServiceǁupdate_task__mutmut_15': xǁTaskServiceǁupdate_task__mutmut_15, 
        'xǁTaskServiceǁupdate_task__mutmut_16': xǁTaskServiceǁupdate_task__mutmut_16, 
        'xǁTaskServiceǁupdate_task__mutmut_17': xǁTaskServiceǁupdate_task__mutmut_17, 
        'xǁTaskServiceǁupdate_task__mutmut_18': xǁTaskServiceǁupdate_task__mutmut_18, 
        'xǁTaskServiceǁupdate_task__mutmut_19': xǁTaskServiceǁupdate_task__mutmut_19, 
        'xǁTaskServiceǁupdate_task__mutmut_20': xǁTaskServiceǁupdate_task__mutmut_20, 
        'xǁTaskServiceǁupdate_task__mutmut_21': xǁTaskServiceǁupdate_task__mutmut_21, 
        'xǁTaskServiceǁupdate_task__mutmut_22': xǁTaskServiceǁupdate_task__mutmut_22, 
        'xǁTaskServiceǁupdate_task__mutmut_23': xǁTaskServiceǁupdate_task__mutmut_23, 
        'xǁTaskServiceǁupdate_task__mutmut_24': xǁTaskServiceǁupdate_task__mutmut_24, 
        'xǁTaskServiceǁupdate_task__mutmut_25': xǁTaskServiceǁupdate_task__mutmut_25, 
        'xǁTaskServiceǁupdate_task__mutmut_26': xǁTaskServiceǁupdate_task__mutmut_26, 
        'xǁTaskServiceǁupdate_task__mutmut_27': xǁTaskServiceǁupdate_task__mutmut_27, 
        'xǁTaskServiceǁupdate_task__mutmut_28': xǁTaskServiceǁupdate_task__mutmut_28, 
        'xǁTaskServiceǁupdate_task__mutmut_29': xǁTaskServiceǁupdate_task__mutmut_29, 
        'xǁTaskServiceǁupdate_task__mutmut_30': xǁTaskServiceǁupdate_task__mutmut_30, 
        'xǁTaskServiceǁupdate_task__mutmut_31': xǁTaskServiceǁupdate_task__mutmut_31, 
        'xǁTaskServiceǁupdate_task__mutmut_32': xǁTaskServiceǁupdate_task__mutmut_32, 
        'xǁTaskServiceǁupdate_task__mutmut_33': xǁTaskServiceǁupdate_task__mutmut_33, 
        'xǁTaskServiceǁupdate_task__mutmut_34': xǁTaskServiceǁupdate_task__mutmut_34, 
        'xǁTaskServiceǁupdate_task__mutmut_35': xǁTaskServiceǁupdate_task__mutmut_35, 
        'xǁTaskServiceǁupdate_task__mutmut_36': xǁTaskServiceǁupdate_task__mutmut_36, 
        'xǁTaskServiceǁupdate_task__mutmut_37': xǁTaskServiceǁupdate_task__mutmut_37, 
        'xǁTaskServiceǁupdate_task__mutmut_38': xǁTaskServiceǁupdate_task__mutmut_38, 
        'xǁTaskServiceǁupdate_task__mutmut_39': xǁTaskServiceǁupdate_task__mutmut_39, 
        'xǁTaskServiceǁupdate_task__mutmut_40': xǁTaskServiceǁupdate_task__mutmut_40, 
        'xǁTaskServiceǁupdate_task__mutmut_41': xǁTaskServiceǁupdate_task__mutmut_41, 
        'xǁTaskServiceǁupdate_task__mutmut_42': xǁTaskServiceǁupdate_task__mutmut_42, 
        'xǁTaskServiceǁupdate_task__mutmut_43': xǁTaskServiceǁupdate_task__mutmut_43, 
        'xǁTaskServiceǁupdate_task__mutmut_44': xǁTaskServiceǁupdate_task__mutmut_44, 
        'xǁTaskServiceǁupdate_task__mutmut_45': xǁTaskServiceǁupdate_task__mutmut_45, 
        'xǁTaskServiceǁupdate_task__mutmut_46': xǁTaskServiceǁupdate_task__mutmut_46, 
        'xǁTaskServiceǁupdate_task__mutmut_47': xǁTaskServiceǁupdate_task__mutmut_47, 
        'xǁTaskServiceǁupdate_task__mutmut_48': xǁTaskServiceǁupdate_task__mutmut_48, 
        'xǁTaskServiceǁupdate_task__mutmut_49': xǁTaskServiceǁupdate_task__mutmut_49, 
        'xǁTaskServiceǁupdate_task__mutmut_50': xǁTaskServiceǁupdate_task__mutmut_50, 
        'xǁTaskServiceǁupdate_task__mutmut_51': xǁTaskServiceǁupdate_task__mutmut_51, 
        'xǁTaskServiceǁupdate_task__mutmut_52': xǁTaskServiceǁupdate_task__mutmut_52, 
        'xǁTaskServiceǁupdate_task__mutmut_53': xǁTaskServiceǁupdate_task__mutmut_53, 
        'xǁTaskServiceǁupdate_task__mutmut_54': xǁTaskServiceǁupdate_task__mutmut_54, 
        'xǁTaskServiceǁupdate_task__mutmut_55': xǁTaskServiceǁupdate_task__mutmut_55, 
        'xǁTaskServiceǁupdate_task__mutmut_56': xǁTaskServiceǁupdate_task__mutmut_56, 
        'xǁTaskServiceǁupdate_task__mutmut_57': xǁTaskServiceǁupdate_task__mutmut_57, 
        'xǁTaskServiceǁupdate_task__mutmut_58': xǁTaskServiceǁupdate_task__mutmut_58, 
        'xǁTaskServiceǁupdate_task__mutmut_59': xǁTaskServiceǁupdate_task__mutmut_59, 
        'xǁTaskServiceǁupdate_task__mutmut_60': xǁTaskServiceǁupdate_task__mutmut_60, 
        'xǁTaskServiceǁupdate_task__mutmut_61': xǁTaskServiceǁupdate_task__mutmut_61, 
        'xǁTaskServiceǁupdate_task__mutmut_62': xǁTaskServiceǁupdate_task__mutmut_62, 
        'xǁTaskServiceǁupdate_task__mutmut_63': xǁTaskServiceǁupdate_task__mutmut_63, 
        'xǁTaskServiceǁupdate_task__mutmut_64': xǁTaskServiceǁupdate_task__mutmut_64, 
        'xǁTaskServiceǁupdate_task__mutmut_65': xǁTaskServiceǁupdate_task__mutmut_65, 
        'xǁTaskServiceǁupdate_task__mutmut_66': xǁTaskServiceǁupdate_task__mutmut_66, 
        'xǁTaskServiceǁupdate_task__mutmut_67': xǁTaskServiceǁupdate_task__mutmut_67, 
        'xǁTaskServiceǁupdate_task__mutmut_68': xǁTaskServiceǁupdate_task__mutmut_68, 
        'xǁTaskServiceǁupdate_task__mutmut_69': xǁTaskServiceǁupdate_task__mutmut_69, 
        'xǁTaskServiceǁupdate_task__mutmut_70': xǁTaskServiceǁupdate_task__mutmut_70
    }
    xǁTaskServiceǁupdate_task__mutmut_orig.__name__ = 'xǁTaskServiceǁupdate_task'

    def add_tag(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        args = [task_id, tag, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁadd_tag__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁadd_tag__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁadd_tag__mutmut_orig(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_1(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = None
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_2(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_3(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_4(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_5(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_6(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_7(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = None
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_8(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(None)
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_9(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags and [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_10(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_11(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(None)
            task.tags = tags
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_12(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = None
            return self.repository.update(task)
        return task

    def xǁTaskServiceǁadd_tag__mutmut_13(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Add a tag to a task (idempotent)."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        tags = list(task.tags or [])
        if tag not in tags:
            tags.append(tag)
            task.tags = tags
            return self.repository.update(None)
        return task
    
    xǁTaskServiceǁadd_tag__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁadd_tag__mutmut_1': xǁTaskServiceǁadd_tag__mutmut_1, 
        'xǁTaskServiceǁadd_tag__mutmut_2': xǁTaskServiceǁadd_tag__mutmut_2, 
        'xǁTaskServiceǁadd_tag__mutmut_3': xǁTaskServiceǁadd_tag__mutmut_3, 
        'xǁTaskServiceǁadd_tag__mutmut_4': xǁTaskServiceǁadd_tag__mutmut_4, 
        'xǁTaskServiceǁadd_tag__mutmut_5': xǁTaskServiceǁadd_tag__mutmut_5, 
        'xǁTaskServiceǁadd_tag__mutmut_6': xǁTaskServiceǁadd_tag__mutmut_6, 
        'xǁTaskServiceǁadd_tag__mutmut_7': xǁTaskServiceǁadd_tag__mutmut_7, 
        'xǁTaskServiceǁadd_tag__mutmut_8': xǁTaskServiceǁadd_tag__mutmut_8, 
        'xǁTaskServiceǁadd_tag__mutmut_9': xǁTaskServiceǁadd_tag__mutmut_9, 
        'xǁTaskServiceǁadd_tag__mutmut_10': xǁTaskServiceǁadd_tag__mutmut_10, 
        'xǁTaskServiceǁadd_tag__mutmut_11': xǁTaskServiceǁadd_tag__mutmut_11, 
        'xǁTaskServiceǁadd_tag__mutmut_12': xǁTaskServiceǁadd_tag__mutmut_12, 
        'xǁTaskServiceǁadd_tag__mutmut_13': xǁTaskServiceǁadd_tag__mutmut_13
    }
    xǁTaskServiceǁadd_tag__mutmut_orig.__name__ = 'xǁTaskServiceǁadd_tag'

    def remove_tag(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        args = [task_id, tag, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁremove_tag__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁremove_tag__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁremove_tag__mutmut_orig(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_1(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = None
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_2(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_3(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_4(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_5(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_6(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_7(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        task.tags = None
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_8(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags and []) if t != tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_9(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t == tag]
        return self.repository.update(task)

    def xǁTaskServiceǁremove_tag__mutmut_10(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(None)
    
    xǁTaskServiceǁremove_tag__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁremove_tag__mutmut_1': xǁTaskServiceǁremove_tag__mutmut_1, 
        'xǁTaskServiceǁremove_tag__mutmut_2': xǁTaskServiceǁremove_tag__mutmut_2, 
        'xǁTaskServiceǁremove_tag__mutmut_3': xǁTaskServiceǁremove_tag__mutmut_3, 
        'xǁTaskServiceǁremove_tag__mutmut_4': xǁTaskServiceǁremove_tag__mutmut_4, 
        'xǁTaskServiceǁremove_tag__mutmut_5': xǁTaskServiceǁremove_tag__mutmut_5, 
        'xǁTaskServiceǁremove_tag__mutmut_6': xǁTaskServiceǁremove_tag__mutmut_6, 
        'xǁTaskServiceǁremove_tag__mutmut_7': xǁTaskServiceǁremove_tag__mutmut_7, 
        'xǁTaskServiceǁremove_tag__mutmut_8': xǁTaskServiceǁremove_tag__mutmut_8, 
        'xǁTaskServiceǁremove_tag__mutmut_9': xǁTaskServiceǁremove_tag__mutmut_9, 
        'xǁTaskServiceǁremove_tag__mutmut_10': xǁTaskServiceǁremove_tag__mutmut_10
    }
    xǁTaskServiceǁremove_tag__mutmut_orig.__name__ = 'xǁTaskServiceǁremove_tag'

    async def reanalyze_priority(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return await _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁreanalyze_priority__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁreanalyze_priority__mutmut_mutants'), args, kwargs, self)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_orig(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_1(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = None
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_2(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_3(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_4(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_5(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_6(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_7(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = ""
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_8(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_9(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = None
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_10(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(None)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_11(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_12(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = None

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_13(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            None, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_14(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, None, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_15(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=None, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_16(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=None
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_17(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_18(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_19(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_20(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_21(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = None
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_22(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = None
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_23(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = None
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_24(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority != Priority.HIGH
        return self.repository.update(task)

    async def xǁTaskServiceǁreanalyze_priority__mutmut_25(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[Task]:
        """
        Re-analyze priority for an existing task using AI.

        Args:
            task_id: Task identifier
            owner_id: If set, only process the task if it belongs to this user

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        category_name: Optional[str] = None
        if task.category_id is not None:
            category = self.repository.get_category(task.category_id)
            category_name = category.name if category else None

        priority, priority_reason = await self.ai_service.suggest_priority(
            task.title, task.description, category_name=category_name, due_date=task.due_date
        )

        task.priority = priority
        task.priority_reason = priority_reason
        task.ai_override = priority == Priority.HIGH
        return self.repository.update(None)
    
    xǁTaskServiceǁreanalyze_priority__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁreanalyze_priority__mutmut_1': xǁTaskServiceǁreanalyze_priority__mutmut_1, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_2': xǁTaskServiceǁreanalyze_priority__mutmut_2, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_3': xǁTaskServiceǁreanalyze_priority__mutmut_3, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_4': xǁTaskServiceǁreanalyze_priority__mutmut_4, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_5': xǁTaskServiceǁreanalyze_priority__mutmut_5, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_6': xǁTaskServiceǁreanalyze_priority__mutmut_6, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_7': xǁTaskServiceǁreanalyze_priority__mutmut_7, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_8': xǁTaskServiceǁreanalyze_priority__mutmut_8, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_9': xǁTaskServiceǁreanalyze_priority__mutmut_9, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_10': xǁTaskServiceǁreanalyze_priority__mutmut_10, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_11': xǁTaskServiceǁreanalyze_priority__mutmut_11, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_12': xǁTaskServiceǁreanalyze_priority__mutmut_12, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_13': xǁTaskServiceǁreanalyze_priority__mutmut_13, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_14': xǁTaskServiceǁreanalyze_priority__mutmut_14, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_15': xǁTaskServiceǁreanalyze_priority__mutmut_15, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_16': xǁTaskServiceǁreanalyze_priority__mutmut_16, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_17': xǁTaskServiceǁreanalyze_priority__mutmut_17, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_18': xǁTaskServiceǁreanalyze_priority__mutmut_18, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_19': xǁTaskServiceǁreanalyze_priority__mutmut_19, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_20': xǁTaskServiceǁreanalyze_priority__mutmut_20, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_21': xǁTaskServiceǁreanalyze_priority__mutmut_21, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_22': xǁTaskServiceǁreanalyze_priority__mutmut_22, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_23': xǁTaskServiceǁreanalyze_priority__mutmut_23, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_24': xǁTaskServiceǁreanalyze_priority__mutmut_24, 
        'xǁTaskServiceǁreanalyze_priority__mutmut_25': xǁTaskServiceǁreanalyze_priority__mutmut_25
    }
    xǁTaskServiceǁreanalyze_priority__mutmut_orig.__name__ = 'xǁTaskServiceǁreanalyze_priority'

    def get_stats(self) -> dict:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁget_stats__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁget_stats__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁget_stats__mutmut_orig(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_1(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = None
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_2(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(None)
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_3(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = None
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_4(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(None)
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_5(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "XXtotalXX": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_6(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "TOTAL": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_7(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "XXby_statusXX": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_8(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "BY_STATUS": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_9(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(None, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_10(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, None) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_11(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_12(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, ) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_13(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 1) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_14(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "XXby_priorityXX": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_15(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "BY_PRIORITY": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_16(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(None, 0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_17(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, None) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_18(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(0) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_19(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, ) for p in Priority},
        }

    def xǁTaskServiceǁget_stats__mutmut_20(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 1) for p in Priority},
        }
    
    xǁTaskServiceǁget_stats__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁget_stats__mutmut_1': xǁTaskServiceǁget_stats__mutmut_1, 
        'xǁTaskServiceǁget_stats__mutmut_2': xǁTaskServiceǁget_stats__mutmut_2, 
        'xǁTaskServiceǁget_stats__mutmut_3': xǁTaskServiceǁget_stats__mutmut_3, 
        'xǁTaskServiceǁget_stats__mutmut_4': xǁTaskServiceǁget_stats__mutmut_4, 
        'xǁTaskServiceǁget_stats__mutmut_5': xǁTaskServiceǁget_stats__mutmut_5, 
        'xǁTaskServiceǁget_stats__mutmut_6': xǁTaskServiceǁget_stats__mutmut_6, 
        'xǁTaskServiceǁget_stats__mutmut_7': xǁTaskServiceǁget_stats__mutmut_7, 
        'xǁTaskServiceǁget_stats__mutmut_8': xǁTaskServiceǁget_stats__mutmut_8, 
        'xǁTaskServiceǁget_stats__mutmut_9': xǁTaskServiceǁget_stats__mutmut_9, 
        'xǁTaskServiceǁget_stats__mutmut_10': xǁTaskServiceǁget_stats__mutmut_10, 
        'xǁTaskServiceǁget_stats__mutmut_11': xǁTaskServiceǁget_stats__mutmut_11, 
        'xǁTaskServiceǁget_stats__mutmut_12': xǁTaskServiceǁget_stats__mutmut_12, 
        'xǁTaskServiceǁget_stats__mutmut_13': xǁTaskServiceǁget_stats__mutmut_13, 
        'xǁTaskServiceǁget_stats__mutmut_14': xǁTaskServiceǁget_stats__mutmut_14, 
        'xǁTaskServiceǁget_stats__mutmut_15': xǁTaskServiceǁget_stats__mutmut_15, 
        'xǁTaskServiceǁget_stats__mutmut_16': xǁTaskServiceǁget_stats__mutmut_16, 
        'xǁTaskServiceǁget_stats__mutmut_17': xǁTaskServiceǁget_stats__mutmut_17, 
        'xǁTaskServiceǁget_stats__mutmut_18': xǁTaskServiceǁget_stats__mutmut_18, 
        'xǁTaskServiceǁget_stats__mutmut_19': xǁTaskServiceǁget_stats__mutmut_19, 
        'xǁTaskServiceǁget_stats__mutmut_20': xǁTaskServiceǁget_stats__mutmut_20
    }
    xǁTaskServiceǁget_stats__mutmut_orig.__name__ = 'xǁTaskServiceǁget_stats'

    def delete_task(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁdelete_task__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁdelete_task__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁdelete_task__mutmut_orig(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier
            owner_id: If set, only delete the task if it belongs to this user

        Returns:
            True if deleted, False if not found or not accessible
        """
        return self.repository.delete(task_id, owner_id=owner_id)

    def xǁTaskServiceǁdelete_task__mutmut_1(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier
            owner_id: If set, only delete the task if it belongs to this user

        Returns:
            True if deleted, False if not found or not accessible
        """
        return self.repository.delete(None, owner_id=owner_id)

    def xǁTaskServiceǁdelete_task__mutmut_2(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier
            owner_id: If set, only delete the task if it belongs to this user

        Returns:
            True if deleted, False if not found or not accessible
        """
        return self.repository.delete(task_id, owner_id=None)

    def xǁTaskServiceǁdelete_task__mutmut_3(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier
            owner_id: If set, only delete the task if it belongs to this user

        Returns:
            True if deleted, False if not found or not accessible
        """
        return self.repository.delete(owner_id=owner_id)

    def xǁTaskServiceǁdelete_task__mutmut_4(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier
            owner_id: If set, only delete the task if it belongs to this user

        Returns:
            True if deleted, False if not found or not accessible
        """
        return self.repository.delete(task_id, )
    
    xǁTaskServiceǁdelete_task__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁdelete_task__mutmut_1': xǁTaskServiceǁdelete_task__mutmut_1, 
        'xǁTaskServiceǁdelete_task__mutmut_2': xǁTaskServiceǁdelete_task__mutmut_2, 
        'xǁTaskServiceǁdelete_task__mutmut_3': xǁTaskServiceǁdelete_task__mutmut_3, 
        'xǁTaskServiceǁdelete_task__mutmut_4': xǁTaskServiceǁdelete_task__mutmut_4
    }
    xǁTaskServiceǁdelete_task__mutmut_orig.__name__ = 'xǁTaskServiceǁdelete_task'

    def get_task_history(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁget_task_history__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁget_task_history__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁget_task_history__mutmut_orig(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_1(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = None
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_2(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_3(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_4(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_5(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_6(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_7(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = None
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_8(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(None)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_9(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = None
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_10(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(None)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_11(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = None

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_12(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(None)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_13(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = None
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_14(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = None
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_15(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(None)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_16(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = None
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_17(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=None,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_18(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=None,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_19(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=None,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_20(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=None,
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_21(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=None,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_22(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=None,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_23(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=None,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_24(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=None,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_25(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_26(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_27(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_28(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_29(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_30(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_31(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_32(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_33(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "XXunknownXX",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_34(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "UNKNOWN",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_history__mutmut_35(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskHistoryResponse]]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history for tasks belonging to this user

        Returns:
            List of history entries or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        history_repo = TaskHistoryRepository(self.session)
        history_entries = history_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for entry in history_entries:
            user = user_repo.get_by_id(entry.user_id)
            response = TaskHistoryResponse(
                id=entry.id,
                task_id=entry.task_id,
                user_id=entry.user_id,
                user_email=user.email if user else "unknown",
                field_name=entry.field_name,
                old_value=entry.old_value,
                new_value=entry.new_value,
                changed_at=entry.changed_at,
            )
            result.append(None)
        return result
    
    xǁTaskServiceǁget_task_history__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁget_task_history__mutmut_1': xǁTaskServiceǁget_task_history__mutmut_1, 
        'xǁTaskServiceǁget_task_history__mutmut_2': xǁTaskServiceǁget_task_history__mutmut_2, 
        'xǁTaskServiceǁget_task_history__mutmut_3': xǁTaskServiceǁget_task_history__mutmut_3, 
        'xǁTaskServiceǁget_task_history__mutmut_4': xǁTaskServiceǁget_task_history__mutmut_4, 
        'xǁTaskServiceǁget_task_history__mutmut_5': xǁTaskServiceǁget_task_history__mutmut_5, 
        'xǁTaskServiceǁget_task_history__mutmut_6': xǁTaskServiceǁget_task_history__mutmut_6, 
        'xǁTaskServiceǁget_task_history__mutmut_7': xǁTaskServiceǁget_task_history__mutmut_7, 
        'xǁTaskServiceǁget_task_history__mutmut_8': xǁTaskServiceǁget_task_history__mutmut_8, 
        'xǁTaskServiceǁget_task_history__mutmut_9': xǁTaskServiceǁget_task_history__mutmut_9, 
        'xǁTaskServiceǁget_task_history__mutmut_10': xǁTaskServiceǁget_task_history__mutmut_10, 
        'xǁTaskServiceǁget_task_history__mutmut_11': xǁTaskServiceǁget_task_history__mutmut_11, 
        'xǁTaskServiceǁget_task_history__mutmut_12': xǁTaskServiceǁget_task_history__mutmut_12, 
        'xǁTaskServiceǁget_task_history__mutmut_13': xǁTaskServiceǁget_task_history__mutmut_13, 
        'xǁTaskServiceǁget_task_history__mutmut_14': xǁTaskServiceǁget_task_history__mutmut_14, 
        'xǁTaskServiceǁget_task_history__mutmut_15': xǁTaskServiceǁget_task_history__mutmut_15, 
        'xǁTaskServiceǁget_task_history__mutmut_16': xǁTaskServiceǁget_task_history__mutmut_16, 
        'xǁTaskServiceǁget_task_history__mutmut_17': xǁTaskServiceǁget_task_history__mutmut_17, 
        'xǁTaskServiceǁget_task_history__mutmut_18': xǁTaskServiceǁget_task_history__mutmut_18, 
        'xǁTaskServiceǁget_task_history__mutmut_19': xǁTaskServiceǁget_task_history__mutmut_19, 
        'xǁTaskServiceǁget_task_history__mutmut_20': xǁTaskServiceǁget_task_history__mutmut_20, 
        'xǁTaskServiceǁget_task_history__mutmut_21': xǁTaskServiceǁget_task_history__mutmut_21, 
        'xǁTaskServiceǁget_task_history__mutmut_22': xǁTaskServiceǁget_task_history__mutmut_22, 
        'xǁTaskServiceǁget_task_history__mutmut_23': xǁTaskServiceǁget_task_history__mutmut_23, 
        'xǁTaskServiceǁget_task_history__mutmut_24': xǁTaskServiceǁget_task_history__mutmut_24, 
        'xǁTaskServiceǁget_task_history__mutmut_25': xǁTaskServiceǁget_task_history__mutmut_25, 
        'xǁTaskServiceǁget_task_history__mutmut_26': xǁTaskServiceǁget_task_history__mutmut_26, 
        'xǁTaskServiceǁget_task_history__mutmut_27': xǁTaskServiceǁget_task_history__mutmut_27, 
        'xǁTaskServiceǁget_task_history__mutmut_28': xǁTaskServiceǁget_task_history__mutmut_28, 
        'xǁTaskServiceǁget_task_history__mutmut_29': xǁTaskServiceǁget_task_history__mutmut_29, 
        'xǁTaskServiceǁget_task_history__mutmut_30': xǁTaskServiceǁget_task_history__mutmut_30, 
        'xǁTaskServiceǁget_task_history__mutmut_31': xǁTaskServiceǁget_task_history__mutmut_31, 
        'xǁTaskServiceǁget_task_history__mutmut_32': xǁTaskServiceǁget_task_history__mutmut_32, 
        'xǁTaskServiceǁget_task_history__mutmut_33': xǁTaskServiceǁget_task_history__mutmut_33, 
        'xǁTaskServiceǁget_task_history__mutmut_34': xǁTaskServiceǁget_task_history__mutmut_34, 
        'xǁTaskServiceǁget_task_history__mutmut_35': xǁTaskServiceǁget_task_history__mutmut_35
    }
    xǁTaskServiceǁget_task_history__mutmut_orig.__name__ = 'xǁTaskServiceǁget_task_history'

    def add_comment(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        args = [task_id, owner_id, user_id, content]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁadd_comment__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁadd_comment__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁadd_comment__mutmut_orig(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_1(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = None
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_2(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_3(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_4(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_5(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_6(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_7(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = None
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_8(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(None)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_9(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = None
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_10(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(None, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_11(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, None, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_12(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, None)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_13(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_14(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_15(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, )
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_16(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = None
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_17(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(None)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_18(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = None

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_19(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(None)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_20(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=None,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_21(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=None,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_22(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=None,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_23(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=None,
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_24(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=None,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_25(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=None,
        )

    def xǁTaskServiceǁadd_comment__mutmut_26(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_27(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_28(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_29(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_30(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_31(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "unknown",
            content=comment.content,
            )

    def xǁTaskServiceǁadd_comment__mutmut_32(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "XXunknownXX",
            content=comment.content,
            created_at=comment.created_at,
        )

    def xǁTaskServiceǁadd_comment__mutmut_33(
        self, task_id: int, owner_id: Optional[int], user_id: int, content: str
    ) -> Optional[TaskCommentResponse]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only allow comments on tasks belonging to this user
            user_id: ID of the user adding the comment
            content: Comment text

        Returns:
            Created comment response or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comment = comment_repo.create(task_id, user_id, content)
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_id(user_id)

        return TaskCommentResponse(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            user_email=user.email if user else "UNKNOWN",
            content=comment.content,
            created_at=comment.created_at,
        )
    
    xǁTaskServiceǁadd_comment__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁadd_comment__mutmut_1': xǁTaskServiceǁadd_comment__mutmut_1, 
        'xǁTaskServiceǁadd_comment__mutmut_2': xǁTaskServiceǁadd_comment__mutmut_2, 
        'xǁTaskServiceǁadd_comment__mutmut_3': xǁTaskServiceǁadd_comment__mutmut_3, 
        'xǁTaskServiceǁadd_comment__mutmut_4': xǁTaskServiceǁadd_comment__mutmut_4, 
        'xǁTaskServiceǁadd_comment__mutmut_5': xǁTaskServiceǁadd_comment__mutmut_5, 
        'xǁTaskServiceǁadd_comment__mutmut_6': xǁTaskServiceǁadd_comment__mutmut_6, 
        'xǁTaskServiceǁadd_comment__mutmut_7': xǁTaskServiceǁadd_comment__mutmut_7, 
        'xǁTaskServiceǁadd_comment__mutmut_8': xǁTaskServiceǁadd_comment__mutmut_8, 
        'xǁTaskServiceǁadd_comment__mutmut_9': xǁTaskServiceǁadd_comment__mutmut_9, 
        'xǁTaskServiceǁadd_comment__mutmut_10': xǁTaskServiceǁadd_comment__mutmut_10, 
        'xǁTaskServiceǁadd_comment__mutmut_11': xǁTaskServiceǁadd_comment__mutmut_11, 
        'xǁTaskServiceǁadd_comment__mutmut_12': xǁTaskServiceǁadd_comment__mutmut_12, 
        'xǁTaskServiceǁadd_comment__mutmut_13': xǁTaskServiceǁadd_comment__mutmut_13, 
        'xǁTaskServiceǁadd_comment__mutmut_14': xǁTaskServiceǁadd_comment__mutmut_14, 
        'xǁTaskServiceǁadd_comment__mutmut_15': xǁTaskServiceǁadd_comment__mutmut_15, 
        'xǁTaskServiceǁadd_comment__mutmut_16': xǁTaskServiceǁadd_comment__mutmut_16, 
        'xǁTaskServiceǁadd_comment__mutmut_17': xǁTaskServiceǁadd_comment__mutmut_17, 
        'xǁTaskServiceǁadd_comment__mutmut_18': xǁTaskServiceǁadd_comment__mutmut_18, 
        'xǁTaskServiceǁadd_comment__mutmut_19': xǁTaskServiceǁadd_comment__mutmut_19, 
        'xǁTaskServiceǁadd_comment__mutmut_20': xǁTaskServiceǁadd_comment__mutmut_20, 
        'xǁTaskServiceǁadd_comment__mutmut_21': xǁTaskServiceǁadd_comment__mutmut_21, 
        'xǁTaskServiceǁadd_comment__mutmut_22': xǁTaskServiceǁadd_comment__mutmut_22, 
        'xǁTaskServiceǁadd_comment__mutmut_23': xǁTaskServiceǁadd_comment__mutmut_23, 
        'xǁTaskServiceǁadd_comment__mutmut_24': xǁTaskServiceǁadd_comment__mutmut_24, 
        'xǁTaskServiceǁadd_comment__mutmut_25': xǁTaskServiceǁadd_comment__mutmut_25, 
        'xǁTaskServiceǁadd_comment__mutmut_26': xǁTaskServiceǁadd_comment__mutmut_26, 
        'xǁTaskServiceǁadd_comment__mutmut_27': xǁTaskServiceǁadd_comment__mutmut_27, 
        'xǁTaskServiceǁadd_comment__mutmut_28': xǁTaskServiceǁadd_comment__mutmut_28, 
        'xǁTaskServiceǁadd_comment__mutmut_29': xǁTaskServiceǁadd_comment__mutmut_29, 
        'xǁTaskServiceǁadd_comment__mutmut_30': xǁTaskServiceǁadd_comment__mutmut_30, 
        'xǁTaskServiceǁadd_comment__mutmut_31': xǁTaskServiceǁadd_comment__mutmut_31, 
        'xǁTaskServiceǁadd_comment__mutmut_32': xǁTaskServiceǁadd_comment__mutmut_32, 
        'xǁTaskServiceǁadd_comment__mutmut_33': xǁTaskServiceǁadd_comment__mutmut_33
    }
    xǁTaskServiceǁadd_comment__mutmut_orig.__name__ = 'xǁTaskServiceǁadd_comment'

    def get_task_comments(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        args = [task_id, owner_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskServiceǁget_task_comments__mutmut_orig'), object.__getattribute__(self, 'xǁTaskServiceǁget_task_comments__mutmut_mutants'), args, kwargs, self)

    def xǁTaskServiceǁget_task_comments__mutmut_orig(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_1(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = None
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_2(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(None, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_3(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=None)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_4(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_5(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, )
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_6(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_7(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = None
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_8(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(None)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_9(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = None
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_10(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(None)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_11(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = None

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_12(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(None)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_13(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = None
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_14(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = None
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_15(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(None)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_16(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = None
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_17(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=None,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_18(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=None,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_19(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=None,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_20(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=None,
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_21(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=None,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_22(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=None,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_23(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_24(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_25(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_26(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_27(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_28(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_29(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "XXunknownXX",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_30(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "UNKNOWN",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(response)
        return result

    def xǁTaskServiceǁget_task_comments__mutmut_31(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list[TaskCommentResponse]]:
        """
        Get all comments for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments for tasks belonging to this user

        Returns:
            List of comments or None if task not found
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        comment_repo = TaskCommentRepository(self.session)
        comments = comment_repo.get_by_task(task_id)
        user_repo = UserRepository(self.session)

        result = []
        for comment in comments:
            user = user_repo.get_by_id(comment.user_id)
            response = TaskCommentResponse(
                id=comment.id,
                task_id=comment.task_id,
                user_id=comment.user_id,
                user_email=user.email if user else "unknown",
                content=comment.content,
                created_at=comment.created_at,
            )
            result.append(None)
        return result
    
    xǁTaskServiceǁget_task_comments__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskServiceǁget_task_comments__mutmut_1': xǁTaskServiceǁget_task_comments__mutmut_1, 
        'xǁTaskServiceǁget_task_comments__mutmut_2': xǁTaskServiceǁget_task_comments__mutmut_2, 
        'xǁTaskServiceǁget_task_comments__mutmut_3': xǁTaskServiceǁget_task_comments__mutmut_3, 
        'xǁTaskServiceǁget_task_comments__mutmut_4': xǁTaskServiceǁget_task_comments__mutmut_4, 
        'xǁTaskServiceǁget_task_comments__mutmut_5': xǁTaskServiceǁget_task_comments__mutmut_5, 
        'xǁTaskServiceǁget_task_comments__mutmut_6': xǁTaskServiceǁget_task_comments__mutmut_6, 
        'xǁTaskServiceǁget_task_comments__mutmut_7': xǁTaskServiceǁget_task_comments__mutmut_7, 
        'xǁTaskServiceǁget_task_comments__mutmut_8': xǁTaskServiceǁget_task_comments__mutmut_8, 
        'xǁTaskServiceǁget_task_comments__mutmut_9': xǁTaskServiceǁget_task_comments__mutmut_9, 
        'xǁTaskServiceǁget_task_comments__mutmut_10': xǁTaskServiceǁget_task_comments__mutmut_10, 
        'xǁTaskServiceǁget_task_comments__mutmut_11': xǁTaskServiceǁget_task_comments__mutmut_11, 
        'xǁTaskServiceǁget_task_comments__mutmut_12': xǁTaskServiceǁget_task_comments__mutmut_12, 
        'xǁTaskServiceǁget_task_comments__mutmut_13': xǁTaskServiceǁget_task_comments__mutmut_13, 
        'xǁTaskServiceǁget_task_comments__mutmut_14': xǁTaskServiceǁget_task_comments__mutmut_14, 
        'xǁTaskServiceǁget_task_comments__mutmut_15': xǁTaskServiceǁget_task_comments__mutmut_15, 
        'xǁTaskServiceǁget_task_comments__mutmut_16': xǁTaskServiceǁget_task_comments__mutmut_16, 
        'xǁTaskServiceǁget_task_comments__mutmut_17': xǁTaskServiceǁget_task_comments__mutmut_17, 
        'xǁTaskServiceǁget_task_comments__mutmut_18': xǁTaskServiceǁget_task_comments__mutmut_18, 
        'xǁTaskServiceǁget_task_comments__mutmut_19': xǁTaskServiceǁget_task_comments__mutmut_19, 
        'xǁTaskServiceǁget_task_comments__mutmut_20': xǁTaskServiceǁget_task_comments__mutmut_20, 
        'xǁTaskServiceǁget_task_comments__mutmut_21': xǁTaskServiceǁget_task_comments__mutmut_21, 
        'xǁTaskServiceǁget_task_comments__mutmut_22': xǁTaskServiceǁget_task_comments__mutmut_22, 
        'xǁTaskServiceǁget_task_comments__mutmut_23': xǁTaskServiceǁget_task_comments__mutmut_23, 
        'xǁTaskServiceǁget_task_comments__mutmut_24': xǁTaskServiceǁget_task_comments__mutmut_24, 
        'xǁTaskServiceǁget_task_comments__mutmut_25': xǁTaskServiceǁget_task_comments__mutmut_25, 
        'xǁTaskServiceǁget_task_comments__mutmut_26': xǁTaskServiceǁget_task_comments__mutmut_26, 
        'xǁTaskServiceǁget_task_comments__mutmut_27': xǁTaskServiceǁget_task_comments__mutmut_27, 
        'xǁTaskServiceǁget_task_comments__mutmut_28': xǁTaskServiceǁget_task_comments__mutmut_28, 
        'xǁTaskServiceǁget_task_comments__mutmut_29': xǁTaskServiceǁget_task_comments__mutmut_29, 
        'xǁTaskServiceǁget_task_comments__mutmut_30': xǁTaskServiceǁget_task_comments__mutmut_30, 
        'xǁTaskServiceǁget_task_comments__mutmut_31': xǁTaskServiceǁget_task_comments__mutmut_31
    }
    xǁTaskServiceǁget_task_comments__mutmut_orig.__name__ = 'xǁTaskServiceǁget_task_comments'
