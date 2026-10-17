---
marp: true
theme: default
paginate: true
title: Generowanie testów z pomocą AI — jednostkowe, brzegowe, regresyjne, asynchroniczne, wydajnościowe
---

<!-- _class: lead -->

# Generowanie testów z pomocą AI
## Claude Code na przykładzie backendu `mono_todo`

Testy jednostkowe z poziomu funkcji → uzupełnianie klas testowych → przypadki brzegowe i regresyjne → asynchroniczność i wydajność → jak oceniać to, co wygenerował model

---

# Agenda

1. Punkt wyjścia: suita `mono_todo` w liczbach
2. Jak LLM generuje testy i czego potrzebuje w kontekście
3. Testy jednostkowe z poziomu funkcji / metody
4. Automatyczne uzupełnianie istniejącej klasy testowej
5. Przypadki brzegowe
6. Testy regresyjne i charakteryzujące
7. Testy asynchroniczności
8. Testy wydajności
9. Best practices przy ocenie testów wygenerowanych przez LLM
10. Workflow w Claude Code: `CLAUDE.md`, skill, hook, subagent

---

# Punkt wyjścia — suita backendu dziś

```
$ cd services/backend && pytest -q --cov=app --cov-report=term-missing
146 passed in 23.26s        TOTAL 1100 stmts, 41 miss, 96%
```

| Plik | LOC | Co testuje |
|---|---|---|
| `test_tasks_api.py` | 483 | CRUD zadań, AI priority, reanalyze |
| `test_deadlines.py` | 388 | terminy, `overdue`, `upcoming`, AI + `due_date` |
| `test_projects_ws.py` | 350 | WebSocket: snapshot, komendy, `request_id`, 4401 |
| `test_ai_priority_service.py` | 344 | **klasy testowe** `TestMockAIPriorityService`, `TestOpenAIPriorityService` |
| `test_categories_tags.py` | 336 | kategorie, tagi, filtry |
| `test_tasks_realtime.py` | 130 | push `task_created/updated/deleted` po REST |

Konwencje z `conftest.py` i `CLAUDE.md`: `client` / `other_client` / `admin_client` / `unauth_client`, plikowy SQLite per test, `mocker` zamiast `unittest.mock`, `autouse` czyszczący `_PRIORITY_CACHE`, `asyncio_mode = auto`.

Niewykonane linie, do których wrócimy: `task_service.py:189, 201, 238-240`, `realtime.py:37-38`, `routers/tasks.py:89-92, 318, 352, 382`.

---

# Jak LLM generuje testy

Model **dopełnia wzorzec** z kontekstu. Jakość testu zależy od tego, co mu pokażesz, a nie od tego, co „wie o pytest”.

| W kontekście | Bez tego w kontekście |
|---|---|
| funkcja / klasa pod testem (`@app/...`) | test do wyobrażonej sygnatury |
| istniejący plik testów (styl, helpery) | nowe helpery zamiast `patch_async_client`, `_next_after_sentinel` |
| `conftest.py` | zmyślone fixtures: `async_client`, `db_session` |
| sekcja *Testing* z `CLAUDE.md` | `unittest.mock.patch` jako context manager, in-memory SQLite |
| wynik `pytest` (czerwony lub zielony) | test „wygląda dobrze”, nikt go nie uruchomił |

Trzy sytuacje, trzy prompty:

- **test-first** (skill `tdd`): zachowanie → czerwony test → kod
- **test-after** dla kodu zastanego: testy charakteryzujące obecne zachowanie
- **uzupełnianie luk**: `pytest --cov` + analiza gałęzi → brakujące scenariusze

---

# Anatomia promptu do generowania testów

```
[CEL]        Testy jednostkowe dla _build_cache_key z @app/services/ai_priority_service.py.
[STYL]       Jak w @tests/test_ai_priority_service.py; fixtures z @tests/conftest.py.
[ZAKRES]     Tylko tests/. Nie zmieniaj kodu produkcyjnego.
[KOLEJNOŚĆ]  Najpierw lista zachowań (checklista), potem po jednym teście na pozycję.
[ZAKAZ]      Nie mockuj funkcji pod testem. Nie pisz asercji, które przejdą zawsze.
[DOWÓD]      Uruchom pytest na nowych testach i pokaż wynik. Jeśli coś jest czerwone,
             powiedz dlaczego — nie poprawiaj asercji, żeby przeszło.
```

