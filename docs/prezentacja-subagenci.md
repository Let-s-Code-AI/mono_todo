---
marp: true
theme: default
paginate: true
title: Subagenci w Claude Code — e2e-runner w projekcie mono_todo
---

<!-- _class: lead -->

# Subagenci w Claude Code
## Na przykładzie `e2e-runner` w projekcie `mono_todo`

Osobny kontekst, własne narzędzia, tańszy model — do głównej sesji wraca tylko raport

---

# Subagent — co to jest

Plik `.claude/agents/<nazwa>.md`: frontmatter z konfiguracją + system prompt. Główna sesja
deleguje zadanie, agent wykonuje je **we własnym oknie kontekstu** i zwraca jeden komunikat.

```
.claude/
├── agents/
│   └── e2e-runner.md      ← name, description, tools, model + instrukcja
├── skills/
│   └── projekt/SKILL.md
└── settings.json
```

| | `CLAUDE.md` | Skill | Subagent |
|---|---|---|---|
| Kontekst | główna sesja | główna sesja | **własny, osobny** |
| Narzędzia | wszystkie | wszystkie | **wybrane** (np. bez `Edit`) |
| Model | sesji | sesji | **dowolny** (haiku / sonnet / opus) |
| Wynik | — | — | **tylko raport**, logi zostają u agenta |

`description` jest triggerem — tak jak w skillu: pisz *kiedy* użyć, nie tylko *co* robi.

---

# Kiedy subagent się opłaca — a kiedy nie

**Opłaca się, gdy zadanie:**
- produkuje dużo szumu (logi testów, trace, output buildu) — do sesji wraca 20 linii zamiast 2000
- powinno mieć **mniej uprawnień** niż sesja — runner testów nie potrzebuje `Edit`
- jest powtarzalne i tanie dla słabszego modelu — sonnet czyta traceback równie dobrze jak opus
- wymaga stałej wiedzy o pułapkach, której nie chcesz powtarzać w każdym prompcie

**Nie opłaca się, gdy:**
- agent i tak musi przeczytać to samo co sesja — frontend to jeden `App.jsx` (1300 linii), lepszy jest fork
- wbudowany `Explore` lub `Plan` już to robi
- zadanie to trzy wywołania narzędzi — zrób je sam

Koszt ukryty: agent zna tylko to, co dostał w prompcie, a ty widzisz tylko jego raport.

---

# Subagenci dla `mono_todo`

| Agent | Model | Narzędzia | Robi |
|---|---|---|---|
| `backend-tdd` | domyślny | pełne, tylko `services/backend` | implementacja cyklem red → green → refactor |
| **`e2e-runner`** | sonnet | Bash, Read — bez `Edit` | `start.sh` → pytest `-n auto` → trace → raport |
| `contract-checker` | sonnet | read-only | `realtime.py` ↔ `useProjectsSocket`, routery ↔ `api.js` |
| `style-reviewer` | haiku | read-only | `async def`, AI tylko w service, polski UI, paleta Figma |
| `db-migrator` | sonnet | Bash, Read | autogenerate + round-trip upgrade/downgrade na kopii bazy |

Trzy z pięciu są read-only na tańszym modelu — najtańsza i najbezpieczniejsza kategoria.

Czego nie robić: osobnego agenta do frontendu (jeden plik, fork tańszy) ani „plannera epików”
(wbudowany `Plan` + skill `projekt`).

---

# `e2e-runner` — frontmatter

```yaml
---
name: e2e-runner
description: Uruchamia testy E2E (Playwright + pytest) z services/e2e i zwraca TYLKO
  zwięzłe podsumowanie. Użyj po zmianach w App.jsx, api.js, routerach backendu albo
  pages.py / test_*.py, lub gdy użytkownik prosi "odpal e2e", "czy UI dalej działa".
  Sam startuje backend i frontend (bez OPENAI_API_KEY). Nie edytuje żadnych plików.
tools: Bash, Read, Grep, Glob
model: sonnet
---
```

- `tools` bez `Edit` i `Write` — agent fizycznie nie może „poprawić” testu, żeby przeszedł
- `model: sonnet` — czytanie logów i tracebacków nie wymaga najdroższego modelu
- `description` wymienia pliki, po których zmianie warto go odpalić → sesja deleguje sama

