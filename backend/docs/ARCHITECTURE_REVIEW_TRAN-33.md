# Architecture Review - Branch TRAN-33-book-endpoints-logic

**Data:** 2025-12-10  
**Reviewer:** AI Assistant  
**Bazowy branch:** develop  
**Review zgodnie z:** ARCHITECTURE_REVIEW_GUIDELINES.md

---

## 📊 Podsumowanie Wykonawcze

| Kategoria | Ocena | Status |
|-----------|-------|--------|
| **Architektura warstwowa** | 9/10 | ✅ Świetna |
| **Zasady SOLID** | 7/10 | ⚠️ Dobre z błędami |
| **Wzorce projektowe** | 8/10 | ✅ Dobrze zastosowane |
| **Coupling & Cohesion** | 8/10 | ✅ Dobra separacja |
| **Skalowalność** | 7/10 | ⚠️ Wymaga uwagi |
| **Testowalność** | 8/10 | ✅ Dobra |
| **Bezpieczeństwo** | 6/10 | ⚠️ Braki |

**Ocena ogólna: 7.6/10** - Solidna architektura z drobnymi problemami

---

## ✅ Checklist warstw aplikacji

### Warstwa Domain (`domain/`)

#### ✅ Encje (`domain/entities/`)

**Book, Chapter, File, User**

- ✅ **Reprezentują koncepty biznesowe** - Book, Chapter, File, User to jasne pojęcia domenowe
- ✅ **Niezależne od infrastruktury** - Brak importów z SQLAlchemy, FastAPI
- ✅ **Zawierają logikę biznesową** - `rename()`, `change_owner()`, `mark_parsed()`, `_update_version()`
- ✅ **Walidacja w encji** - Sprawdzanie pustych stringów, walidacja stanu
- ✅ **Mutable aggregates (poprawnie!)** - Encje są mutable przez design - to właściwa implementacja wzorca Aggregate w DDD

**📘 Wyjaśnienie: Immutability vs Mutable Aggregates**

W Domain-Driven Design rozróżniamy:

1. **Value Objects (powinny być immutable):**
   ```python
   # ✅ Dobrze - FileKind, QuoteType są immutable (Enum)
   class FileKind(str, Enum):
       MARKDOWN = "markdown"
       XLSX = "xlsx"
   ```

2. **Entities/Aggregates (mogą i POWINNY być mutable):**
   ```python
   # ✅ Dobrze - Book jest mutable aggregate
   @dataclass
   class Book:
       id: str
       title: str
       status: BookStatus
       version: int
       
       def rename_title(self, new_title: str) -> None:
           # Mutacja jest kontrolowana przez metodę biznesową
           self.title = new_title.strip()
           self._update_version()  # Automatyczne zarządzanie spójności
   ```

**Dlaczego encje POWINNY być mutable:**

- **Cykl życia** - Encje mają tożsamość i przechodzą przez stany (UPLOADED → PARSED → TRANSLATED)
- **Kontrolowana mutacja** - Zmiany przez metody biznesowe (nie bezpośrednio `book.title = "..."`)
- **Transakcje** - ORM potrzebuje śledzić zmiany w obiekcie
- **Zarządzanie spójnością** - `_update_version()` przy każdej zmianie

**❌ Gdyby były immutable (anty-pattern dla agregatów):**
```python
# ❌ Źle dla aggregates
@dataclass(frozen=True)  # immutable
class Book:
    id: str
    title: str
    
    def rename_title(self, new_title: str) -> Book:
        # Tworzy nową instancję - traci historię, utrudnia persystencję
        return Book(id=self.id, title=new_title)
```

**✅ Obecna implementacja jest POPRAWNA** - encje jako mutable aggregates z kontrolowaną mutacją.

**Przykład dobrej logiki biznesowej:**
```python
class Book:
    def rename_title(self, new_title: str) -> None:
        if not new_title or not new_title.strip():
            raise ValueError(BookErrors.TITLE_CANNOT_BE_EMPTY)
        self.title = new_title.strip()
        self._update_version()  # Automatyczne zarządzanie wersją
```

