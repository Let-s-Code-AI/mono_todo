"""E2E tests – Task change history modal
Coverage:
  - New task → empty history message, no rows
  - Title edit → 'Tytuł' row with old and new value
"""

import uuid

import pytest
from playwright.sync_api import Page, expect

from pages import DashboardPage


def unique_title(prefix: str = "Zadanie E2E") -> str:
    """Unique title without keywords the mock AI heuristic reacts to."""
    return f"{prefix} {uuid.uuid4().hex[:6]}"


@pytest.fixture
def dashboard(logged_in_page: Page) -> DashboardPage:
    return DashboardPage(logged_in_page)


class TestTaskHistory:

    def test_new_task_has_empty_history(self, dashboard: DashboardPage):
        """A freshly created task shows the empty-history message and no rows."""
        title = unique_title()
        dashboard.add_task(title)

        modal = dashboard.open_history_modal(title)

        expect(modal.empty).to_be_visible()
        expect(modal.rows).to_have_count(0)
        modal.close()

    def test_title_edit_appears_in_history(self, dashboard: DashboardPage):
        """Editing the title adds a 'Tytuł' row showing the old and the new value."""
        title, edited = unique_title(), unique_title("Zadanie E2E po edycji")
        dashboard.add_task(title)
        edit = dashboard.open_edit_modal(title)
        edit.title_input.fill(edited)
        edit.submit()

        modal = dashboard.open_history_modal(edited)

        row = modal.row("Tytuł")
        expect(row).to_be_visible()
        expect(row).to_contain_text(title)
        expect(row).to_contain_text(edited)
        modal.close()
