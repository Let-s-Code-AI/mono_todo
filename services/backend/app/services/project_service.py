"""Business logic layer for projects and project membership."""

from enum import Enum

from app.db.models import Project, ProjectMember, ProjectRole, User
from app.db.repository import ProjectRepository, UserRepository
from app.schemas.project import ProjectCreate


class MemberError(str, Enum):
    """Outcomes of a failed membership operation; the router maps them to HTTP codes."""

    PROJECT_NOT_FOUND = "project_not_found"
    NOT_MEMBER = "not_member"
    NOT_OWNER = "not_owner"
    USER_NOT_FOUND = "user_not_found"
    ALREADY_MEMBER = "already_member"
    MEMBER_NOT_FOUND = "member_not_found"
    CANNOT_REMOVE_OWNER = "cannot_remove_owner"


class ProjectService:
    """Service layer for project business logic."""

    def __init__(self, repository: ProjectRepository, user_repository: UserRepository) -> None:
        self.repository = repository
        self.user_repository = user_repository

    def create_project(self, data: ProjectCreate, owner_id: int) -> Project:
        """Create a project owned by the given user."""
        return self.repository.create(Project(name=data.name, owner_id=owner_id))

    def list_projects(self, user_id: int) -> list[Project]:
        """Return projects the user belongs to."""
        return self.repository.get_for_user(user_id)

    def _is_owner(self, project_id: int, user_id: int) -> bool:
        member = self.repository.get_member(project_id, user_id)
        return member is not None and member.role == ProjectRole.OWNER

    def add_member(
        self, project_id: int, email: str, actor_id: int
    ) -> tuple[ProjectMember, User] | MemberError:
        """
        Add the user with the given email to the project on behalf of `actor_id`.

        Returns:
            (membership, user) on success, or a MemberError describing why it failed.
        """
        if not self.repository.get_by_id(project_id):
            return MemberError.PROJECT_NOT_FOUND
        if not self._is_owner(project_id, actor_id):
            return MemberError.NOT_OWNER
        user = self.user_repository.get_by_email(email)
        if not user:
            return MemberError.USER_NOT_FOUND
        if self.repository.get_member(project_id, user.id):
            return MemberError.ALREADY_MEMBER
        member = self.repository.add_member(project_id, user.id)
        return member, user

    def list_members(
        self, project_id: int, actor_id: int
    ) -> list[tuple[ProjectMember, User]] | MemberError:
        """Return the project's members as (membership, user) pairs; members only."""
        if not self.repository.get_by_id(project_id):
            return MemberError.PROJECT_NOT_FOUND
        if not self.repository.get_member(project_id, actor_id):
            return MemberError.NOT_MEMBER
        return self.repository.list_members(project_id)

    def remove_member(self, project_id: int, user_id: int, actor_id: int) -> MemberError | None:
        """Remove a user from the project on behalf of `actor_id`. None means success."""
        if not self.repository.get_by_id(project_id):
            return MemberError.PROJECT_NOT_FOUND
        if not self._is_owner(project_id, actor_id):
            return MemberError.NOT_OWNER
        member = self.repository.get_member(project_id, user_id)
        if not member:
            return MemberError.MEMBER_NOT_FOUND
        if member.role == ProjectRole.OWNER:
            return MemberError.CANNOT_REMOVE_OWNER
        self.repository.remove_member(member)
        return None
