# Code Review - Branch TRAN-7-tests-data-base

**Data:** 2025-01-20  
**Reviewer:** AI Assistant  
**Bazowy branch:** develop  
**Typ zmian:** Testy + refaktoring encji domenowych

---

## Podsumowanie

| Kategoria | Ilość |
|-----------|-------|
| 🚨 BLOCKER | 2 |
| 🚩 MAJOR | 3 |
| 💡 SUGGESTION | 5 |
| 📝 NIT | 4 |
| ✅ PRAISE | 8 |

---

## 🚨 BLOCKER - Muszą być poprawione przed mergem

### 1. Brak walidacji None w User.change_name()
**Plik:** `backend/src/app/domain/entities/user.py:16`  
**Linia:** 16

```python
def change_name(self, new_name) -> None:
    self.name = new_name.strip()  # ❌ AttributeError jeśli new_name = None
```

**Problem:** Metoda nie sprawdza czy `new_name` jest `None`. Wywołanie `None.strip()` spowoduje `AttributeError`.

**Rekomendacja:**
```python
def change_name(self, new_name: Optional[str]) -> None:
    if new_name is None:
        self.name = None
        return
    self.name = new_name.strip() if new_name.strip() else None
```

**Priorytet:** 🚨 CRITICAL - może powodować runtime error

---

### 2. Brak type hints w metodach User
**Plik:** `backend/src/app/domain/entities/user.py:11,16`  
**Linie:** 11, 16

```python
def change_email(self, new_email) -> None:  # ❌ Brak: new_email: str
def change_name(self, new_name) -> None:    # ❌ Brak: new_name: Optional[str]
```

**Problem:** Brak type hints utrudnia:
- Wykrywanie błędów przez mypy/pyright
- Autocomplete w IDE
- Zrozumienie API przez innych developerów

**Rekomendacja:**
```python
def change_email(self, new_email: str) -> None:
    ...

def change_name(self, new_name: Optional[str]) -> None:
    ...
```

**Priorytet:** 🚨 HIGH - standard projektu wymaga type hints

---

## 🚩 MAJOR - Poważne problemy do poprawy

### 1. Duplikacja kodu book = book w testach
**Plik:** `tests/unit/test_book_entity.py`  
**Linie:** 21, 27, 33, 39, 49

```python
def test_book_version_increments_on_changes(book):
    book = book  # ❌ Niepotrzebne przypisanie
    version = book.version
    ...
```

**Problem:** W każdym teście jest `book = book` co jest:
- Niepotrzebne (fixture już dostarcza book)
- Mylące (wygląda jak błąd)
- Redundantne

**Rekomendacja:** Usuń wszystkie `book = book`:
```python
def test_book_version_increments_on_changes(book):
    version = book.version  # Bezpośrednio użyj fixture
    book.rename_title("New Title")
    ...
```

**Priorytet:** 🚩 MEDIUM - nie wpływa na działanie, ale obniża jakość kodu

---

### 2. Brak testów dla edge cases w Chapter
**Plik:** `tests/unit/test_chapter_entity.py`

**Problem:** Brakuje testów dla:
- `set_parent()` z `parent_id == self.id` (powinien rzucić ValueError)
- `rename_title()` z pustym stringiem
- `is_subchapter()` dla różnych scenariuszy

**Rekomendacja:** Dodaj testy:
```python
def test_chapter_cannot_be_its_own_parent():
    chapter = Chapter(id="c1", book_id="b1", chapter_number=1, title="Title")
    with pytest.raises(ValueError, match="cannot be its own parent"):
        chapter.set_parent("c1")

def test_rename_title_empty_raises():
    chapter = Chapter(id="c1", book_id="b1", chapter_number=1, title="Title")
    with pytest.raises(ValueError):
        chapter.rename_title("  ")
```

**Priorytet:** 🚩 MEDIUM - testy powinny pokrywać edge cases

---

### 3. Brak testów dla AnnotationSet i TranslationTask
**Pliki:** `tests/unit/test_annotation_set_entity.py`, `tests/unit/test_translation_task_entity.py`

**Problem:** Pliki istnieją ale mogą być puste lub niepełne. Encje mają złożoną logikę state machine, która powinna być przetestowana.

**Rekomendacja:** Dodaj testy dla:
- **AnnotationSet**: Przepływ statusów (EXTRACTED → TRANSLATED → REVIEWED → APPLIED)
- **TranslationTask**: Start, update progress, complete, fail, cancel, reset
- Edge cases: próba zmiany statusu z nieprawidłowego stanu

**Priorytet:** 🚩 MEDIUM - złożona logika wymaga testów

---

## 💡 SUGGESTION - Zalecane do poprawy

### 1. Inconsistent return types w __repr__ i __str__
**Pliki:** `user.py`, `chapter.py`

