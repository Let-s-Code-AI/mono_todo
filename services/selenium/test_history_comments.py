"""
Testy E2E – Historia zmian i komentarze (Epic 4)
Pokrycie:
  - US-4.1: Wyświetlanie historii zmian zadania
  - US-4.2: Auto-logowanie zmian podczas edycji
  - US-4.3: Dodawanie komentarzy
  - US-4.4: Wyświetlanie listy komentarzy
"""

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
TASK_TITLE = "Historia i komentarze test"
WAIT_DEFAULT = float(os.getenv("SELENIUM_WAIT_DEFAULT", "6"))
WAIT_PRESENCE = float(os.getenv("SELENIUM_WAIT_PRESENCE", "4"))
WAIT_CLEANUP = float(os.getenv("SELENIUM_WAIT_CLEANUP", "3"))


# ── cleanup fixture ───────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def cleanup_test_tasks(driver_logged_in):
    """Po każdym teście usuwa zadania testowe."""
    yield
    driver = driver_logged_in
    try:
        driver.execute_script("window.confirm = function() { return true; }")
        while True:
            cards = driver.find_elements(
                By.XPATH,
                f"//*[contains(@class,'task-card') and .//*[contains(text(),'{TASK_TITLE}')]]"
            )
            if not cards:
                break
            try:
                del_btn = cards[0].find_element(By.CSS_SELECTOR, ".icon-btn.danger")
                del_btn.click()
                WebDriverWait(driver, WAIT_CLEANUP).until(EC.staleness_of(cards[0]))
            except Exception:
                break
    except Exception:
        pass


# ── helpers ───────────────────────────────────────────────────────────────────

def wait(driver, timeout=WAIT_DEFAULT):
    return WebDriverWait(driver, timeout)


def create_task(driver, title):
    """Tworzy nowe zadanie o podanym tytule."""
    btn = wait(driver).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Nowe zadanie')]"))
    )
    btn.click()
    modal = wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))
    title_input = modal.find_element(By.CSS_SELECTOR, "input[placeholder='Co chcesz zrobić?']")
    title_input.clear()
    title_input.send_keys(title)
    save_btn = modal.find_element(By.XPATH, ".//button[contains(text(),'Dodaj zadanie')]")
    save_btn.click()
    wait(driver).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))


def open_task_edit(driver, title):
    """Otwiera modal edycji zadania o podanym tytule."""
    task_card = wait(driver, WAIT_PRESENCE).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(@class,'task-card') and .//*[contains(text(),'{title}')]]")
        )
    )
    task_card.click()
    return wait(driver).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))


def switch_tab(driver, tab_name):
    """Przełącza na wskazaną zakładkę w modalu (Edycja, Historia, Komentarze)."""
    tab_btn = wait(driver).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class,'modal-tab') and contains(text(),'{tab_name}')]"))
    )
    tab_btn.click()


def get_history_entries(driver, timeout=WAIT_PRESENCE):
    """Zwraca listę wpisów historii z widocznego panelu."""
    wait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".history-entry"))
    )
    return driver.find_elements(By.CSS_SELECTOR, ".history-entry")


def get_comments(driver, timeout=WAIT_PRESENCE):
    """Zwraca listę komentarzy z widocznego panelu."""
    wait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".comment-item"))
    )
    return driver.find_elements(By.CSS_SELECTOR, ".comment-item")


# ── Testy: Historia zmian (US-4.1, US-4.2) ────────────────────────────────────

