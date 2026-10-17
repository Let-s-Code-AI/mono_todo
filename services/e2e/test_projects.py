"""E2E tests – Projects and members (Playwright + pytest)
Coverage:
  - Create project: modal (+ Nowy projekt) → name → appears as a chip in the 'Projekty' panel
  - Members: add an existing user by email, error for unknown email, remove a member
  - Tasks in a project: select project in the task modal → project chip filters the list
  - Realtime: a second user sees the project appear and disappear without reloading (WebSocket push)
"""

import uuid

import pytest
from typing import Callable

from playwright.sync_api import APIRequestContext, BrowserContext, Page, expect

from pages import DashboardPage, ProjectsPanel, TaskModal

TEST_PASSWORD = "testpass123"


def unique_name(prefix: str = "Projekt E2E") -> str:
    return f"{prefix} {uuid.uuid4().hex[:6]}"


@pytest.fixture
def dashboard(logged_in_page: Page) -> DashboardPage:
    return DashboardPage(logged_in_page)


@pytest.fixture
def projects(logged_in_page: Page) -> ProjectsPanel:
    return ProjectsPanel(logged_in_page)


@pytest.fixture
def other_user_email(api: APIRequestContext) -> str:
    """A second registered user that can be added to a project."""
    email = f"e2e_member_{uuid.uuid4().hex[:8]}@example.com"
    resp = api.post("/auth/register", data={"email": email, "password": TEST_PASSWORD})
    assert resp.status == 201, f"Rejestracja drugiego użytkownika nie powiodła się: {resp.text()}"
    return email


@pytest.fixture
def other_user_page(
    new_context: Callable[..., BrowserContext],
    base_url: str,
    api: APIRequestContext,
    other_user_email: str,
) -> Page:
    """Dashboard opened in a separate browser context, logged in as the second user."""
    resp = api.post("/auth/login", form={"username": other_user_email, "password": TEST_PASSWORD})
    assert resp.ok, f"Logowanie drugiego użytkownika nie powiodło się: {resp.text()}"
    context = new_context(
        storage_state={
            "cookies": [],
            "origins": [
                {
                    "origin": base_url,
                    "localStorage": [
                        {"name": "token", "value": resp.json()["access_token"]},
                        {"name": "userEmail", "value": other_user_email},
                    ],
                }
            ],
        }
    )
    page = context.new_page()
    page.goto("/")
    expect(page.get_by_role("button", name="Wyloguj")).to_be_visible()
    return page


# ── CREATE PROJECT ────────────────────────────────────────────────────────────


class TestCreateProject:

    def test_create_project_appears_as_chip(self, dashboard: DashboardPage, projects: ProjectsPanel):
        """'+ Nowy projekt' → name → 'Utwórz' → the chip is visible and a toast confirms."""
        name = unique_name()

        chip = projects.add_project(name)

        expect(chip).to_be_visible()
        expect(dashboard.toast("Projekt utworzony")).to_be_visible()

    def test_create_project_empty_name_blocked(self, projects: ProjectsPanel):
        """The 'Utwórz' button stays disabled until a name is typed."""
        modal = projects.open_new_project_modal()

        expect(modal.submit_button).to_be_disabled()
        modal.name_input.fill("x")
        expect(modal.submit_button).to_be_enabled()

        modal.cancel_button.click()
        expect(modal.overlay).to_be_hidden()


# ── MEMBERS ───────────────────────────────────────────────────────────────────


class TestMembers:

    def test_owner_is_listed_and_member_added_by_email(
        self, dashboard: DashboardPage, projects: ProjectsPanel, test_user: tuple[str, str], other_user_email: str
    ):
        """The members modal lists the owner; adding an email adds a 'Członek' row."""
        owner_email, _ = test_user
        name = unique_name()
        projects.add_project(name)

        modal = projects.open_members(name)
        expect(modal.member_row(owner_email)).to_contain_text("Właściciel")

        modal.add_member(other_user_email)

        expect(modal.member_row(other_user_email)).to_contain_text("Członek")
        expect(dashboard.toast("Dodano członka")).to_be_visible()

    def test_add_unknown_email_shows_error(self, projects: ProjectsPanel):
        """Adding an email that is not registered shows an error inside the modal."""
        name = unique_name()
        projects.add_project(name)
        modal = projects.open_members(name)

        modal.add_member("nobody_e2e@example.com")

        expect(modal.error).to_be_visible()
        expect(modal.rows).to_have_count(1)

    def test_remove_member(self, projects: ProjectsPanel, other_user_email: str):
        """Removing a member makes their row disappear."""
        name = unique_name()
        projects.add_project(name)
        modal = projects.open_members(name)
        modal.add_member(other_user_email)
        expect(modal.member_row(other_user_email)).to_be_visible()

        modal.remove_member(other_user_email)

        expect(modal.member_row(other_user_email)).to_have_count(0)


# ── TASKS IN A PROJECT ────────────────────────────────────────────────────────


class TestProjectTasks:

    def test_task_assigned_to_project_is_filtered_by_chip(
        self, dashboard: DashboardPage, projects: ProjectsPanel
    ):
        """A task created with a project selected shows up only when that project chip is active."""
        name = unique_name()
        projects.add_project(name)
        in_project, outside = unique_name("Zadanie w projekcie"), unique_name("Zadanie poza")
        dashboard.add_task(outside)

        modal = dashboard.open_new_task_modal()
        modal.title_input.fill(in_project)
        modal.root.locator(".form-group", has_text="Projekt").locator("select").select_option(label=name)
        modal.submit()

        expect(dashboard.task_card(in_project)).to_be_visible()
        expect(dashboard.task_card(in_project).locator(".badge-project")).to_have_text(name)

        projects.select(name)
        expect(dashboard.task_card(in_project)).to_be_visible()
        expect(dashboard.task_card(outside)).to_have_count(0)


# ── REALTIME (WebSocket) ──────────────────────────────────────────────────────


class TestRealtime:

    def test_projects_panel_reports_live_connection(self, projects: ProjectsPanel):
        """The 'Projekty' panel shows the socket as online once the dashboard is up."""
        expect(projects.live_status).to_have_attribute("data-status", "online")

    def test_added_member_sees_project_without_reload(
        self, projects: ProjectsPanel, other_user_email: str, other_user_page: Page
    ):
        """Adding a member pushes the project to their open dashboard; removing them takes it away."""
        other_projects = ProjectsPanel(other_user_page)
        expect(other_projects.live_status).to_have_attribute("data-status", "online")
        name = unique_name()
        projects.add_project(name)
        expect(other_projects.chip(name)).to_have_count(0)

        modal = projects.open_members(name)
        modal.add_member(other_user_email)

        expect(other_projects.chip(name)).to_be_visible()

        modal.remove_member(other_user_email)

        expect(other_projects.chip(name)).to_have_count(0)
