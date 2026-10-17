---
marp: true
theme: default
paginate: true
title: Analiza kodu zastanego i planowanie zmian z udziałem LLM
---

<!-- _class: lead -->

# Analiza kodu zastanego i planowanie zmian z udziałem LLM
## Claude Code na przykładzie monorepo `mono_todo`

Przegląd nieznanego repo → analiza klas i zależności → refaktoryzacje i luki w testach

---

# Agenda

1. Monorepo: czym jest i jak wygląda `mono_todo`
2. Kontekst agenta: co w nim siedzi, `/context`, `/clear`, `/compact`, `/rewind`
3. Tryby pracy: default, acceptEdits, plan, auto
4. Modele: który do jakiego zadania
5. Przegląd nieznanego repozytorium przy pomocy AI
6. Prompty do analizy klas, funkcji i zależności
7. Wnioskowanie o refaktoryzacjach
8. Od analizy do planu zmian
9. Luki w testach i `pytest --cov`

---

# Monorepo — czym jest

Jedno repozytorium, wiele serwisów lub pakietów, wspólna historia git.

| | Monorepo | Multirepo |
|---|---|---|
| Zmiana przez kilka serwisów | jeden PR, jeden commit | N PR-ów, koordynacja wersji |
| Konwencje i tooling | jeden `CLAUDE.md`, jedno CI | kopiowane między repozytoriami |
| Rozmiar, czas klonowania | rośnie z każdym serwisem | małe repo |
| Widoczność zależności | pełna: grep po całym kodzie | tylko przez opublikowane pakiety |

Przykłady: Google, Meta; Nx / Turborepo w JS; `uv workspaces` w Pythonie.

Dla LLM monorepo to **jeden kontekst na całą aplikację**: agent widzi backend, frontend i testy E2E naraz, więc może prześledzić przepływ od kliknięcia w UI do zapytania SQL. Cena: łatwiej wciągnąć do kontekstu pół repo, gdy nie zawęzisz zakresu.

---

# `mono_todo` — nasze monorepo

```
mono_todo/
├── CLAUDE.md, .claude/skills/projekt/   ← reguły wspólne dla całego repo
├── services/
│   ├── backend/   FastAPI + SQLModel + SQLite   (app/ ~2 600 LOC, tests/ ~2 400 LOC)
│   ├── frontend/  React 18 + Vite, cały UI w jednym App.jsx
│   ├── e2e/       pytest + Playwright, page objects w pages.py
│   └── mcp_tool/  serwer MCP
├── start.sh / install.sh
└── docs/
```

Zbudowane z trzech osobnych repozytoriów przez `git subtree`:

```bash
git subtree add  --prefix=services/backend todo_ai_worshop main --squash
git subtree pull --prefix=services/backend todo_ai_worshop main --squash
```

Historia zaczyna się od commitów "Squashed 'services/backend/' content…". Tak wygląda **kod zastany**: przyszedł z zewnątrz, z historią spłaszczoną do jednego commita na serwis, bez kontekstu decyzji.

---

# Kontekst agenta — co w nim siedzi

Okno kontekstu to wszystko, co model "widzi" w danej turze. Wypełniają je:

| Składnik | Kiedy trafia do kontekstu | Jak kontrolujesz |
|---|---|---|
| System prompt, definicje narzędzi | zawsze | — |
| `CLAUDE.md` (user, repo, katalog) | start sesji; katalogowy, gdy agent dotknie pliku w nim | krótkie reguły, nie dokumentacja |
| Skille | gdy pasuje `description` lub `/nazwa` | opis skilla = trigger |
| Pliki `@ścieżka`, wyniki `Read` / `Grep` / `Bash` | każde użycie narzędzia | zakres promptu, subagenty |
| Historia rozmowy | rośnie z każdą turą | `/clear`, `/compact`, `/rewind` |

`/context` — kolorowa siatka: ile tokenów zajmuje każda kategoria, które `CLAUDE.md` się załadowały, co puchnie. `/cost` — ile sesja kosztuje.

Zasada: **kontekst to budżet uwagi, nie dysk**. Nieistotny plik z trzech tur wstecz nadal odciąga uwagę modelu. Analiza `App.jsx` w tej samej sesji, co refaktor repozytorium SQL, pogarsza obie.

---

# `/clear`, `/compact`, `/rewind`

| | `/clear` | `/compact [instrukcja]` | `/rewind` (Esc Esc) |
|---|---|---|---|
| Co robi | nowa rozmowa, pusty kontekst | zastępuje historię streszczeniem | cofa rozmowę i/lub pliki do punktu |
| Zostaje | `CLAUDE.md`, skille, auto-memory | j.w. + streszczenie | wszystko sprzed punktu |
| Kiedy | nowe, niezwiązane zadanie | to samo zadanie, kontekst zapchany wynikami narzędzi | agent poszedł w złą stronę |

