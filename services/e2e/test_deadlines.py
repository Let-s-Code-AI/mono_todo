"""E2E tests – Epic 3: Due dates and deadline management (Playwright + pytest)
Coverage:
  US-3.1  Setting due_date when creating and editing a task
  US-3.2  Overdue tasks filter (?overdue=true)
  US-3.3  AI receives due_date as context and raises the priority of near deadlines
  US-3.4  Upcoming week view (/tasks/upcoming?days=7)

The AI tests assume a backend without OPENAI_API_KEY (deterministic MockAIPriorityService):
due date within 3 days → 'high', neutral title without a near deadline → 'medium'.
"""

import uuid
from datetime import date, timedelta

import pytest
from playwright.sync_api import Page, expect

from pages import OVERDUE_CLASS, DashboardPage


def unique_title(prefix: str = "Zadanie E2E") -> str:
    """Unique title without keywords the mock AI heuristic reacts to."""
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def iso_date(days_from_today: int) -> str:
    return (date.today() + timedelta(days=days_from_today)).isoformat()


@pytest.fixture
def dashboard(logged_in_page: Page) -> DashboardPage:
    return DashboardPage(logged_in_page)


# ── US-3.1: Setting due_date ──────────────────────────────────────────────────


class TestDueDate:

    def test_create_task_with_due_date_shows_date_on_card(self, dashboard: DashboardPage):
        """Task created with a due_date → the card shows a badge with that date."""
        due = date.today() + timedelta(days=5)

        card = dashboard.add_task(unique_title(), due_date=due.isoformat())

        badge = card.locator(".due-date")
        expect(badge).to_be_visible()
        expect(badge).to_contain_text(str(due.day))
        expect(badge).to_contain_text(str(due.year))

    def test_create_task_without_due_date_has_no_date_badge(self, dashboard: DashboardPage):
        """Task without a due_date → no date badge on the card."""
        card = dashboard.add_task(unique_title())

        expect(card).to_be_visible()
        expect(card.locator(".due-date")).to_have_count(0)

    def test_edit_task_can_set_due_date(self, dashboard: DashboardPage):
        """Editing an existing task → setting a due_date → the date appears on the card."""
        title = unique_title()
        due = date.today() + timedelta(days=7)
        dashboard.add_task(title)

        modal = dashboard.open_edit_modal(title)
        expect(modal.due_date_input).to_have_value("")
        modal.due_date_input.fill(due.isoformat())
        modal.submit()

        badge = dashboard.task_card(title).locator(".due-date")
        expect(badge).to_be_visible()
        expect(badge).to_contain_text(str(due.year))

    def test_edit_task_can_clear_due_date(self, dashboard: DashboardPage):
        """Editing a task with a due_date → clearing the date → the card shows no date."""
        title = unique_title()
        due = iso_date(4)
        dashboard.add_task(title, due_date=due)

        modal = dashboard.open_edit_modal(title)
        expect(modal.due_date_input).to_have_value(due)
        modal.due_date_input.fill("")
        modal.submit()

        card = dashboard.task_card(title)
        expect(card).to_be_visible()
        expect(card.locator(".due-date")).to_have_count(0)


# ── US-3.2: Overdue tasks filter ─────────────────────────────────────────────


