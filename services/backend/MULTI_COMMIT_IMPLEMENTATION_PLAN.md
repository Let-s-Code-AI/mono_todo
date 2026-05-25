# Multi-commit implementation plan (backend)

## Założenia operacyjne

- Repo root: `/home/user/repos/mono_todo`
- Zakres: `services/backend`
- Każdy commit:
  - ma mały zakres,
  - jest reviewowalny,
  - jest niezależnie testowalny.

### Bazowe komendy testowe

```bash
cd /home/user/repos/mono_todo/services/backend
pytest -q
```

---

## Commit 1 — Typy DI: użycie protokołu `AIPriorityService` w routerze

**Cel:** naprawa punktu #5 (`REFACTORING.md`) bez zmiany logiki runtime.

**Zmiany:**

- `app/api/routers/tasks.py`
  - import `AIPriorityService` z `app.services.ai_priority_service`,
  - zmiana sygnatur:
    - `get_ai_service() -> AIPriorityService`,
    - zależności w `get_task_service` i endpointach na `AIPriorityService`,
  - pozostawienie implementacji Mock/OpenAI bez zmian.

**Dlaczego osobny commit:** czysta poprawa kontraktów typów, brak zmian behawioralnych.

**Testy:**

```bash
cd /home/user/repos/mono_todo/services/backend
pytest -q tests/test_tasks_api.py tests/test_ai_priority_service.py
python3 -m compileall app/api/routers/tasks.py
```

---

## Commit 2 — Przeniesienie zależności serwisowych z routera do `deps.py`

**Cel:** realizacja punktu #7 (`REFACTORING.md`).

**Zmiany:**

- `app/api/deps.py`
  - dodać:
    - `get_task_repository(...) -> TaskRepository`,
    - `get_ai_service(...) -> AIPriorityService`,
    - `get_task_service(...) -> TaskService`.
- `app/api/routers/tasks.py`
  - usunąć lokalne definicje powyższych dependency providerów,
  - importować je z `app.api.deps`.

**Dlaczego osobny commit:** zmiana architektoniczna DI bez zmiany biznesowej logiki endpointów.

**Testy:**

```bash
cd /home/user/repos/mono_todo/services/backend
pytest -q tests/test_tasks_api.py tests/test_auth_api.py
python3 -m compileall app/api
```

---

## Commit 3 — Przeniesienie walidacji kategorii z routera do serwisu

**Cel:** realizacja punktu #4 (`REFACTORING.md`) — router nie powinien zawierać logiki biznesowej o kategorii.

**Zmiany:**

- `app/services/task_service.py`
  - dodać metodę pomocniczą, np. `_resolve_category_name_or_404(category_id)` (lub równoważną),
  - w `create_task(...)` robić walidację i rozpoznanie kategorii w serwisie,
  - w `update_task(...)` walidować `category_id`, jeśli jest przekazane.
- `app/api/routers/tasks.py`
  - usunąć helper `_get_category_name` (stanie się zbędny),
  - usunąć bezpośrednią walidację `session.get(Category, ...)` w endpointach,
  - przekazywać do serwisu wyłącznie dane wejściowe i `owner_id`.

**Dlaczego osobny commit:** zmiana dotyka granicy warstw (router ↔ service), potencjalnie behawioralna (miejsce rzucania 404).

**Testy:**

```bash
cd /home/user/repos/mono_todo/services/backend
pytest -q tests/test_tasks_api.py tests/test_categories_tags.py
```

---

## Commit 4 — Async OpenAI: usunięcie blokującego wywołania

**Cel:** realizacja punktu #6 (`REFACTORING.md`) — nieblokowanie event loop w `async def`.

**Zmiany:**

- `app/services/ai_priority_service.py`
  - przejście z klienta synchronicznego na `AsyncOpenAI`,
  - użycie `await client.chat.completions.create(...)`,
  - zachowanie istniejącego kontraktu interfejsu i fallbacków.

**Dlaczego osobny commit:** zmiana integracyjna z SDK OpenAI, wyższe ryzyko regresji.

**Testy:**

```bash
cd /home/user/repos/mono_todo/services/backend
pytest -q tests/test_ai_priority_service.py tests/test_tasks_api.py
```

---

## Commit 5 — Porządki i aktualizacja dokumentacji refaktoryzacji

**Cel:** domknięcie zmian i czytelna dokumentacja stanu.

**Zmiany:**

- `REFACTORING.md`
  - odznaczyć zrealizowane punkty,
  - dopisać krótkie adnotacje „co i gdzie zmieniono”.
- ewentualne drobne cleanupy importów po poprzednich commitach.

**Dlaczego osobny commit:** niski risk, łatwy przegląd dokumentacyjny.

**Testy:**

```bash
cd /home/user/repos/mono_todo/services/backend
pytest -q
```

---

## Sugerowane tytuły commitów

1. `refactor(tasks): type DI providers against AIPriorityService protocol`
2. `refactor(api): move task dependency providers to app.api.deps`
3. `refactor(tasks): move category validation from router to service layer`
4. `fix(ai): use AsyncOpenAI in async priority service`
5. `docs(refactoring): mark completed backend refactor items`

---

## Kolejność i zależności

- Kolejność: C1 → C2 → C3 → C4 → C5
- C3 zależy od C2 (zmiany miejsc dostarczania zależności).
- C4 można wykonać niezależnie od C3, ale praktycznie lepiej po C3, żeby zminimalizować konflikty.