y# Immutability vs Mutability w Domain-Driven Design

## TL;DR

- **Value Objects** → IMMUTABLE
- **Entities/Aggregates** → MUTABLE (z kontrolowaną mutacją)

---

## 📚 Podstawy teoretyczne

### Value Objects (Obiekty Wartości)

**Definicja:** Obiekty definiowane przez swoją wartość, bez tożsamości.

**Charakterystyka:**
- Porównywane przez wartość (`5 PLN == 5 PLN`)
- Nie mają ID
- Nie mają cyklu życia
- **MUSZĄ BYĆ IMMUTABLE**

**Przykłady z projektu:**
```python
# ✅ Value Object - immutable przez Enum
class FileKind(str, Enum):
    MARKDOWN = "markdown"
    XLSX = "xlsx"
    TRANSLATED_MARKDOWN = "translated_md"

# Użycie:
kind = FileKind.MARKDOWN
# kind.value = "other"  # ❌ Niemożliwe - immutable!
```

```python
# ✅ Value Object - immutable przez frozen dataclass
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str
    
    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Different currencies")
        return Money(self.amount + other.amount, self.currency)
```

**Dlaczego immutable:**
- Bezpieczne w wielowątkowości
- Można używać jako klucze w dict/set
- Nie ma "side effects" - `money.add(5)` nie zmienia `money`

---

### Entities/Aggregates (Encje/Agregaty)

**Definicja:** Obiekty definiowane przez tożsamość (ID), nie wartość.

**Charakterystyka:**
- Porównywane przez ID (`user1.id == user2.id`)
- Mają unikalne ID
- Mają cykl życia (tworzone → modyfikowane → usuwane)
- **POWINNY BYĆ MUTABLE** (ale z kontrolowaną mutacją!)

**Przykłady z projektu:**
```python
# ✅ Entity - mutable aggregate
@dataclass
class Book:
    id: str              # Tożsamość
    owner_id: str
    title: str
    status: BookStatus   # Stan - zmienia się w czasie
    version: int         # Historia zmian
    chapters: List[Chapter]
    
    def rename_title(self, new_title: str) -> None:
        """Kontrolowana mutacja - walidacja + side effects"""
        if not new_title or not new_title.strip():
            raise ValueError(BookErrors.TITLE_CANNOT_BE_EMPTY)
        self.title = new_title.strip()
        self._update_version()  # Automatyczne zarządzanie wersją
    
    def mark_parsed(self) -> None:
        """Zmiana stanu przez cykl życia"""
        self.status = BookStatus.PARSED
        self._update_version()
```

```python
# ✅ Użycie:
book = Book(id="123", title="Original Title", ...)

# Mutacja przez metodę biznesową (kontrolowana):
book.rename_title("New Title")  # ✅ OK - walidacja + side effects

# Bezpośrednia mutacja (niebezpieczna, ale możliwa):
book.title = ""  # ⚠️ Omija walidację - ale czasem potrzebne (np. ORM)
```

**Dlaczego mutable:**

1. **Cykl życia:**
   ```python
   book = repository.get("123")
   book.status  # UPLOADED
   
   # Książka przechodzi przez stany:
   book.mark_parsed()       # UPLOADED → PARSED
   book.start_translation() # PARSED → IN_TRANSLATION
   book.mark_translated()   # IN_TRANSLATION → TRANSLATED
   ```

2. **ORM/Persystencja:**
   ```python
   # ORM (SQLAlchemy) wymaga mutacji:
   book = session.get(Book, "123")
   book.title = "New Title"  # ORM śledzi zmianę
   session.commit()          # Zapisuje tylko zmienione pola (UPDATE title)
   
   # Gdyby immutable:
   book = session.get(Book, "123")
   new_book = book.with_title("New Title")  # Nowa instancja
   session.commit()  # ❌ ORM nie wie co się zmieniło!
   ```

3. **Transakcje:**
   ```python
   # W jednej transakcji wiele mutacji:
   book = repository.get("123")
   book.rename_title("New Title")
   book.change_genre("Fiction")
   book.change_quotation_marks(QuoteType.EN)
   repository.update(book)  # Jedna operacja UPDATE
   
   # Gdyby immutable (anty-pattern):
   book = repository.get("123")
   book2 = book.with_title("New Title")
   book3 = book2.with_genre("Fiction")
   book4 = book3.with_quotation_marks(QuoteType.EN)
   repository.update(book4)  # Utraciliśmy referencję do oryginału!
   ```

4. **Zarządzanie spójnością:**
   ```python
   class Book:
       def _update_version(self) -> None:
           self.version += 1  # Automatyczna wersja przy każdej zmianie
       
       def rename_title(self, new_title: str) -> None:
           self.title = new_title
           self._update_version()  # Side effect
   
   # ✅ Każda zmiana automatycznie zwiększa wersję
   book.version  # 1
   book.rename_title("New")
   book.version  # 2
   ```

---

## ⚖️ Porównanie

| Aspekt | Value Object | Entity/Aggregate |
|--------|--------------|------------------|
| **Tożsamość** | Brak (wartość = tożsamość) | ID |
| **Porównanie** | Przez wartość | Przez ID |
| **Mutability** | **IMMUTABLE** | **MUTABLE** |
| **Cykl życia** | Brak | Tak (create → update → delete) |
| **Walidacja** | W konstruktorze | W metodach biznesowych |
| **Persystencja** | Embedded w encji | Własna tabela |
| **Przykład** | Money, Email, Address | User, Book, Order |

