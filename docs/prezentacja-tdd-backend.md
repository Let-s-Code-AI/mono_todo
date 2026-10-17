---
marp: true
theme: default
paginate: true
title: TDD w praktyce — backend FastAPI + Claude Code
---

<!-- _class: lead -->

# TDD w praktyce
## Backend FastAPI + Claude Code

**Red → Green → Refactor** na przykładzie projektu `mono_todo`

---

# Agenda

1. Aplikacja: co robi i jak jest zbudowana
2. Stack: FastAPI, Pydantic, WebSocket
3. Czym jest Test-Driven Development
4. Cykl Red → Green → Refactor na realnym kodzie
5. TDD vs BDD vs klasyczne testowanie
6. Wartość biznesowa testów przed kodem
7. Claude Code: podstawowe komendy
8. `CLAUDE.md` — pamięć projektu
9. Skille i tworzenie skilla `tdd`

---

# Aplikacja: TODO API

MVP aplikacji do zadań, backend w `services/backend`.

| Obszar | Co robi |
|---|---|
| Auth | rejestracja, logowanie, JWT Bearer, role admin |
| Tasks | CRUD, filtry (status, priorytet, tag, `overdue`), terminy |
| Categories / Tags | kategorie z kolorem, tagi na zadaniach |
| AI priority | `MockAIPriorityService` lub OpenAI; AI nigdy nie blokuje zapisu |
| Projects | projekty wieloosobowe, członkowie, role owner/member |
| Realtime | `/ws/projects` — snapshot, komendy, push do wszystkich członków |

Stack: Python 3.10+, FastAPI, SQLModel + SQLite, Alembic, Pydantic v2, pytest.

---

# Architektura warstwowa

Każda warstwa korzysta tylko z warstwy poniżej. Routery nie znają repozytoriów.

```
API        app/api/routers/tasks.py      HTTP, statusy, HTTPException
Service    app/services/task_service.py  logika biznesowa, orkiestracja
Repository app/db/repository.py          wyłącznie zapytania SQL
Models     app/db/models.py              SQLModel ORM
Schemas    app/schemas/task.py           Pydantic — wejście / wyjście API
```

Łańcuch dependency injection:

```
get_session → get_task_repository → get_ai_service → get_task_service
```

Serwisy i repozytoria dostają zależności przez `Depends`, nie tworzą ich same.
Dzięki temu w testach podmieniamy sesję i AI jedną linią (`dependency_overrides`).

---

# FastAPI — dlaczego

- **Typy = kontrakt.** Sygnatura endpointu generuje walidację, dokumentację OpenAPI i serializację.
- **Dependency injection** wbudowane w framework — bez kontenera, bez magii.
- **`async def` tylko tam, gdzie jest `await`** (wywołanie AI). Zwykłe `def` FastAPI uruchamia w threadpoolu, więc synchroniczna sesja SQLModel nie blokuje event loopu.
- **`TestClient`** (httpx) wykonuje prawdziwe żądania HTTP i WebSocket bez odpalania serwera.

```python
def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
    ai_service: MockAIPriorityService | OpenAIPriorityService = Depends(get_ai_service),
) -> TaskService:
    return TaskService(repository, ai_service)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task_data: TaskCreate, service: TaskService = Depends(get_task_service), ...):
    ...
```

---

# Pydantic v2 i `pydantic-core`

Pydantic v2 waliduje w **`pydantic-core`** (Rust) — walidacja jest 5-50x szybsza niż w v1, a model Pythonowy to tylko opis schematu.

W projekcie Pydantic robi trzy rzeczy:

- **Schematy API** — `TaskCreate`, `TaskResponse` z `Field(max_length=...)`, `from_attributes=True` do mapowania ORM → JSON.
- **Konfiguracja** — `pydantic-settings` czyta `.env` (`JWT_SECRET_KEY`, `OPENAI_API_KEY`).
- **Protokół WebSocket** — discriminated union komend + `TypeAdapter`:

```python
Command = Annotated[
    CreateProjectCommand | ListMembersCommand | AddMemberCommand | RemoveMemberCommand,
    Field(discriminator="type"),
]
command_adapter: TypeAdapter[Command] = TypeAdapter(Command)

command = command_adapter.validate_json(raw)   # jedno wywołanie, pełna walidacja ramki
```

Nieprawidłowa ramka to `ValidationError`, który zamieniamy na `ErrorMessage(code="invalid_message")`.

---

# WebSocket `/ws/projects`

