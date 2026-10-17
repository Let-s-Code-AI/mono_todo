"""API routes for projects and project membership."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.models import User
from app.db.repository import ProjectRepository, UserRepository
from app.db.session import get_session
from app.schemas.project import MemberAdd, MemberResponse, ProjectCreate, ProjectResponse
from app.services.project_service import MemberError, ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_repository(session: Session = Depends(get_session)) -> ProjectRepository:
    """Dependency to get project repository."""
    return ProjectRepository(session)


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    """Dependency to get user repository."""
    return UserRepository(session)


def get_project_service(
    repository: ProjectRepository = Depends(get_project_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ProjectService:
    """Dependency to get project service."""
    return ProjectService(repository, user_repository)


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> ProjectResponse:
    """
    Create a new project owned by the authenticated user.

    Args:
        data: Project creation data
        service: Project service dependency
        current_user: Authenticated user

    Returns:
        Created project
    """
    project = service.create_project(data, owner_id=current_user.id)
    return ProjectResponse.model_validate(project)


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> list[ProjectResponse]:
    """
    List projects the authenticated user is a member of.

    Args:
        service: Project service dependency
        current_user: Authenticated user

    Returns:
        Projects where the user is owner or member
    """
    projects = service.list_projects(user_id=current_user.id)
    return [ProjectResponse.model_validate(p) for p in projects]


@router.post("/{project_id}/members", response_model=MemberResponse, status_code=201)
def add_member(
    project_id: int,
    data: MemberAdd,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> MemberResponse:
    """
    Add an existing user to a project by email.

    Args:
        project_id: Project identifier
        data: Email of the user to add
        service: Project service dependency
        current_user: Authenticated user

    Returns:
        The new membership

    Raises:
        HTTPException: 404 if the project or the user does not exist,
            403 if the current user is not the project owner,
            409 if the user is already a member
    """
    result = service.add_member(project_id, data.email, actor_id=current_user.id)
    if isinstance(result, MemberError):
        raise _member_error_to_http(result)
    member, user = result
    return MemberResponse(user_id=user.id, email=user.email, role=member.role)


@router.get("/{project_id}/members", response_model=list[MemberResponse])
def list_members(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> list[MemberResponse]:
    """
    List members of a project.

    Args:
        project_id: Project identifier
        service: Project service dependency
        current_user: Authenticated user

    Returns:
        Members with their roles, owner first

    Raises:
        HTTPException: 404 if the project does not exist,
            403 if the current user is not a member
    """
    result = service.list_members(project_id, actor_id=current_user.id)
    if isinstance(result, MemberError):
        raise _member_error_to_http(result)
    return [
        MemberResponse(user_id=user.id, email=user.email, role=member.role)
        for member, user in result
    ]


@router.delete("/{project_id}/members/{user_id}", status_code=204)
def remove_member(
    project_id: int,
    user_id: int,
    service: ProjectService = Depends(get_project_service),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Remove a user from a project.

    Args:
        project_id: Project identifier
        user_id: Identifier of the user to remove
        service: Project service dependency
        current_user: Authenticated user

    Raises:
        HTTPException: 404 if the project or the membership does not exist,
            403 if the current user is not the project owner
    """
    error = service.remove_member(project_id, user_id, actor_id=current_user.id)
    if error:
        raise _member_error_to_http(error)


_MEMBER_ERRORS: dict[MemberError, tuple[int, str]] = {
    MemberError.PROJECT_NOT_FOUND: (404, "Project not found"),
    MemberError.NOT_MEMBER: (403, "Not a member of this project"),
    MemberError.NOT_OWNER: (403, "Only the project owner can manage members"),
    MemberError.USER_NOT_FOUND: (404, "User not found"),
    MemberError.ALREADY_MEMBER: (409, "User is already a member of this project"),
    MemberError.MEMBER_NOT_FOUND: (404, "User is not a member of this project"),
}


def _member_error_to_http(error: MemberError) -> HTTPException:
    """Translate a service-level membership error into an HTTPException."""
    status_code, detail = _MEMBER_ERRORS[error]
    return HTTPException(status_code=status_code, detail=detail)
