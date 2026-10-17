"""Tests for the projects WebSocket (`/ws/projects`).

Scenarios:
  - Authentication by token in the query string
  - Snapshot of the user's projects on connect
  - Commands (create_project, list_members, add_member, remove_member) with ack / error replies
  - create_project with member_emails: members added atomically, unknown email creates nothing
  - Push events delivered to other members' connections
"""

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.core.security import create_access_token
from app.db.models import User


def _socket_url(user: User) -> str:
    return f"/ws/projects?token={create_access_token({'sub': str(user.id)})}"


def _create_project(client: TestClient, name: str = "Remont") -> int:
    response = client.post("/projects/", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def _member(user: User, role: str) -> dict:
    return {"user_id": user.id, "email": user.email, "role": role}


# ─────────────────────────────────────────────────────────────────────────────
# Connection
# ─────────────────────────────────────────────────────────────────────────────


def test_invalid_token_closes_socket_with_4401(client: TestClient) -> None:
    """Scenario: Połączenie z nieprawidłowym tokenem jest zamykane kodem 4401."""
    with (
        client.websocket_connect("/ws/projects?token=invalid") as socket,
        pytest.raises(WebSocketDisconnect) as exc_info,
    ):
        socket.receive_json()

    assert exc_info.value.code == 4401


def test_snapshot_lists_user_projects_on_connect(client: TestClient, test_user: User) -> None:
    """Scenario: Zaraz po połączeniu klient dostaje listę swoich projektów."""
    _create_project(client, "Remont")

    with client.websocket_connect(_socket_url(test_user)) as socket:
        snapshot = socket.receive_json()

    assert snapshot["type"] == "projects"
    assert [p["name"] for p in snapshot["projects"]] == ["Remont"]


# ─────────────────────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────────────────────


def test_create_project_pushes_project_added_then_ack(client: TestClient, test_user: User) -> None:
    """Scenario: create_project tworzy projekt, wysyła project_added i ack z tym samym request_id."""
    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()  # snapshot
        socket.send_json({"type": "create_project", "request_id": "r1", "name": "Remont"})
        added = socket.receive_json()
        ack = socket.receive_json()

    assert added["type"] == "project_added"
    assert added["project"]["name"] == "Remont"
    assert added["project"]["owner_id"] == test_user.id
    assert ack == {"type": "ack", "request_id": "r1"}
    assert [p["name"] for p in client.get("/projects/").json()] == ["Remont"]


def test_list_members_replies_with_request_id(client: TestClient, test_user: User) -> None:
    """Scenario: list_members zwraca członków projektu w odpowiedzi z request_id."""
    project_id = _create_project(client)

    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()
        socket.send_json({"type": "list_members", "request_id": "r1", "project_id": project_id})
        reply = socket.receive_json()

    assert reply == {
        "type": "members",
        "request_id": "r1",
        "project_id": project_id,
        "members": [_member(test_user, "owner")],
    }


def test_add_member_with_unknown_email_returns_error(client: TestClient, test_user: User) -> None:
    """Scenario: add_member z nieznanym emailem zwraca error z kodem i request_id."""
    project_id = _create_project(client)

    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()
        socket.send_json(
            {
                "type": "add_member",
                "request_id": "r1",
                "project_id": project_id,
                "email": "nobody@example.com",
            }
        )
        reply = socket.receive_json()

    assert reply == {
        "type": "error",
        "request_id": "r1",
        "code": "user_not_found",
        "detail": "User not found",
        "email": None,
    }


def test_malformed_command_returns_invalid_message_error(
    client: TestClient, test_user: User
) -> None:
    """Scenario: Nieznane polecenie dostaje error invalid_message, ale połączenie żyje dalej."""
    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()
        socket.send_json({"type": "explode", "request_id": "r1"})
        reply = socket.receive_json()
        socket.send_json({"type": "create_project", "request_id": "r2", "name": "Nadal działa"})
        socket.receive_json()  # project_added
        ack = socket.receive_json()

    assert reply["type"] == "error"
    assert reply["request_id"] == "r1"
    assert reply["code"] == "invalid_message"
    assert ack == {"type": "ack", "request_id": "r2"}


# ─────────────────────────────────────────────────────────────────────────────
# Push events to other members
# ─────────────────────────────────────────────────────────────────────────────


def test_add_member_notifies_new_member_and_owner(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Dodany użytkownik dostaje project_added i member_added, owner tylko member_added."""
    project_id = _create_project(client)

    with (
        client.websocket_connect(_socket_url(test_user)) as owner_socket,
        client.websocket_connect(_socket_url(other_user)) as member_socket,
    ):
        owner_socket.receive_json()
        assert member_socket.receive_json()["projects"] == []
        owner_socket.send_json(
            {
                "type": "add_member",
                "request_id": "r1",
                "project_id": project_id,
                "email": other_user.email,
            }
        )
        project_added = member_socket.receive_json()
        member_added_for_member = member_socket.receive_json()
        member_added_for_owner = owner_socket.receive_json()
        ack = owner_socket.receive_json()

    assert project_added == {
        "type": "project_added",
        "project": {"id": project_id, "name": "Remont", "owner_id": test_user.id},
    }
    assert member_added_for_member == {
        "type": "member_added",
        "project_id": project_id,
        "member": _member(other_user, "member"),
    }
    assert member_added_for_owner == member_added_for_member
    assert ack == {"type": "ack", "request_id": "r1"}


def test_remove_member_notifies_everyone_and_revokes_project(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Usunięty członek dostaje member_removed i project_removed, owner member_removed."""
    project_id = _create_project(client)
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    with (
        client.websocket_connect(_socket_url(test_user)) as owner_socket,
        client.websocket_connect(_socket_url(other_user)) as member_socket,
    ):
        owner_socket.receive_json()
        member_socket.receive_json()
        owner_socket.send_json(
            {
                "type": "remove_member",
                "request_id": "r1",
                "project_id": project_id,
                "user_id": other_user.id,
            }
        )
        owner_events = [owner_socket.receive_json(), owner_socket.receive_json()]
        member_events = [member_socket.receive_json(), member_socket.receive_json()]

    member_removed = {"type": "member_removed", "project_id": project_id, "user_id": other_user.id}
    assert owner_events == [member_removed, {"type": "ack", "request_id": "r1"}]
    assert member_events == [member_removed, {"type": "project_removed", "project_id": project_id}]
    assert client.get(f"/projects/{project_id}/members").json() == [_member(test_user, "owner")]


def test_connection_sees_changes_made_through_rest(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Długo otwarte połączenie nie trzyma nieaktualnych danych między poleceniami."""
    project_id = _create_project(client)
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    with client.websocket_connect(_socket_url(other_user)) as member_socket:
        member_socket.receive_json()
        member_socket.send_json(
            {"type": "list_members", "request_id": "r1", "project_id": project_id}
        )
        assert len(member_socket.receive_json()["members"]) == 2

        client.delete(f"/projects/{project_id}/members/{other_user.id}")

        member_socket.send_json(
            {"type": "list_members", "request_id": "r2", "project_id": project_id}
        )
        reply = member_socket.receive_json()

    assert reply["type"] == "error"
    assert reply["code"] == "not_member"


# ─────────────────────────────────────────────────────────────────────────────
# Create project with initial members
# ─────────────────────────────────────────────────────────────────────────────


def test_create_project_with_member_emails_adds_members_and_notifies_them(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: create_project z member_emails dodaje członków i wysyła im project_added."""
    with (
        client.websocket_connect(_socket_url(test_user)) as owner_socket,
        client.websocket_connect(_socket_url(other_user)) as member_socket,
    ):
        owner_socket.receive_json()
        member_socket.receive_json()
        owner_socket.send_json(
            {
                "type": "create_project",
                "request_id": "r1",
                "name": "Remont",
                "member_emails": [other_user.email],
            }
        )
        owner_added = owner_socket.receive_json()
        ack = owner_socket.receive_json()
        project_id = owner_added["project"]["id"]
        # REST check first so a missing push fails the test instead of blocking on receive.
        assert client.get(f"/projects/{project_id}/members").json() == [
            _member(test_user, "owner"),
            _member(other_user, "member"),
        ]
        member_added = member_socket.receive_json()

    assert ack == {"type": "ack", "request_id": "r1"}
    assert owner_added["type"] == "project_added"
    assert member_added == owner_added


def test_create_project_with_unknown_email_creates_nothing(
    client: TestClient, test_user: User
) -> None:
    """Scenario: Nieznany email w member_emails zwraca error z tym emailem; projekt nie powstaje."""
    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()
        socket.send_json(
            {
                "type": "create_project",
                "request_id": "r1",
                "name": "Remont",
                "member_emails": ["nobody@example.com"],
            }
        )
        reply = socket.receive_json()

    assert reply == {
        "type": "error",
        "request_id": "r1",
        "code": "user_not_found",
        "detail": "User not found: nobody@example.com",
        "email": "nobody@example.com",
    }
    assert client.get("/projects/").json() == []


def test_create_project_ignores_blank_duplicate_and_own_email(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Puste wpisy, duplikaty i własny email właściciela są pomijane bez błędu."""
    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()
        socket.send_json(
            {
                "type": "create_project",
                "request_id": "r1",
                "name": "Remont",
                "member_emails": [
                    f" {other_user.email} ",
                    other_user.email,
                    test_user.email,
                    "   ",
                ],
            }
        )
        added = socket.receive_json()
        ack = socket.receive_json()

    assert ack == {"type": "ack", "request_id": "r1"}
    project_id = added["project"]["id"]
    assert client.get(f"/projects/{project_id}/members").json() == [
        _member(test_user, "owner"),
        _member(other_user, "member"),
    ]


def test_create_project_with_too_many_emails_is_rejected(
    client: TestClient, test_user: User
) -> None:
    """Scenario: Więcej niż 20 emaili to invalid_message, projekt nie powstaje."""
    with client.websocket_connect(_socket_url(test_user)) as socket:
        socket.receive_json()
        socket.send_json(
            {
                "type": "create_project",
                "request_id": "r1",
                "name": "Remont",
                "member_emails": [f"user{i}@example.com" for i in range(21)],
            }
        )
        reply = socket.receive_json()

    assert reply["type"] == "error"
    assert reply["code"] == "invalid_message"
    assert client.get("/projects/").json() == []