| Składnik | Co zapobiega |
|---|---|
| lista zachowań przed kodem | testy „pod linię” bez znaczenia biznesowego |
| styl z istniejącego pliku | drugi zestaw helperów, inna konwencja nazw |
| zakaz zmian w `app/` | „poprawka” kodu, żeby test przeszedł |
| zakaz dopasowywania asercji | najczęstszy sposób, w jaki agent „zazielenia” test |

---

# Testy jednostkowe z poziomu funkcji — `_build_cache_key`

Funkcja czysta, zero zależności: idealny start.

```python
def _build_cache_key(title, description, category_name=None, due_date=None) -> str:
    normalized_title = title.strip().lower()
    normalized_description = (description or "").strip().lower()
    normalized_category = (category_name or "").strip().lower()
    normalized_due = str(due_date) if due_date else ""
    return f"{normalized_title}|{normalized_description}|{normalized_category}|{normalized_due}"
```

Lista zachowań, którą zwraca model (po jednym teście na pozycję):

```
- [ ] wielkość liter i białe znaki nie zmieniają klucza        ("  Raport " == "raport")
- [ ] description=None i description="" dają ten sam klucz
- [ ] category_name wchodzi do klucza — ta sama treść, inna kategoria → inny klucz
- [ ] due_date wchodzi do klucza — ta sama treść, inny dzień → cache miss
- [ ] separator "|" w tytule nie skleja pól?  → tytuł "a|b" + opis "" vs "a" + opis "b"
```

Ostatnia pozycja to pytanie, nie test: model znalazł **kolizję klucza**. Decyzja (ignorować w MVP, czy zmienić separator) należy do człowieka. Test charakteryzujący dokumentuje wybór.

---

# Testy jednostkowe z poziomu metody — `TaskNotifier`

Metoda prywatna `_recipients` + kolejkowanie w `BackgroundTasks`. Testujemy przez publiczne `created()`, zależności jako `MagicMock`, bez bazy i bez `TestClient`.

```python
def test_project_task_event_goes_to_owner_and_members_once(mocker) -> None:
    """Scenario: właściciel będący też członkiem projektu dostaje zdarzenie raz."""
    manager = mocker.MagicMock()
    repo = mocker.MagicMock(member_ids=mocker.Mock(return_value=[1, 2, 3]))
    background = BackgroundTasks()
    notifier = TaskNotifier(manager, repo, background)
    task = mocker.MagicMock(owner_id=1, project_id=10)

    notifier.created(task, response=mocker.MagicMock())

    queued = background.tasks[0]
    assert queued.func is manager.send_to_users
    assert queued.args[0] == {1, 2, 3}          # set — bez duplikatu właściciela
```

Co model powinien dopisać sam: `project_id=None` → tylko `{owner_id}`; `owner_id=None` → tylko członkowie; `deleted()` niesie `task_id` i `project_id`.

Czego nie powinien: testować `_recipients` bezpośrednio (`notifier._recipients(...)`) — przypina test do nazwy prywatnej metody.

---

# Uzupełnianie istniejącej klasy testowej

`TestMockAIPriorityService` ma 18 testów, fixture `service`, `async def` bez markera. Prompt:

```
Porównaj gałęzie MockAIPriorityService.suggest_priority (@app/services/ai_priority_service.py)
z testami klasy TestMockAIPriorityService w @tests/test_ai_priority_service.py.
Zanim coś dopiszesz, przeszukaj cały katalog tests/ — scenariusz może już istnieć w innym pliku.
Wypisz: gałąź | test, który ją pokrywa (plik::nazwa) | brak.
Dopisz tylko brakujące, wewnątrz klasy, z fixture `service`, w stylu sąsiednich testów.
```

Co model znajduje (zweryfikowane):

| Gałąź | Stan |
|---|---|
| `due_date` ≤ 3 dni → HIGH (przeterminowane / dziś / za 2 dni) | jest, ale w `test_deadlines.py`, nie w klasie |
| **granica**: dokładnie 3 dni (HIGH) i 4 dni (nie HIGH) | **brak** |
| kategoria `egzaminy` / `exams` (liczba mnoga) | brak — testowane tylko `egzamin` |
| `urgent_keywords[:3]` — 4 słowa kluczowe, w uzasadnieniu tylko 3 | brak |
| `OpenAIPriorityService`: `category_name` i `due_date` w treści promptu (`:101, :103`) | brak — linie niewykonane |

