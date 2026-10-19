"""Tests for task change history endpoint."""

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.db.models import TaskHistory, User


def test_get_history_of_new_task_returns_empty_list(client: TestClient) -> None:
    """Scenario: a freshly created task has no recorded changes."""
    created = client.post("/tasks/", json={"title": "Fresh task"}).json()

    response = client.get(f"/tasks/{created['id']}/history")

    assert response.status_code == 200
    assert response.json() == []


def test_title_change_is_recorded_in_history(client: TestClient, test_user: User) -> None:
    """Scenario: patching a title adds one history entry with old and new values."""
    created = client.post("/tasks/", json={"title": "Old title"}).json()

    client.patch(f"/tasks/{created['id']}", json={"title": "New title"})
    response = client.get(f"/tasks/{created['id']}/history")

    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 1
    assert entries[0]["field"] == "title"
    assert entries[0]["old_value"] == "Old title"
    assert entries[0]["new_value"] == "New title"
    assert entries[0]["changed_by_id"] == test_user.id


def test_patch_with_same_value_adds_no_history(client: TestClient) -> None:
    """Scenario: patching a field to its current value records nothing."""
    created = client.post("/tasks/", json={"title": "Same title"}).json()

    client.patch(f"/tasks/{created['id']}", json={"title": "Same title"})
    response = client.get(f"/tasks/{created['id']}/history")

    assert response.status_code == 200
    assert response.json() == []


def test_adding_and_removing_tag_is_recorded_in_history(client: TestClient) -> None:
    """Scenario: adding and removing a tag each record a `tags` entry."""
    created = client.post("/tasks/", json={"title": "Tagged"}).json()

    client.post(f"/tasks/{created['id']}/tags", json={"name": "work"})
    client.delete(f"/tasks/{created['id']}/tags/work")
    entries = client.get(f"/tasks/{created['id']}/history").json()

    assert [(e["field"], e["old_value"], e["new_value"]) for e in entries] == [
        ("tags", "work", None),
        ("tags", None, "work"),
    ]


def test_history_of_missing_task_returns_404(client: TestClient) -> None:
    """Scenario: asking for the history of an unknown task returns 404."""
    response = client.get("/tasks/999999/history")

    assert response.status_code == 404


def test_history_of_task_owned_by_other_user_returns_404(
    client: TestClient, other_client: TestClient
) -> None:
    """Scenario: a user cannot read history of a task they neither own nor share."""
    created = other_client.post("/tasks/", json={"title": "Private"}).json()
    other_client.patch(f"/tasks/{created['id']}", json={"title": "Still private"})

    response = client.get(f"/tasks/{created['id']}/history")

    assert response.status_code == 404


def test_project_member_can_read_history_of_shared_task(
    client: TestClient, other_client: TestClient, other_user: User
) -> None:
    """Scenario: a project member sees changes made to a task in that project."""
    project_id = client.post("/projects/", json={"name": "Wspólny"}).json()["id"]
    client.post(f"/projects/{project_id}/members", json={"email": other_user.email})
    created = client.post("/tasks/", json={"title": "Shared", "project_id": project_id}).json()
    client.patch(f"/tasks/{created['id']}", json={"title": "Shared again"})

    response = other_client.get(f"/tasks/{created['id']}/history")

    assert response.status_code == 200
    assert [e["field"] for e in response.json()] == ["title"]


def test_history_requires_authentication(unauth_client: TestClient) -> None:
    """Scenario: history endpoint rejects requests without a token."""
    response = unauth_client.get("/tasks/1/history")

    assert response.status_code == 401


def test_history_lists_newest_change_first(client: TestClient) -> None:
    """Scenario: entries are ordered from the most recent change to the oldest."""
    created = client.post("/tasks/", json={"title": "First"}).json()
    client.patch(f"/tasks/{created['id']}", json={"title": "Second"})
    client.patch(f"/tasks/{created['id']}", json={"title": "Third"})

    entries = client.get(f"/tasks/{created['id']}/history").json()

    assert [e["new_value"] for e in entries] == ["Third", "Second"]


def test_deleting_task_removes_its_history(client: TestClient, test_db: Session) -> None:
    """Scenario: deleting a task also removes its history entries."""
    created = client.post("/tasks/", json={"title": "Doomed"}).json()
    client.patch(f"/tasks/{created['id']}", json={"title": "Doomed too"})

    client.delete(f"/tasks/{created['id']}")

    remaining = test_db.exec(select(TaskHistory).where(TaskHistory.task_id == created["id"]))
    assert list(remaining) == []
