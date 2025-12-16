# Code Review - Branch TRAN-33-book-endpoints-logic

**Data:** 2025-12-10  
**Reviewer:** AI Assistant  
**Bazowy branch:** develop

---

## Podsumowanie

| Kategoria | Ilość |
|-----------|-------|
| 🚫 BLOCKER | 6 |
| 💡 SUGGESTION | 4 |
| 📝 NIT | 4 |

---

## 🚫 BLOCKER - Muszą być poprawione przed mergem

### 1. Nazwa klasy Query vs Command (CQS violation)
**Plik:** `application/queries/get_user_books.py`

Klasa `GetUserBooksCommand` powinna nazywać się `GetUserBooksQuery`. Jest to operacja odczytu, nie zapisu - łamie konwencję Command/Query Separation.

**Rekomendacja:** Zmień nazwę na `GetUserBooksQuery`.

---

### 2. Repozytoria rzucają wyjątki zamiast zwracać None
**Pliki:**
- `infrastructure/db/repositories/file_repo_sqlalchemy.py`
- `infrastructure/db/repositories/user_repo_sqlalchemy.py`
- `infrastructure/db/repositories/book_repo_sqlalchemy.py`

Metody `get()` i `get_by_email()` rzucają `ValueError` gdy nie znajdą rekordu, mimo że sygnatura mówi `Optional[...]`. To łamie kontrakt portu i powoduje:
- Duplikację obsługi błędów
- Niemożliwość użycia `if repo.get(id):` w logice biznesowej
- **BUG w CreateUserCommand:** `if self.repo.get_by_email(dto.email)` nigdy nie zadziała poprawnie - zamiast zwrócić `None`, metoda rzuci wyjątek

**Rekomendacja:** Metody `get*()` powinny zwracać `None` gdy nie znajdą. Rzucanie wyjątków powinno być w warstwie application (commands/queries).

---

### 3. Brak return w endpoint create_user
**Plik:** `api/http/controllers/users_controller.py`

```python
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(dto: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        CreateUserCommand(user_repo(db)).run(dto)  # Brak return!
    except ValueError as e:
        raise HTTPException(...)
```

Endpoint deklaruje `response_model=UserResponse`, ale nie zwraca niczego.

**Rekomendacja:** Dodaj `return` przed wywołaniem command.

---

### 4. Błędna ścieżka w endpoint list_files_for_owner
**Plik:** `api/http/controllers/file_controller.py`

```python
@router.get("/by-owner/{book_id}", ...)  # Ścieżka ma {book_id}
def list_files_for_owner(owner_id: str, ...):  # Funkcja przyjmuje owner_id
```

Ścieżka URL zawiera `{book_id}`, ale parametr funkcji to `owner_id`.

**Rekomendacja:** Zmień ścieżkę na `/by-owner/{owner_id}`.

---

### 5. Błędna ścieżka w endpoint list_user_books
**Plik:** `api/http/controllers/users_controller.py`

```python
@router.get("/{user_id}/books", ...)  # Ścieżka ma {user_id}
def list_user_books(owner_id: str, ...):  # Funkcja przyjmuje owner_id
```

Parametr funkcji nie odpowiada zmiennej w ścieżce.

**Rekomendacja:** Zmień parametr na `user_id`.

---

## 💡 SUGGESTION - Zalecane do poprawy

### 1. Nieużywana zmienna content w upload_file
**Plik:** `api/http/controllers/file_controller.py`

```python
async def upload_file(...):
    content = await file.read()  # Odczytane ale nigdzie nie użyte
    return UploadFileCommand(file_repo(db)).run(dto)
```

Plik jest odczytywany, ale content nie jest przekazywany do command ani zapisywany.

**Rekomendacja:** Zaimplementuj faktyczny zapis pliku lub usuń nieużywany kod.

---

### 2. Literówka w enum FileKind
**Plik:** `domain/value_objects/file_kind.py`

