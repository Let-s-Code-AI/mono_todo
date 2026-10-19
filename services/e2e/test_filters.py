"""E2E regression test: switching views must not leak state between them.

Reported bug (Polish):
  1. Otwórz widok "Wszystkie" i sprawdź liczbę zadań.
  2. Przejdź do innego widoku.
  3. Kliknij filtr "Pilne".
  4. Wróć do widoku "Wszystkie".
  5. Licznik / stan widoku "Wszystkie" zostaje nieoczekiwanie wyzerowany lub
     zmieniony, mimo że nie powinien się zmienić.

Root cause (see services/frontend/src/App.jsx): the sidebar "Pilne" nav item
sets filters.priority = 'high'. The content-area "Wszystkie" filter tab only
calls setView('all') and never clears filters.priority/status, unlike the
sidebar's own "Wszystkie" nav item (selectNav('all')). Since `view` is already
'all' once "Pilne" is selected, clicking that tab triggers no refetch at all,
so the task list — and every counter derived from it (count-pill, hero stats,
board section headers) — stays stuck on the 'Pilne' subset.
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


class TestViewSwitchingRegression:

    def test_returning_to_all_view_after_pilne_does_not_zero_out_the_list(self, dashboard: DashboardPage):
        """Wszystkie -> inny widok -> Pilne -> powrót do Wszystkie: zadanie o
        priorytecie domyślnym ('Średni') musi pozostać widoczne, a licznik
        'Wszystkie' w sidebarze musi dalej pokazywać 1, a nie zero."""
        title = unique_title()
        card = dashboard.add_task(title)  # domyślny priorytet: 'Średni' (medium)

        expect(card).to_be_visible()
        expect(dashboard.count_pill("Wszystkie")).to_have_text("1")

        dashboard.show_overdue()  # "przejdź do innego widoku"
        dashboard.show_priority_high()  # "kliknij filtr Pilne"
        expect(card).to_have_count(0)  # zadanie 'Średni' nie jest 'Pilne' — to poprawne

        dashboard.all_chip.click()  # "wróć do widoku Wszystkie"

        expect(card).to_be_visible()
        expect(dashboard.count_pill("Wszystkie")).to_have_text("1")


class TestSidebarCountersStayGlobal:
    """Regresja: liczniki w sidebarze (np. 'Wszystkie') muszą zawsze pokazywać
    sumę wszystkich zadań — a nie tylko podzbiór aktualnie załadowany dla
    aktywnego filtra (np. 'Pilne'). Zob. zrzuty ekranu w zgłoszeniu: po
    kliknięciu 'Pilne' licznik 'Wszystkie' spadał do 0, mimo że zadania nadal
    istniały."""

    def test_all_counter_stays_global_while_viewing_urgent(self, dashboard: DashboardPage):
        """2 zadania (1 'Wysoki', 1 domyślny 'Średni'). Po przejściu na widok
        'Pilne' licznik 'Wszystkie' nadal pokazuje 2, a licznik 'Pilne' — 1."""
        urgent_title = unique_title("Zadanie pilne")
        normal_title = unique_title("Zadanie zwykle")
        dashboard.add_task(urgent_title, priority="high")
        dashboard.add_task(normal_title)

        expect(dashboard.count_pill("Wszystkie")).to_have_text("2")

        dashboard.show_priority_high()

        expect(dashboard.task_card(urgent_title)).to_be_visible()
        expect(dashboard.task_card(normal_title)).to_have_count(0)
        expect(dashboard.count_pill("Pilne")).to_have_text("1")
        expect(dashboard.count_pill("Wszystkie")).to_have_text("2")
