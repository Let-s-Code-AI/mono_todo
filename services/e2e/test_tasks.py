"""E2E tests – Task operations (Playwright + pytest)
Coverage:
  - Add task: modal (+ Nowe zadanie) → fill in → save → appears on the list
  - Edit: edit modal → change data → save / cancel
  - Delete: confirm() accepted / dismissed
  - Status: toggle todo ↔ done
"""

import uuid

import pytest
from playwright.sync_api import APIRequestContext, Page, expect

from pages import DONE_CLASS, DashboardPage


def unique_title(prefix: str = "Zadanie E2E") -> str:
    """Unique title without keywords the mock AI heuristic reacts to."""
    return f"{prefix} {uuid.uuid4().hex[:6]}"


@pytest.fixture
def dashboard(logged_in_page: Page) -> DashboardPage:
    return DashboardPage(logged_in_page)


# ── ADD TASK ──────────────────────────────────────────────────────────────────


class TestAddTask:

    def test_add_task_appears_on_list(self, dashboard: DashboardPage):
        """Open the modal, fill in the form and save → the task appears on the list."""
        title = unique_title()

        card = dashboard.add_task(title)

        expect(card).to_be_visible()
        expect(dashboard.toast("Zadanie dodane")).to_be_visible()

    def test_add_task_clears_input(self, dashboard: DashboardPage):
        """After adding a task, a re-opened modal has an empty title field."""
        dashboard.add_task(unique_title())

        modal = dashboard.open_new_task_modal()

        expect(modal.title_input).to_have_value("")
        modal.cancel()

    def test_add_task_empty_title_blocked(self, dashboard: DashboardPage):
        """The 'Dodaj zadanie' button is disabled without a title and becomes enabled once one is typed."""
        modal = dashboard.open_new_task_modal()

        expect(modal.submit_button).to_be_disabled()
        modal.title_input.fill("x")
        expect(modal.submit_button).to_be_enabled()
        modal.title_input.fill("")
        expect(modal.submit_button).to_be_disabled()

        modal.cancel()


# ── EDIT TASK ─────────────────────────────────────────────────────────────────


class TestEditTask:

    def test_edit_task_via_modal(self, dashboard: DashboardPage):
        """Edit → change the title → save → the list shows the new title instead of the old one."""
        title, edited = unique_title(), unique_title("Zadanie E2E edytowane")
        dashboard.add_task(title)

        modal = dashboard.open_edit_modal(title)
        expect(modal.title_input).to_have_value(title)
        modal.title_input.fill(edited)
        modal.submit()

        expect(dashboard.task_card(edited)).to_be_visible()
        expect(dashboard.task_card(title)).to_have_count(0)
        expect(dashboard.toast("Zadanie zaktualizowane")).to_be_visible()

    def test_edit_cancel_keeps_original(self, dashboard: DashboardPage):
        """Cancelling the edit → the original title stays unchanged."""
        title, edited = unique_title(), unique_title("Zadanie E2E edytowane")
        dashboard.add_task(title)

        modal = dashboard.open_edit_modal(title)
        modal.title_input.fill(edited)
        modal.cancel()

        expect(dashboard.task_card(title)).to_be_visible()
        expect(dashboard.task_card(edited)).to_have_count(0)


# ── DELETE TASK ───────────────────────────────────────────────────────────────


class TestDeleteTask:

    def test_delete_task_disappears_from_list(self, dashboard: DashboardPage):
        """Delete → confirm() accepted → the task disappears from the list."""
        title = unique_title()
        card = dashboard.add_task(title)
        expect(card).to_be_visible()

        dashboard.delete_task(title, confirm=True)

        expect(card).to_have_count(0)

    def test_delete_task_shows_toast(self, dashboard: DashboardPage):
        """After deleting a task the 'Zadanie usunięte' toast appears."""
        title = unique_title()
        dashboard.add_task(title)

        dashboard.delete_task(title, confirm=True)

        expect(dashboard.toast("Zadanie usunięte")).to_be_visible()

    def test_delete_cancelled_keeps_task(self, dashboard: DashboardPage, user_api: APIRequestContext):
        """Delete → confirm() dismissed → the task stays on the list and in the backend."""
        title = unique_title()
        card = dashboard.add_task(title)
        expect(card).to_be_visible()

        dashboard.delete_task(title, confirm=False)

        expect(card).to_be_visible()
        titles_in_backend = [task["title"] for task in user_api.get("/tasks/").json()]
        assert title in titles_in_backend, "Odrzucenie confirm() nie powinno wywołać DELETE"


# ── TOGGLE STATUS ─────────────────────────────────────────────────────────────


class TestToggleStatus:

    def test_toggle_task_to_done(self, dashboard: DashboardPage):
        """Clicking the checkbox → the card gets the 'done' class and lands in the Ukończone section."""
        title = unique_title()
        card = dashboard.add_task(title)

        dashboard.toggle_task(title)

        expect(card).to_have_class(DONE_CLASS)
        expect(dashboard.page.get_by_role("heading", name="Ukończone (1)")).to_be_visible()

    def test_toggle_task_back_to_todo(self, dashboard: DashboardPage):
        """Clicking the checkbox twice → back to the 'todo' status."""
        title = unique_title()
        card = dashboard.add_task(title)

        dashboard.toggle_task(title)
        expect(card).to_have_class(DONE_CLASS)

        dashboard.toggle_task(title)

        expect(card).not_to_have_class(DONE_CLASS)
        expect(dashboard.page.get_by_role("heading", name="Do zrobienia (1)")).to_be_visible()
