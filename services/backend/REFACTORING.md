# Refactoring — backend

## Status realizacji

Wszystkie punkty z tej listy zostały zrealizowane na branchu `refactor`.

- [x] 1. Importy wewnątrz metod (`repository.py`) — importy datetime są na górze pliku.
- [x] 2. Nieużywany import (`tasks.py`) — usunięto `CategoryRepository`.
- [x] 3. Martwa funkcja `_get_category_name` (`tasks.py`) — usunięta po przeniesieniu logiki do serwisu.
- [x] 4. Walidacja kategorii w routerze zamiast w serwisie (`tasks.py`) — przeniesiona do `TaskService`.
- [x] 5. Zły typ zwracany przez `get_ai_service` (`tasks.py`) — dependency typowane przez `AIPriorityService`.
- [x] 6. Synchroniczny klient OpenAI w `async def` (`ai_priority_service.py`) — użyto `AsyncOpenAI` + `await`.
- [x] 7. Dependencje serwisów w routerze zamiast w `deps.py` (`tasks.py`) — przeniesione do `app/api/deps.py`.

## Powiązane commity (branch `refactor`)

- `56646eb` — remove unused import + reuse helper
- `dba68c0` — type AI dependency as protocol
- `452d1e7` — move task dependencies to `app.api.deps`
- `975422f` — move category validation to service layer
- `48751fc` — switch OpenAI service to async client
- `f2bbd89` — adapt tests to async OpenAI mocks

## 1. Importy wewnątrz metod (`repository.py`)

`from datetime import timedelta` (linia 132) i `from datetime import datetime, timezone` (linia 146) są wewnątrz ciał metod. Powinny być na górze pliku.

## 2. Nieużywany import (`tasks.py` linia 12)

`CategoryRepository` jest importowany, ale nigdy nie używany — router robi `session.get(Category, ...)` bezpośrednio.

## 3. Martwa funkcja `_get_category_name` (`tasks.py` linia 69)

Zdefiniowana, ale żaden endpoint jej nie wywołuje. `create_task` i `update_task` duplikują tę samą logikę inline.

## 4. Walidacja kategorii w routerze zamiast w serwisie (`tasks.py`)

`create_task` i `update_task` robią `session.get(Category, ...)` bezpośrednio w routerze, omijając warstwę serwisu. Narusza to architekturę: router nie powinien dotykać sesji bazy danych poza wstrzykiwaniem zależności.

## 5. Zły typ zwracany przez `get_ai_service` (`tasks.py` linia 54)

Sygnatura zwraca `MockAIPriorityService | OpenAIPriorityService` zamiast `AIPriorityService` (Protocol). Cały sens protokołu jest po to, żeby ukryć konkretną implementację.

## 6. Synchroniczny klient OpenAI w `async def` (`ai_priority_service.py` linia 105)

`self._client.chat.completions.create(...)` to wywołanie blokujące event loop. Należy użyć `AsyncOpenAI` z `await client.chat.completions.create(...)`.

## 7. Dependencje serwisów w routerze zamiast w `deps.py` (`tasks.py` linie 49–66)

`get_task_repository`, `get_ai_service`, `get_task_service` to reużywalne zależności infrastrukturalne — powinny żyć obok `get_current_user` w `app/api/deps.py`.

---

| # | Plik | Priorytet | Kategoria |
|---|------|-----------|-----------|
| 4 | `tasks.py` | wysoki | poprawność architektury |
| 5 | `tasks.py` | wysoki | poprawność typów |
| 6 | `ai_priority_service.py` | wysoki | poprawność (async) |
| 3 | `tasks.py` | średni | martwy kod |
| 7 | `tasks.py` | średni | architektura |
| 1 | `repository.py` | niski | styl |
| 2 | `tasks.py` | niski | styl |