**Ocena: 9/10** - Świetnie zaprojektowane encje

---

#### ✅ Porty (`domain/ports/`)

**BookRepository, FileRepository, UserRepository, LLMCompletionPort**

- ✅ **Zdefiniowane jako Protocol** - Poprawne użycie typing.Protocol
- ✅ **Niezależne od implementacji** - Tylko sygnatury metod
- ✅ **Nazwy domenowe** - `get()`, `add()`, `list_books_for_owner()` zamiast `select_from_db()`
- ❌ **PROBLEM: FileRepository łączy dwie odpowiedzialności**
  ```python
  class FileRepository(Protocol):
      def add(self, file: File) -> None: ...      # Metadata
      def get(self, file_id: str) -> Optional[File]: ...
      def save(self, destination_name: str) -> str: ...  # Storage ❌
      def open(self, path: str) -> str: ...              # Storage ❌
  ```
  **Problem:** Port łączy operacje bazodanowe z operacjami na systemie plików - łamie SRP

**Ocena: 7/10** - Dobre porty, ale FileRepository potrzebuje podziału

---

#### ✅ Value Objects (`domain/value_objects/`)

**FileKind, QuoteType, ChapterContent, BookStatus, Footnotes**

- ✅ **Są immutable** - Używane Enum lub frozen dataclass
- ✅ **Walidacja w konstruktorze** - ChapterContent waliduje dane
- ✅ **Porównanie przez wartość** - Enum automatycznie
- ✅ **Brak setterów** - Nie ma mutacji

**Przykład:**
```python
class FileKind(str, Enum):
    MARKDOWN = "markdown"
    XLSX = "xlsx"
    TRANSALTED_MARKDOWN = "translated_md"  # ⚠️ Literówka
```

**Ocena: 9/10** - Doskonałe użycie Value Objects

---

#### ✅ Serwisy domenowe (`domain/services/`)

**chapter_extraction, markdown_text_processing, parser_extraction, quotes_processing**

- ✅ **Zawierają logikę cross-cutting** - Ekstrakcja rozdziałów nie pasuje do jednej encji
- ✅ **Bezstanowe** - Czyste funkcje
- ✅ **Nie duplikują logiki z encji** - Zajmują się rzeczami spoza encji

**Ocena: 9/10** - Właściwe użycie serwisów domenowych

---

### Warstwa Application (`application/`)

#### ✅ Commands (`application/commands/`)

**CreateUserCommand, UploadFileCommand, UpdateFileCommand, DeleteFileCommand**

- ✅ **Reprezentują operacje biznesowe** - Jasne intencje
- ✅ **Modyfikują stan** - Commands to write operations
- ✅ **Jedna odpowiedzialność** - Każdy command robi jedną rzecz
- ✅ **DI przez konstruktor** - `def __init__(self, repo: FileRepository)`

**Przykład:**
```python
class CreateUserCommand:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def run(self, dto: CreateUserRequest) -> UserResponse:
        if self.repo.get_by_email(dto.email):  # ❌ Bug - rzuca wyjątek
            raise ValueError(UserErrors.EMAIL_ALREADY_IN_USE)
        user = User(id=uuid.uuid4().hex, email=dto.email, name=dto.name)
        self.repo.add(user)
        return UserResponse(...)
```

**Ocena: 8/10** - Dobre commands, ale bug w obsłudze błędów

---

#### ⚠️ Queries (`application/queries/`)

**GetFileQuery, ListFilesForOwnerQuery, GetUserQuery, GetUserBooksCommand**

- ✅ **Tylko odczytują dane** - Brak mutacji stanu
- ✅ **Zwracają DTO** - Nie wyciekają encji domenowych
- ❌ **PROBLEM: GetUserBooksCommand** - Powinno być Query, nie Command (CQS violation)

**Ocena: 7/10** - Dobre z jednym błędem nazewnictwa

