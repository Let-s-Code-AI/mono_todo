"""Messages exchanged over the projects WebSocket (`/ws/projects`).

Commands (client → server) carry a `request_id`; the server answers each one with
`ack`, `members` or `error` echoing that id, and pushes change events to every
member of the affected project.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter, field_validator

from app.schemas.project import MemberResponse, ProjectResponse
from app.schemas.task import TaskResponse

RequestId = Annotated[str, Field(min_length=1, max_length=64)]
Email = Annotated[str, Field(max_length=255)]

MAX_INITIAL_MEMBERS = 20


# ── Commands: client → server ───────────────────────────────────────────────


class CreateProjectCommand(BaseModel):
    """Create a project owned by the connected user, optionally with initial members.

    `member_emails` must all belong to registered users, otherwise nothing is created
    and the reply is an `error` with code `user_not_found` naming the unknown email.
    """

    type: Literal["create_project"]
    request_id: RequestId
    name: str = Field(min_length=1, max_length=100)
    member_emails: list[Email] = Field(default_factory=list, max_length=MAX_INITIAL_MEMBERS)

    @field_validator("member_emails")
    @classmethod
    def _strip_and_dedupe(cls, emails: list[str]) -> list[str]:
        """Drop surrounding whitespace, blank entries and repeated emails (order kept)."""
        return [email for email in dict.fromkeys(e.strip() for e in emails) if email]


class ListMembersCommand(BaseModel):
    """Request the member list of a project."""

    type: Literal["list_members"]
    request_id: RequestId
    project_id: int


class AddMemberCommand(BaseModel):
    """Add an existing user to a project by email (owner only)."""

    type: Literal["add_member"]
    request_id: RequestId
    project_id: int
    email: str = Field(max_length=255)


class RemoveMemberCommand(BaseModel):
    """Remove a member from a project (owner only)."""

    type: Literal["remove_member"]
    request_id: RequestId
    project_id: int
    user_id: int


Command = Annotated[
    CreateProjectCommand | ListMembersCommand | AddMemberCommand | RemoveMemberCommand,
    Field(discriminator="type"),
]

command_adapter: TypeAdapter[Command] = TypeAdapter(Command)


# ── Events and replies: server → client ─────────────────────────────────────


class ProjectsSnapshot(BaseModel):
    """Full list of the user's projects, sent right after connecting."""

    type: Literal["projects"] = "projects"
    projects: list[ProjectResponse]


class ProjectAdded(BaseModel):
    """The user gained access to a project (created it or was added to it)."""

    type: Literal["project_added"] = "project_added"
    project: ProjectResponse


class ProjectRemoved(BaseModel):
    """The user lost access to a project."""

    type: Literal["project_removed"] = "project_removed"
    project_id: int


class MembersList(BaseModel):
    """Reply to `list_members`."""

    type: Literal["members"] = "members"
    request_id: str
    project_id: int
    members: list[MemberResponse]


class MemberAdded(BaseModel):
    """Someone joined a project the user belongs to."""

    type: Literal["member_added"] = "member_added"
    project_id: int
    member: MemberResponse


class MemberRemoved(BaseModel):
    """Someone left a project the user belongs to."""

    type: Literal["member_removed"] = "member_removed"
    project_id: int
    user_id: int


class TaskCreated(BaseModel):
    """A task the user can see was created (own task or one in a shared project)."""

    type: Literal["task_created"] = "task_created"
    task: TaskResponse


class TaskUpdated(BaseModel):
    """A task the user can see changed (fields, status, tags or priority)."""

    type: Literal["task_updated"] = "task_updated"
    task: TaskResponse


class TaskDeleted(BaseModel):
    """A task the user could see was deleted."""

    type: Literal["task_deleted"] = "task_deleted"
    task_id: int
    project_id: int | None


class Ack(BaseModel):
    """The command with `request_id` succeeded."""

    type: Literal["ack"] = "ack"
    request_id: str


class ErrorMessage(BaseModel):
    """The command with `request_id` failed; `code` is machine-readable.

    `email` names the address the error is about (set for `user_not_found` when the
    command carried several emails).
    """

    type: Literal["error"] = "error"
    request_id: str | None = None
    code: str
    detail: str
    email: str | None = None
