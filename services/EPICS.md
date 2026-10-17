# Epiki — nowe funkcjonalności

## Epic 4: Historia zmian i komentarze

**Cel:** Pełna audytowalność — śledzenie kto i kiedy zmienił zadanie oraz możliwość dyskusji.

**User Stories:**
- `US-4.1` Jako użytkownik chcę zobaczyć historię zmian zadania (`GET /tasks/{id}/history`)
- `US-4.2` Jako system chcę automatycznie logować każdą zmianę pola (old value → new value)
- `US-4.3` Jako użytkownik chcę dodawać komentarze do zadań (`POST /tasks/{id}/comments`)
- `US-4.4` Jako użytkownik chcę listować komentarze (`GET /tasks/{id}/comments`)

**Techniczne:** nowe modele `TaskHistory` (event sourcing light), `Comment`, hook w `TaskRepository.update()` do zapisu diff
