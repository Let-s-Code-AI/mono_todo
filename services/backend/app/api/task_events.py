"""Push task change events over the projects WebSocket to everyone who can see the task.

Task mutations stay on REST; after the response is sent, the owner and every member of
the task's project receive `task_created` / `task_updated` / `task_deleted` so their open
dashboards refresh without a reload.
"""

from fastapi import BackgroundTasks, Depends
from pydantic import BaseModel

from app.api.realtime import ConnectionManager, get_http_connection_manager
from app.api.routers.projects import get_project_repository
from app.db.models import Task
from app.db.repository import ProjectRepository
from app.schemas.realtime import TaskCreated, TaskDeleted, TaskUpdated
from app.schemas.task import TaskResponse


class TaskNotifier:
    """Queues task events for delivery once the current HTTP response has been sent."""

    def __init__(
        self,
        manager: ConnectionManager,
        project_repository: ProjectRepository,
        background_tasks: BackgroundTasks,
    ) -> None:
        self.manager = manager
        self.project_repository = project_repository
        self.background_tasks = background_tasks

    def created(self, task: Task, response: TaskResponse) -> None:
        self._push(TaskCreated(task=response), task)

    def updated(self, task: Task, response: TaskResponse) -> None:
        self._push(TaskUpdated(task=response), task)

    def deleted(self, task: Task) -> None:
        """Queue the event while the row still exists; it is sent after the response."""
        self._push(TaskDeleted(task_id=task.id, project_id=task.project_id), task)

    def _push(self, message: BaseModel, task: Task) -> None:
        recipients = self._recipients(task.owner_id, task.project_id)
        self.background_tasks.add_task(
            self.manager.send_to_users, recipients, message.model_dump(mode="json")
        )

    def _recipients(self, owner_id: int | None, project_id: int | None) -> set[int]:
        recipients = {owner_id} if owner_id is not None else set()
        if project_id is not None:
            recipients.update(self.project_repository.member_ids(project_id))
        return recipients


def get_task_notifier(
    background_tasks: BackgroundTasks,
    manager: ConnectionManager = Depends(get_http_connection_manager),
    project_repository: ProjectRepository = Depends(get_project_repository),
) -> TaskNotifier:
    """Dependency to get the task event notifier."""
    return TaskNotifier(manager, project_repository, background_tasks)
