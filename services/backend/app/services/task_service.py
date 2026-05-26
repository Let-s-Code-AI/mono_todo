"""Business logic layer for task operations."""

from enum import Enum
from typing import Optional

from app.db.models import Comment, Priority, Status, Task
from app.db.repository import CommentRepository, TaskRepository
from app.schemas.task import CategoryResponse, TaskCreate, TaskResponse, TaskUpdate
from app.services.ai_priority_service import AIPriorityService, MockAIPriorityService


class TaskService:
    """Service layer for task business logic."""

    def __init__(
        self,
        repository: TaskRepository,
        ai_service: Optional[AIPriorityService] = None,
        comment_repository: Optional[CommentRepository] = None,
    ) -> None:
        """Initialize task service with repository, AI service, and comment repository."""
        self.repository = repository
        self.ai_service = ai_service or MockAIPriorityService()
        self.comment_repository = comment_repository

    def to_response(self, task: Task) -> TaskResponse:
        """Build a TaskResponse, resolving the nested category object."""
        category: Optional[CategoryResponse] = None
        if task.category_id:
            cat = self.repository.get_category(task.category_id)
            if cat:
                category = CategoryResponse.model_validate(cat)
        response = TaskResponse.model_validate(task)
        return response.model_copy(update={"category": category})

    async def create_task(
        self,
        task_data: TaskCreate,
        use_ai_priority: bool = False,
        owner_id: Optional[int] = None,
        category_name: Optional[str] = None,
    ) -> Task:
        """
        Create a new task with optional AI-based prioritization.

        Args:
            task_data: Task creation data
            use_ai_priority: Whether to use AI category context for priority suggestion
            owner_id: ID of the owning user
            category_name: Name of the assigned category (used by AI when use_ai_priority=True)

        Returns:
            Created task
        """
        user_priority = task_data.priority

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

    def get_task(self, task_id: int, owner_id: Optional[int] = None) -> Optional[Task]:
        """
        Get a task by ID, scoped to owner if provided.

        Args:
            task_id: Task identifier
            owner_id: If set, only return the task if it belongs to this user

        Returns:
            Task if found and accessible, None otherwise
        """
        return self.repository.get_by_id(task_id, owner_id=owner_id)

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

    def get_upcoming_tasks(
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

    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        owner_id: Optional[int] = None,
        changed_by_id: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Update an existing task, optionally recording history.

        Args:
            task_id: Task identifier
            task_data: Task update data
            owner_id: If set, only update the task if it belongs to this user
            changed_by_id: If set, record history entries for changes

        Returns:
            Updated task if found and accessible, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)

        # Snapshot old values before mutation
        changes: dict[str, tuple[str | None, str | None]] = {}
        for field, new_value in update_data.items():
            old_raw = getattr(task, field, None)
            # Use .value for enums, str() otherwise
            if isinstance(old_raw, Enum):
                old_str = old_raw.value
            else:
                old_str = str(old_raw) if old_raw is not None else None
            if isinstance(new_value, Enum):
                new_str = new_value.value
            else:
                new_str = str(new_value) if new_value is not None else None
            if old_str != new_str:
                changes[field] = (old_str, new_str)
            setattr(task, field, new_value)

        return self.repository.update(
            task,
            changes=changes if changes else None,
            changed_by_id=changed_by_id,
        )

    def add_tag(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
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

    def remove_tag(self, task_id: int, tag: str, owner_id: Optional[int] = None) -> Optional[Task]:
        """Remove a tag from a task."""
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        task.tags = [t for t in (task.tags or []) if t != tag]
        return self.repository.update(task)

    async def reanalyze_priority(
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

    def get_stats(self) -> dict:
        """Return task counts grouped by status and priority."""
        status_counts = dict(self.repository.count_by_status())
        priority_counts = dict(self.repository.count_by_priority())
        return {
            "total": self.repository.count_total(),
            "by_status": {s.value: status_counts.get(s, 0) for s in Status},
            "by_priority": {p.value: priority_counts.get(p, 0) for p in Priority},
        }

    def delete_task(self, task_id: int, owner_id: Optional[int] = None) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task identifier
            owner_id: If set, only delete the task if it belongs to this user

        Returns:
            True if deleted, False if not found or not accessible
        """
        return self.repository.delete(task_id, owner_id=owner_id)

    def get_task_history(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list]:
        """
        Get change history for a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return history if task belongs to this user

        Returns:
            List of history entries if task found, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        return self.repository.get_history(task_id)

    def add_comment(
        self,
        task_id: int,
        content: str,
        author_id: int,
        owner_id: Optional[int] = None,
    ) -> Optional[Comment]:
        """
        Add a comment to a task.

        Args:
            task_id: Task identifier
            content: Comment text
            author_id: User ID of the comment author
            owner_id: If set, only add comment if task belongs to this user

        Returns:
            Created comment if task found, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        comment = Comment(task_id=task_id, author_id=author_id, content=content)
        return self.comment_repository.create(comment)

    def get_comments(
        self, task_id: int, owner_id: Optional[int] = None
    ) -> Optional[list]:
        """
        Get all comments on a task.

        Args:
            task_id: Task identifier
            owner_id: If set, only return comments if task belongs to this user

        Returns:
            List of comments if task found, None otherwise
        """
        task = self.repository.get_by_id(task_id, owner_id=owner_id)
        if not task:
            return None
        return self.comment_repository.get_by_task(task_id)