---

#### ✅ DTOs (`application/dto/`)

**FileResponse, UploadFileRequest, UserResponse, CreateUserRequest, BookResponse**

- ✅ **Proste struktury danych** - Używają Pydantic BaseModel
- ✅ **Brak logiki biznesowej** - Tylko dane + walidacja Pydantic
- ✅ **Transfer między warstwami** - API → Application

**Przykład:**
```python
class FileResponse(BaseModel):
    id: str
    owner_id: str
    kind: FileKind
    path: str
    filename: str
    book_id: Optional[str] = None
    version: int
```

**Ocena: 10/10** - Perfekcyjne użycie DTO

---

### Warstwa Infrastructure (`infrastructure/`)

#### ✅ Repozytoria (`infrastructure/db/repositories/`)

**SqlAlchemyFileRepository, SqlAlchemyUserRepository, SqlAlchemyBookRepository**

- ✅ **Implementują porty z domain** - Są zgodne z Protocol
- ✅ **Mapują domain ↔ ORM** - Funkcje `_row_to_domain_*` i `_domain_to_row_*`
- ❌ **PROBLEM: ORM nie wycieka, ale wyjątki TAK**
  ```python
  def get(self, user_id: str) -> Optional[User]:
      user_row = self.session.get(UserDB, user_id)
      if not user_row:
          raise ValueError(UserErrors.USER_NOT_FOUND)  # ❌ Powinno: return None
  ```
  **Problem:** Łamie kontrakt portu (Optional = może być None), narusza LSP

- ⚠️ **Transakcje** - `self.session.commit()` po każdej operacji - brak Unit of Work

**Ocena: 6/10** - Dobra struktura, ale krytyczne błędy w implementacji

---

#### ✅ Adaptery

**LLMCompletionAdapter, MarkdownAnalyzerAdapter**

- ✅ **Implementują porty z domain**
- ✅ **Ukrywają szczegóły techniczne** - Application nie wie o OpenAI/konkretnej bibliotece
- ✅ **Łatwa podmiana** - Można wymienić na inny LLM przez DI

**Ocena: 9/10** - Doskonałe użycie Adapter Pattern

---

### Warstwa API (`api/`)

#### ⚠️ Kontrolery (`api/http/controllers/`)

**file_controller, users_controller**

- ✅ **Cienkie kontrolery** - Delegują do application layer
- ✅ **Tylko HTTP** - Request/response, HTTPException
- ❌ **PROBLEMY:**
  - Brak `return` w `create_user` endpoint
  - Błędne path params (`{book_id}` vs `owner_id`)
  - Tworzenie repo w każdym endpoint (`file_repo(db)`) - powinna być DI

**Przykład błędu:**
```python
@router.get("/by-owner/{book_id}", ...)  # Path: book_id
def list_files_for_owner(owner_id: str, ...):  # Param: owner_id ❌
```

**Ocena: 6/10** - Koncepcyjnie dobre, ale błędy wykonawcze

---

## 🎯 Zasady SOLID

### ✅ Single Responsibility Principle (SRP)

**Status: 7/10**

- ✅ Commands robią jedną rzecz
- ✅ Queries robią jedną rzecz
- ✅ Encje reprezentują jeden koncept
- ❌ **FileRepository łamie SRP** - Metadata + Storage w jednym interfejsie
- ✅ Kontrolery tylko obsługują HTTP

**Rekomendacja:** Podziel FileRepository na:
```python
class FileMetadataRepository(Protocol):
    def add(self, file: File) -> None: ...
    def get(self, file_id: str) -> Optional[File]: ...

class FileStoragePort(Protocol):
    def save(self, content: bytes, path: str) -> None: ...
    def read(self, path: str) -> bytes: ...
```

---

### ⚠️ Liskov Substitution Principle (LSP)

**Status: 4/10** ❌

**Krytyczny problem:** Implementacje repozytoriów łamią LSP

