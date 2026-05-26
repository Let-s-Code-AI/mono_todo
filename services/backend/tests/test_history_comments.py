"""Tests for task history and comments (Epic 4)."""

from sqlmodel import Session

from app.db.models import Priority, Status, Task, User
from fastapi.testclient import TestClient


class TestTaskHistory:
    """Test suite for task change history (US-4.1, US-4.2)."""

    def test_historia_zadania_pusta_po_utworzeniu(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Historia zadania jest pusta zaraz po jego utworzeniu."""
        task = Task(
            title="Test task",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.get(f"/tasks/{task.id}/history")
        assert response.status_code == 200
        assert response.json() == []

    def test_historia_zadania_dla_nieistniejacego_zadania_zwraca_404(
        self, client: TestClient
    ) -> None:
        """Scenario: GET /tasks/{nonexistent}/history zwraca 404."""
        response = client.get("/tasks/999/history")
        assert response.status_code == 404

    def test_jeden_wpis_historii_na_zmienione_pole(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Zmiana jednego pola tworzy dokładnie jeden wpis historii."""
        task = Task(
            title="Oryginalny tytuł",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.patch(
            f"/tasks/{task.id}", json={"title": "Nowy tytuł"}
        )
        assert response.status_code == 200

        history_response = client.get(f"/tasks/{task.id}/history")
        assert history_response.status_code == 200
        data = history_response.json()
        assert len(data) == 1
        assert data[0]["field_name"] == "title"
        assert data[0]["old_value"] == "Oryginalny tytuł"
        assert data[0]["new_value"] == "Nowy tytuł"
        assert data[0]["changed_by_id"] == test_user.id

    def test_wiele_wpisow_historii_dla_wielu_zmienionych_pol(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: PATCH ze zmianami w wielu polach tworzy wiele wpisów."""
        task = Task(
            title="Original",
            description="Desc",
            priority=Priority.LOW,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.patch(
            f"/tasks/{task.id}",
            json={
                "title": "Updated",
                "description": "Updated desc",
                "priority": "high",
            },
        )
        assert response.status_code == 200

        history_response = client.get(f"/tasks/{task.id}/history")
        assert history_response.status_code == 200
        data = history_response.json()
        assert len(data) == 3

        field_changes = {entry["field_name"]: entry for entry in data}
        assert "title" in field_changes
        assert "description" in field_changes
        assert "priority" in field_changes

    def test_aktualizacja_bez_zmian_nie_tworzy_historii(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: PATCH z tą samą wartością nie tworzy wpisu historii."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.patch(f"/tasks/{task.id}", json={"title": "Test"})
        assert response.status_code == 200

        history_response = client.get(f"/tasks/{task.id}/history")
        assert history_response.status_code == 200
        assert history_response.json() == []

    def test_historia_przechowuje_zmiane_statusu(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Zmiana statusu jest poprawnie zalogowana."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.patch(f"/tasks/{task.id}", json={"status": "done"})
        assert response.status_code == 200

        history_response = client.get(f"/tasks/{task.id}/history")
        data = history_response.json()
        assert len(data) == 1
        assert data[0]["field_name"] == "status"
        assert data[0]["old_value"] == "todo"
        assert data[0]["new_value"] == "done"

    def test_historia_przechowuje_zmiane_priorytetu(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Zmiana priorytetu jest poprawnie zalogowana."""
        task = Task(
            title="Test",
            priority=Priority.LOW,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.patch(f"/tasks/{task.id}", json={"priority": "high"})
        assert response.status_code == 200

        history_response = client.get(f"/tasks/{task.id}/history")
        data = history_response.json()
        assert len(data) == 1
        assert data[0]["field_name"] == "priority"
        assert data[0]["old_value"] == "low"
        assert data[0]["new_value"] == "high"

    def test_historia_ma_poprawny_changed_by_id(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: changed_by_id równa się ID bieżącego użytkownika."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.patch(f"/tasks/{task.id}", json={"title": "Changed"})
        assert response.status_code == 200

        history_response = client.get(f"/tasks/{task.id}/history")
        data = history_response.json()
        assert data[0]["changed_by_id"] == test_user.id

    def test_historia_posortowana_od_najnowszej(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Historia zwrócona od najnowszej do najstarszej zmiany."""
        task = Task(
            title="v1",
            priority=Priority.LOW,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        # First change
        client.patch(f"/tasks/{task.id}", json={"title": "v2"})
        # Second change
        client.patch(f"/tasks/{task.id}", json={"priority": "high"})

        history_response = client.get(f"/tasks/{task.id}/history")
        data = history_response.json()
        assert len(data) == 2
        # Newest should be priority change
        assert data[0]["field_name"] == "priority"
        assert data[1]["field_name"] == "title"

    def test_uzytkownik_nie_widzi_historii_cudzego_zadania(
        self, client: TestClient, test_db: Session, test_user: User, test_admin: User
    ) -> None:
        """Scenario: Użytkownik nie ma dostępu do historii zadania innego użytkownika."""
        task = Task(
            title="Admin's task",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_admin.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        # Regular user tries to GET history of admin's task
        response = client.get(f"/tasks/{task.id}/history")
        assert response.status_code == 404


class TestTaskComments:
    """Test suite for task comments (US-4.3, US-4.4)."""

    def test_lista_komentarzy_pusta_przed_dodaniem(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Lista komentarzy nowego zadania jest pusta."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.get(f"/tasks/{task.id}/comments")
        assert response.status_code == 200
        assert response.json() == []

    def test_dodanie_komentarza_do_zadania(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: POST /tasks/{id}/comments tworzy komentarz."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.post(
            f"/tasks/{task.id}/comments", json={"content": "Great task!"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["task_id"] == task.id
        assert data["content"] == "Great task!"
        assert data["author_id"] == test_user.id
        assert "id" in data
        assert "created_at" in data

    def test_dodanie_komentarza_do_nieistniejacego_zadania_zwraca_404(
        self, client: TestClient
    ) -> None:
        """Scenario: POST /tasks/{nonexistent}/comments zwraca 404."""
        response = client.post("/tasks/999/comments", json={"content": "Test"})
        assert response.status_code == 404

    def test_author_id_ustawiony_na_zalogowanego_uzytkownika(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: author_id komentarza równa się ID bieżącego użytkownika."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.post(
            f"/tasks/{task.id}/comments", json={"content": "My comment"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["author_id"] == test_user.id

    def test_tresc_komentarza_jest_wymagana(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: POST z pustą treścią zwraca 422 (Pydantic validation)."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        response = client.post(f"/tasks/{task.id}/comments", json={"content": ""})
        assert response.status_code == 422

    def test_lista_komentarzy_po_dodaniu(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: GET /tasks/{id}/comments zwraca dodane komentarze."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        client.post(f"/tasks/{task.id}/comments", json={"content": "First"})
        client.post(f"/tasks/{task.id}/comments", json={"content": "Second"})

        response = client.get(f"/tasks/{task.id}/comments")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["content"] == "First"
        assert data[1]["content"] == "Second"

    def test_lista_komentarzy_dla_nieistniejacego_zadania_zwraca_404(
        self, client: TestClient
    ) -> None:
        """Scenario: GET /tasks/{nonexistent}/comments zwraca 404."""
        response = client.get("/tasks/999/comments")
        assert response.status_code == 404

    def test_komentarze_posortowane_od_najstarszego(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Komentarze posortowane od najstarszego do najnowszego."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        client.post(f"/tasks/{task.id}/comments", json={"content": "First"})
        client.post(f"/tasks/{task.id}/comments", json={"content": "Second"})

        response = client.get(f"/tasks/{task.id}/comments")
        data = response.json()
        assert data[0]["content"] == "First"
        assert data[1]["content"] == "Second"

    def test_uzytkownik_nie_widzi_komentarzy_cudzego_zadania(
        self, client: TestClient, test_db: Session, test_user: User, test_admin: User
    ) -> None:
        """Scenario: Użytkownik nie ma dostępu do komentarzy zadania innego użytkownika."""
        task = Task(
            title="Admin's task",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_admin.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        # Regular user tries to GET comments of admin's task
        response = client.get(f"/tasks/{task.id}/comments")
        assert response.status_code == 404


class TestHistoryAndCommentsCrossCutting:
    """Cross-cutting tests ensuring history and comments are independent."""

    def test_dodanie_komentarza_nie_tworzy_historii(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Dodawanie komentarza nie tworzy wpisów historii."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        # Add a comment
        client.post(f"/tasks/{task.id}/comments", json={"content": "Comment"})

        # Check history is still empty
        history_response = client.get(f"/tasks/{task.id}/history")
        assert history_response.json() == []

    def test_aktualizacja_zadania_nie_tworzy_komentarzy(
        self, client: TestClient, test_db: Session, test_user: User
    ) -> None:
        """Scenario: Aktualizacja zadania nie tworzy komentarzy."""
        task = Task(
            title="Test",
            priority=Priority.MEDIUM,
            status=Status.TODO,
            owner_id=test_user.id,
        )
        test_db.add(task)
        test_db.commit()
        test_db.refresh(task)

        # Update the task
        client.patch(f"/tasks/{task.id}", json={"title": "Updated"})

        # Check comments are still empty
        comments_response = client.get(f"/tasks/{task.id}/comments")
        assert comments_response.json() == []