Bez „przeszukaj cały `tests/`” model dopisze duplikaty testów terminów do klasy.

---

# Uzupełnianie klasy — co wraca i co sprawdzić

```python
class TestMockAIPriorityService:
    ...
    async def test_due_in_exactly_3_days_is_high(self, service):
        soon = date.today() + timedelta(days=3)
        priority, reason = await service.suggest_priority("Projekt", None, due_date=soon)
        assert priority == Priority.HIGH
        assert "3 dni" in reason

    async def test_due_in_4_days_is_not_boosted(self, service):
        later = date.today() + timedelta(days=4)
        priority, _ = await service.suggest_priority("Projekt", None, due_date=later)
        assert priority == Priority.MEDIUM

    async def test_reason_lists_at_most_three_urgent_keywords(self, service):
        _, reason = await service.suggest_priority("urgent critical asap important", None)
        assert reason.count("'") == 6          # 3 słowa w cudzysłowach
```

| Sprawdź | Dlaczego |
|---|---|
| używa fixture `service`, nie tworzy `MockAIPriorityService()` w teście | spójność z klasą |
| data **względna** (`date.today() + ...`), nie `date(2026, 10, 20)` | test nie zepsuje się za tydzień |
| test 4 dni asercja na `MEDIUM`, nie `!= HIGH` | `!= HIGH` przejdzie też dla LOW |
| czy zmiana `<= 3` → `< 3` w kodzie zrobi czerwień | właśnie po to jest test granicy |

---

# Przypadki brzegowe — granice są w kodzie

Prompt: *„Dla każdego parametru wejściowego wypisz granice z kodu (`Field`, `Query`, porównania, `[:n]`). Dla każdej granicy test po obu stronach.”*

| Źródło granicy | Wartości | Oczekiwane | Test dziś |
|---|---|---|---|
| `days_until_due <= 3` | 3 / 4 | HIGH / bez zmiany | **brak** |
| `title: Field(max_length=200)` | 200 / 201 znaków | 201 / 422 | **brak** |
| `limit: Query(ge=1, le=1000)` | 0, 1, 1000, 1001 | 422 / 200 / 200 / 422 | **brak** |
| `skip: Query(ge=0)` | -1 | 422 | **brak** |
| `days: Query(ge=1, le=365)` w `/tasks/upcoming` | 0 / 366 | 422 | **brak** |
| `add_tag` idempotentne | duplikat | tag raz | jest |
| `remove_tag` tagu, którego nie ma | `DELETE .../tags/nieistniejacy` | 200, lista bez zmian | **brak** |
| `add_tag` / `remove_tag` na cudzym lub nieistniejącym zadaniu | | 404 | **brak** (`task_service.py:189, 201`) |

Walidacje Pydantic/FastAPI wydają się „za darmo”, ale test granicy chroni przed **usunięciem** `le=1000` podczas refaktoru. To sekundy pracy modelu.

---

# Przypadki brzegowe — `parametrize` i mutanty

Model chętnie składa granice w `parametrize`. Dobrze, gdy zachowanie jest to samo, a zmieniają się dane:

```python
@pytest.mark.parametrize(
    ("limit", "expected_status"),
    [(0, 422), (1, 200), (1000, 200), (1001, 422)],
    ids=["below-min", "min", "max", "above-max"],
)
def test_list_tasks_limit_boundaries(client: TestClient, limit: int, expected_status: int) -> None:
    """Scenario: limit poza [1, 1000] jest odrzucany przez walidację."""
    assert client.get(f"/tasks/?limit={limit}").status_code == expected_status
```

Źle, gdy `parametrize` skleja **różne zachowania** (HIGH z powodu terminu i HIGH z powodu słowa kluczowego) — przy czerwieni nie wiesz, które pękło.

Mutation testing w CI (`mutmut run`, job `mutation`) pokazuje, po co są granice: mutant `<= 3` → `< 3` **przeżywa** bez testu na dokładnie 3 dni. Z testem — ginie.

---

# Testy regresyjne — trzy źródła

**1. Bug zgłoszony teraz** — reguła ze skilla `tdd`: najpierw test reprodukujący (RED), potem fix. Test zostaje. W repo:

```python
def test_reanalyze_clears_ai_override_when_priority_no_longer_overridden(...):
    """ai_override must become False when reanalysis no longer overrides user priority.

    Regression: TaskUpdate had no ai_override field, so the flag was never updated ...
```