```python
# Port (kontrakt):
def get(self, file_id: str) -> Optional[File]: ...  # Optional = może być None

# Implementacja:
def get(self, file_id: str) -> Optional[File]:
    if not file_row:
        raise ValueError(...)  # ❌ Zmienia kontrakt!
```

**Skutek:** Nie można bezpiecznie podstawić implementacji - kod który działa z jednym repo, nie zadziała z innym.

**Rekomendacja:** Zmień implementacje, aby zwracały `None`, nie rzucały wyjątków.

---

### ✅ Dependency Inversion Principle (DIP)

**Status: 9/10** ✅

- ✅ Application zależy od portów (abstrakcji), nie implementacji
- ✅ Infrastructure implementuje porty
- ✅ Dependency Injection przez konstruktor
- ✅ Domain nie zależy od niczego

**Diagram zależności:**
```
     API
      ↓
 Application  →  Domain  ←  Infrastructure
     uses          ↑           implements
              (interfaces)
```

**Doskonale zaimplementowane!**

---

### ⚠️ Interface Segregation Principle (ISP)

**Status: 7/10**

- ✅ Porty są fokusowane (UserRepository, BookRepository)
- ❌ **FileRepository jest za duży** - wymusza implementację `save()` i `open()` nawet gdy nie jest potrzebne

**Rekomendacja:** Zobacz SRP - podziel interfejs

---

### ✅ Open/Closed Principle (OCP)

**Status: 8/10**

- ✅ Można dodać nowe commands/queries bez zmiany istniejących
- ✅ Można dodać nowe repozytoria przez implementację portów
- ✅ Można dodać nowe encje bez zmian w infrastrukturze

**Przykład:** Dodanie `PostgresUserRepository` nie wymaga zmian w application layer.

---

## 🏗️ Wzorce projektowe

### ✅ Repository Pattern (9/10)

- ✅ Abstrakcja persystencji za interfejsem
- ✅ Domenowy język (nie SQL)
- ❌ Problem z LSP (opisany wyżej)

---

### ⚠️ Command/Query Separation (7/10)

- ✅ Jasny podział katalogowy
- ✅ Commands modyfikują, Queries odczytują
- ❌ **GetUserBooksCommand** - złe nazewnictwo

---

### ✅ Dependency Injection (9/10)

- ✅ Wszystkie zależności przez konstruktor
- ✅ Łatwa podmiana implementacji
- ✅ Brak `new` w logice biznesowej
- ⚠️ W kontrolerach tworzenie `file_repo(db)` - można poprawić

---

### ❌ Anti-patterns wykryte

#### 1. **Leaky Abstraction (w repozytoriach)**
```python
# Szczegóły infrastruktury (ValueError) wyciekają do application
raise ValueError(FileErrors.FILE_NOT_FOUND)  # ❌
```

#### 2. **Anemic nie występuje** ✅
Encje mają logikę biznesową - dobra praktyka!

---

## 🔗 Coupling & Cohesion

### ✅ Low Coupling (8/10)

- ✅ Domain jest całkowicie niezależny
- ✅ Application zależy tylko od Domain
- ✅ Infrastructure zależy od Domain (implementuje porty)
- ✅ API zależy od Application
- ✅ Brak cyklicznych zależności

**Diagram zależności:**
```
API (4) → Application (3) → Domain (0) ← Infrastructure (1)
```
Liczby = liczba zależności zewnętrznych (niskie = dobre)

**Instability Index:**
- Domain: 0.0 (stabilny - dobrze!)
- Application: ~0.3 (średnio stabilny - OK)
- Infrastructure: ~0.5 (niestabilny - OK dla adapterów)

---

### ✅ High Cohesion (8/10)

- ✅ Moduły commands, queries, entities - wysoka spójność
- ✅ Każdy moduł ma jasny cel
- ✅ Brak "utility" klas z losowymi metodami

---

## 🚀 Skalowalność i wydajność

### ⚠️ Pytania architektoniczne (6/10)

