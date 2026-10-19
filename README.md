# mono_todo

Monorepo for the Todo Workshop project, made up of three services:

| Directory | Source repo | Description |
|---|---|---|
| `services/backend` | `todo_ai_worshop` | FastAPI + SQLite + AI priority |
| `services/frontend` | `todo_workshop_frontend` | React + Vite |
| `services/e2e` | `todo_e2e` | E2E tests (Playwright) |

## Structure

```
mono_todo/
├── services/
│   ├── backend/    # Python / FastAPI
│   ├── frontend/   # JavaScript / React
│   └── e2e/        # Python / Pytest + Playwright
└── README.md
```

## Updating the subtrees

```bash
# Backend
git subtree pull --prefix=services/backend todo_ai_worshop main --squash

# Frontend
git subtree pull --prefix=services/frontend todo_workshop_frontend main --squash

# E2E
git subtree pull --prefix=services/e2e todo_selenium main --squash
```
