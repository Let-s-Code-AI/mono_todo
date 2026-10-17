"""Tests for projects and project membership.

BDD scenarios for:
  - Creating and listing projects
  - Adding and removing project members by email
  - Project-scoped task visibility
"""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.db.models import Project, User


# ─────────────────────────────────────────────────────────────────────────────
# Projects
# ─────────────────────────────────────────────────────────────────────────────


def test_create_project_returns_201_with_current_user_as_owner(
    client: TestClient, test_user: User
) -> None:
    """Scenario: Zalogowany użytkownik tworzy projekt i staje się jego ownerem."""
    response = client.post("/projects/", json={"name": "Remont"})

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Remont"
    assert data["owner_id"] == test_user.id


def test_list_projects_returns_only_projects_user_belongs_to(
    client: TestClient, test_db: Session, other_user: User
) -> None:
    """Scenario: Lista projektów zawiera moje projekty, a nie cudze."""
    client.post("/projects/", json={"name": "Mój projekt"})
    test_db.add(Project(name="Cudzy projekt", owner_id=other_user.id))
    test_db.commit()

    response = client.get("/projects/")

    assert response.status_code == 200
    names = [p["name"] for p in response.json()]
    assert names == ["Mój projekt"]


# ─────────────────────────────────────────────────────────────────────────────
# Members
# ─────────────────────────────────────────────────────────────────────────────


def _create_project(client: TestClient, name: str = "Projekt") -> int:
    """Create a project through the API and return its id."""
    response = client.post("/projects/", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def test_add_member_by_email_as_owner_returns_201(
    client: TestClient, other_user: User
) -> None:
    """Scenario: Owner dodaje istniejącego użytkownika do projektu po emailu."""
    project_id = _create_project(client)

    response = client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == other_user.id
    assert data["email"] == other_user.email
    assert data["role"] == "member"


def test_add_member_as_non_owner_returns_403(
    client: TestClient, other_client: TestClient, other_user: User, test_db: Session
) -> None:
    """Scenario: Zwykły członek próbuje dodać kogoś do projektu."""
    project_id = _create_project(client)
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})
    test_db.add(User(email="third@example.com", hashed_password="x"))
    test_db.commit()

    response = other_client.post(f"/projects/{project_id}/members", json={"email": "third@example.com"})

    assert response.status_code == 403


def test_add_member_with_unknown_email_returns_404(client: TestClient) -> None:
    """Scenario: Owner podaje email, którego nie ma w systemie."""
    project_id = _create_project(client)

    response = client.post(f"/projects/{project_id}/members", json={"email": "nobody@example.com"})

    assert response.status_code == 404


def test_add_member_to_unknown_project_returns_404(client: TestClient, other_user: User) -> None:
    """Scenario: Dodawanie członka do projektu, który nie istnieje."""
    response = client.post("/projects/9999/members", json={"email": other_user.email})

    assert response.status_code == 404


def test_add_member_twice_returns_409(client: TestClient, other_user: User) -> None:
    """Scenario: Owner dodaje tego samego użytkownika drugi raz."""
    project_id = _create_project(client)
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    response = client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    assert response.status_code == 409


def test_list_members_returns_owner_and_members_with_roles(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Członek projektu widzi listę członków z rolami."""
    project_id = _create_project(client)
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    response = client.get(f"/projects/{project_id}/members")

    assert response.status_code == 200
    members = {m["email"]: m["role"] for m in response.json()}
    assert members == {test_user.email: "owner", other_user.email: "member"}


def test_list_members_as_non_member_returns_403(
    client: TestClient, other_client: TestClient
) -> None:
    """Scenario: Użytkownik spoza projektu próbuje podejrzeć jego członków."""
    project_id = _create_project(client)

    response = other_client.get(f"/projects/{project_id}/members")

    assert response.status_code == 403


def test_remove_member_as_owner_returns_204_and_removes_from_list(
    client: TestClient, test_user: User, other_user: User
) -> None:
    """Scenario: Owner usuwa członka z projektu."""
    project_id = _create_project(client)
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})

    response = client.delete(f"/projects/{project_id}/members/{other_user.id}")

    assert response.status_code == 204
    emails = [m["email"] for m in client.get(f"/projects/{project_id}/members").json()]
    assert emails == [test_user.email]