**2. Znany, nienaprawiony bug** — `xfail(strict=True)` w `services/e2e/test_deadlines.py`:
`POST /tasks/priority/analyze` ignoruje `due_date` (`PriorityAnalysisRequest` nie ma pola).
`XPASS(strict)` = ktoś naprawił backend → usuń marker. Test regresyjny powstaje **przed** fixem.

**3. Historia git** — prompt:

```
Przejrzyj git log -p --grep=fix -i dla services/backend. Dla każdej poprawki: jakie zachowanie
chroni, który test w tests/ je pokrywa (plik::nazwa). Dla poprawek bez testu zaproponuj
test regresyjny z docstringiem "Regression: <co było zepsute>".
```

---

# Testy charakteryzujące dla kodu zastanego

Gdy nie wiesz, czy zachowanie jest poprawne, **zapisz je** zanim coś zmienisz (Feathers, *Working Effectively with Legacy Code*).

```
Napisz testy charakteryzujące dla TaskService.reanalyze_priority. Nie oceniaj, czy zachowanie
jest poprawne. Każdy docstring zaczyna się od "Charakteryzacja:". Gdy zachowanie różni się
od create_task, zaznacz to w komentarzu, ale nie zmieniaj kodu.
```

Co model wychwytuje w `mono_todo`:

```python
# create_task:       ai_override = (ai == HIGH) and (user_priority != HIGH)
# reanalyze_priority: ai_override = (priority == HIGH)        ← także gdy user sam dał HIGH
```

Test charakteryzujący utrwala drugą regułę z komentarzem *„różni się od create_task — do decyzji”*. Gdy zespół zdecyduje, że to bug: test zmienia się w regresyjny (RED), potem fix.

Prompt na luki: *„Porównaj `@app/services/task_service.py` z `@tests/`; wypisz publiczne metody bez testu i ścieżki `None`/404.”* Dziś: `get_stats` (`:238-240`, cały endpoint `/tasks/stats` bez testu), `add_tag`/`remove_tag` → `None`.

---

# Testy asynchroniczności — mechanika w tym projekcie

| Element | Jak działa u nas |
|---|---|
| `asyncio_mode = "auto"` | `async def test_...` bez `@pytest.mark.asyncio` (markery w `test_deadlines.py` są zbędne, ale nieszkodliwe) |
| `AsyncOpenAI` | `mocker.AsyncMock()` przez helper `patch_async_client(mocker)` |
| `TestClient` | portal: **synchroniczny** test wywołuje `async def` endpoint i `websocket_connect` |
| `BackgroundTasks` | wykonywane po odpowiedzi, wewnątrz tego samego `TestClient` |
| WS handler | `async def` + `run_in_threadpool` dla synchronicznej sesji SQLModel |

Cztery błędy, które LLM robi najczęściej:

| Błąd w wygenerowanym teście | Objaw |
|---|---|
| `mocker.MagicMock()` zamiast `AsyncMock` dla metody `await`-owanej | `TypeError: object MagicMock can't be used in 'await' expression` |
| brak `await` przed `service.suggest_priority(...)` | `RuntimeWarning: coroutine ... was never awaited` — **test przechodzi pusto** |
| `asyncio.run(...)` w teście `async def` | `RuntimeError: asyncio.run() cannot be called from a running event loop` |
| `time.sleep` / blokujące I/O w `async def` | test „działa”, ale nie testuje współbieżności |

Uruchom z `-W error::RuntimeWarning`, żeby „never awaited” był czerwienią, nie ostrzeżeniem.

---

# Async — test 1: martwy socket jest usuwany

`realtime.py:37-38` — gałąź `except (WebSocketDisconnect, RuntimeError)` nigdy nie wykonana (coverage). Prompt: *„Napisz test jednostkowy `ConnectionManager.send_to_users` dla socketu, który rzuca przy wysyłce. Fałszywe sockety przez `mocker.AsyncMock`.”*

```python
async def test_dead_socket_is_dropped_and_others_still_receive(mocker) -> None:
    """Scenario: socket rzucający WebSocketDisconnect znika z rejestru, drugi dostaje wiadomość."""
    manager = ConnectionManager()
    dead = mocker.MagicMock(send_json=mocker.AsyncMock(side_effect=WebSocketDisconnect()))
    alive = mocker.MagicMock(send_json=mocker.AsyncMock())
    manager.register(1, dead)
    manager.register(1, alive)

    await manager.send_to_users([1], {"type": "ping"})

    alive.send_json.assert_awaited_once_with({"type": "ping"})
    assert manager.connection_count(1) == 1
```

