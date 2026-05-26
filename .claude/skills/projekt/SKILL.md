---
name: projekt
description: Standardy kodu, testowania, narzędzi i workflow dla tego monorepo (FastAPI backend + React frontend + Selenium E2E). Użyj gdy pracujesz nad tym projektem i potrzebujesz przypomnienia konwencji, komend lub architektury.
---

# Projekt mono_todo — przewodnik

Monorepo z trzema serwisami:

| Serwis | Ścieżka | Technologia |
|---|---|---|
| Backend | `services/backend` | Python 3.11+ / FastAPI / SQLite / Alembic |
| Frontend | `services/frontend` | JavaScript / React 18 / Vite |
| E2E tests | `services/selenium` | Python / Pytest / Selenium |

---

## 1. Code generation

### Backend (Python / FastAPI)

- `async def` dla wszystkich endpointów
- Architektura warstwowa — każda warstwa korzysta tylko z warstwy poniżej:
  ```
  API (routers) → Service → Repository → Models/Schemas
  ```
- DI chain: `get_session → get_task_repository → get_ai_service → get_task_service`
- Early returns i guard clauses — happy path na końcu
- Nazwy zmiennych z czasownikami pomocniczymi: `is_active`, `has_permission`
- Brak nieużywanych importów i martwego kodu
- AI calls wyłącznie w service layer — nigdy nie blokują podstawowej funkcjonalności
- Linia maks. 100 znaków (`ruff`, `black`)
- Docstringi w stylu Google dla endpointów

### Frontend (React / Vite)

- React 18, JSX, CSS variables — brak frameworka CSS
- Cały UI w jednym pliku `App.jsx` (single-file architecture)
- API calls tylko przez `api.js` — token `Bearer` w nagłówku, przechowywany w `localStorage`
- Język interfejsu: **polski**
- Ciemny motyw, kolor akcentu `#6366f1`

---

## 2. Testing

### Backend — pytest

```bash
cd services/backend && source .venv/bin/activate

pytest                                                    # wszystkie testy
pytest --cov=app --cov-report=html                        # z pokryciem
pytest tests/test_tasks_api.py::test_create_task          # pojedynczy test
```

Konwencje:
- Framework: **pytest** + **pytest-asyncio** (`asyncio_mode = auto`)
- Mockowanie: **pytest-mock** (`mocker` fixture) — nigdy `unittest.mock.patch` bezpośrednio
- Baza danych w testach: plik SQLite (nie in-memory) — bezpieczeństwo wątkowe z `TestClient`
- AI service zastępowany przez `MockAIPriorityService` via dependency override w `conftest.py`
- Każdy test dostaje świeżą bazę (fixture function-scoped)
- Globalne cache (`_PRIORITY_CACHE`) czyszczone przez `autouse` fixture

### E2E — Selenium

```bash
cd services/selenium
pytest                               # wszystkie testy E2E
pytest test_tasks.py                 # konkretny moduł
BASE_URL=http://localhost:5173 pytest
```

- Wymaga działającego backendu i frontendu (`./start.sh`)
- Nowy użytkownik tworzony raz na sesję (fixture `session`-scoped w `conftest.py`)
- Driver `function`-scoped — świeża przeglądarka dla każdego testu

---

## 3. Narzędzia projektu

### Backend

| Narzędzie | Rola |
|---|---|
| FastAPI | Framework HTTP |
| SQLModel | ORM (Pydantic + SQLAlchemy) |
| Alembic | Migracje bazy danych |
| Pydantic v2 + pydantic-settings | Walidacja i konfiguracja |
| uvicorn | ASGI server |
| OpenAI SDK | AI prioritization (opcjonalne, wymaga `OPENAI_API_KEY`) |
| ruff | Linter |
| black | Formatter |
| pytest / pytest-asyncio / httpx | Testy |

### Frontend

| Narzędzie | Rola |
|---|---|
| React 18 | UI framework |
| Vite | Bundler / dev server |
| Vanilla CSS | Stylowanie (bez frameworka) |

### E2E

| Narzędzie | Rola |
|---|---|
| Selenium | Automatyzacja przeglądarki |
| webdriver-manager | Automatyczne pobieranie ChromeDriver |
| pytest | Test runner |

---

## 4. Workflow

### Instalacja (pierwsze uruchomienie)

```bash
./install.sh   # tworzy .venv, instaluje zależności, generuje .env, uruchamia migracje
```

### Uruchamianie aplikacji

```bash
./start.sh     # backend (8000) + frontend (5173) jednocześnie
```

Ręcznie:

```bash
# Backend
cd services/backend && source .venv/bin/activate && uvicorn app.main:app --reload

# Frontend
cd services/frontend && npm run dev
```

Adresy:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### Linting i formatowanie (backend)

```bash
cd services/backend
ruff check app tests
black app tests
```

### Migracje bazy danych

```bash
cd services/backend && source .venv/bin/activate
alembic upgrade head
alembic revision --autogenerate -m "opis"
alembic downgrade -1
```

### Build frontendu

```bash
cd services/frontend
npm run build     # dist/
npm run preview   # podgląd produkcyjnego builda
```


### Zmienne środowiskowe (backend)

Plik `services/backend/.env` (generowany przez `install.sh`):

```
JWT_SECRET_KEY=<losowy klucz>
DATABASE_URL=sqlite:///./todo.db
# OPENAI_API_KEY=sk-...   # opcjonalne — włącza AI prioritization
```