Przeglądarka nie ustawi nagłówka przy handshake'u, więc JWT jedzie w `?token=`.
Zły token zamyka socket kodem **4401** po `accept()`.

```
klient ──connect──▶ snapshot {type: "projects", projects: [...]}
klient ──{type: "create_project", request_id: "r1", name: "Remont"}──▶
       ◀── {type: "project_added", project: {...}}      (do każdego członka)
       ◀── {type: "ack", request_id: "r1"}               (do nadawcy)
```

- Każda komenda ma `request_id`; odpowiedź (`ack` / `members` / `error`) go echo'uje.
- `ConnectionManager` na `app.state` trzyma sockety per użytkownik i robi fan-out.
- Handler jest `async def`, ale serwis woła przez `run_in_threadpool`, a sesja jest zamykana po każdej komendzie — długie połączenie nie serwuje przeterminowanych wierszy.
- REST `/projects/` zostaje bez zmian i nic nie broadcastuje — frontend używa tylko socketu.

---

# Czym jest Test-Driven Development

**Technika projektowania kodu**, w której test powstaje *przed* implementacją.

Zasada nadrzędna z naszego skilla `tdd`:

> Żadnej linii kodu produkcyjnego bez wcześniej failującego testu.

Co TDD **nie** jest:
- "napiszę kod, potem dopiszę testy" — to testowanie, nie TDD
- celowanie w procent pokrycia
- pisanie testów do każdej metody prywatnej

Co TDD **jest**:
- test definiuje kontrakt: URL, status, kształt JSON
- małe kroki: jedno zachowanie = jeden test = jeden cykl
- natychmiastowy feedback, czy kod robi to, co miał robić

---

# Filozofia: Red → Green → Refactor

| Faza | Co robisz | Komenda w projekcie |
|---|---|---|
| **RED** | jeden test dla jednego zachowania; uruchom i **zobacz** czerwień, sprawdź powód | `pytest tests/test_x.py::test_y -q` |
| **GREEN** | najmniejszy kod, który przechodzi; hardkod jest OK | `pytest -q` (cała suita) |
| **REFACTOR** | porządek przy zielonych: duplikacja, nazwy, warstwy | `pytest -q && ruff check app tests && black app tests` |

Zanim zaczniesz: **lista zachowań** jako checklista. Każda pozycja to przyszły test.

```
- [ ] POST /projects/ zwraca 201 i tworzy projekt z owner_id = zalogowany
- [ ] POST /projects/ bez tokena → 401
- [ ] POST /projects/{id}/members przez nie-ownera → 403
- [ ] POST /projects/{id}/members z nieznanym emailem → 404
```

Dobry powód czerwieni: `404 != 201`, `ImportError`. Zły powód: literówka, brak `.env`.

---

# Cykl na realnym kodzie — RED

Zachowanie: *połączenie WS ze złym tokenem jest zamykane kodem 4401*.

```python
def test_invalid_token_closes_socket_with_4401(client: TestClient) -> None:
    """Scenario: Połączenie z nieprawidłowym tokenem jest zamykane kodem 4401."""
    with (
        client.websocket_connect("/ws/projects?token=invalid") as socket,
        pytest.raises(WebSocketDisconnect) as exc_info,
    ):
        socket.receive_json()

    assert exc_info.value.code == 4401
```

```
$ pytest tests/test_projects_ws.py::test_invalid_token_closes_socket_with_4401 -q
FAILED ... assert 1000 == 4401
```

Czerwień z **dobrego powodu**: endpoint istnieje, ale zamyka socket domyślnym kodem 1000.

---

# Cykl na realnym kodzie — GREEN i REFACTOR

**GREEN** — minimum, które zazielenia test:

```python
WS_4401_UNAUTHORIZED = 4401

await websocket.accept()
user = await run_in_threadpool(get_user_from_token, token, session)
if user is None:
    await websocket.close(code=WS_4401_UNAUTHORIZED, reason="Invalid or expired token")
    return
```

**REFACTOR** — przy zielonej suicie:
- `get_user_from_token` wyciągnięty do `app/api/deps.py`, bo używa go też `get_current_user` (REST)
- guard clause na górze, happy path niżej
- `pytest -q && ruff check app tests && black app tests`

Następna pozycja z listy: *snapshot projektów zaraz po połączeniu* — i znowu RED.

---

# TDD vs BDD vs klasyczne testowanie

