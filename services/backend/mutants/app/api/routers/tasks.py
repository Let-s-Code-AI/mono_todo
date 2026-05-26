"""API routes for task operations."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import (
    get_ai_service,
    get_current_admin_user,
    get_current_user,
    get_task_service,
)
from app.db.models import Priority, Status, User
from app.schemas.task import (
    PriorityAnalysisRequest,
    PriorityAnalysisResponse,
    TagCreate,
    TaskCommentCreate,
    TaskCommentResponse,
    TaskCreate,
    TaskHistoryResponse,
    TaskResponse,
    TaskUpdate,
)
from app.services.ai_priority_service import AIPriorityService
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
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


class TaskListParams:
    """Common query parameters for task listing endpoints."""

    def __init__(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        args = [status, priority, category_id, tag, overdue, skip, limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTaskListParamsǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTaskListParamsǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁTaskListParamsǁ__init____mutmut_orig(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = priority
        self.category_id = category_id
        self.tag = tag
        self.overdue = overdue
        self.skip = skip
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_1(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = None
        self.priority = priority
        self.category_id = category_id
        self.tag = tag
        self.overdue = overdue
        self.skip = skip
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_2(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = None
        self.category_id = category_id
        self.tag = tag
        self.overdue = overdue
        self.skip = skip
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_3(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = priority
        self.category_id = None
        self.tag = tag
        self.overdue = overdue
        self.skip = skip
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_4(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = priority
        self.category_id = category_id
        self.tag = None
        self.overdue = overdue
        self.skip = skip
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_5(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = priority
        self.category_id = category_id
        self.tag = tag
        self.overdue = None
        self.skip = skip
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_6(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = priority
        self.category_id = category_id
        self.tag = tag
        self.overdue = overdue
        self.skip = None
        self.limit = limit

    def xǁTaskListParamsǁ__init____mutmut_7(
        self,
        status: Optional[Status] = Query(default=None, description="Filter by status"),
        priority: Optional[Priority] = Query(default=None, description="Filter by priority"),
        category_id: Optional[int] = Query(default=None, description="Filter by category ID"),
        tag: Optional[str] = Query(default=None, description="Filter by tag"),
        overdue: bool = Query(
            default=False, description="Return only overdue tasks (past due_date, not done)"
        ),
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records"),
    ):
        self.status = status
        self.priority = priority
        self.category_id = category_id
        self.tag = tag
        self.overdue = overdue
        self.skip = skip
        self.limit = None
    
    xǁTaskListParamsǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTaskListParamsǁ__init____mutmut_1': xǁTaskListParamsǁ__init____mutmut_1, 
        'xǁTaskListParamsǁ__init____mutmut_2': xǁTaskListParamsǁ__init____mutmut_2, 
        'xǁTaskListParamsǁ__init____mutmut_3': xǁTaskListParamsǁ__init____mutmut_3, 
        'xǁTaskListParamsǁ__init____mutmut_4': xǁTaskListParamsǁ__init____mutmut_4, 
        'xǁTaskListParamsǁ__init____mutmut_5': xǁTaskListParamsǁ__init____mutmut_5, 
        'xǁTaskListParamsǁ__init____mutmut_6': xǁTaskListParamsǁ__init____mutmut_6, 
        'xǁTaskListParamsǁ__init____mutmut_7': xǁTaskListParamsǁ__init____mutmut_7
    }
    xǁTaskListParamsǁ__init____mutmut_orig.__name__ = 'xǁTaskListParamsǁ__init__'


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    use_ai_priority: bool = Query(default=False, description="Use AI for priority suggestion"),
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        use_ai_priority: Whether to use AI for priority suggestion
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Created task

    Raises:
        HTTPException: 404 if category_id does not exist
    """
    task = await service.create_task(
        task_data,
        use_ai_priority=use_ai_priority,
        owner_id=current_user.id,
    )
    return service.to_response(task)


@router.post("/priority/analyze", response_model=PriorityAnalysisResponse)
async def analyze_priority(
    payload: PriorityAnalysisRequest,
    ai_service: AIPriorityService = Depends(get_ai_service),
    _: User = Depends(get_current_user),
) -> PriorityAnalysisResponse:
    """
    Analyze task content and suggest a priority without creating a task.

    Args:
        payload: Task title and optional description for analysis
        ai_service: AI priority service dependency

    Returns:
        Suggested priority and analysis reason
    """
    priority, reason = await ai_service.suggest_priority(payload.title, payload.description)
    return PriorityAnalysisResponse(priority=priority, priority_reason=reason)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    params: TaskListParams = Depends(),
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    """
    Get the authenticated user's tasks with optional filtering.

    Args:
        params: Filter and pagination parameters
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        List of tasks belonging to the current user
    """
    tasks = service.get_tasks(
        status=params.status,
        priority=params.priority,
        skip=params.skip,
        limit=params.limit,
        owner_id=current_user.id,
        category_id=params.category_id,
        tag=params.tag,
        overdue=params.overdue,
    )
    return [service.to_response(task) for task in tasks]