#### ❌ **10x większy ruch**
- **Problem:** Brak cachingu
- **Problem:** Synchroniczne operacje (brak async w repozytoriach)
- **Problem:** N+1 queries możliwe w `list_books_for_owner` (ładowanie chapters)

#### ⚠️ **Caching**
- Architektura pozwala na dodanie cache (przez nowy adapter)
- Ale: brakuje strategii cache invalidation

#### ⚠️ **Single point of failure**
- Baza danych - brak connection pooling widocznego w kodzie
- Brak retry logic w repozytoriach

---

### ⚠️ Baza danych (6/10)

**Problemy wykryte:**

1. **N+1 queries możliwe:**
```python
# W BookRepository:
def get(self, book_id: str) -> Optional[Book]:
    book_row = self.session.get(BookDB, book_id)
    return _row_to_domain_book(book_row)  # ładuje chapters → N+1
```

2. **Brak eager loading:**
Relacje `book.chapters` nie są eager-loaded - SQLAlchemy zrobi kolejne query

3. **Transakcje po każdej operacji:**
```python
self.session.commit()  # Po każdym add(), update() - nieoptymalne
```
**Rekomendacja:** Unit of Work pattern

4. **Indeksy:**
```python
owner_id = Column(..., ForeignKey("users.id"), index=True)  # ✅ Dobrze!
```

---

### ⚠️ Zewnętrzne zależności (5/10)

**Brakuje:**
- ❌ Timeout handling
- ❌ Retry logic
- ❌ Circuit breaker
- ❌ Fallback strategies

**Ryzyko:** Awaria LLM API powali całą aplikację

---

## 🧪 Testowalność (8/10)

### ✅ Komponenty można testować w izolacji
- ✅ Unit testy dla encji (bez zależności)
- ✅ Unit testy dla commands z mockami
- ✅ Integration testy dla repozytoriów

### ✅ Łatwe mockowanie
```python
@pytest.fixture
def mock_file_repository():
    return Mock(spec=FileRepository)  # ✅ Doskonałe użycie Protocol
```

### ✅ Brak ukrytych zależności
- ✅ Wszystko przez konstruktor
- ✅ Brak globalnych zmiennych

### ⚠️ Piramida testów
```
Obecna struktura:
      E2E (0)     ❌ Brakuje
      /----\
     /      \  Integration (~5 testów)
    /--------\
   /          \ Unit (~20 testów)
```

**Rekomendacja:** Dodaj E2E testy dla krytycznych ścieżek (np. upload → parse → translate)

---

## 🔒 Bezpieczeństwo architektoniczne (6/10)

### ⚠️ Granice zaufania

#### ✅ Walidacja na granicy
```python
class CreateUserRequest(BaseModel):
    email: EmailStr  # ✅ Pydantic waliduje
    name: Optional[str]
```

#### ❌ Brakuje:
- **Autoryzacja** - Brak sprawdzenia "czy user może zobaczyć ten book?"
```python
@router.get("/{user_id}/books", ...)
def list_user_books(owner_id: str, ...):
    # ❌ Każdy może zobaczyć książki każdego!
    return GetUserBooksCommand(book_repo(db)).run(owner_id)
```

- **IDOR (Insecure Direct Object Reference)**
```python
@router.get("/{file_id}", ...)
def get_file(file_id: str, ...):
    # ❌ Każdy może pobrać każdy plik po ID!
```

---

### ❌ Autoryzacja (3/10)

**Brakuje całkowicie!**
- Brak sprawdzania uprawnień
- Brak kontekstu użytkownika (current_user)
- Autoryzacja powinna być w application layer:
```python
class GetFileQuery:
    def run(self, file_id: str, current_user_id: str) -> FileResponse:
        file = self.repo.get(file_id)
        if file.owner_id != current_user_id:  # ✅ Sprawdzenie!
            raise PermissionDenied()
```

---

### ⚠️ Audit (5/10)