```
/compact zachowaj listę problemów znalezionych w task_service.py i plan zmian; pomiń wyniki grep
```

- Auto-compact uruchamia się sam przy granicy kontekstu (`/autocompact 200k` obniża próg). Nie czekaj na niego: zrób `/compact` z instrukcją **po zamknięciu etapu**, gdy wiesz, co jest ważne.
- Po `/compact` `CLAUDE.md` jest doczytywany ponownie. Warto mieć w nim linię: *"When compacting, always preserve the list of modified files and test commands."*
- Rozmowa po `/clear` nie ginie: `/resume` ją przywraca.
- Plan i ustalenia zapisuj **do pliku** (`docs/PLAN.md`), nie w czacie. Plik przeżyje `/clear` i wróci przez `@docs/PLAN.md`.

---

# Tryby pracy (permission modes)

Przełączanie: `Shift+Tab` (default → acceptEdits → plan → auto), `/plan [opis]`, `claude --permission-mode plan`. Tryb domyślny projektu: `permissions.defaultMode` w `settings.json`.

| Tryb | Co agent robi bez pytania | Do czego |
|---|---|---|
| **default** | tylko czyta; każda edycja i komenda czeka na zgodę | pierwsze sesje w obcym repo |
| **acceptEdits** | edycje plików i proste komendy FS (`mkdir`, `mv`, `cp`) | implementacja wg zatwierdzonego planu |
| **plan** | czyta, grepuje, komendy tylko do odczytu; **zero edycji** | przegląd kodu zastanego, projektowanie zmiany |
| **auto** | wszystko, ale osobny model-klasyfikator ocenia każdą akcję | dłuższe zadania z gotowym planem |
| **bypassPermissions** / **dontAsk** | wszystko / nic, co wymagałoby pytania | tylko kontener lub CI |

Plan mode w praktyce:
- agent kończy **planem w rozmowie**, nie zmianą; wybierasz: "tak, w auto", "tak, zatwierdzam edycje ręcznie", "planuj dalej"
- `Ctrl+G` otwiera plan w edytorze: poprawiasz, zanim ruszy implementacja
- `Shift+Tab` wychodzi z plan mode bez zatwierdzania

Przy kodzie zastanym plan mode wymusza rozdzielenie **"co trzeba zrobić"** od **"robię"**. Nie znasz jeszcze skutków zmiany.

---

# Explore → Plan → Code → Commit

```
1. Explore   plan mode    "Przeczytaj services/backend/app. Nie pisz kodu. Opisz warstwy,
                           łańcuch DI i gdzie żyje logika priorytetów."
2. Plan      plan mode    "Zaplanuj wyciągnięcie reguły ai_override do jednej funkcji.
                           Pliki do zmiany, ryzyka, testy, które muszą przejść bez zmian."
                           → Ctrl+G: poprawiasz plan; zapis do docs/PLAN.md
3. Code      acceptEdits  "Zrealizuj krok 1 z @docs/PLAN.md zgodnie ze skillem tdd."
4. Commit    default      "pytest -q && ruff check app tests; commit z opisem zmiany"
```

Między etapami: `/compact` z instrukcją albo `/clear` + `@docs/PLAN.md`.

Z dokumentacji: planowanie to narzut. **Pomiń je, gdy diff da się opisać jednym zdaniem.** Kod zastany rzadko spełnia ten warunek.

Antywzorzec: "popraw to" w acceptEdits na kodzie, którego nikt jeszcze nie przeczytał. Agent zmieni osiem plików, a Ty nie wiesz, który z nich był istotny.

---

# Modele — który do jakiego zadania

| Model | $/1M tok. (in / out) | Mocne strony | W analizie kodu zastanego |
|---|---|---|---|
| **Haiku 5.5** | 0.10 / 0.50 | szybkość, koszt | subagenty szukające po repo, "gdzie jest X", streszczenia wielu plików |
| **Sonnet 5.5** | 2 / 10 | codzienne kodowanie | implementacja wg planu, pisanie testów, refaktor w jednym module |
| **Opus 5.5** | 4 / 20 | rozumowanie, długie zadania | **domyślny**: plan, analiza architektury, trudne bugi, review |
| **Fable 5.1** | 10 / 50 | najtrudniejsze problemy | wielogodzinne zadania agentowe, analiza całego repo naraz |

