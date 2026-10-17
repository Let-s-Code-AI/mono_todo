"""Shared fixtures for the E2E tests (Playwright + pytest).

Requires a running frontend (BASE_URL) and backend (AUTH_URL).
The test user is registered once per session (with pytest-xdist: once per worker),
and their tasks are cleared through the API before and after every test, so tests
do not have to clean up after themselves through the UI.
"""

from __future__ import annotations

import os
import uuid
from typing import Callable, Iterator

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Page, Playwright, expect

DEFAULT_BASE_URL = "http://localhost:5173"
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8000").rstrip("/")
TEST_PASSWORD = "testpass123"


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    """Frontend URL: the --base-url flag, then the BASE_URL variable, then localhost:5173."""
    url = request.config.getoption("base_url", default=None) or os.getenv("BASE_URL", DEFAULT_BASE_URL)
    return url.rstrip("/")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Fixed viewport size and Polish locale (dates on task cards are formatted with pl-PL)."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 900},
        "locale": "pl-PL",
    }


# ── Backend API ───────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Iterator[APIRequestContext]:
    """Anonymous HTTP client for the backend (registration, login)."""
    ctx = playwright.request.new_context(base_url=AUTH_URL)
    yield ctx
    ctx.dispose()


@pytest.fixture(scope="session")
def test_user(api: APIRequestContext) -> tuple[str, str]:
    """Registers the session user and returns (email, password)."""
    email = f"e2e_{uuid.uuid4().hex[:8]}@example.com"
    resp = api.post("/auth/register", data={"email": email, "password": TEST_PASSWORD})
    assert resp.status == 201, f"Rejestracja użytkownika sesji nie powiodła się: {resp.text()}"
    return email, TEST_PASSWORD


@pytest.fixture(scope="session")
def auth_token(api: APIRequestContext, test_user: tuple[str, str]) -> str:
    """JWT token of the session user."""
    email, password = test_user
    resp = api.post("/auth/login", form={"username": email, "password": password})
    assert resp.ok, f"Logowanie użytkownika sesji nie powiodło się: {resp.text()}"
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def user_api(playwright: Playwright, auth_token: str) -> Iterator[APIRequestContext]:
    """HTTP client authenticated as the session user (data seeding and cleanup)."""
    ctx = playwright.request.new_context(
        base_url=AUTH_URL,
        extra_http_headers={"Authorization": f"Bearer {auth_token}"},
    )
    yield ctx
    ctx.dispose()


def _delete_all_tasks(user_api: APIRequestContext) -> None:
    resp = user_api.get("/tasks/")
    assert resp.ok, f"Nie udało się pobrać zadań do wyczyszczenia: {resp.text()}"
    for task in resp.json():
        user_api.delete(f"/tasks/{task['id']}")


@pytest.fixture(autouse=True)
def clean_tasks(user_api: APIRequestContext) -> Iterator[None]:
    """Every test starts and ends with an empty task list for the session user."""
    _delete_all_tasks(user_api)
    yield
    _delete_all_tasks(user_api)


# ── Browser ───────────────────────────────────────────────────────────────────


@pytest.fixture
def logged_in_page(
    new_context: Callable[..., BrowserContext],
    base_url: str,
    test_user: tuple[str, str],
    auth_token: str,
) -> Page:
    """Page with the session user logged in.

    The token is injected into localStorage via the context's storage_state, so we do not
    go through the login form in every test.
    """
    email, _ = test_user
    context = new_context(
        storage_state={
            "cookies": [],
            "origins": [
                {
                    "origin": base_url,
                    "localStorage": [
                        {"name": "token", "value": auth_token},
                        {"name": "userEmail", "value": email},
                    ],
                }
            ],
        }
    )
    page = context.new_page()
    page.goto("/")
    expect(page.get_by_role("button", name="Wyloguj")).to_be_visible()
    return page
