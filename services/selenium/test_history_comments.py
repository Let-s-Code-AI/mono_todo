"""E2E tests for task history and comments functionality."""

import os
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("BASE_URL", "http://localhost:5173")
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8000")


def test_history_visible_after_edit(driver_logged_in, existing_user):
    """After editing a task, the history tab should show the change."""
    email, password = existing_user
    driver = driver_logged_in

    resp = requests.post(
        f"{AUTH_URL}/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = resp.json().get("access_token", "")

    task_data = {
        "title": "History Test Task",
        "description": "A task to test history",
        "priority": "medium",
        "status": "todo",
    }
    res = requests.post(
        f"{AUTH_URL}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    task_id = res.json()["id"]

    driver.get(f"{BASE_URL}")
    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "task-card"))
    )

    task_cards = driver.find_elements(By.CLASS_NAME, "task-card")
    history_test_card = None
    for card in task_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "task-title").text
            if "History Test Task" in title:
                history_test_card = card
                break
        except:
            pass

    assert history_test_card is not None, "Task not found on page"
    history_test_card.click()

    modal = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal"))
    )

    title_input = modal.find_element(By.XPATH, ".//input[@value='History Test Task']")
    title_input.clear()
    title_input.send_keys("Updated History Test Task")

    save_btn = modal.find_element(By.XPATH, ".//button[contains(text(), 'Zapisz')]")
    save_btn.click()

    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "modal"))
    )

    task_cards = driver.find_elements(By.CLASS_NAME, "task-card")
    for card in task_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "task-title").text
            if "Updated History Test Task" in title:
                history_test_card = card
                break
        except:
            pass

    history_test_card.click()

    modal = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal"))
    )

    history_tab = modal.find_element(By.XPATH, ".//button[contains(text(), 'Historia zmian')]")
    history_tab.click()

    history_entry = WebDriverWait(modal, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "history-entry"))
    )

    history_text = history_entry.text
    assert "title" in history_text.lower()
    assert "History Test Task" in history_text
    assert "Updated History Test Task" in history_text


def test_add_comment_ui(driver_logged_in, existing_user):
    """User can add a comment via the UI and see it in the comments list."""
    email, password = existing_user
    driver = driver_logged_in

    resp = requests.post(
        f"{AUTH_URL}/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = resp.json().get("access_token", "")

    task_data = {
        "title": "Comment Test Task",
        "description": "A task to test comments",
        "priority": "low",
        "status": "todo",
    }
    res = requests.post(
        f"{AUTH_URL}/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    task_id = res.json()["id"]

    driver.get(f"{BASE_URL}")
    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "task-card"))
    )

    task_cards = driver.find_elements(By.CLASS_NAME, "task-card")
    comment_test_card = None
    for card in task_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "task-title").text
            if "Comment Test Task" in title:
                comment_test_card = card
                break
        except:
            pass

    assert comment_test_card is not None, "Task not found on page"
    comment_test_card.click()

    modal = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal"))
    )

    comments_tab = modal.find_element(By.XPATH, ".//button[contains(text(), 'Komentarze')]")
    comments_tab.click()

    comment_textarea = WebDriverWait(modal, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
    )

    comment_textarea.clear()
    comment_textarea.send_keys("This is my first comment about this task!")

    add_comment_btn = modal.find_element(
        By.XPATH, ".//button[contains(text(), 'Dodaj komentarz')]"
    )
    add_comment_btn.click()

    comment_item = WebDriverWait(modal, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "comment-item"))
    )

    comment_text = comment_item.text
    assert "This is my first comment about this task!" in comment_text