- `/model` w sesji, `claude --model sonnet`; aliasy: `opus`, `sonnet`, `haiku`, `fable`, `opusplan`.
- **`opusplan`**: Opus w plan mode, Sonnet w implementacji. Dobry domyślny układ na warsztaty.
- Subagent ma własny model i tryb: `model: haiku`, `permissionMode: plan` we frontmatter `.claude/agents/explorer.md`.
- `/effort low|medium|high|xhigh|max`: na modelach 5.5 domyślnie `medium`. Analiza i plan: `high`; kroki wg planu: `medium`.
- `/fast`: ten sam Opus, do 2,5× szybszy output, ok. 2× cena. Do pętli "popraw → test → popraw".

Zasada: **drogi model na decyzje, tani na zbieranie faktów.** Zła decyzja architektoniczna kosztuje więcej niż dwadzieścia promptów do Opusa.

---

# Przegląd nieznanego repozytorium — krok 1: mapa

Zanim zapytasz o szczegóły, zbuduj mapę. Plan mode, Opus.

```
Jestem nowy w tym repo. Nie zmieniaj plików. Daj mi mapę:
1. Co robi aplikacja (3 zdania).
2. Serwisy w services/ i jak się komunikują (HTTP, WebSocket, pliki).
3. Dla backendu: punkty wejścia, warstwy, łańcuch dependency injection.
4. Jak uruchomić i jak przetestować — komendy z plików repo, nie z pamięci.
5. 5 rzeczy, które Cię zaskoczyły albo wyglądają nietypowo.
Lista, każdy punkt z odnośnikiem plik:linia.
```

Dlaczego tak:
- **"Nie zmieniaj plików"** + plan mode: podwójne zabezpieczenie.
- **"z plików, nie z pamięci"**: model zna FastAPI, ale nie zna *tego* `start.sh`.
- **"co Cię zaskoczyło"**: najtańszy sposób na znalezienie długu technicznego.
- **`plik:linia`**: odpowiedź da się zweryfikować, a nie tylko przeczytać.

Alternatywa na start: `/init` wygeneruje `CLAUDE.md`. To opis dla agenta, nie dla Ciebie. Przeczytaj go krytycznie, zanim trafi do repo.

---

# Przykłady promptów — przegląd repo

**Przepływ żądania (end-to-end):**
```
Prześledź, co dzieje się od kliknięcia "Dodaj zadanie" w services/frontend/src/App.jsx
do zapisu w SQLite. Wypisz każdy plik i funkcję po drodze, w kolejności wywołań.
```

**Konwencje, których nie ma w dokumentacji:**
```
Porównaj routery w app/api/routers/. Jakie konwencje są wspólne (nazewnictwo, obsługa błędów,
auth), a gdzie któryś router odstaje? Pokaż odstępstwa jako listę plik:linia.
```

**Historia zamiast dokumentacji:**
```
Przeczytaj git log -p dla app/services/ai_priority_service.py. Jakie decyzje projektowe widać
w zmianach? Co było poprawiane więcej niż raz?
```

**Delegowanie szukania (tani model, osobny kontekst):**
```
Użyj subagenta Explore: znajdź wszystkie miejsca, gdzie kod czyta task.tags. Zwróć tylko listę
plik:linia z jednym zdaniem kontekstu.
```

---

# Prompt do analizy klasy — `TaskService`

```
Przeanalizuj klasę TaskService w @app/services/task_service.py. Nie zmieniaj kodu.
Dla każdej metody: odpowiedzialność (1 zdanie), zależności (co woła), efekty uboczne (DB, AI).
Potem: które metody mają więcej niż jedną odpowiedzialność, gdzie powtarza się logika,
co zależy od owner_id, a co nie. Tabela + lista pytań do autora kodu.
```

Co dostajemy (skrót, zweryfikowany w kodzie):

| Metoda | Zależności | Uwaga modelu |
|---|---|---|
| `create_task` | `ai_service.suggest_priority`, `repository.create` | reguła `ai_override` liczona inline (`:64`) |
| `reanalyze_priority` | j.w. + `repository.get_category` | **ta sama reguła, inny wynik** (`:233`) |
| `to_response` | `repository.get_category` | zapytanie DB **per zadanie** |
| `update_task` | `setattr` po `model_dump(exclude_unset=True)` | pola ogranicza tylko schemat `TaskUpdate` |
| `get_stats` | `count_*` | jedyna metoda bez `owner_id`: celowo (admin)? |

Lista pytań do autora, którą generuje model, to gotowa **lista ryzyk** do planu zmian.

---

# Analiza funkcji i zależności

**Graf importów i reguła warstw:**
```
Narysuj graf zależności modułów w app/ (kto importuje kogo). Reguła z CLAUDE.md:
routers → services → db; schemas i core mogą wszędzie. Które moduły łamią regułę?
```

