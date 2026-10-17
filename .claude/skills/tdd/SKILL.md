---
name: tdd
description: Cykl TDD (red → green → refactor) dla tego monorepo. Użyj ZAWSZE, zanim napiszesz kod produkcyjny w services/backend — przy nowym endpoincie, modelu, serwisie, zmianie zachowania lub naprawie buga. Prowadzi krok po kroku: lista zachowań, jeden failujący test, minimalna implementacja, refaktor, z komendami pytest/ruff/black i konwencjami testów z conftest.py.
---

# TDD — red → green → refactor

Zasada nadrzędna: **żadnej linii kodu produkcyjnego bez wcześniej failującego testu.**
Nie „napiszę kod, potem dopiszę testy”. Test jest pierwszy, bo definiuje kontrakt.

---

## 0. Zanim zaczniesz: lista zachowań

Rozbij zadanie na małe, obserwowalne zachowania i zapisz je jako checklistę.
Każda pozycja = jeden przyszły test. Odhaczaj w trakcie pracy.

```
- [ ] POST /projects/ zwraca 201 i tworzy projekt z owner_id = zalogowany
- [ ] POST /projects/ bez tokena → 401
- [ ] POST /projects/{id}/members przez nie-ownera → 403
- [ ] POST /projects/{id}/members z nieznanym emailem → 404
- [ ] POST /projects/{id}/members dla istniejącego członka → 409
```

Kolejność: od najprostszego happy path, potem przypadki brzegowe i błędy.

---

## 1. Cykl — powtarzaj dla każdej pozycji z listy

### RED — jeden failujący test

1. Napisz **jeden** test dla **jednego** zachowania.
2. Uruchom tylko ten test:
   ```bash
   cd services/backend && source .venv/bin/activate
   pytest tests/test_projects_api.py::test_create_project -q
   ```
3. Zobacz czerwień i **sprawdź powód**. Dobry powód: `404 != 201`, `ImportError` nowego
   modułu, `AssertionError` na polu odpowiedzi. Zły powód: literówka, zły fixture, brak
   `.env` (testy odpalaj z katalogu `services/backend`, `Settings` czyta `.env` z cwd).
4. Test, który przechodzi od razu, nic nie weryfikuje — popraw go albo usuń.

### GREEN — najmniejszy kod, który przechodzi

1. Napisz minimum, żeby ten test był zielony. Bez „na przyszłość”, bez dodatkowych pól,
   bez obsługi błędów, których jeszcze nie ma na liście.
2. Hardkod jest OK na tym etapie, jeśli następny test i tak go wymusi do uogólnienia.
3. Uruchom ten test, potem **całą suitę**:
   ```bash
   pytest -q
   ```

### REFACTOR — porządek przy zielonych testach

1. Usuń duplikację, popraw nazwy, przywróć warstwy (`router → service → repository`),
   wyciągnij wspólne fixtures do `conftest.py`.
2. Nie zmieniaj zachowania. Jeśli chcesz nowe zachowanie — to nowa pozycja na liście.
3. Uruchom całą suitę + lint:
   ```bash
   pytest -q && ruff check app tests && black app tests
   ```

Wróć do RED z kolejną pozycją.

---

## 2. Outside-in: od którego testu zacząć

- **Zaczynaj od testu API** przez `TestClient` — to on ustala URL, status i kształt JSON.
  Jeden test API przeciąga przez router, service, repository i model.
- **Unit test serwisu** piszesz tylko, gdy logika biznesowa jest nietrywialna (uprawnienia,
  reguły, fallbacki). Repozytorium podstawiasz przez `mocker.MagicMock()`.
- **Repozytorium** testujesz przez API albo przez fixture `test_db`. Nie piszesz testów SQL
  „dla pokrycia”.
- **Bugfix**: najpierw test reprodukujący błąd (RED), dopiero potem naprawa. Test zostaje
  jako regresja.

---

## 3. Konwencje testów w tym projekcie

Fixtures z `tests/conftest.py` (wszystkie `function`-scoped, świeża baza SQLite na test):

| Fixture | Co daje |
|---|---|
| `client` | `TestClient` zalogowany jako `test_user` |
| `admin_client` | `TestClient` zalogowany jako `test_admin` |
| `unauth_client` | `TestClient` bez tokena |
| `test_db` | `Session` do bezpośredniego seedowania danych |
| `test_user`, `test_admin` | obiekty `User` w bazie |

Zasady:
- Nazwa: `test_<akcja>_<warunek>_<wynik>`, np. `test_add_member_as_non_owner_returns_403`.
- Docstring jednolinijkowy w stylu `"""Scenario: ..."""` (jak w `test_categories_tags.py`).
- Układ Arrange / Act / Assert rozdzielony pustą linią.
- Asercje: status code + kluczowe pola odpowiedzi. Nie porównuj całego JSON-a.
- Potrzebujesz drugiego użytkownika albo klienta zalogowanego jako ktoś inny → dodaj
  fixture do `conftest.py`, nie kopiuj kodu między plikami testów.
- Mockowanie wyłącznie przez `mocker` (pytest-mock). AI zawsze jako `MockAIPriorityService`.
- Test dotykający AI → `autouse` fixture czyszczący `_PRIORITY_CACHE`.
- `asyncio_mode = auto` — testy `async def` nie potrzebują markera.

---

## 4. Czego nie robić

- Implementacja przed testem, „testy dopiszę później”.
- Więcej niż jeden czerwony test naraz.
- Pominięcie uruchomienia testu w fazie RED — musisz **zobaczyć** czerwień.
- Dopasowywanie testu do implementacji. Jeśli test był błędny, powiedz to wprost
  i popraw test w osobnym kroku.
- Zostawianie czerwonej suity między cyklami lub w commicie.
- Refaktor i nowe zachowanie w jednym kroku.

---

## 5. Frontend i E2E

Frontend (`services/frontend`) nie ma testów jednostkowych. Zachowanie UI pokrywasz
scenariuszem E2E w `services/selenium` (Playwright) jako zewnętrzną pętlą:

1. Napisz scenariusz E2E przed zmianą UI (będzie czerwony).
2. Zaimplementuj UI w `App.jsx` + `api.js`.
3. Uruchom `./start.sh`, potem `cd services/selenium && pytest test_<modul>.py`.

---

## 6. Jak raportować użytkownikowi

Po każdym cyklu lub na końcu pracy pokaż przebieg, nie tylko wynik:
- który test był czerwony i z jakiego powodu,
- co minimalnie go zazieleniło,
- co zrefaktorowano,
- wynik pełnej suity (`N passed`) i lintów.
