"""WebSocket endpoint streaming projects and membership changes in real time.

The client authenticates with its JWT in the `token` query parameter (browsers cannot
set headers on a WebSocket handshake), receives a snapshot of its projects right after
connecting and may then send commands described in `app.schemas.realtime`. Every command
is answered with `ack`, `members` or `error` carrying the same `request_id`; changes are
additionally pushed to every member of the affected project.
"""

import json

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from sqlmodel import Session
from starlette.concurrency import run_in_threadpool

from app.api.deps import get_user_from_token
from app.api.realtime import ConnectionManager, get_connection_manager
from app.api.routers.projects import MEMBER_ERRORS, get_project_service
from app.db.models import ProjectMember, User
from app.db.session import get_session
from app.schemas.project import MemberResponse, ProjectCreate, ProjectResponse
from app.schemas.realtime import (
    Ack,
    AddMemberCommand,
    Command,
    CreateProjectCommand,
    ErrorMessage,
    ListMembersCommand,
    MemberAdded,
    MemberRemoved,
    MembersList,
    ProjectAdded,
    ProjectRemoved,
    ProjectsSnapshot,
    RemoveMemberCommand,
    command_adapter,
)
from app.services.project_service import MemberError, ProjectService, UnknownEmail

router = APIRouter(tags=["projects"])

WS_4401_UNAUTHORIZED = 4401

# (recipient user ids, message) pairs produced by a command
Outgoing = tuple[list[int], BaseModel]


@router.websocket("/ws/projects")
async def projects_socket(
    websocket: WebSocket,
    token: str = Query(default="", description="JWT access token"),
    session: Session = Depends(get_session),
    service: ProjectService = Depends(get_project_service),
    manager: ConnectionManager = Depends(get_connection_manager),
) -> None:
    """
    Stream the authenticated user's projects and execute project commands.

    Args:
        websocket: The client connection
        token: JWT access token passed as a query parameter
        session: Database session of this connection, released after every command
        service: Project service dependency
        manager: Registry of open connections used to push changes to other users

    The socket is closed with code 4401 when the token is invalid or expired.
    """
    await websocket.accept()
    user = await run_in_threadpool(get_user_from_token, token, session)
    if user is None:
        await websocket.close(code=WS_4401_UNAUTHORIZED, reason="Invalid or expired token")
        return
    user_id = user.id

    manager.register(user_id, websocket)
    try:
        snapshot = await run_in_threadpool(_snapshot_and_release, user_id, service, session)
        await _send(websocket, snapshot)
        while True:
            raw = await websocket.receive_text()
            await _handle_message(raw, user_id, websocket, session, service, manager)
    except WebSocketDisconnect:
        pass
    finally:
        manager.unregister(user_id, websocket)


async def _handle_message(
    raw: str,
    user_id: int,
    websocket: WebSocket,
    session: Session,
    service: ProjectService,
    manager: ConnectionManager,
) -> None:
    """Validate one incoming frame, execute it and deliver the reply and the push events."""
    try:
        command = command_adapter.validate_json(raw)
    except ValidationError as exc:
        error = ErrorMessage(
            request_id=_request_id_of(raw), code="invalid_message", detail=_describe(exc)
        )
        await _send(websocket, error)
        return

    reply, outgoing = await run_in_threadpool(
        _execute_and_release, command, user_id, service, session
    )
    for recipients, message in outgoing:
        await manager.send_to_users(recipients, message.model_dump(mode="json"))
    await _send(websocket, reply)


async def _send(websocket: WebSocket, message: BaseModel) -> None:
    await websocket.send_json(message.model_dump(mode="json"))


def _snapshot_and_release(user_id: int, service: ProjectService, session: Session) -> BaseModel:
    try:
        projects = service.list_projects(user_id)
        return ProjectsSnapshot(projects=[ProjectResponse.model_validate(p) for p in projects])
    finally:
        session.close()


def _execute_and_release(
    command: Command, user_id: int, service: ProjectService, session: Session
) -> tuple[BaseModel, list[Outgoing]]:
    """Run a command in the threadpool; closing the session returns its pooled connection
    and drops cached rows, so the next command sees changes made by other users."""
    try:
        return _execute(command, user_id, service)
    finally:
        session.close()