`TRANSALTED_MARKDOWN` powinno być `TRANSLATED_MARKDOWN`.

**Uwaga:** Zmiana wymaga migracji danych w bazie, jeśli wartość jest już używana.

---

### 3. Brak walidacji pustego name w User.change_name()
**Plik:** `domain/entities/user.py`

Metoda `change_name()` nie sprawdza czy `new_name` jest `None`, co spowoduje `AttributeError` przy wywołaniu `.strip()` na `None`.

**Rekomendacja:** Dodaj walidację lub obsługę `None`.

---

### 4. FileRepository łączy dwie odpowiedzialności
**Plik:** `domain/ports/file_repository.py`

Port łączy operacje bazodanowe (`add`, `get`, `update`, `delete`) z operacjami na systemie plików (`save`, `open`). To łamie SRP.

**Rekomendacja:** Rozważ podział na `FileMetadataRepository` i `FileStoragePort`.

---

## 📝 NIT - Drobne uwagi

### 1. Brak type hints
**Plik:** `domain/entities/user.py`

```python
def change_email(self, new_email) -> None:  # Brak: new_email: str
def change_name(self, new_name) -> None:    # Brak: new_name: str
```

---

### 2. Literówki w komunikatach błędów
**Plik:** `domain/errors.py`

- `"Must be EXTRACTED before TRANSALTED"` → `TRANSLATED`
- `"Must be TRANSLATED before APPLIED"` → powinno być `"Must be REVIEWED before APPLIED"`

---

### 3. Niespójne formatowanie
**Plik:** `domain/value_objects/file_kind.py`

```python
MARKDOWN ="markdown"  # Brak spacji przed =
XLSX = "xlsx"         # Spacja przed =
```

---

### 4. Puste implementacje metod w repozytorium
**Plik:** `infrastructure/db/repositories/file_repo_sqlalchemy.py`

```python
def save(self, destination_name: str) -> None:
    pass

def open(self, path: str) -> None:
    pass
```

Metody z pustą implementacją - albo zaimplementuj, albo oznacz jako `NotImplementedError`.

---

## ✅ PRAISE - Co jest dobrze zrobione

1. **Architektura warstwowa** - Poprawny podział na domain, application, infrastructure, api
2. **Encje z logiką biznesową** - `Book`, `File`, `Chapter` zawierają metody biznesowe, nie są anemiczne
3. **Porty jako Protocol** - Abstrakcje repozytoriów są dobrze zdefiniowane
4. **Separation of concerns** - Commands i Queries są oddzielone
5. **Testy** - Istnieją testy jednostkowe i integracyjne
6. **DTOs** - Poprawne użycie DTO do transferu danych między warstwami
7. **Value Objects** - Właściwe użycie dla FileKind, QuoteType, ChapterContent
8. **Centralizacja błędów** - Klasy błędów w `domain/errors.py`

---

## Akcje do podjęcia (priorytet)

### Przed mergem (BLOCKER):
1. [ ] Zmień nazwę `GetUserBooksCommand` → `GetUserBooksQuery`
2. [ ] Popraw repozytoria - `get()` powinno zwracać `None`, nie rzucać wyjątek
3. [ ] Dodaj `return` w endpoint `create_user`
4. [ ] Popraw ścieżkę `/by-owner/{book_id}` → `/by-owner/{owner_id}`
5. [ ] Popraw parametr `owner_id` → `user_id` w `list_user_books`

### Po mergu (SUGGESTION/NIT):
6. [ ] Zaimplementuj faktyczny upload pliku lub usuń nieużywany kod
7. [ ] Popraw literówkę `TRANSALTED` → `TRANSLATED` (z migracją)
8. [ ] Dodaj type hints do metod w User
9. [ ] Popraw literówki w komunikatach błędów
10. [ ] Rozważ podział FileRepository na dwa porty

---

*Review wykonane zgodnie z wytycznymi z `CODE_REVIEW_GUIDELINES.md`*