- ❌ Brak logowania operacji
- ❌ Brak audit trail (kto, kiedy, co zmienił)
- ✅ Versioning w encjach (version field) - dobry start!

---

## 🚩 Red Flags - sygnały ostrzegawcze

### 🚫 Natychmiastowa interwencja

1. **❌ LSP violation w repozytoriach** - `get()` rzuca wyjątek zamiast zwrócić None
2. **❌ Brak autoryzacji** - Każdy może zobaczyć/edytować dane każdego
3. **❌ IDOR vulnerability** - Bezpośredni dostęp po ID bez sprawdzenia uprawnień

### ⚠️ Do dyskusji

4. **FileRepository łamie SRP** - Metadata + Storage w jednym interfejsie
5. **N+1 queries** - Możliwe przy ładowaniu relacji
6. **Brak Unit of Work** - Transakcje po każdej operacji
7. **Brak retry/timeout** - Awaria zewnętrznego API powali system

### 💡 Sugestie

8. Dodać E2E testy
9. Dodać caching strategy
10. Dodać observability (metryki, tracing)

---

## 📋 Podsumowanie i rekomendacje

### Ocena końcowa: **7.6/10** - Solidna architektura z problemami

### ✅ Co jest świetne:

1. **Hexagonal Architecture** - Doskonale zaimplementowana
2. **Domain-Driven Design** - Encje z logiką, Value Objects, Domain Services
3. **Dependency Inversion** - Perfekcyjne użycie portów i adapterów
4. **Separation of Concerns** - Jasny podział warstw
5. **Testowalność** - Łatwo testować w izolacji

### ⚠️ Krytyczne problemy do naprawy:

#### 🚫 BLOCKER (przed produkcją):

1. **Dodać autoryzację i sprawdzanie uprawnień**
   ```python
   # W każdym command/query:
   if not can_access(current_user, resource):
       raise PermissionDenied()
   ```

2. **Naprawić LSP violation w repozytoriach**
   ```python
   # get() powinno zwracać None, nie rzucać wyjątku
   def get(self, id: str) -> Optional[Entity]:
       row = self.session.get(EntityDB, id)
       return _to_domain(row) if row else None
   ```

3. **Podzielić FileRepository (SRP)**
   ```python
   FileMetadataRepository + FileStoragePort
   ```

#### ⚠️ Ważne (przed skalowaniem):

4. **Dodać Unit of Work pattern** - Transakcje per request, nie per operacja
5. **Optymalizacja N+1** - Eager loading dla relacji
6. **Retry logic + Circuit Breaker** - Dla zewnętrznych zależności
7. **Caching strategy** - Redis dla często czytanych danych

#### 💡 Nice to have:

8. E2E testy
9. Observability (metryki, tracing)
10. Audit log
11. Rate limiting

---

## 🎯 Plan działania

### Sprint 1 (krytyczne):
- [ ] Dodać authorization layer w application
- [ ] Naprawić LSP w repozytoriach
- [ ] Podzielić FileRepository
- [ ] Dodać testy dla authorization

### Sprint 2 (performance):
- [ ] Implementować Unit of Work
- [ ] Optymalizacja N+1 queries
- [ ] Dodać retry logic
- [ ] Dodać caching

### Sprint 3 (obserwability):
- [ ] E2E testy
- [ ] Metryki i monitoring
- [ ] Audit log
- [ ] Dokumentacja ADR

---

## 🏆 Verdict

**Architektura:** ⭐⭐⭐⭐☆ (4/5)
**Implementacja:** ⭐⭐⭐☆☆ (3/5)
**Production-ready:** ❌ **NIE** (brak autoryzacji!)

**Podsumowanie:**
- Świetnie zaprojektowana architektura na poziomie Senior
- Implementacja na poziomie Mid-level
- **Nie można wypuścić na produkcję** bez autoryzacji
- Po naprawieniu blockerów - świetna podstawa do skalowania

---

*Architecture Review wykonane zgodnie z ARCHITECTURE_REVIEW_GUIDELINES.md*

