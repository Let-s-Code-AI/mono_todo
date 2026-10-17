"""E2E tests – Authentication (Playwright + pytest)
Coverage:
  - Registration: success (new email), existing email, HTML5 validation
  - Login: valid credentials, wrong password, empty fields
  - Logout
  - Session persistence (page reload, token in localStorage)
"""

import uuid

from playwright.sync_api import Page, expect

from pages import AuthPage, DashboardPage


def unique_email() -> str:
    return f"e2e_{uuid.uuid4().hex[:8]}@example.com"


# ── REGISTRATION ───────────────────────────────────────────────────────────────


class TestRegistration:

    def test_register_new_user_success(self, page: Page):
        """Registration with a unique email → success toast and back to the login tab."""
        auth = AuthPage(page).open()

        auth.register(unique_email(), "haslo123")

        expect(DashboardPage(page).toast("Konto utworzone")).to_be_visible()
        expect(auth.active_tab).to_have_text("Logowanie")

    def test_register_existing_email_shows_error(self, page: Page, test_user: tuple[str, str]):
        """Registration with an already existing email → error message, still on the auth screen."""
        email, password = test_user
        auth = AuthPage(page).open()

        auth.register(email, password)

        expect(auth.error).to_be_visible()
        expect(auth.error).to_contain_text("Email already registered")
        expect(auth.card).to_be_visible()

    def test_register_empty_fields_blocked(self, page: Page):
        """An empty registration form is blocked by HTML5 validation (required)."""
        auth = AuthPage(page).open()
        auth.switch_to_register()

        auth.submit()

        assert not auth.form_is_valid(), "Pusty formularz nie powinien przejść walidacji"
        expect(auth.card).to_be_visible()
        expect(DashboardPage(page).logout_button).to_have_count(0)

    def test_register_invalid_email_format_blocked(self, page: Page):
        """An invalid email format is blocked by HTML5 validation (type=email)."""
        auth = AuthPage(page).open()
        auth.switch_to_register()
        auth.fill_form("nieprawidlowy-email", "haslo123")

        auth.submit()

        assert not auth.form_is_valid(), "Email bez '@' nie powinien przejść walidacji"
        expect(auth.card).to_be_visible()
        expect(DashboardPage(page).logout_button).to_have_count(0)

    def test_register_then_login_with_new_credentials(self, page: Page):
        """After registering a new account the user can log in with it."""
        auth = AuthPage(page).open()
        email, password = unique_email(), "haslo123"

        auth.register(email, password)
        expect(DashboardPage(page).toast("Konto utworzone")).to_be_visible()
        expect(auth.active_tab).to_have_text("Logowanie")

        auth.login(email, password)

        dashboard = DashboardPage(page)
        expect(dashboard.logout_button).to_be_visible()
        expect(dashboard.user_label).to_have_text(email)


# ── LOGIN ─────────────────────────────────────────────────────────────────────


class TestLogin:

    def test_login_valid_credentials(self, page: Page, test_user: tuple[str, str]):
        """Login with valid credentials → dashboard with the user's email in the top bar."""
        email, password = test_user
        AuthPage(page).open().login(email, password)

        dashboard = DashboardPage(page)
        expect(dashboard.logout_button).to_be_visible()
        expect(dashboard.user_label).to_have_text(email)

    def test_login_wrong_password_shows_error(self, page: Page, test_user: tuple[str, str]):
        """Login with a wrong password → error message, no dashboard."""
        email, _ = test_user
        auth = AuthPage(page).open()

        auth.login(email, "bledne_haslo_xyz")

        expect(auth.error).to_be_visible()
        expect(auth.error).to_contain_text("Invalid credentials")
        expect(auth.card).to_be_visible()
        expect(DashboardPage(page).logout_button).to_have_count(0)

    def test_login_empty_fields_blocked(self, page: Page):
        """An empty login form is blocked by HTML5 validation (required)."""
        auth = AuthPage(page).open()

        auth.submit()

        assert not auth.form_is_valid(), "Pusty formularz nie powinien przejść walidacji"
        expect(auth.card).to_be_visible()
        expect(DashboardPage(page).logout_button).to_have_count(0)


# ── LOGOUT ────────────────────────────────────────────────────────────────────


class TestLogout:

    def test_logout_redirects_to_auth(self, logged_in_page: Page):
        """Clicking 'Wyloguj' → back to the login screen."""
        DashboardPage(logged_in_page).logout()

        expect(AuthPage(logged_in_page).card).to_be_visible()

    def test_logout_clears_token(self, logged_in_page: Page):
        """After logout the token and email are removed from localStorage."""
        DashboardPage(logged_in_page).logout()
        expect(AuthPage(logged_in_page).card).to_be_visible()

        assert logged_in_page.evaluate("localStorage.getItem('token')") is None
        assert logged_in_page.evaluate("localStorage.getItem('userEmail')") is None


# ── SESSION PERSISTENCE ───────────────────────────────────────────────────────


class TestSessionPersistence:

    def test_session_persists_after_page_reload(self, page: Page, test_user: tuple[str, str]):
        """After logging in and reloading the page the user is still logged in."""
        email, password = test_user
        AuthPage(page).open().login(email, password)
        dashboard = DashboardPage(page)
        expect(dashboard.logout_button).to_be_visible()

        page.reload()

        expect(dashboard.logout_button).to_be_visible()
        expect(dashboard.user_label).to_have_text(email)

    def test_no_token_shows_auth_page(self, page: Page):
        """A fresh context without a token in localStorage → login screen."""
        page.goto("/")

        expect(AuthPage(page).card).to_be_visible()
        assert page.evaluate("localStorage.getItem('token')") is None

    def test_login_stores_token_in_localstorage(self, page: Page, test_user: tuple[str, str]):
        """After a successful login the JWT token is stored in localStorage."""
        email, password = test_user
        AuthPage(page).open().login(email, password)
        expect(DashboardPage(page).logout_button).to_be_visible()

        token = page.evaluate("localStorage.getItem('token')")

        assert token, "Token powinien być zapisany w localStorage po zalogowaniu"
        assert token.count(".") == 2, f"Token nie wygląda jak JWT: {token[:20]}…"
