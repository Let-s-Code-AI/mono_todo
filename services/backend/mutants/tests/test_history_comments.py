"""Tests for task history and comments functionality."""

from fastapi.testclient import TestClient

from app.db.models import Status, Priority
from app.schemas.task import TaskCreate, TaskUpdate


def test_update_task_creates_history(client: TestClient, test_db):
    """Updating a task title should create a history entry."""
    task_data = TaskCreate(title="Original Title", description="Test task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    update_data = TaskUpdate(title="Updated Title")
    res = client.patch(f"/tasks/{task_id}", json=update_data.model_dump(exclude_unset=True))
    assert res.status_code == 200

    res = client.get(f"/tasks/{task_id}/history")
    assert res.status_code == 200
    history = res.json()
    assert len(history) == 1
    assert history[0]["field_name"] == "title"
    assert history[0]["old_value"] == "Original Title"
    assert history[0]["new_value"] == "Updated Title"


def test_history_multiple_fields(client: TestClient):
    """Updating multiple fields should create multiple history entries."""
    task_data = TaskCreate(title="Test", priority=Priority.LOW, status=Status.TODO)
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    update_data = TaskUpdate(priority=Priority.HIGH, status=Status.DONE)
    res = client.patch(f"/tasks/{task_id}", json=update_data.model_dump(exclude_unset=True))
    assert res.status_code == 200

    res = client.get(f"/tasks/{task_id}/history")
    assert res.status_code == 200
    history = res.json()
    assert len(history) == 2
    field_names = {h["field_name"] for h in history}
    assert field_names == {"priority", "status"}


def test_history_not_found_for_other_user(client: TestClient, unauth_client: TestClient, test_db):
    """Getting history for another user's task should return 404."""
    task_data = TaskCreate(title="Private Task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    from app.db.models import User
    from app.core.security import hash_password, create_access_token

    other_user = User(email="other@example.com", hashed_password=hash_password("pass"))
    test_db.add(other_user)
    test_db.commit()
    test_db.refresh(other_user)

    other_token = create_access_token({"sub": str(other_user.id)})
    unauth_client.headers.update({"Authorization": f"Bearer {other_token}"})

    res = unauth_client.get(f"/tasks/{task_id}/history")
    assert res.status_code == 404


def test_add_comment(client: TestClient):
    """Adding a comment should return 201 with comment details."""
    task_data = TaskCreate(title="Test Task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    comment_data = {"content": "This is a test comment"}
    res = client.post(f"/tasks/{task_id}/comments", json=comment_data)
    assert res.status_code == 201
    comment = res.json()
    assert comment["content"] == "This is a test comment"
    assert comment["task_id"] == task_id
    assert "user_email" in comment
    assert "created_at" in comment


def test_get_comments(client: TestClient):
    """Getting comments should return list of all comments for a task."""
    task_data = TaskCreate(title="Test Task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    res = client.post(f"/tasks/{task_id}/comments", json={"content": "First comment"})
    assert res.status_code == 201

    res = client.post(f"/tasks/{task_id}/comments", json={"content": "Second comment"})
    assert res.status_code == 201

    res = client.get(f"/tasks/{task_id}/comments")
    assert res.status_code == 200
    comments = res.json()
    assert len(comments) == 2
    assert comments[0]["content"] == "First comment"
    assert comments[1]["content"] == "Second comment"


def test_comments_unauthorized(unauth_client: TestClient):
    """Unauthorized users cannot add comments (requires token)."""
    res = unauth_client.post("/tasks/1/comments", json={"content": "Hacker comment"})
    assert res.status_code == 401


def test_empty_history_for_new_task(client: TestClient):
    """A newly created task should have no history."""
    task_data = TaskCreate(title="New Task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    res = client.get(f"/tasks/{task_id}/history")
    assert res.status_code == 200
    assert res.json() == []


def test_empty_comments_for_new_task(client: TestClient):
    """A newly created task should have no comments."""
    task_data = TaskCreate(title="New Task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    res = client.get(f"/tasks/{task_id}/comments")
    assert res.status_code == 200
    assert res.json() == []


def test_history_includes_user_email(client: TestClient, test_user):
    """History entries should include the user's email."""
    task_data = TaskCreate(title="Original")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    update_data = TaskUpdate(title="Modified")
    res = client.patch(f"/tasks/{task_id}", json=update_data.model_dump(exclude_unset=True))
    assert res.status_code == 200

    res = client.get(f"/tasks/{task_id}/history")
    assert res.status_code == 200
    history = res.json()
    assert history[0]["user_email"] == test_user.email


def test_comments_include_user_email(client: TestClient, test_user):
    """Comments should include the user's email."""
    task_data = TaskCreate(title="Test Task")
    res = client.post("/tasks/", json=task_data.model_dump())
    assert res.status_code == 201
    task_id = res.json()["id"]

    res = client.post(f"/tasks/{task_id}/comments", json={"content": "A comment"})
    assert res.status_code == 201
    comment = res.json()
    assert comment["user_email"] == test_user.email
