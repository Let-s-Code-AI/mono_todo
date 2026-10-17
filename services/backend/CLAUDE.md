# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. Prefer minimal, incremental changes over rewrites.

MVP TODO application. Scope rule: keep solutions simple but production-ready; favor clarity over cleverness.

## Stack

Python 3.10+, FastAPI, SQLModel (SQLAlchemy 2.0) on SQLite with synchronous sessions, Alembic, Pydantic v2 + pydantic-settings, OpenAI SDK, pytest + pytest-asyncio + pytest-mock, ruff + black (line length 100, configured in `pyproject.toml`).

## Commands

```bash
# Install dependencies
pip install -e ".[dev]"

# Run dev server
uvicorn app.main:app --reload

# Run tests
pytest
pytest --cov=app --cov-report=html   # with coverage
pytest tests/test_tasks_api.py::test_create_task  # single test

# Lint and format
ruff check app tests
black app tests

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "Description"
alembic downgrade -1
```

## Development Workflow: TDD

Every change to `app/` follows the `tdd` skill (`services/backend/.claude/skills/tdd/SKILL.md`): **red → green → refactor**.

- Before coding, write a checklist of observable behaviors; each item becomes one test.
- Write one failing test, run it, confirm it fails for the right reason. No production code before that.
- Write the minimum that makes it pass, then run the whole suite.
- Refactor only on green, then `pytest -q && ruff check app tests && black app tests`.
- Start outside-in: an API test through `TestClient` first; service unit tests only for non-trivial logic.
- Bugfix = reproduce with a failing test first, then fix; the test stays as a regression guard.
- Never leave the suite red between cycles or in a commit.

## Architecture

Clean layered architecture — no layer should skip the one below it:

```
API Layer       app/api/routers/tasks.py       HTTP request/response handling
Service Layer   app/services/task_service.py   Business logic, orchestration
Repository      app/db/repository.py           All database queries
Models          app/db/models.py               SQLModel ORM definitions
Schemas         app/schemas/task.py            Pydantic models for API I/O
Config          app/core/config.py             Settings via Pydantic BaseSettings
```

Realtime (projects over WebSocket):

```
WS endpoint     app/api/routers/projects_ws.py  /ws/projects — auth by ?token=, snapshot, commands, push events
Connections     app/api/realtime.py             ConnectionManager on app.state (set in lifespan), fan-out per user
Messages        app/schemas/realtime.py         Commands (client→server) and events/replies (server→client)
```

The WebSocket handler is `async def`; every service call runs through `run_in_threadpool`, and the
connection's session is `close()`d after each command so a long-lived socket never serves stale rows.
REST project endpoints stay as they are and do **not** broadcast; the frontend uses the socket only.

FastAPI's dependency injection chain: `get_session → get_task_repository → get_ai_service → get_task_service` — route handlers receive fully composed services.

Layer rules:
- Routers never import repositories directly; they talk to services only.
- Services receive the repository and AI service via DI; they never create a `Session` or instantiate a repository themselves.
- Repositories contain queries only — no business logic.
- Shared state goes through `Depends`, never module-level singletons (the AI `_PRIORITY_CACHE` is the one deliberate exception).

## AI Prioritization

`app/services/ai_priority_service.py` defines a `AIPriorityService` Protocol with two implementations:

- `OpenAIPriorityService` — calls GPT-3.5-turbo through `AsyncOpenAI` (awaited, never blocks the event loop); uses in-memory caching
- `MockAIPriorityService` — heuristic fallback using keyword matching (Polish + English)

The mock is always used in tests (via dependency override in `conftest.py`). The real service activates only when `OPENAI_API_KEY` is set. AI can override user-set priority for detected critical cases (urgent/exam keywords).

AI rules:
- All OpenAI calls stay inside `ai_priority_service.py`. Routers and `TaskService` only see the `AIPriorityService` Protocol.
- AI failure must never break a request: `suggest_priority` falls back to `(Priority.MEDIUM, None)` and the task is still saved.
- New implementations satisfy the Protocol structurally; do not inherit from it.
- Caching is in-memory only (`_PRIORITY_CACHE`); no external stores in MVP scope.

## Testing

Tests use dependency overrides to replace the AI service with `MockAIPriorityService` and use a file-based SQLite test database (not in-memory) for thread safety with FastAPI `TestClient`. Fixtures are function-scoped, so each test gets a fresh DB.

Use **pytest-mock** (`mocker` fixture) for all mocking — never `unittest.mock.patch` directly. Key conventions:
- `mocker.patch(...)` — auto-reverts after each test, no `with` block needed
- `mocker.MagicMock()` — for constructing fake objects
- Module-level globals (e.g. `_PRIORITY_CACHE`) must be cleared in an `autouse` fixture when testing modules that use them

Coverage expectations:
- Every piece of business logic in `app/services/` has unit tests.
- Every endpoint is exercised through `TestClient`.
- `asyncio_mode = "auto"` is set, so `async def` tests need no `@pytest.mark.asyncio` marker (existing markers are harmless).

## Code Style

- Run `ruff check app tests` and `black app tests` before finishing; never hand-format.
- Type hints on every function signature. Pydantic models for all request and response bodies, not raw dicts.
- `async def` only for endpoints that `await` something (the AI service). Plain `def` for endpoints that only use the synchronous SQLModel session, so FastAPI runs them in the threadpool. Never call blocking I/O inside `async def`.
- Plain functions for endpoints and dependencies; classes for services and repositories (existing pattern).
- Lowercase snake_case for files and directories. Descriptive names with auxiliary verbs (`is_admin`, `has_permission`, `use_ai_priority`).
- Google-style docstrings (Args / Returns / Raises) on all endpoints.
- Small, well-named functions; extract shared logic instead of duplicating it.
- No unused imports, dead code, or commented-out code.
- Startup/shutdown via the `lifespan` context manager in `app/main.py`, not `@app.on_event`.

## Error Handling

- Guard clauses first, happy path last. Early return instead of nested `if`/`else`.
- Routers raise `HTTPException` with an explicit status code for expected errors (404, 409, 401...) and list them under `Raises:` in the docstring.
- Services and repositories return results or `None`; they do not raise `HTTPException`. The router translates the outcome.
- No silent failures: never swallow an exception without a defined fallback. The only sanctioned broad `except` is the AI fallback in `ai_priority_service.py`.

## API Conventions

- `use_ai_priority` query param on `POST /tasks/` controls whether AI prioritizes the task.
- Endpoints returning user data pass `owner_id=current_user.id`; ownership scoping happens in the router.
- `create_db_and_tables()` is for dev/test only. Production schema changes go through Alembic.
- `/ws/projects`: the JWT travels in the `token` query parameter (browsers cannot set headers on a
  WebSocket handshake); an invalid token closes the socket with code 4401 after accept. Each command
  carries a `request_id` echoed by `ack` / `members` / `error`; `error.code` is the `MemberError` value.