class TestOverdueFilter:

    def test_overdue_task_visible_in_overdue_filter(self, dashboard: DashboardPage):
        """A task with a past due_date is visible after enabling the 'Przeterminowane' filter."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(-2))
        expect(card).to_be_visible()

        dashboard.show_overdue()

        expect(card).to_be_visible()

    def test_future_task_not_in_overdue_filter(self, dashboard: DashboardPage):
        """A task with a future due_date disappears after enabling the 'Przeterminowane' filter."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(5))
        expect(card).to_be_visible()

        dashboard.show_overdue()

        expect(card).to_have_count(0)

    def test_task_without_due_date_not_in_overdue_filter(self, dashboard: DashboardPage):
        """A task without a due_date disappears after enabling the 'Przeterminowane' filter."""
        card = dashboard.add_task(unique_title())
        expect(card).to_be_visible()

        dashboard.show_overdue()

        expect(card).to_have_count(0)

    def test_overdue_task_has_visual_indicator(self, dashboard: DashboardPage):
        """The card of an overdue task has the 'overdue' class and a red date badge."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(-1))

        expect(card).to_have_class(OVERDUE_CLASS)
        expect(card.locator(".due-date.due-overdue")).to_be_visible()

    def test_all_filter_restores_full_list(self, dashboard: DashboardPage):
        """After the 'Przeterminowane' filter, the 'Wszystkie' button restores the full list."""
        future_card = dashboard.add_task(unique_title(), due_date=iso_date(5))
        dashboard.show_overdue()
        expect(future_card).to_have_count(0)

        dashboard.show_all()

        expect(future_card).to_be_visible()


# ── US-3.3: AI priority with due_date ────────────────────────────────────────


class TestAIPriorityWithDueDate:

    def test_ai_suggestion_button_requires_title(self, dashboard: DashboardPage):
        """The 'Sugestia AI' button is disabled without a title and enabled once one is typed."""
        modal = dashboard.open_new_task_modal()

        expect(modal.ai_suggest_button).to_be_visible()
        expect(modal.ai_suggest_button).to_be_disabled()
        modal.title_input.fill(unique_title())
        expect(modal.ai_suggest_button).to_be_enabled()

        modal.cancel()

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "Backend: POST /tasks/priority/analyze ignoruje due_date "
            "(PriorityAnalysisRequest nie ma tego pola), więc sugestia dla bliskiego "
            "terminu zostaje 'medium'. Frontend wysyła due_date w body."
        ),
    )
    def test_ai_suggestion_for_near_deadline_is_high(self, dashboard: DashboardPage):
        """Due date in 1 day → 'Sugestia AI' sets the priority to 'high' and shows a reason."""
        modal = dashboard.open_new_task_modal()
        modal.title_input.fill(unique_title())
        modal.due_date_input.fill(iso_date(1))

        modal.request_ai_suggestion()

        expect(modal.priority_select).to_have_value("high")
        expect(modal.priority_reason).to_be_visible()
        modal.cancel()

    def test_ai_suggestion_for_distant_deadline_is_not_high(self, dashboard: DashboardPage):
        """Due date in 30 days and a neutral title → 'Sugestia AI' does not raise the priority to 'high'."""
        modal = dashboard.open_new_task_modal()
        modal.title_input.fill(unique_title())
        modal.due_date_input.fill(iso_date(30))

        modal.request_ai_suggestion()

        expect(modal.priority_reason).to_be_visible()
        expect(modal.priority_select).not_to_have_value("high")
        modal.cancel()

    def test_create_with_ai_boosts_near_deadline_to_high(self, dashboard: DashboardPage):
        """'Użyj AI przy zapisie' + due date in 1 day → the card has 'Wysoki' priority and an AI badge."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(1), use_ai=True)

        expect(card.locator(".badge-priority-high")).to_have_text("Wysoki")
        expect(card.locator(".ai-badge")).to_be_visible()

    def test_create_with_ai_keeps_distant_deadline_medium(self, dashboard: DashboardPage):
        """'Użyj AI przy zapisie' + due date in 30 days → the priority stays 'Średni', no AI badge."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(30), use_ai=True)

        expect(card.locator(".badge-priority-medium")).to_have_text("Średni")
        expect(card.locator(".ai-badge")).to_have_count(0)


# ── US-3.4: Upcoming week view ───────────────────────────────────────────────


class TestUpcomingTasks:

    def test_upcoming_filter_shows_task_within_7_days(self, dashboard: DashboardPage):
        """A task with a due_date in 5 days is visible in the 'Nadchodzące (7 dni)' view."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(5))
        expect(card).to_be_visible()

        dashboard.show_upcoming()

        expect(card).to_be_visible()

    def test_upcoming_filter_excludes_task_beyond_7_days(self, dashboard: DashboardPage):
        """A task with a due_date in 10 days disappears in the 'Nadchodzące (7 dni)' view."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(10))
        expect(card).to_be_visible()

        dashboard.show_upcoming()

        expect(card).to_have_count(0)

    def test_upcoming_filter_excludes_overdue_task(self, dashboard: DashboardPage):
        """An overdue task disappears in the 'Nadchodzące' view."""
        card = dashboard.add_task(unique_title(), due_date=iso_date(-2))
        expect(card).to_be_visible()

        dashboard.show_upcoming()

        expect(card).to_have_count(0)

    def test_upcoming_filter_excludes_task_without_due_date(self, dashboard: DashboardPage):
        """A task without a due_date disappears in the 'Nadchodzące' view."""
        card = dashboard.add_task(unique_title())
        expect(card).to_be_visible()

        dashboard.show_upcoming()

        expect(card).to_have_count(0)

    def test_upcoming_tasks_sorted_by_due_date(self, dashboard: DashboardPage):
        """Tasks in the 'Nadchodzące' view are sorted ascending by due_date."""
        later_title = unique_title("Zadanie E2E za 6 dni")
        sooner_title = unique_title("Zadanie E2E za 2 dni")
        dashboard.add_task(later_title, due_date=iso_date(6))
        dashboard.add_task(sooner_title, due_date=iso_date(2))

        dashboard.show_upcoming()

        expect(dashboard.cards).to_have_count(2)
        assert dashboard.card_titles() == [sooner_title, later_title]