@router.get("/admin/all", response_model=list[TaskResponse])
def admin_get_all_tasks(
    params: TaskListParams = Depends(),
    service: TaskService = Depends(get_task_service),
    _: User = Depends(get_current_admin_user),
) -> list[TaskResponse]:
    """
    Admin: get all tasks across all users.

    Args:
        params: Filter and pagination parameters
        service: Task service dependency

    Returns:
        All tasks (unscoped)
    """
    tasks = service.get_tasks(
        status=params.status,
        priority=params.priority,
        skip=params.skip,
        limit=params.limit,
        category_id=params.category_id,
        tag=params.tag,
        overdue=params.overdue,
    )
    return [service.to_response(task) for task in tasks]


@router.get("/admin/stats", response_model=dict)
def admin_get_stats(
    service: TaskService = Depends(get_task_service),
    _: User = Depends(get_current_admin_user),
) -> dict:
    """
    Admin: get task statistics across all users.

    Returns:
        Counts per status and priority
    """
    return service.get_stats()


@router.get("/upcoming", response_model=list[TaskResponse])
def get_upcoming_tasks(
    days: int = Query(default=7, ge=1, le=365, description="Number of days to look ahead"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    """
    Get tasks due within the next `days` days for the authenticated user.

    Args:
        days: Look-ahead window in days (default 7)
        skip: Number of records to skip
        limit: Maximum number of records to return
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        List of upcoming tasks ordered by due_date
    """
    tasks = service.get_upcoming_tasks(days=days, owner_id=current_user.id, skip=skip, limit=limit)
    return [service.to_response(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Get a task by ID (must belong to the authenticated user).

    Args:
        task_id: Task identifier
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Task details

    Raises:
        HTTPException: If task not found or not owned by current user
    """
    task = service.get_task(task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return service.to_response(task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Update an existing task (must belong to the authenticated user).

    Args:
        task_id: Task identifier
        task_data: Task update data
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Updated task

    Raises:
        HTTPException: If task/category not found or not owned by current user
    """
    task = service.update_task(
        task_id, task_data, owner_id=current_user.id, user_id=current_user.id
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return service.to_response(task)


@router.post("/{task_id}/tags", response_model=TaskResponse)
def add_tag(
    task_id: int,
    tag_data: TagCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Add a tag to an existing task (idempotent).

    Args:
        task_id: Task identifier
        tag_data: Tag to add
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    task = service.add_tag(task_id, tag_data.name, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return service.to_response(task)


@router.delete("/{task_id}/tags/{tag_name}", response_model=TaskResponse)
def remove_tag(
    task_id: int,
    tag_name: str,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Remove a tag from a task.

    Args:
        task_id: Task identifier
        tag_name: Tag to remove
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    task = service.remove_tag(task_id, tag_name, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return service.to_response(task)


@router.post("/{task_id}/reanalyze-priority", response_model=TaskResponse)
async def reanalyze_task_priority(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """
    Re-analyze and update priority for an existing task using AI.

    Args:
        task_id: Task identifier
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Updated task with new priority and reason

    Raises:
        HTTPException: If task not found or not owned by current user
    """
    updated_task = await service.reanalyze_priority(task_id, owner_id=current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return service.to_response(updated_task)


@router.get("/{task_id}/history", response_model=list[TaskHistoryResponse])
def get_task_history(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> list[TaskHistoryResponse]:
    """
    Get change history for a task (must belong to the authenticated user).

    Args:
        task_id: Task identifier
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        List of change history entries

    Raises:
        HTTPException: If task not found or not owned by current user
    """
    history = service.get_task_history(task_id, owner_id=current_user.id)
    if history is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return history


@router.post("/{task_id}/comments", response_model=TaskCommentResponse, status_code=201)
def add_comment(
    task_id: int,
    comment_data: TaskCommentCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> TaskCommentResponse:
    """
    Add a comment to a task (must belong to the authenticated user).

    Args:
        task_id: Task identifier
        comment_data: Comment content
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        Created comment

    Raises:
        HTTPException: If task not found or not owned by current user
    """
    comment = service.add_comment(
        task_id, owner_id=current_user.id, user_id=current_user.id, content=comment_data.content
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Task not found")
    return comment


@router.get("/{task_id}/comments", response_model=list[TaskCommentResponse])
def get_task_comments(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> list[TaskCommentResponse]:
    """
    Get all comments for a task (must belong to the authenticated user).

    Args:
        task_id: Task identifier
        service: Task service dependency
        current_user: Authenticated user

    Returns:
        List of comments

    Raises:
        HTTPException: If task not found or not owned by current user
    """
    comments = service.get_task_comments(task_id, owner_id=current_user.id)
    if comments is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return comments


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a task by ID (must belong to the authenticated user).

    Args:
        task_id: Task identifier
        service: Task service dependency
        current_user: Authenticated user

    Raises:
        HTTPException: If task not found or not owned by current user
    """
    deleted = service.delete_task(task_id, owner_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