Dlaczego to dobry test wygenerowany: `MagicMock` z atrybutem `AsyncMock` (socket to obiekt, metoda jest async), asercja na **skutek** (`connection_count`), nie na wywołanie `unregister`.

---

# Async — test 2: współbieżność, której nikt nie zaprojektował

Prompt: *„Czy cache w `OpenAIPriorityService` chroni przed równoległymi wywołaniami o tym samym kluczu? Napisz test z `asyncio.gather`.”*

```python
async def test_concurrent_calls_with_same_key_hit_openai_once(mocker, service) -> None:
    _, mock_create = patch_async_client(mocker)
    async def slow(**kwargs):
        await asyncio.sleep(0.05)
        return make_openai_response(mocker, "PRIORITY: high\nREASON: test")
    mock_create.side_effect = slow

    await asyncio.gather(*[service.suggest_priority("Pilne", None) for _ in range(5)])

    assert mock_create.await_count == 1
```

```
FAILED  assert 5 == 1
```

Zmierzone: **5 równoległych wywołań = 5 requestów do OpenAI**. Cache zapisuje wynik dopiero po `await`, bez blokady ani rejestru „w locie”.

Decyzja człowieka, nie modelu: w MVP ruch jest znikomy → test zostaje jako **charakteryzujący** (`== 5`, komentarz *„brak ochrony przed stampede, świadome”*) albo fix z `asyncio.Lock` per klucz i test `== 1`. Model nie zna ruchu produkcyjnego.

---

# Async — test 3: push po `BackgroundTasks` i pułapka blokady

Naiwna wersja, którą generuje model dla „członek dostaje `task_created`”:

```python
with client.websocket_connect(url) as socket:
    socket.receive_json()                     # snapshot
    client.post("/tasks/", json={...})
    event = socket.receive_json()             # ← gdy push nie przyjdzie, test WISI, nie pada
```

Wzorzec z `test_tasks_realtime.py`: każde oczekiwanie ma **granicę**.

```python
def _next_after_sentinel(socket, project_id: int) -> dict:
    """First queued message once a `list_members` reply is guaranteed to follow it."""
    socket.send_json({"type": "list_members", "request_id": "sentinel", "project_id": project_id})
    return socket.receive_json()
```

Brak pusha → odbieramy `members` zamiast `task_created` → **czerwień w sekundę** zamiast zawieszonego CI.

Do promptu: *„Każde `receive_json()` po akcji REST przez `_next_after_sentinel`; żadnego gołego `receive_json()` poza snapshotem.”* Alternatywy, gdy nie ma sentinela: `anyio.fail_after(2)`, `asyncio.wait_for`, `pytest-timeout` (niezainstalowany).

---

# Testy wydajności — co mierzyć w suicie pytest

Nie czas zegarowy (CI jest wolniejsze i losowe), tylko **liczby, które rosną ze skalą**: zapytania SQL, wywołania zewnętrzne, `await`-y.

Zmierzone na `GET /tasks/` (zadania z kategorią): **10 zadań → 12 zapytań, 20 zadań → 22**. `to_response` woła `get_category` per zadanie — N+1 (+ auth, + lista).

```python
@pytest.fixture
def sql_counter(test_engine) -> list[str]:
    statements: list[str] = []
    event.listen(test_engine, "before_cursor_execute",
                 lambda conn, cur, stmt, *_: statements.append(stmt))
    return statements

def test_task_list_query_count_does_not_grow_with_task_count(client, sql_counter) -> None:
    """Perf: liczba zapytań GET /tasks/ nie zależy od liczby zadań."""
    category_id = client.post("/categories/", json={"name": "Praca"}).json()["id"]
    for i in range(20):
        client.post("/tasks/", json={"title": f"T{i}", "category_id": category_id})
    sql_counter.clear()

    client.get("/tasks/")

    assert len(sql_counter) <= 3      # dziś: 22 → RED
```

Prompt: *„Napisz test liczący zapytania SQL dla `GET /tasks/` przy 10 i 20 zadaniach. Test ma pokazać, czy liczba zapytań rośnie z liczbą zadań. Nie poprawiaj kodu.”* Potem decyzja: fix (join / batch `get_categories(ids)`) albo test charakteryzujący `== n + 2`.