```python
# user.py
def __repr__(self):  # ❌ Brak -> str
    ...

def __str__(self):  # ❌ Brak -> str
    ...
```

**Rekomendacja:** Dodaj type hints dla spójności:
```python
def __repr__(self) -> str:
    ...

def __str__(self) -> str:
    ...
```

---

### 2. Brak walidacji chapter_number w Chapter
**Plik:** `backend/src/app/domain/entities/chapter.py`

```python
@dataclass
class Chapter:
    chapter_number: int  # ❌ Brak walidacji - może być ujemne lub 0
```

**Rekomendacja:** Dodaj walidację w `__post_init__`:
```python
def __post_init__(self):
    if self.chapter_number < 1:
        raise ValueError("Chapter number must be positive")
```

---

### 3. Brak docstringów w publicznych metodach
**Pliki:** Wszystkie encje

**Problem:** Metody biznesowe nie mają docstringów wyjaśniających:
- Co robią
- Jakie rzucają wyjątki
- Przykłady użycia

**Rekomendacja:**
```python
def mark_translated(self) -> None:
    """
    Marks annotation set as translated.
    
    Raises:
        ValueError: If status is not EXTRACTED_FROM_MD_TO_XLSX
    
    Example:
        >>> annotation_set.mark_translated()
        >>> assert annotation_set.status == AnnotationStatus.TRANSLATED
    """
    if self.status != AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX:
        raise ValueError(AnnotationSetErrors.MUST_BE_EXTRACTED_BEFORE_TRANSLATED)
    ...
```

---

### 4. Magic string "PRAGMA foreign_keys=ON" w conftest
**Plik:** `tests/conftest.py:26`

```python
conn.execute(text("PRAGMA foreign_keys=ON"))  # ❌ Magic string
```

**Rekomendacja:** Wydziel do stałej:
```python
SQLITE_ENABLE_FOREIGN_KEYS = "PRAGMA foreign_keys=ON"

# W kodzie:
conn.execute(text(SQLITE_ENABLE_FOREIGN_KEYS))
```

---

### 5. Brak walidacji email w User.change_email()
**Plik:** `backend/src/app/domain/entities/user.py:11`

```python
def change_email(self, new_email: str) -> None:
    if not new_email or not new_email.strip():
        raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
    self.email = new_email.strip()  # ❌ Brak walidacji formatu email
```

**Problem:** Metoda sprawdza tylko czy email nie jest pusty, ale nie waliduje formatu (np. "abc" przejdzie).

**Rekomendacja:** Dodaj walidację formatu lub użyj Value Object:
```python
# Opcja 1: Prosta walidacja
import re
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def change_email(self, new_email: str) -> None:
    email = new_email.strip()
    if not email:
        raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
    if not re.match(EMAIL_REGEX, email):
        raise ValueError(UserErrors.INVALID_EMAIL_FORMAT)
    self.email = email

# Opcja 2: Value Object (lepsze)
@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self):
        if not self.value or not re.match(EMAIL_REGEX, self.value):
            raise ValueError("Invalid email format")
```

---

## 📝 NIT - Drobne uwagi

### 1. Nieużywana zmienna version w teście
**Plik:** `tests/unit/test_book_entity.py:21-29`

```python
def test_book_version_increments_on_changes(book):
    version = book.version
    book.rename_title("New Title")
    assert book.version == version + 1
    version = book.version  # ❌ Można uprościć
    book.change_genre("science")
    assert book.version == version + 1
```

**Rekomendacja:** Uprość test:
```python
def test_book_version_increments_on_changes(book):
    initial_version = book.version
    
    book.rename_title("New Title")
    assert book.version == initial_version + 1
    
    book.change_genre("science")
    assert book.version == initial_version + 2
    
    book.change_quotation_marks(QuoteType.GR)
    assert book.version == initial_version + 3
```

---

### 2. Inconsistent spacing w conftest.py
**Plik:** `tests/conftest.py:5`

```python
import os, logging  # ❌ Dwa importy w jednej linii
```

**Rekomendacja:** Rozdziel na osobne linie (PEP 8):
```python
import os
import logging
```

---

### 3. Długa linia w __repr__ (>120 znaków)
**Plik:** `backend/src/app/domain/entities/translation_task.py:68-70`

**Rekomendacja:** Złam linię:
```python
def __repr__(self):
    cls = self.__class__.__name__
    total = self.total_chapters if self.total_chapters is not None else "?"
    return (
        f"{cls}(id={self.id!r}, book_id={self.book_id!r}, "
        f"status={self.status.name}, progress={self.progress}%, "
        f"progress_in_chapters={self.translated_chapters}/{total}, "
        f"message={self.message!r})"
    )
```

---

### 4. Brak spacji wokół operatora w test assertion
**Plik:** `tests/unit/test_book_entity.py:54`