**Jedna funkcja, wszystkie wywołania:**
```
Kto wywołuje TaskRepository.get_by_id? Dla każdego wywołania: czy przekazuje owner_id?
Które wywołanie bez owner_id jest celowe (admin), a które wygląda na przeoczenie?
```

**Kontrakt, nie implementacja:**
```
Jaki jest kontrakt WebSocket /ws/projects? Wypisz typy komend z app/schemas/realtime.py,
kto je wysyła w App.jsx i co backend odsyła. Zaznacz komendy, których frontend nie używa.
```

Technika: pytaj o **relacje** (kto woła, kto importuje, kto wysyła), nie "co robi ten plik". Relacji nie widać w pojedynczym pliku, a to one psują się przy zmianie.

---

# Anatomia dobrego promptu analitycznego

```
[CEL]      Chcę wyciągnąć regułę ai_override do jednej funkcji.
[ZAKRES]   @app/services/task_service.py @tests/test_tasks_api.py — tylko to.
[ZAKAZ]    Nie zmieniaj plików. Nie proponuj jeszcze kodu.
[FORMAT]   Tabela: miejsce | obecne zachowanie | ryzyko zmiany | test, który to pokrywa.
[DOWÓD]    Każdy wiersz z odnośnikiem plik:linia.
[GRANICA]  Jeśli czegoś nie widać w kodzie, napisz "nie wiem", nie zgaduj.
```

| Składnik | Bez niego |
|---|---|
| Cel | model opisuje wszystko, Ty szukasz igły |
| Zakres (`@pliki`) | agent czyta pół repo, kontekst pełny po jednej turze |
| Zakaz zmian | "pomocna" edycja, zanim zrozumiałeś problem |
| Format | proza zamiast listy do odhaczenia |
| Dowód `plik:linia` | halucynacji nie da się odróżnić od faktu |
| Granica | pewnie brzmiąca, zmyślona odpowiedź |

---

# Wnioskowanie o refaktoryzacjach

```
Na podstawie analizy TaskService i routera tasks.py zaproponuj refaktoryzacje. Dla każdej:
problem, propozycja, testy, które muszą przejść bez zmian, ryzyko (niskie/średnie/wysokie),
czy mieści się w jednym PR. Posortuj od najtańszej. Nie pisz kodu.
```

Co wyszło dla `mono_todo` (każdy punkt potwierdzony w kodzie):

| # | Problem | Propozycja | Ryzyko |
|---|---|---|---|
| 1 | `_get_category_name` w `routers/tasks.py:86` nigdy nie wywołana | usunąć martwy kod | zerowe |
| 2 | Reguła `ai_override` w dwóch miejscach, w `reanalyze_priority` daje inny wynik | jedna funkcja `resolve_priority(user, ai)` | niskie |
| 3 | Router robi `session.get(Category)` (`tasks.py:123, 309`) z pominięciem serwisu i repo | przenieść do `CategoryService`, router zna tylko serwis | niskie |
| 4 | `to_response` woła `get_category` per zadanie; listy w `tasks.py:187, 216, 255` → N+1 | relacja w SQLModel albo batch `get_categories(ids)` | średnie |

Rola człowieka: **odrzucać**, nie tylko zatwierdzać. Nr 4 może nie być problemem przy stu zadaniach na użytkownika. Model nie zna skali produkcji.

---

# Od analizy do planu zmian

Plan mode. Model zna kod z poprzednich tur albo dostał streszczenie przez `/compact`.

```
Zaplanuj refaktoryzację nr 2 (ai_override). Plan ma zawierać:
- kroki w kolejności, każdy ≤ 1 plik, każdy zostawia zielone testy
- najpierw test charakteryzujący obecne zachowanie, potem zmiana
- co sprawdzić ręcznie, czego nie pokryją testy
- jak cofnąć, jeśli coś pójdzie nie tak
Zapisz plan do docs/PLAN.md. Nie zaczynaj implementacji.
```

Checklista przeglądu planu (człowiek, `Ctrl+G`):
- Czy każdy krok ma **test, który go chroni**? Jeśli nie, krok jest za duży.
- Czy plan dotyka plików spoza zakresu analizy? Jeśli tak, wróć do analizy.
- Czy model coś założył o produkcji (skala, dane, użytkownicy)? Sprawdź założenia.
- Czy plan da się wykonać w **innej sesji** tylko na podstawie pliku? Jeśli nie, dopisz kontekst.

Dopiero teraz: `/clear`, `acceptEdits`, `"Zrealizuj krok 1 z @docs/PLAN.md"`.