class TestTaskHistory:
    """Testy wyświetlania i logowania historii zmian."""

    def test_historia_pusta_dla_nowego_zadania(self, driver_logged_in):
        """Scenario: Nowe zadanie nie ma żadnych zmian w historii."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na zakładkę Historia
        switch_tab(driver, "Historia")

        # Sprawdzamy że historia jest pusta
        empty_hint = wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".empty-hint"))
        )
        assert "Brak zmian" in empty_hint.text

    def test_historia_rejestruje_zmiane_pola(self, driver_logged_in):
        """Scenario: Zmiana tytułu zadania pojawia się w historii."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Zmieniamy tytuł
        title_input = modal.find_element(By.CSS_SELECTOR, "input[placeholder='Co chcesz zrobić?']")
        title_input.clear()
        title_input.send_keys(TASK_TITLE + " (zmienione)")

        # Zapisujemy
        save_btn = modal.find_element(By.XPATH, ".//button[contains(text(),'Zapisz')]")
        save_btn.click()
        wait(driver).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Ponownie otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE + " (zmienione)")

        # Przełączamy na Historia
        switch_tab(driver, "Historia")

        # Sprawdzamy że zmiana jest zalogowana
        entries = get_history_entries(driver)
        assert len(entries) > 0, "Brak wpisów historii"

        # Szukamy wpisu ze zmianą tytułu
        first_entry = entries[0].text
        assert "Tytuł" in first_entry, "Wpis historii nie zawiera nazwy pola 'Tytuł'"
        assert "zmienione" in first_entry, "Wpis historii nie zawiera nowej wartości"

    def test_historia_rejestruje_zmiane_priorytetu(self, driver_logged_in):
        """Scenario: Zmiana priorytetu pojawia się w historii."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Zmieniamy priorytet
        priority_select = modal.find_element(By.CSS_SELECTOR, "select[value='medium']")
        priority_select.send_keys("high")

        # Zapisujemy
        save_btn = modal.find_element(By.XPATH, ".//button[contains(text(),'Zapisz')]")
        save_btn.click()
        wait(driver).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Ponownie otwieramy
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Historia
        switch_tab(driver, "Historia")

        # Sprawdzamy wpis
        entries = get_history_entries(driver)
        assert len(entries) > 0
        first_entry = entries[0].text
        assert "Priorytet" in first_entry, "Wpis historii nie zawiera zmian priorytetu"

    def test_historia_posortowana_od_najnowszej(self, driver_logged_in):
        """Scenario: Historia wyświetlana od najnowszej zmiany."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Pierwsza zmiana - tytuł
        modal = open_task_edit(driver, TASK_TITLE)
        title_input = modal.find_element(By.CSS_SELECTOR, "input[placeholder='Co chcesz zrobić?']")
        title_input.clear()
        title_input.send_keys(TASK_TITLE + " v2")
        save_btn = modal.find_element(By.XPATH, ".//button[contains(text(),'Zapisz')]")
        save_btn.click()
        wait(driver).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Druga zmiana - priorytet
        modal = open_task_edit(driver, TASK_TITLE + " v2")
        priority_select = modal.find_element(By.CSS_SELECTOR, "select[value='medium']")
        priority_select.send_keys("high")
        save_btn = modal.find_element(By.XPATH, ".//button[contains(text(),'Zapisz')]")
        save_btn.click()
        wait(driver).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Sprawdzamy kolejność
        modal = open_task_edit(driver, TASK_TITLE + " v2")
        switch_tab(driver, "Historia")
        entries = get_history_entries(driver)

        assert len(entries) >= 2, "Powinno być co najmniej 2 wpisy"
        # Pierwszy wpis (najnowszy) powinien być zmiana priorytetu
        assert "Priorytet" in entries[0].text, "Najnowszy wpis powinien być zmiana priorytetu"


# ── Testy: Komentarze (US-4.3, US-4.4) ────────────────────────────────────────