---

# Testy wydajności — async fan-out i czas samej suity

**Fan-out** `send_to_users`: 50 socketów po 10 ms każdy → **0,55 s** (sekwencyjne `await`). Z `asyncio.gather` ≈ 0,01 s.

```python
@pytest.mark.perf
async def test_fanout_to_many_sockets_is_concurrent(mocker) -> None:
    manager = ConnectionManager()
    for user_id in range(50):
        manager.register(user_id, mocker.MagicMock(send_json=mocker.AsyncMock(side_effect=lambda m: asyncio.sleep(0.01))))
    started = time.perf_counter()
    await manager.send_to_users(range(50), {"type": "ping"})
    assert time.perf_counter() - started < 0.2      # sekwencyjnie: ~0.55 s → RED
```

Zasady dla asercji czasowych: margines ≥ 3× oczekiwanej wartości, marker `perf` i `-m "not perf"` domyślnie, osobny job w CI. `pytest-benchmark` (nieinstalowany) do mikrobenchmarków, `locust` / `k6` do obciążenia — poza pytest.

**Suita sama w sobie**: `pytest --durations=8` → setup 0,34 s w testach z dwoma użytkownikami: dwa `hash_password` (bcrypt, domyślne 12 rund). 146 testów = 23 s. Propozycja modelu: w testach `mocker.patch("bcrypt.gensalt", return_value=bcrypt.gensalt(rounds=4))` w `conftest.py`. Decyzja: OK, bo to test, nie produkcja; bezpieczeństwo hasha sprawdza osobny test `verify_password`.

---

# Ocena testów od LLM — pytanie nr 1: czy ten test może być czerwony?

Test, który nie umie być czerwony, jest kosztem bez wartości. Sprawdź **zanim** zmergujesz:

| Metoda | Jak |
|---|---|
| uruchom | `pytest tests/test_x.py -q` — model „zapomina” to zrobić, gdy nie każesz |
| zepsuj kod celowo | zakomentuj linię, odwróć warunek → test musi paść; wróć `git checkout` |
| mutmut | `mutmut run` na module — przeżywające mutanty = testy bez zębów |
| pokrycie przed / po | `--cov-report=term-missing`: czy zniknęły linie, które miały zniknąć (`189, 201`, `37-38`) |

Wzorce testów, które **zawsze przechodzą** (szukaj ich w diffie):

```python
assert response.status_code in (200, 201, 404)     # „jeden z”
assert result is not None                            # bez treści
try: assert ...; except AssertionError: pass         # połknięta asercja
with pytest.raises(Exception): ...                   # każdy wyjątek, także literówka
mocker.patch("app.services.task_service.TaskService.create_task")   # mock tego, co testujemy
expected = _build_cache_key(...); assert _build_cache_key(...) == expected   # tautologia
service.suggest_priority("x", None)                  # bez await → coroutine, zero asercji
```

---

# Ocena testów od LLM — checklista review

| Kryterium | Dobrze | Źle |
|---|---|---|
| Nazwa | `test_add_tag_to_missing_task_returns_404` | `test_add_tag_2`, `test_line_189` |
| Docstring | `"""Scenario: ..."""` po polsku, jak sąsiednie | brak albo powtórzenie nazwy |
| Zakres | jeden test = jedno zachowanie, Arrange / Act / Assert | 5 asercji na 5 zachowań |
| Asercje | status + kluczowe pola | porównanie całego JSON-a; pełne zdanie `reason` po polsku |
| Determinizm | daty względne, `_PRIORITY_CACHE` czyszczony, brak zależności od kolejności | `date(2026, 10, 20)`, współdzielony stan między testami |
| Konwencje projektu | `mocker`, fixtures z `conftest.py`, plikowy SQLite | `unittest.mock.patch` z `with`, własny `TestClient(app)` |
| Halucynacje | tylko istniejące fixtures i API | `async_client`, `app.test_client()`, `pytest.mark.anyio` |
| Duplikaty | sprawdzone w całym `tests/` | ten sam scenariusz pod nową nazwą w innym pliku |
| Szybkość | bez `sleep`, bez prawdziwego OpenAI | `time.sleep(1)` „na wszelki wypadek” |

Kruche stringi to pułapka specyficzna dla tego repo: uzasadnienia AI są po polsku i zmieniają się. Asercja `"3 dni" in reason` przeżyje; `reason == "Wysoki priorytet: termin wykonania zadania za 3 dni (2026-10-20)."` nie.