def _execute(
    command: Command, user_id: int, service: ProjectService
) -> tuple[BaseModel, list[Outgoing]]:
    match command:
        case CreateProjectCommand():
            return _create_project(command, user_id, service)
        case ListMembersCommand():
            return _list_members(command, user_id, service)
        case AddMemberCommand():
            return _add_member(command, user_id, service)
        case RemoveMemberCommand():
            return _remove_member(command, user_id, service)
    raise AssertionError(f"Unhandled command: {command!r}")


def _create_project(
    command: CreateProjectCommand, user_id: int, service: ProjectService
) -> tuple[BaseModel, list[Outgoing]]:
    result = service.create_project_with_members(
        ProjectCreate(name=command.name), owner_id=user_id, member_emails=command.member_emails
    )
    if isinstance(result, UnknownEmail):
        error = ErrorMessage(
            request_id=command.request_id,
            code=MemberError.USER_NOT_FOUND.value,
            detail=f"User not found: {result.email}",
            email=result.email,
        )
        return error, []
    project, members = result
    added = ProjectAdded(project=ProjectResponse.model_validate(project))
    recipients = [user_id, *(member.id for member in members)]
    return Ack(request_id=command.request_id), [(recipients, added)]


def _list_members(
    command: ListMembersCommand, user_id: int, service: ProjectService
) -> tuple[BaseModel, list[Outgoing]]:
    result = service.list_members(command.project_id, actor_id=user_id)
    if isinstance(result, MemberError):
        return _error(command.request_id, result), []
    members = [_member_response(member, user) for member, user in result]
    reply = MembersList(
        request_id=command.request_id, project_id=command.project_id, members=members
    )
    return reply, []


def _add_member(
    command: AddMemberCommand, user_id: int, service: ProjectService
) -> tuple[BaseModel, list[Outgoing]]:
    result = service.add_member(command.project_id, command.email, actor_id=user_id)
    if isinstance(result, MemberError):
        return _error(command.request_id, result), []
    member, new_user = result
    project = service.get_project(command.project_id)
    project_added = ProjectAdded(project=ProjectResponse.model_validate(project))
    member_added = MemberAdded(
        project_id=command.project_id, member=_member_response(member, new_user)
    )
    recipients = _member_ids(command.project_id, user_id, service)
    return Ack(request_id=command.request_id), [
        ([new_user.id], project_added),
        (recipients, member_added),
    ]


def _remove_member(
    command: RemoveMemberCommand, user_id: int, service: ProjectService
) -> tuple[BaseModel, list[Outgoing]]:
    # Resolve recipients before the removal so the removed user is notified as well.
    recipients = _member_ids(command.project_id, user_id, service)
    error = service.remove_member(command.project_id, command.user_id, actor_id=user_id)
    if error:
        return _error(command.request_id, error), []
    member_removed = MemberRemoved(project_id=command.project_id, user_id=command.user_id)
    project_removed = ProjectRemoved(project_id=command.project_id)
    return Ack(request_id=command.request_id), [
        (recipients, member_removed),
        ([command.user_id], project_removed),
    ]


def _member_ids(project_id: int, actor_id: int, service: ProjectService) -> list[int]:
    result = service.list_members(project_id, actor_id=actor_id)
    if isinstance(result, MemberError):
        return []
    return [member.user_id for member, _ in result]


def _member_response(member: ProjectMember, user: User) -> MemberResponse:
    return MemberResponse(user_id=user.id, email=user.email, role=member.role)


def _error(request_id: str, error: MemberError) -> ErrorMessage:
    _, detail = MEMBER_ERRORS[error]
    return ErrorMessage(request_id=request_id, code=error.value, detail=detail)


def _describe(exc: ValidationError) -> str:
    """Compact, single-line summary of a validation error."""
    return "; ".join(
        f"{'.'.join(str(part) for part in err['loc']) or 'message'}: {err['msg']}"
        for err in exc.errors()
    )


def _request_id_of(raw: str) -> str | None:
    """Best-effort `request_id` of a frame that failed validation."""
    try:
        payload = json.loads(raw)
    except ValueError:
        return None
    request_id = payload.get("request_id") if isinstance(payload, dict) else None
    return request_id if isinstance(request_id, str) else None