---

## 🎯 Wzorce mutacji w agregatach

### ✅ Poprawnie - Kontrolowana mutacja

```python
@dataclass
class Book:
    id: str
    title: str
    status: BookStatus
    version: int
    
    def rename_title(self, new_title: str) -> None:
        """Publiczna metoda biznesowa - kontrolowana mutacja"""
        if not new_title or not new_title.strip():
            raise ValueError(BookErrors.TITLE_CANNOT_BE_EMPTY)
        self.title = new_title.strip()
        self._update_version()
    
    def _update_version(self) -> None:
        """Prywatna - automatyczne zarządzanie wersją"""
        self.version += 1
```

**Zalety:**
- ✅ Walidacja w jednym miejscu
- ✅ Side effects (version) są automatyczne
- ✅ Łatwe testowanie
- ✅ Ekspresywne (`book.rename_title()` zamiast `book.title = ...`)

---

### ❌ Źle - Anemic Domain Model

```python
@dataclass
class Book:
    """Tylko dane - brak logiki (anty-pattern!)"""
    id: str
    title: str
    status: BookStatus
    version: int
    
# Logika w serwisie (nie w encji):
class BookService:
    def rename_book(self, book: Book, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError(...)
        book.title = new_title.strip()  # ❌ Bezpośrednia mutacja
        book.version += 1  # ❌ Łatwo zapomnieć!
```

**Problemy:**
- ❌ Walidacja rozproszona (w wielu serwisach)
- ❌ Łatwo zapomnieć o `version += 1`
- ❌ Trudne testowanie
- ❌ Brak ekspresywności

---

### ❌ Źle dla agregatów - Immutable

```python
@dataclass(frozen=True)  # Immutable
class Book:
    id: str
    title: str
    status: BookStatus
    version: int
    
    def rename_title(self, new_title: str) -> 'Book':
        """Zwraca NOWĄ instancję - anty-pattern dla agregatów!"""
        if not new_title or not new_title.strip():
            raise ValueError(...)
        return Book(
            id=self.id,
            title=new_title.strip(),
            status=self.status,
            version=self.version + 1  # Trzeba pamiętać!
        )

# Użycie:
book = repository.get("123")
new_book = book.rename_title("New Title")  # Nowa instancja!

# ❌ Problemy:
repository.update(new_book)  # ORM nie wie że to ta sama książka!
# book.id == new_book.id, ale to różne obiekty w pamięci
```

**Problemy:**
- ❌ ORM nie śledzi zmian (każda zmiana = nowy obiekt)
- ❌ Utrata referencji (musimy pamiętać o przypisaniu `book = new_book`)
- ❌ Performance - tworzenie nowych obiektów za każdym razem
- ❌ Transakcje - ciężko śledzić co się zmieniło

---

## 🏗️ Dobre praktyki w projekcie

### ✅ Obecna implementacja (POPRAWNA)

```python
# Value Objects - immutable
class FileKind(str, Enum):
    MARKDOWN = "markdown"
    XLSX = "xlsx"

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

# Entities - mutable z kontrolowaną mutacją
@dataclass
class Book:
    id: str
    title: str
    
    def rename_title(self, new_title: str) -> None:
        # Kontrolowana mutacja
        self.title = new_title
        self._update_version()

@dataclass
class User:
    id: str
    email: str
    
    def change_email(self, new_email: str) -> None:
        # Walidacja + mutacja
        if not new_email:
            raise ValueError(...)
        self.email = new_email
```

---

## 📖 Literatura

### Książki:
1. **"Domain-Driven Design" - Eric Evans** (rozdział 5: Model-Driven Design)
   - Rozdział o Entities vs Value Objects

2. **"Implementing Domain-Driven Design" - Vaughn Vernon**
   - Rozdział 6: Value Objects
   - Rozdział 5: Entities

3. **"Patterns of Enterprise Application Architecture" - Martin Fowler**
   - Wzorzec: Value Object
   - Wzorzec: Identity Field

### Artykuły:
- [Martin Fowler - Value Object](https://martinfowler.com/bliki/ValueObject.html)
- [DDD Aggregate Pattern](https://martinfowler.com/bliki/DDD_Aggregate.html)

---

## 🎓 Podsumowanie

### Kiedy immutable:
- ✅ Value Objects (Money, Email, Address, FileKind)
- ✅ DTOs (do transferu danych)
- ✅ Konfiguracja (Settings)

### Kiedy mutable:
- ✅ Entities/Aggregates (User, Book, Order)
- ✅ Obiekty z cyklem życia
- ✅ Obiekty śledzone przez ORM

### Kluczowe zasady:
1. **Value Objects** → frozen/immutable
2. **Entities** → mutable, ale mutacja przez **publiczne metody biznesowe**
3. **NIE bezpośrednia mutacja** → `book.title = "x"` ❌, `book.rename_title("x")` ✅
4. **Automatyczne side effects** → `_update_version()` przy każdej zmianie

---

**Obecna implementacja w projekcie jest POPRAWNA i zgodna z DDD best practices!** ✅