---

# Luki w testach — pytanie do modelu

```
Porównaj @app/services/task_service.py z @tests/. Dla każdej publicznej metody: który test ją
pokrywa (nazwa), a jeśli żaden, jaki scenariusz brakuje. Osobno wypisz ścieżki błędów
(None, 404, puste listy), których nie ma w testach.
```

Co model znajduje w `mono_todo` (potwierdzone przez `pytest --cov`):

| Luka | Gdzie | Dlaczego ważna |
|---|---|---|
| `add_tag` / `remove_tag` na nieistniejącym zadaniu | `task_service.py:189, 201`; router `:343, :371` | ścieżka 404 nigdy nie wykonana |
| `GET /tasks/stats` (admin) | `task_service.py:238-240`; router `:230` | cały endpoint bez testu |
| `PATCH` z nieistniejącą kategorią | `routers/tasks.py:311` | 404 obsłużone, ale nie sprawdzone |
| filtr `?priority=` | `repository.py:183` | gałąź `if priority` nigdy nie wykonana |

Model widzi luki **semantycznie** (brak scenariusza), coverage widzi je **mechanicznie** (linia nie wykonana). Potrzebujesz obu.

---

# `pytest --cov` — pokrycie testami

```bash
cd services/backend && source .venv/bin/activate
pytest --cov=app --cov-report=term-missing          # tabela + numery brakujących linii
pytest --cov=app --cov-report=html && open htmlcov/index.html
pytest --cov=app --cov-branch --cov-fail-under=90    # gałęzie if/else + próg w CI
```

Stan `mono_todo` dziś: **141 testów, 96% pokrycia, 40 niewykonanych linii**.

```
Name                                  Stmts   Miss  Cover   Missing
app/services/task_service.py             78      5    94%   189, 201, 238-240
app/api/routers/tasks.py                112      8    93%   88-91, 230, 311, 343, 371
app/db/repository.py                    139      5    96%   116, 183, 232, 236, 242
TOTAL                                  1046     40    96%
```

Czego pokrycie **nie** mówi:
- linia wykonana ≠ zachowanie sprawdzone; test bez `assert` też "pokrywa"
- 100% na `routers/` bez asercji o treści odpowiedzi to iluzja
- stąd `mutmut` w `pyproject.toml`: mutuje kod i sprawdza, czy testy to zauważą

---

# Coverage + LLM — zamknięcie pętli

```
Oto raport pytest --cov --cov-report=term-missing: [wklej tabelę].
Dla każdej brakującej linii w app/services/ i app/api/: jaki scenariusz biznesowy ją wykonuje?
Zaproponuj nazwę testu i Arrange/Act/Assert. Nie pisz testów "pod linię": jeśli linia
nie odpowiada żadnemu zachowaniu, zaproponuj jej usunięcie.
```

| Dobrze | Źle |
|---|---|
| nazwa od zachowania: `test_add_tag_to_missing_task_returns_404` | `test_line_189` |
| brak linii → pytanie "czy ten kod jest potrzebny?" (`_get_category_name`) | test do martwego kodu |
| `/compact`, potem skill `tdd`: czerwony test → zielony | dwanaście testów w jednej turze bez uruchomienia |
| próg `--cov-fail-under` w CI pilnuje regresji | pogoń za 100% kosztem czytelności |

W CI (`.github/`): `pytest --cov=app --cov-fail-under=95` + raport jako artefakt. Model nie podnosi progu. Człowiek decyduje, co jest warte testowania.

---

# Podsumowanie

**Kontekst**: budżet uwagi. `/context` pokazuje, `/compact` z instrukcją kompresuje, `/clear` zeruje, `/rewind` cofa. Ustalenia do pliku, nie do czatu.

**Tryby**: plan mode do analizy i projektowania, acceptEdits do realizacji planu, auto tam, gdzie plan jest gotowy, a skutki łatwo cofnąć.

**Modele**: Opus na decyzje i plany, Sonnet na implementację, Haiku na subagenty zbierające fakty, Fable na zadania, które przerastają Opusa. `opusplan` łączy dwa pierwsze.

**Przegląd kodu zastanego**: mapa → relacje (kto woła, kto importuje) → klasa po klasie. Zawsze: cel, zakres, zakaz zmian, format, `plik:linia`.

**Refaktoryzacje i testy**: model proponuje i sortuje po koszcie, człowiek odrzuca. `pytest --cov` daje fakty, model nadaje im znaczenie.

```bash
claude --permission-mode plan --model opusplan
> Jestem nowy w tym repo. Nie zmieniaj plików. Daj mi mapę...
```

Pytania?
