---
name: backend
description: Audit or review code in this FastAPI todo backend. Use when asked to check architecture compliance, layer boundaries, DI chain correctness, testing conventions, or async usage.
---

When invoked, perform the following steps:

1. **Check scope** — run `git diff HEAD` (or `git diff main...HEAD` for a branch) to see what changed.

2. **Audit layer boundaries** (hard rule: no layer skips the one below it):
   - Router must not import `TaskRepository` directly — only through `TaskService`
   - Service must not create `Session` objects — only receive them via DI
   - Repository must contain only SQL queries — no business logic

3. **Verify DI chain** — new dependencies must slot into the existing chain:
   ```
   get_session → get_task_repository → get_ai_service → get_task_service
   ```
   Horizontal dependencies between services are forbidden.

4. **async/def correctness**:
   - `async def` when the endpoint calls `await ai_service.*` or delegates to an async service method
   - `def` when the endpoint only touches the synchronous SQLModel session
   - Never wrap the SQLModel session in `asyncio.run`

5. **Error handling** — routers raise `HTTPException`, never propagate service-layer exceptions; guard clauses at the top, happy path last; no `try/except` for domain errors in routers.

6. **Auth scoping** — endpoints that return user data must pass `owner_id=current_user.id`; scoping happens in the router, not the service.

7. **AI service rules**:
   - `AIPriorityService` is a `Protocol` — new implementations must not inherit from it
   - `_PRIORITY_CACHE` must be cleared in an `autouse` fixture in any test that touches the AI module
   - AI errors must not propagate — `suggest_priority` returns `(Priority.MEDIUM, None)` on failure

8. **Testing conventions**:
   - Only `pytest-mock` (`mocker` fixture) — never `unittest.mock.patch` as a context manager
   - File-based SQLite (`test.db`), not in-memory
   - All fixtures must be `function`-scoped
   - AI service swapped via `app.dependency_overrides[get_ai_service]`

9. **Migration hygiene** — `create_db_and_tables()` only in dev/test; production always uses Alembic; no `create_all` in environments with an existing database.

10. **Code style**:
    - Google-style docstrings on all endpoints (Args / Returns / Raises)
    - Auxiliary-verb names: `is_admin`, `has_permission`, `use_ai_priority`
    - No unused imports (`ruff check` enforces this)
    - `black` for formatting — do not edit style manually

Report findings grouped by severity (blocking / warning / suggestion). For each finding cite the file and line number.