---

# `e2e-runner` — procedura

1. **Health check** — `curl -sf localhost:8000/health` i `localhost:5173`. Działa → nie startuj drugiej instancji.
2. **Start bez klucza** — `grep -q '^OPENAI_API_KEY=.' .env` (tylko *czy* jest, nigdy wartość),
   potem `OPENAI_API_KEY= ./start.sh` w tle.
3. **Testy do pliku** — `.venv/bin/pytest -n auto -q -rfExX --tb=short > e2e.log`; do rozmowy trafia `tail -n 40`.
4. **Analiza każdego FAILED** — traceback → ramka z `pages.py` + lokator; screenshot (`Read` na PNG);
   `unzip -p trace.zip trace.trace` → ostatnia akcja i błąd; `trace.network` → statusy HTTP.
5. **Powtórka** `--lf -n 0` — deterministyczny czy flaky.
6. **Sprzątanie** — `kill $(cat .dev-pids)`, tylko gdy to agent startował serwisy.
7. **Raport** ≤ 30 linii według szablonu.

---

# Gotchas wbudowane w agenta

Rzeczy, które inaczej trzeba by powtarzać w każdym prompcie:

| Pułapka | Skutek, gdy o niej zapomnisz |
|---|---|
| backend z `OPENAI_API_KEY` | mock AI nieaktywny → testy terminów i priorytetów losowe |
| użytkownik per worker xdist | „rejestracja nie powiodła się” = backend leży, nie bug testu |
| selektory tylko w `pages.py` | poprawka należy do page objectu, nie do `test_*.py` |
| `xfail(strict=True)` w `test_deadlines.py` | `XPASS` = backend naprawiony, usuń marker — to nie regresja |
| `pilne`, `deadline`, `egzamin` w tytule | mock AI zmienia priorytet, test pada „bez powodu” |
| `--output test-results` | pytest-playwright czyści katalog na starcie — log pisz gdzie indziej |

Każda z nich to kiedyś stracona godzina. W agencie kosztuje jedną linię.

---

# Agent w akcji

Prompt w głównej sesji:

> Zmieniłem etykietę przycisku zapisu w modalu zadania. Odpal e2e.

Co wraca do sesji (zamiast ~1500 linii logu):

```
E2E: 66 passed, 2 failed, 1 xfailed · 71 s · 4 workery
Serwisy: uruchomione przeze mnie i zatrzymane · AI: mock (klucz nieustawiony)
Pełny log: .../scratchpad/e2e.log

FAILED test_tasks.py::TestAddTask::test_add_task_appears_on_list   [deterministyczny]
  Page object: TaskModal.submit_button → get_by_role("button", name=re.compile(r"^(Dodaj zadanie|Zapisz)$"))
  Błąd: TimeoutError 5000 ms — locator nie znaleziony
  Ekran: modal „Nowe zadanie” nadal otwarty, przycisk ma etykietę „Utwórz”
  Trace: ostatnia akcja click; brak requestu POST /tasks/
  Kategoria: nieaktualny selektor
  Artefakty: services/e2e/test-results/.../test-failed-1.png, trace.zip

FAILED test_tasks.py::TestEditTask::test_edit_task_via_modal   [deterministyczny] — ta sama przyczyna
```

Sesja wie od razu: jedna poprawka w `pages.py`, nie dwie w testach.

---

# Podsumowanie

- **Subagent** = osobny kontekst + własne narzędzia + własny model + jeden raport na wyjściu.
- Opłaca się tam, gdzie jest **szum** (logi), potrzeba **mniej uprawnień** albo wystarczy **tańszy model**.
- `e2e-runner`: sonnet, bez `Edit`, zna pułapki projektu — mock AI, użytkownik per worker, selektory w `pages.py`.
- Raport: *który test, który page object, jaki selektor, jaka kategoria* — i nic więcej.
- Nie rób agenta tam, gdzie i tak musi przeczytać cały `App.jsx` — fork jest tańszy.

```
# wywołanie z głównej sesji
> użyj agenta e2e-runner i powiedz, co padło
```
