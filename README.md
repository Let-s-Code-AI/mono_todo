# mono_todo

Monorepo dla projektu Todo Workshop składające się z trzech serwisów:

| Katalog | Repo źródłowe | Opis |
|---|---|---|
| `services/backend` | `todo_ai_worshop` | FastAPI + SQLite + AI priority |
| `services/frontend` | `todo_workshop_frontend` | React + Vite |
| `services/e2e` | `todo_e2e` | Testy E2E (Playwright) |

## Struktura

```
mono_todo/
├── services/
│   ├── backend/    # Python / FastAPI
│   ├── frontend/   # JavaScript / React
│   └── e2e/        # Python / Pytest + Playwright
└── README.md
```

## Aktualizacja subdrzew

```bash
# Backend
git subtree pull --prefix=services/backend todo_ai_worshop main --squash

# Frontend
git subtree pull --prefix=services/frontend todo_workshop_frontend main --squash

# E2E
git subtree pull --prefix=services/e2e todo_selenium main --squash
```
