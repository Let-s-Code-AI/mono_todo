# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Monorepo of a Todo app (UI and docs in Polish). Each service has its own `CLAUDE.md` with commands, architecture and conventions — read the one for the service you touch:

| Path | Stack | Notes |
|---|---|---|
| `services/backend` | FastAPI + SQLModel + SQLite, Alembic | layered architecture, TDD workflow, REST + `/ws/projects` WebSocket |
| `services/frontend` | React 18 + Vite (single-file `App.jsx`) | Vite proxies `/auth /tasks /categories /projects` and `/ws` to `:8000` |
| `services/e2e` | pytest + Playwright (Chromium) | needs the whole stack running |
| `services/mcp_tool` | FastMCP server | wraps the backend OpenAPI spec; needs the backend up on `:8000` at start; has a hardcoded `X-API-Key` |

`services/EPICS.md` holds planned features (not implemented). The `projekt` skill (`.claude/skills/projekt`) summarizes repo-wide conventions; `.claude/agents/e2e-runner.md` runs the E2E suite and reports a short summary.

## Commands (from the repo root)

```bash
./install.sh   # venv + pip install -e ".[dev]", generates backend/.env (JWT secret, SQLite), alembic upgrade head, npm install
./start.sh     # backend on :8000 (uvicorn --reload) + frontend on :5173; Ctrl+C stops both; PIDs in .dev-pids
```

Requires Python 3.11+ and Node 18+. `start.sh` refuses to run until `install.sh` has created `services/backend/.venv`, `node_modules` and `.env`. API docs at http://localhost:8000/docs. `OPENAI_API_KEY` in `services/backend/.env` is optional; without it the heuristic `MockAIPriorityService` is used.

Per-service test/lint commands (run inside the service directory, backend needs `source .venv/bin/activate`):

```bash
# backend
pytest tests/test_tasks_api.py::test_create_task   # single test
ruff check app tests && black app tests
# frontend
npm run build                                      # only check; no test framework
# e2e (stack must be running via ./start.sh, WITHOUT OPENAI_API_KEY)
.venv/bin/pytest -n auto
.venv/bin/pytest "test_tasks.py::TestAddTask::test_add_task_appears_on_list"
```

## Cross-service things to know

- Changing a backend route or response shape usually requires updating `services/frontend/src/api.js` **and** the E2E page objects (`services/e2e/pages.py`). E2E results depend on deterministic mock-AI priorities (due date within 3 days → `high`).
- CI (`.github/workflows/`): `backend.yml` and `frontend.yml` are path-filtered per service; `e2e.yml` triggers on backend/frontend changes and runs the built frontend (`vite preview`) against uvicorn after `alembic upgrade head`.
- Services were merged in as git subtrees (`git subtree pull --prefix=services/<name> <remote> main --squash`, see `README.md`); don't rewrite their history.
- The working tree may receive foreign auto-commits mid-task — avoid `git stash`.