| | Klasyczne testowanie | TDD | BDD |
|---|---|---|---|
| **Kiedy test** | po implementacji | przed implementacją | przed, jako scenariusz |
| **Kto pisze** | dev / QA | dev | biznes + dev + QA |
| **Język** | kod | kod | Given / When / Then |
| **Jednostka** | metoda, klasa | **zachowanie** | scenariusz użytkownika |
| **Główny cel** | wykryć regresje | zaprojektować kod | uzgodnić wymagania |
| **Ryzyko** | testy dopasowane do kodu | mikro-kroki bez widoku całości | ceremonia bez automatyzacji |

W projekcie łączymy dwa światy: test API przez `TestClient` (TDD) z docstringiem
`"""Scenario: ..."""` po polsku (język BDD), np. `test_add_member_as_non_owner_returns_403`.

E2E w Playwright to zewnętrzna pętla BDD; testy backendu to wewnętrzna pętla TDD.

---

# Wartość biznesowa pisania testów przed kodem

- **Tańsze błędy.** Bug znaleziony w cyklu RED kosztuje minuty; na produkcji — incydent, hotfix, rollback.
- **Specyfikacja, która nie kłamie.** 141 testów to wykonywalna dokumentacja API. README może się zestarzeć, test nie.
- **Bezpieczny refaktor.** Zmiana warstw, migracja, nowy serwis — suita mówi w sekundy, czy coś pękło.
- **Mniejsze PR-y, szybszy review.** Jeden cykl = jedno zachowanie = czytelny diff.
- **Przewidywalna wycena.** Lista zachowań powstaje przed kodem, więc "ile zostało" to liczba nieodhaczonych pozycji.
- **Onboarding.** Nowa osoba (albo agent AI) czyta test i wie, jaki jest kontrakt.

---

# Wartość biznesowa — jak to wygląda w CI

`.github/workflows/backend.yml` na każdym PR:

| Job | Co sprawdza | Dlaczego biznes to obchodzi |
|---|---|---|
| `lint` | `ruff check`, `black --check` | spójny kod = tańszy review |
| `test` | `alembic upgrade head` na świeżej bazie, `pytest --cov-fail-under=80` | migracje działają, pokrycie nie spada |
| `mutation` | `mutmut run` | testy naprawdę wykrywają błędy, nie tylko "przechodzą" |

Mutation testing podmienia operatory w kodzie (`==` → `!=`, `>` → `>=`).
Jeśli suita dalej jest zielona, test nic nie weryfikuje.

Z TDD mutanty giną, bo każdy test powstał po to, żeby **zobaczyć czerwień**.

---

# Claude Code — co to jest

Agent terminalowy: czyta repo, uruchamia komendy, edytuje pliki, pisze testy.
Działa w katalogu projektu i respektuje jego konfigurację (`.claude/`, `CLAUDE.md`).

| Komenda | Co robi |
|---|---|
| `claude` | start sesji interaktywnej w bieżącym katalogu |
| `claude "napraw test X"` | start z promptem |
| `claude -p "..."` | tryb nieinteraktywny, wynik na stdout (CI, skrypty) |
| `claude -c` | kontynuuj ostatnią rozmowę |
| `/init` | wygeneruj `CLAUDE.md` z analizy repo |
| `/clear` / `/compact` | wyczyść lub skompresuj kontekst |
| `/model` | zmień model |
| `/permissions` | zarządzaj uprawnieniami narzędzi |
| `/memory` | edytuj pliki `CLAUDE.md` |

W promptcie: `@app/main.py` dołącza plik, `! pytest -q` uruchamia komendę w sesji.

---

# `CLAUDE.md` — pamięć projektu

Plik Markdown czytany **automatycznie** na starcie każdej sesji. To instrukcja dla agenta, nie dokumentacja dla ludzi.

Hierarchia (od ogólnego do szczegółowego):
- `~/.claude/CLAUDE.md` — Twoje preferencje we wszystkich projektach
- `./CLAUDE.md` — root repo, wspólny dla zespołu (w git)
- `./CLAUDE.local.md` — lokalne nadpisania (gitignore)
- `services/backend/CLAUDE.md` — doczytywany, gdy agent pracuje w tym katalogu

Co trzymamy w `services/backend/CLAUDE.md`:

```
## Commands            pytest, ruff, black, alembic — dokładne komendy
## Development Workflow: TDD
   Every change to app/ follows the `tdd` skill: red → green → refactor
## Architecture        warstwy, łańcuch DI, reguły: router nie importuje repo
## Testing             pytest-mock, SQLite plikowy, autouse fixture na _PRIORITY_CACHE
## Error Handling      guard clauses, HTTPException tylko w routerach
```

