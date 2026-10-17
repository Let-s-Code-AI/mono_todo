"""Tests for task change events pushed over the projects WebSocket (`/ws/projects`).

Scenarios:
  - A task created in a project reaches every member as `task_created`
  - Edits (status, tags) reach members as `task_updated`, deletion as `task_deleted`
  - A personal task (no project) is pushed only to its owner

Each test reads exactly one pushed message after the REST call; a `list_members`
command sent afterwards acts as a sentinel so a missing push fails instead of blocking.
"""

from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.db.models import User


def _socket_url(user: User) -> str:
    return f"/ws/projects?token={create_access_token({'sub': str(user.id)})}"


def _shared_project(client: TestClient, member: User, name: str = "Remont") -> int:
    """Project owned by `client`'s user with `member` added; returns its id."""
    project_id = client.post("/projects/", json={"name": name}).json()["id"]
    response = client.post(f"/projects/{project_id}/members", json={"email": member.email})
    assert response.status_code == 201
    return project_id


def _next_after_sentinel(socket, project_id: int) -> dict:
    """First queued message once a `list_members` reply is guaranteed to follow it."""
    socket.send_json({"type": "list_members", "request_id": "sentinel", "project_id": project_id})
    return socket.receive_json()


def test_task_created_in_project_is_pushed_to_every_member(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Zadanie dodane do projektu trafia jako task_created do obu członków."""
    project_id = _shared_project(client, other_user)

    with (
        client.websocket_connect(_socket_url(test_user)) as owner_socket,
        client.websocket_connect(_socket_url(other_user)) as member_socket,
    ):
        owner_socket.receive_json()
        member_socket.receive_json()
        response = client.post("/tasks/", json={"title": "Kupić farbę", "project_id": project_id})
        assert response.status_code == 201
        member_event = _next_after_sentinel(member_socket, project_id)
        owner_event = _next_after_sentinel(owner_socket, project_id)

    assert member_event == {"type": "task_created", "task": response.json()}
    assert owner_event == member_event


def test_status_change_by_member_is_pushed_as_task_updated(
    client: TestClient, other_client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Członek oznacza zadanie jako zrobione, właściciel dostaje task_updated."""
    project_id = _shared_project(client, other_user)
    task_id = client.post(
        "/tasks/", json={"title": "Kupić farbę", "project_id": project_id}
    ).json()["id"]

    with client.websocket_connect(_socket_url(test_user)) as owner_socket:
        owner_socket.receive_json()
        response = other_client.patch(f"/tasks/{task_id}", json={"status": "done"})
        assert response.status_code == 200
        event = _next_after_sentinel(owner_socket, project_id)

    assert event == {"type": "task_updated", "task": response.json()}
    assert event["task"]["status"] == "done"


def test_tag_change_is_pushed_as_task_updated(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Dodanie tagu wysyła task_updated z nową listą tagów."""
    project_id = _shared_project(client, other_user)
    task_id = client.post(
        "/tasks/", json={"title": "Kupić farbę", "project_id": project_id}
    ).json()["id"]

    with client.websocket_connect(_socket_url(other_user)) as member_socket:
        member_socket.receive_json()
        response = client.post(f"/tasks/{task_id}/tags", json={"name": "sklep"})
        assert response.status_code == 200
        event = _next_after_sentinel(member_socket, project_id)

    assert event == {"type": "task_updated", "task": response.json()}
    assert event["task"]["tags"] == ["sklep"]


def test_task_deleted_is_pushed_to_members(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Usunięcie zadania wysyła task_deleted z id zadania i projektu."""
    project_id = _shared_project(client, other_user)
    task_id = client.post(
        "/tasks/", json={"title": "Kupić farbę", "project_id": project_id}
    ).json()["id"]

    with client.websocket_connect(_socket_url(other_user)) as member_socket:
        member_socket.receive_json()
        assert client.delete(f"/tasks/{task_id}").status_code == 204
        event = _next_after_sentinel(member_socket, project_id)

    assert event == {"type": "task_deleted", "task_id": task_id, "project_id": project_id}


def test_personal_task_is_pushed_only_to_its_owner(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Zadanie bez projektu dostaje tylko właściciel; inny użytkownik nic nie dostaje."""
    project_id = _shared_project(client, other_user)

    with (
        client.websocket_connect(_socket_url(test_user)) as owner_socket,
        client.websocket_connect(_socket_url(other_user)) as member_socket,
    ):
        owner_socket.receive_json()
        member_socket.receive_json()
        response = client.post("/tasks/", json={"title": "Prywatne"})
        assert response.status_code == 201
        owner_event = _next_after_sentinel(owner_socket, project_id)
        member_first = _next_after_sentinel(member_socket, project_id)

    assert owner_event == {"type": "task_created", "task": response.json()}
    assert member_first["type"] == "members"