class TestTaskComments:
    """Testy dodawania i wyświetlania komentarzy."""

    def test_komentarze_puste_dla_nowego_zadania(self, driver_logged_in):
        """Scenario: Nowe zadanie nie ma żadnych komentarzy."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Komentarze
        switch_tab(driver, "Komentarze")

        # Sprawdzamy że lista jest pusta
        empty_hint = wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".empty-hint"))
        )
        assert "Brak komentarzy" in empty_hint.text

    def test_dodanie_komentarza(self, driver_logged_in):
        """Scenario: Dodanie komentarza pojawia się na liście."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Komentarze
        switch_tab(driver, "Komentarze")

        # Dodajemy komentarz
        textarea = wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment-form textarea"))
        )
        textarea.send_keys("Test komentarz")

        submit_btn = driver.find_element(By.CSS_SELECTOR, ".comment-form .btn")
        submit_btn.click()

        # Czekamy na pojawienie się komentarza
        comments = get_comments(driver, WAIT_PRESENCE)
        assert len(comments) > 0, "Komentarz nie pojawił się na liście"
        assert "Test komentarz" in comments[0].text

    def test_wiele_komentarzy_posortowanych_chronologicznie(self, driver_logged_in):
        """Scenario: Wiele komentarzy pojawia się w kolejności dodania."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Komentarze
        switch_tab(driver, "Komentarze")

        # Dodajemy pierwszy komentarz
        textarea = wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment-form textarea"))
        )
        textarea.send_keys("Pierwszy komentarz")
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".comment-form .btn")
        submit_btn.click()

        # Czekamy na pojawienie się
        wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'comment-item') and contains(text(),'Pierwszy')]"))
        )

        # Dodajemy drugi komentarz
        textarea = driver.find_element(By.CSS_SELECTOR, ".comment-form textarea")
        textarea.send_keys("Drugi komentarz")
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".comment-form .btn")
        submit_btn.click()

        # Czekamy
        wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'comment-item') and contains(text(),'Drugi')]"))
        )

        # Sprawdzamy kolejność
        comments = get_comments(driver)
        assert len(comments) >= 2, "Powinno być co najmniej 2 komentarze"
        assert "Pierwszy komentarz" in comments[0].text
        assert "Drugi komentarz" in comments[1].text

    def test_walidacja_pustego_komentarza(self, driver_logged_in):
        """Scenario: Przycisk wysłania wyłączony gdy komentarz jest pusty."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Komentarze
        switch_tab(driver, "Komentarze")

        # Sprawdzamy że przycisk jest wyłączony
        submit_btn = wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment-form .btn"))
        )
        assert submit_btn.get_attribute("disabled"), "Przycisk powinien być wyłączony dla pustego komentarza"

        # Wpisujemy coś
        textarea = driver.find_element(By.CSS_SELECTOR, ".comment-form textarea")
        textarea.send_keys("Komentarz")

        # Przycisk powinien być aktywny
        assert not submit_btn.get_attribute("disabled"), "Przycisk powinien być aktywny dla wypełnionego komentarza"


# ── Testy: Niezależność historii i komentarzy ─────────────────────────────────

class TestHistoryCommentsIndependence:
    """Testy że historia i komentarze są niezależne."""

    def test_komentarz_nie_tworzy_historii(self, driver_logged_in):
        """Scenario: Dodanie komentarza nie pojawia się w historii."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Komentarze
        switch_tab(driver, "Komentarze")

        # Dodajemy komentarz
        textarea = wait(driver, WAIT_PRESENCE).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment-form textarea"))
        )
        textarea.send_keys("Test komentarz")
        submit_btn = driver.find_element(By.CSS_SELECTOR, ".comment-form .btn")
        submit_btn.click()

        # Przełączamy na Historia
        switch_tab(driver, "Historia")

        # Sprawdzamy że historia jest pusta
        try:
            empty_hint = wait(driver, WAIT_PRESENCE).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".empty-hint"))
            )
            assert "Brak zmian" in empty_hint.text
        except Exception:
            # Jeśli nie ma empty_hint, sprawdzamy że nie ma wpisów
            entries = driver.find_elements(By.CSS_SELECTOR, ".history-entry")
            assert len(entries) == 0, "Historia powinna być pusta"

    def test_zmiana_pola_nie_tworzy_komentarza(self, driver_logged_in):
        """Scenario: Zmiana pola zadania nie pojawia się w komentarzach."""
        driver = driver_logged_in
        driver.get(BASE_URL)
        create_task(driver, TASK_TITLE)

        # Otwieramy zadanie
        modal = open_task_edit(driver, TASK_TITLE)

        # Zmieniamy priorytet
        priority_select = modal.find_element(By.CSS_SELECTOR, "select[value='medium']")
        priority_select.send_keys("high")

        # Zapisujemy
        save_btn = modal.find_element(By.XPATH, ".//button[contains(text(),'Zapisz')]")
        save_btn.click()
        wait(driver).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-overlay")))

        # Ponownie otwieramy
        modal = open_task_edit(driver, TASK_TITLE)

        # Przełączamy na Komentarze
        switch_tab(driver, "Komentarze")

        # Sprawdzamy że komentarze są puste
        try:
            empty_hint = wait(driver, WAIT_PRESENCE).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".empty-hint"))
            )
            assert "Brak komentarzy" in empty_hint.text
        except Exception:
            # Jeśli nie ma empty_hint, sprawdzamy że nie ma komentarzy
            comments = driver.find_elements(By.CSS_SELECTOR, ".comment-item")
            assert len(comments) == 0, "Komentarze powinny być puste"