Zasada: **krótko, konkretnie, reguły zamiast opisów.** Każda linia kosztuje kontekst.

---

# Skille — co to jest

Skill to katalog `.claude/skills/<nazwa>/SKILL.md`: instrukcja ładowana **na żądanie**, gdy zadanie pasuje do opisu albo gdy wywołasz `/<nazwa>`.

```
services/backend/.claude/
├── skills/
│   └── tdd/
│       └── SKILL.md       ← frontmatter name + description, potem treść
├── commands/
│   └── backend.md         ← /backend: audyt warstw i konwencji
└── settings.json          ← deny: Read(.env), Read(*.db) ...
```

| | `CLAUDE.md` | Skill |
|---|---|---|
| Ładowany | zawsze, na starcie | gdy pasuje `description` lub `/nazwa` |
| Zawartość | reguły projektu, komendy | procedura krok po kroku dla jednego typu zadania |
| Rozmiar | krótki | może być długi — kosztuje kontekst tylko gdy użyty |

`description` to **trigger**. Pisz w nim *kiedy* użyć, nie tylko *co* robi.

---

# Tworzenie skilla `tdd` — krok po kroku

**1. Frontmatter z mocnym triggerem**

```yaml
---
name: tdd
description: Cykl TDD (red → green → refactor) dla tego monorepo. Użyj ZAWSZE, zanim
  napiszesz kod produkcyjny w services/backend — przy nowym endpoincie, modelu, serwisie,
  zmianie zachowania lub naprawie buga. Prowadzi krok po kroku: lista zachowań, jeden
  failujący test, minimalna implementacja, refaktor, z komendami pytest/ruff/black.
---
```

**2. Treść jako procedura, nie esej**

```
## 0. Zanim zaczniesz: lista zachowań     checklista, każda pozycja = test
## 1. Cykl                                RED / GREEN / REFACTOR z komendami
## 2. Outside-in                          od testu API przez TestClient, unit tylko dla logiki
## 3. Konwencje testów w tym projekcie    fixtures z conftest.py, nazewnictwo, Arrange/Act/Assert
## 4. Czego nie robić                     więcej niż 1 czerwony test, "testy dopiszę później"
## 6. Jak raportować                      który test był czerwony i dlaczego, co zazieleniło
```

**3. Podpięcie w `CLAUDE.md`**: `Every change to app/ follows the tdd skill` — skill staje się obowiązkowy.

---

# Skill `tdd` w akcji

Prompt:

> Dodaj endpoint `DELETE /projects/{id}` — tylko owner może usunąć projekt.

Co robi agent z załadowanym skillem:

1. **Lista zachowań**: 204 dla ownera · 403 dla członka · 404 dla nieistniejącego · 401 bez tokena
2. **RED**: `test_delete_project_as_owner_returns_204` → `pytest ... -q` → `405 Method Not Allowed`
3. **GREEN**: router → `service.delete_project` → `repository.delete`; `pytest -q` → zielono
4. **REFACTOR**: `ruff check app tests && black app tests`
5. Powrót do RED z `test_delete_project_as_member_returns_403`
6. **Raport**: który test był czerwony i dlaczego, co go zazieleniło, `145 passed`

Skill wymusza też konwencje z `conftest.py`: `client`, `other_client`, `unauth_client`,
mockowanie tylko przez `mocker`, docstring `"""Scenario: ..."""`.

---

# Podsumowanie

- **Aplikacja**: FastAPI + Pydantic v2 + SQLModel, warstwy API → Service → Repository, realtime po WebSocket z komendami i `request_id`.
- **TDD** to projektowanie przez testy: lista zachowań, jeden czerwony test, minimum kodu, refaktor na zielonym.
- **TDD vs BDD vs klasyczne**: różni je moment pisania testu, język i cel. W projekcie łączymy TDD na API z scenariuszami po polsku.
- **Biznes**: tańsze błędy, wykonywalna specyfikacja, bezpieczny refaktor, mierzalny postęp; CI pilnuje pokrycia i mutacji.
- **Claude Code**: `CLAUDE.md` to stałe reguły, skill to procedura na żądanie. Skill `tdd` + jedna linia w `CLAUDE.md` sprawia, że agent nie napisze kodu bez czerwonego testu.

```bash
cd services/backend && source .venv/bin/activate
pytest -q && ruff check app tests && black app tests
```

Pytania?