```python
assert book.status == BookStatus.FAILED and book.version == version + 1
# ❌ Trudne do czytania - dwa asserty w jednym
```

**Rekomendacja:** Rozdziel na dwa asserty:
```python
assert book.status == BookStatus.FAILED
assert book.version == version + 1
```

---

## ✅ PRAISE - Co jest dobrze zrobione

### 1. **Encje z logiką biznesową** 🎯
Encje nie są anemiczne - zawierają metody biznesowe:
- `Book`: `rename_title()`, `mark_parsed()`, `start_translation()`
- `Chapter`: `is_subchapter()`, `set_parent()`
- `TranslationTask`: `start_translation_task()`, `update_progress()`

To jest **wzorcowe DDD**!

### 2. **Immutability przez dataclass** 🔒
Użycie `@dataclass` z metodami zamiast setterów to dobra praktyka:
```python
# ✅ Dobrze - kontrolowana mutacja
def rename_title(self, new_title: str) -> None:
    if not new_title or not new_title.strip():
        raise ValueError("Title cannot be empty")
    self.title = new_title.strip()
```

### 3. **Walidacja w encjach** ✅
Walidacja jest w Domain, nie w kontrolerach:
- `Book.rename_title()` sprawdza czy tytuł nie jest pusty
- `Chapter.set_parent()` sprawdza czy chapter nie jest swoim rodzicem
- `TranslationTask` waliduje przepływ statusów

### 4. **Testy jednostkowe dla encji** 🧪
Każda encja ma dedykowane testy jednostkowe:
- `test_book_entity.py` - testuje logikę Book
- `test_user_entity.py` - testuje walidację User
- `test_chapter_entity.py` - testuje Chapter

### 5. **Testy integracyjne z bazą** 🗄️
`test_db_models.py` testuje:
- Relacje między encjami (User → Book → Chapter)
- Kaskadowe usuwanie
- Parent-child relationships

### 6. **Fixture conftest.py** 🛠️
Dobrze skonfigurowane fixtures:
- `engine` (session scope) - jedna baza dla wszystkich testów
- `db_session` (function scope) - rollback po każdym teście
- `clear_mappers()` - czyszczenie po testach

### 7. **Versioning w encjach** 📦
Book i AnnotationSet mają `version` field i `_update_version()`:
```python
def _update_version(self) -> None:
    self.version += 1
```
To przygotowanie pod Optimistic Locking!

### 8. **State machine w encjach** 🔄
TranslationTask i AnnotationSet implementują state machine z walidacją przejść:
```python
def mark_translated(self) -> None:
    if self.status != AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX:
        raise ValueError(...)
    self.status = AnnotationStatus.TRANSLATED
```

---

## Akcje do podjęcia (priorytet)

### Przed mergem (BLOCKER):
1. [ ] **CRITICAL** Dodaj walidację `None` w `User.change_name()`
2. [ ] **HIGH** Dodaj type hints do `User.change_email()` i `User.change_name()`

### Po mergu (MAJOR):
3. [ ] Usuń duplikację `book = book` we wszystkich testach
4. [ ] Dodaj testy dla edge cases w Chapter
5. [ ] Dodaj/uzupełnij testy dla AnnotationSet i TranslationTask

### Nice to have (SUGGESTION/NIT):
6. [ ] Dodaj type hints do `__repr__` i `__str__`
7. [ ] Dodaj walidację `chapter_number > 0`
8. [ ] Dodaj docstringi do publicznych metod
9. [ ] Wydziel magic string "PRAGMA foreign_keys=ON" do stałej
10. [ ] Dodaj walidację formatu email (lub Value Object)
11. [ ] Uprość test `test_book_version_increments_on_changes`
12. [ ] Rozdziel importy `os, logging` na osobne linie
13. [ ] Złam długie linie w `__repr__` (>120 znaków)
14. [ ] Rozdziel złożone asserty na osobne linie

---

## Statystyki

- **Pliki zmienione:** 14 (+ 5 docs)
- **Nowe testy:** ~10 testów jednostkowych + 1 integracyjny
- **Pokrycie:** Encje dobrze pokryte, brakuje testów dla edge cases
- **Linie kodu:** ~500 linii (encje + testy)

---

## Rekomendacja

**Status:** ✅ **APPROVE WITH CHANGES**

Branch jest w dobrej kondycji. Główne problemy to:
1. Brak walidacji `None` w `User.change_name()` - **MUST FIX**
2. Brak type hints - **MUST FIX**
3. Duplikacja w testach - do poprawy po mergu

Po poprawieniu BLOCKER-ów można mergować. Reszta to drobne usprawnienia.

---

*Review wykonane zgodnie z wytycznymi z `CODE_REVIEW_GUIDELINES.md`*
