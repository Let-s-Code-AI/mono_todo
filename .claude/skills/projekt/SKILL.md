---
name: projekt
description: Standardy kodu, testowania, narzędzi i workflow dla tego monorepo (FastAPI backend + React frontend + Playwright E2E). Użyj gdy pracujesz nad tym projektem i potrzebujesz przypomnienia konwencji, komend lub architektury.
---

# Projekt mono_todo — przewodnik

Monorepo z trzema serwisami:

| Serwis | Ścieżka | Technologia |
|---|---|---|
| Backend | `services/backend` | Python 3.11+ / FastAPI / SQLite / Alembic |
| Frontend | `services/frontend` | JavaScript / React 18 / Vite |
| E2E tests | `services/e2e` | Python / Pytest / Playwright |

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
- Projekty i członkowie chodzą przez WebSocket `/ws/projects?token=…` (`api.connectProjects`, hook `useProjectsSocket` w `App.jsx`); backend: `app/api/routers/projects_ws.py`, protokół w `app/schemas/realtime.py`
- Język interfejsu: **polski**
- Jasny motyw wg designu z Figma Make: tło „papier” `#f2f0e9`, grafitowy sidebar `#14171f`, kobaltowy hero `#3c46e8`, akcent limonkowy `#c8ff3d`, font Manrope
- Ikony jako inline SVG (komponent `Icon` w `App.jsx`) — bez emoji i fontów ikon

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

### E2E — Playwright

```bash
cd services/e2e
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium   # jednorazowo

.venv/bin/pytest                     # wszystkie testy E2E (headless)
.venv/bin/pytest -n auto             # równolegle (pytest-xdist)
.venv/bin/pytest test_tasks.py       # konkretny moduł
.venv/bin/pytest --headed            # z widoczną przeglądarką
BASE_URL=http://localhost:5173 AUTH_URL=http://localhost:8000 .venv/bin/pytest
```

- Wymaga działającego backendu i frontendu (`./start.sh`), backend bez `OPENAI_API_KEY`
- Nowy użytkownik rejestrowany przez API raz na sesję (przy xdist: raz na worker)
- Zadania użytkownika czyszczone przez API przed i po każdym teście (`clean_tasks`, autouse)
- `logged_in_page` — świeży kontekst z tokenem JWT w `storage_state`; `page` — kontekst wylogowany
- Selektory tylko w page objectach (`pages.py`), asercje web-first (`expect(...)`), bez `sleep`
- Przy błędzie zrzut ekranu i trace w `test-results/` (`playwright show-trace <trace.zip>`)

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
| Playwright (sync API) | Automatyzacja przeglądarki (Chromium) |
| pytest-playwright | Fixtures `page`/`new_context`, screenshot i trace przy błędzie |
| pytest-xdist | Równoległe uruchamianie (`-n auto`) |
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