---

# Ocena testów od LLM — proces

Traktuj wygenerowane testy jak **PR od juniora**: czytasz diff, nie ufasz opisowi.

1. **Lista zachowań przed kodem** — oceniasz listę (10 linii), nie 200 linii testów.
2. **Jeden test na turę** przy TDD; przy uzupełnianiu luk — paczka, ale uruchomiona przez model i z wynikiem w rozmowie.
3. **Czerwony test = informacja**, nie problem do „naprawienia” asercją. Zdanie w transkrypcie agenta *„dostosuję asercję do obecnego zachowania”* to sygnał stop: albo bug w kodzie, albo zły test, i to Ty decydujesz.
4. **Drugi przebieg innym promptem**: *„Znajdź w tym diffie testy, które przejdą nawet gdy kod będzie zepsuty”* — ten sam model w roli recenzenta łapie inne rzeczy niż w roli autora. Albo `/code-review`.
5. **`ruff check tests && black tests`** — wygenerowany kod potrafi mieć nieużywane importy i linie > 100 znaków.
6. **Pokrycie i mutanty w CI** (`--cov-fail-under=80`, job `mutation`) pilnują regresji jakości, ale progu nie podnosi model.

Zasada: model generuje szybciej, niż Ty czytasz. Jeśli nie masz czasu przeczytać testu, nie masz czasu go utrzymywać.

---

# Workflow w Claude Code

| Mechanizm | Rola w generowaniu testów |
|---|---|
| `CLAUDE.md` → sekcja *Testing* | konwencje w każdej sesji: `mocker`, plikowy SQLite, `autouse` cache, `asyncio_mode` |
| skill `tdd` | procedura: lista zachowań → jeden czerwony test → minimum kodu; zakaz dopasowywania testu |
| `/backend` (krok 8) | audyt konwencji testowych w diffie: `mocker`, scope fixtures, override `get_ai_service` |
| `settings.json` → `allow: Bash(pytest *)` | agent uruchamia testy bez pytania — nie ma wymówki „nie uruchomiłem” |
| hook `PostToolUse` | po każdej edycji w `tests/` automatycznie `pytest -q -x` |
| subagent `test-reviewer` (haiku, read-only) | drugi przebieg: szuka testów bez zębów, raport ≤ 20 linii |

```json
"hooks": {
  "PostToolUse": [{
    "matcher": "Edit|Write",
    "hooks": [{ "type": "command",
      "command": "jq -r '.tool_input.file_path' | grep -q '/tests/' && cd services/backend && .venv/bin/pytest -q -x 2>&1 | tail -5 || true" }]
  }]
}
```

Hook dostaje JSON na stdin; filtr po ścieżce ogranicza go do plików testów. Agent widzi wynik od razu, w tej samej turze.

---

# Podsumowanie

- **Model dopełnia wzorzec**: pokaż mu funkcję, sąsiednie testy, `conftest.py` i `CLAUDE.md`. Każ mu najpierw wypisać zachowania, potem pisać testy, potem **uruchomić**.
- **Z poziomu funkcji / metody**: funkcje czyste (`_build_cache_key`) i metody z zależnościami jako `MagicMock` (`TaskNotifier`). Testuj przez publiczny interfejs.
- **Uzupełnianie klasy**: analiza gałęzi vs testy, ale w **całym** `tests/`; styl i fixtures klasy; granice (3 / 4 dni) jako pierwsze luki.
- **Brzegowe**: granice są w kodzie (`Field`, `Query`, `<=`, `[:3]`); test po obu stronach; mutanty pokazują, które są potrzebne.
- **Regresyjne**: bug → RED → fix; `xfail(strict)` na znane bugi; charakteryzacja kodu zastanego przed zmianą.
- **Async**: `AsyncMock`, `await`, granica na każde oczekiwanie (sentinel). Testy współbieżności (stampede, fan-out) znajdują realne luki — decyzja, czy to bugi, jest ludzka.
- **Wydajność**: licz zapytania i wywołania, nie sekundy; czas tylko z marginesem i markerem `perf`.
- **Ocena**: czy test może być czerwony? Uruchom, zepsuj kod, mutuj. Czerwony test to informacja, nie asercja do poprawienia.

```bash
cd services/backend && .venv/bin/pytest -q --cov=app --cov-report=term-missing -W error::RuntimeWarning
```

Pytania?
