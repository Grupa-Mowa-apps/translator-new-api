# Wytyczne Code Review

## Spis treści
1. [Cel i zakres](#cel-i-zakres)
2. [Kiedy przeprowadzać code review](#kiedy-przeprowadzać-code-review)
3. [Checklist code review](#checklist-code-review)
4. [Jakość kodu](#jakość-kodu)
5. [Czytelność i styl](#czytelność-i-styl)
6. [Bezpieczeństwo](#bezpieczeństwo)
7. [Wydajność](#wydajność)
8. [Testy](#testy)
9. [Git i commity](#git-i-commity)
10. [Red Flags - sygnały ostrzegawcze](#red-flags---sygnały-ostrzegawcze)
11. [Kultura code review](#kultura-code-review)

---

## Cel i zakres

### Cel Code Review
- **Jakość**: Zapewnienie wysokiej jakości kodu
- **Błędy**: Wykrycie bugów przed produkcją
- **Wiedza**: Dzielenie się wiedzą w zespole
- **Spójność**: Utrzymanie jednolitego stylu
- **Nauka**: Rozwój umiejętności zespołu

### Różnica między Code Review a Architecture Review
| Aspekt | Code Review | Architecture Review |
|--------|-------------|---------------------|
| Fokus | Jakość kodu, styl, błędy | Struktura, zależności, wzorce |
| Poziom | Linie kodu, funkcje | Moduły, warstwy, komponenty |
| Pytanie | "Czy to działa poprawnie?" | "Czy to jest dobrze zaprojektowane?" |
| Częstotliwość | Każdy PR | Duże zmiany, nowe moduły |

---

## Kiedy przeprowadzać code review

### Obowiązkowe code review:
- [ ] Każdy Pull Request przed merge
- [ ] Zmiany w krytycznych modułach (płatności, autoryzacja)
- [ ] Nowy kod (nie refaktoring)
- [ ] Zmiany w logice biznesowej

### Opcjonalne (ale zalecane):
- [ ] Refaktoring (pair programming może wystarczyć)
- [ ] Dokumentacja
- [ ] Konfiguracja (ale sprawdź secrets!)

### Kiedy można pominąć:
- Hotfix na produkcji (ale code review post-factum!)
- Typo w komentarzu
- Formatowanie (powinno być automatyczne)

---

## Checklist code review

### Podstawowy checklist (każdy PR)

#### 1. Funkcjonalność
- [ ] Czy kod robi to co powinien?
- [ ] Czy obsługuje edge cases?
- [ ] Czy obsługuje błędy poprawnie?
- [ ] Czy nie wprowadza regresji?

#### 2. Czytelność
- [ ] Czy kod jest zrozumiały?
- [ ] Czy nazwy są jasne i opisowe?
- [ ] Czy nie ma zbędnej złożoności?
- [ ] Czy komentarze są potrzebne i aktualne?

#### 3. Testy
- [ ] Czy są testy dla nowego kodu?
- [ ] Czy testy są sensowne (nie tylko dla pokrycia)?
- [ ] Czy testy przechodzą?
- [ ] Czy są testy dla edge cases?

#### 4. Bezpieczeństwo
- [ ] Czy nie ma hardcodowanych secrets?
- [ ] Czy dane wejściowe są walidowane?
- [ ] Czy nie ma SQL injection, XSS?
- [ ] Czy autoryzacja jest sprawdzana?

#### 5. Wydajność
- [ ] Czy nie ma oczywistych problemów wydajnościowych?
- [ ] Czy nie ma N+1 queries?
- [ ] Czy nie ma memory leaks?
- [ ] Czy operacje I/O są asynchroniczne gdzie trzeba?

---

## Jakość kodu

### Nazewnictwo

#### Zmienne i funkcje
```python
# ❌ Źle - niejasne nazwy
def calc(x, y):
    return x * y * 0.23

# ✅ Dobrze - opisowe nazwy
def calculate_vat_amount(net_price: Decimal, quantity: int) -> Decimal:
    VAT_RATE = Decimal("0.23")
    return net_price * quantity * VAT_RATE
```

#### Klasy
```python
# ❌ Źle - zbyt ogólne
class Manager:
    pass

class Handler:
    pass

# ✅ Dobrze - konkretne
class BookRepository:
    pass

class CreateBookCommandHandler:
    pass
```

#### Stałe
```python
# ❌ Źle - magic numbers
if user.age > 18:
    pass

# ✅ Dobrze - nazwane stałe
ADULT_AGE = 18
if user.age > ADULT_AGE:
    pass
```

### Funkcje

#### Długość funkcji
```python
# ❌ Źle - funkcja >50 linii
def process_order(order):
    # 100 linii kodu...
    pass

# ✅ Dobrze - małe, fokusowane funkcje
def process_order(order):
    validate_order(order)
    calculate_total(order)
    apply_discount(order)
    charge_payment(order)
    send_confirmation(order)
```

#### Parametry funkcji
```python
# ❌ Źle - za dużo parametrów
def create_user(name, email, age, address, city, country, phone, newsletter):
    pass

# ✅ Dobrze - obiekt parametrów
@dataclass
class CreateUserCommand:
    name: str
    email: str
    age: int
    address: str
    city: str
    country: str
    phone: str
    newsletter: bool

def create_user(command: CreateUserCommand):
    pass
```

#### Single Responsibility
```python
# ❌ Źle - funkcja robi za dużo
def process_and_send_email(user):
    # Walidacja
    if not user.email:
        raise ValueError()
    
    # Zapis do bazy
    db.save(user)
    
    # Wysyłka emaila
    send_email(user.email, "Welcome")
    
    # Logging
    logger.info(f"User {user.id} created")

# ✅ Dobrze - każda funkcja robi jedno
def create_user(user: User):
    validate_user(user)
    save_user(user)
    send_welcome_email(user)
    log_user_creation(user)
```

### Klasy

#### Długość klasy
- [ ] Czy klasa ma <300 linii?
- [ ] Czy klasa ma jedną odpowiedzialność?
- [ ] Czy nazwa klasy jasno opisuje jej cel?

#### Pola klasy
```python
# ❌ Źle - publiczne pola mutowalne
class Book:
    def __init__(self):
        self.title = ""
        self.price = 0

# ✅ Dobrze - enkapsulacja
class Book:
    def __init__(self, title: str, price: Decimal):
        self._title = title
        self._price = price
    
    @property
    def title(self) -> str:
        return self._title
    
    def change_price(self, new_price: Decimal):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self._price = new_price
```

---

## Czytelność i styl

### Formatowanie

#### Wcięcia i odstępy
```python
# ❌ Źle - niespójne formatowanie
def calculate(x,y):
    if x>0:
        return x+y
    else:
        return x-y

# ✅ Dobrze - spójne formatowanie (PEP 8)
def calculate(x: int, y: int) -> int:
    if x > 0:
        return x + y
    else:
        return x - y
```

#### Długość linii
```python
# ❌ Źle - linia >120 znaków
result = some_very_long_function_name(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6)

# ✅ Dobrze - łamanie linii
result = some_very_long_function_name(
    parameter1,
    parameter2,
    parameter3,
    parameter4,
    parameter5,
    parameter6
)
```

### Komentarze

#### Dobre komentarze (DLACZEGO)
```python
# ✅ Dobrze - wyjaśnia DLACZEGO
# OpenAI API ma rate limit 10 req/s. Sleep zapobiega błędom 429.
# TODO: Zaimplementować exponential backoff (TICKET-123)
time.sleep(0.1)

# ✅ Dobrze - wyjaśnia nieoczywistą logikę biznesową
# Zgodnie z regulaminem RODO, dane użytkownika muszą być usunięte
# po 30 dniach nieaktywności (Art. 17)
expiry_date = today - timedelta(days=30)
```

#### Złe komentarze (CO)
```python
# ❌ Źle - powtarza kod
# Zwiększ counter o 1
counter += 1

# ❌ Źle - nieaktualne
# TODO: Naprawić to później (komentarz z 2020 roku)

# ❌ Źle - zakomentowany kod
# def old_function():
#     return "old"
```

### Docstringi

```python
# ✅ Dobrze - docstring dla publicznego API
def calculate_discount(price: Decimal, discount_percent: int) -> Decimal:
    """
    Oblicza cenę po rabacie.
    
    Args:
        price: Cena bazowa (netto)
        discount_percent: Procent rabatu (0-100)
    
    Returns:
        Cena po rabacie
    
    Raises:
        ValueError: Jeśli discount_percent < 0 lub > 100
    
    Example:
        >>> calculate_discount(Decimal("100"), 20)
        Decimal("80")
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    return price * (1 - Decimal(discount_percent) / 100)
```

---

## Bezpieczeństwo

### Secrets i credentials

```python
# ❌ NIEBEZPIECZNE - hardcodowane secrets
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ Dobrze - secrets z environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Walidacja danych wejściowych

```python
# ❌ Źle - brak walidacji
@app.post("/books")
def create_book(title: str, price: str):
    book = Book(title=title, price=float(price))  # Co jeśli price = "abc"?
    db.save(book)

# ✅ Dobrze - walidacja na granicy
class CreateBookRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    price: Decimal = Field(gt=0, decimal_places=2)

@app.post("/books")
def create_book(request: CreateBookRequest):
    command = CreateBookCommand(
        title=request.title,
        price=request.price
    )
    handler.execute(command)
```

### SQL Injection

```python
# ❌ NIEBEZPIECZNE - SQL injection
def find_user(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ Dobrze - parametryzowane zapytania
def find_user(username: str):
    query = "SELECT * FROM users WHERE username = :username"
    return db.execute(query, {"username": username})

# ✅ Najlepiej - ORM
def find_user(username: str):
    return session.query(User).filter(User.username == username).first()
```

### Autoryzacja

```python
# ❌ Źle - brak sprawdzenia uprawnień
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book_repo.delete(book_id)  # Każdy może usunąć!

# ✅ Dobrze - sprawdzenie uprawnień
@app.delete("/books/{book_id}")
def delete_book(book_id: int, current_user: User = Depends(get_current_user)):
    command = DeleteBookCommand(
        book_id=book_id,
        user_id=current_user.id
    )
    handler.execute(command)  # Handler sprawdza uprawnienia
```

---

## Wydajność

### N+1 Queries

```python
# ❌ Źle - N+1 queries
books = session.query(Book).all()  # 1 query
for book in books:
    print(book.author.name)  # N queries (jeden dla każdej książki)

# ✅ Dobrze - eager loading
books = session.query(Book).options(
    joinedload(Book.author)
).all()  # 1 query z JOIN
for book in books:
    print(book.author.name)  # Bez dodatkowych queries
```

### Niepotrzebne operacje w pętli

```python
# ❌ Źle - operacje w pętli
for book in books:
    vat_rate = get_vat_rate()  # Wywołanie dla każdej książki
    book.price_with_vat = book.price * (1 + vat_rate)

# ✅ Dobrze - operacja przed pętlą
vat_rate = get_vat_rate()  # Jedno wywołanie
for book in books:
    book.price_with_vat = book.price * (1 + vat_rate)
```

### Memory leaks

```python
# ❌ Źle - trzymanie referencji
class Cache:
    def __init__(self):
        self.data = {}  # Rośnie w nieskończoność
    
    def add(self, key, value):
        self.data[key] = value

# ✅ Dobrze - limit rozmiaru
from functools import lru_cache

@lru_cache(maxsize=1000)  # Max 1000 elementów
def expensive_operation(x):
    return x * 2
```

---

## Testy

### Pokrycie testami

```python
# ✅ Nowy kod powinien mieć testy
def calculate_discount(price: Decimal, percent: int) -> Decimal:
    if percent < 0 or percent > 100:
        raise ValueError("Invalid discount")
    return price * (1 - Decimal(percent) / 100)

# Test
def test_calculate_discount():
    assert calculate_discount(Decimal("100"), 20) == Decimal("80")

def test_calculate_discount_invalid():
    with pytest.raises(ValueError):
        calculate_discount(Decimal("100"), 150)
```

### Jakość testów

```python
# ❌ Źle - test nic nie testuje
def test_create_book():
    book = Book("Title", "Author")
    assert book is not None  # Nic nie sprawdza

# ✅ Dobrze - test sprawdza zachowanie
def test_create_book_with_valid_data():
    book = Book("Clean Code", "Robert Martin")
    assert book.title == "Clean Code"
    assert book.author == "Robert Martin"

def test_create_book_with_empty_title_raises_error():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Book("", "Author")
```

### Testy jednostkowe vs integracyjne

```python
# ✅ Unit test - bez zależności
def test_book_publish():
    book = Book("Title", "Author")
    book.publish()
    assert book.status == BookStatus.PUBLISHED

# ✅ Integration test - z bazą danych
def test_book_repository_save(db_session):
    book = Book("Title", "Author")
    repo = BookRepository(db_session)
    
    repo.save(book)
    
    saved_book = repo.find_by_id(book.id)
    assert saved_book.title == "Title"
```

---

## Git i commity

### Commit messages

```bash
# ❌ Źle - niejasne
git commit -m "fix"
git commit -m "update"
git commit -m "changes"

# ✅ Dobrze - opisowe
git commit -m "Fix: Resolve N+1 query in book list endpoint"
git commit -m "Feature: Add email validation to user registration"
git commit -m "Refactor: Extract payment logic to separate service"
```

### Rozmiar commitów

```bash
# ❌ Źle - jeden ogromny commit
git commit -m "Add entire user management module" # 50 plików, 2000 linii

# ✅ Dobrze - małe, atomowe commity
git commit -m "Add User entity with validation"
git commit -m "Add UserRepository interface"
git commit -m "Implement PostgresUserRepository"
git commit -m "Add CreateUserCommand and handler"
git commit -m "Add user registration endpoint"
```

### Branch naming

```bash
# ❌ Źle - niejasne
git checkout -b fix
git checkout -b new-feature

# ✅ Dobrze - konwencja
git checkout -b feature/TRAN-123-user-registration
git checkout -b bugfix/TRAN-456-fix-login-error
git checkout -b refactor/TRAN-789-extract-payment-service
```

---

## Red Flags - sygnały ostrzegawcze

### 🚨 Krytyczne (STOP - nie merguj)

- [ ] Hardcodowane secrets (API keys, passwords)
- [ ] SQL injection vulnerability
- [ ] Brak autoryzacji w krytycznych endpointach
- [ ] Usunięcie testów bez powodu
- [ ] Commit bezpośrednio na main/master
- [ ] Kod który nie kompiluje się / nie przechodzi testów

### 🚩 Poważne (wymaga poprawy)

- [ ] Brak testów dla nowego kodu
- [ ] Logika biznesowa w kontrolerze
- [ ] Duplikacja kodu (copy-paste)
- [ ] Funkcja >100 linii
- [ ] Klasa >500 linii
- [ ] Nieobsłużone wyjątki
- [ ] N+1 queries
- [ ] Memory leaks

### ⚠️ Do poprawy (sugestie)

- [ ] Niejasne nazwy zmiennych (x, y, tmp, data)
- [ ] Brak docstringów w publicznym API
- [ ] Komentarze tłumaczące "co" zamiast "dlaczego"
- [ ] Magic numbers bez stałych
- [ ] Nieużywane importy/zmienne
- [ ] Zbyt długie linie (>120 znaków)
- [ ] Inconsistent formatting

### 💡 Nice to have (opcjonalne)

- [ ] Dodanie type hints
- [ ] Refaktoring dla lepszej czytelności
- [ ] Dodanie przykładów w docstringach
- [ ] Optymalizacja wydajności (jeśli nie jest problem)

---

## Kultura code review

### Dla reviewera

#### ✅ Dobre praktyki

**Bądź konstruktywny:**
```
❌ "Ten kod jest do bani"
✅ "Sugeruję wydzielić tę logikę do osobnej funkcji dla lepszej czytelności"
```

**Pytaj, nie oskarżaj:**
```
❌ "Dlaczego to zrobiłeś tak głupio?"
✅ "Czy rozważałeś użycie wzorca Strategy tutaj? Jakie były twoje przemyślenia?"
```

**Doceniaj dobre rzeczy:**
```
✅ "Świetne testy! Pokrywają wszystkie edge cases"
✅ "Dobry pomysł z użyciem Value Object tutaj"
```

**Rozróżniaj poziomy:**
```
🚨 MUST FIX: "To wprowadza SQL injection vulnerability"
💡 SUGGESTION: "Można by to uprościć używając list comprehension"
❓ QUESTION: "Czy ta logika nie powinna być w Domain?"
```

#### ❌ Złe praktyki

- Nie rób code review "na siłę" (jeśli nie masz czasu, powiedz)
- Nie blokuj PR z powodu preferencji stylistycznych (to do lintera)
- Nie rób code review po 8 godzinach pracy (jesteś zmęczony)
- Nie rób review >500 linii naraz (podziel PR)

### Dla autora PR

#### ✅ Dobre praktyki

**Przygotuj PR:**
- Dodaj opis co i dlaczego
- Dodaj screenshoty/GIFy dla UI changes
- Linkuj do ticketu (JIRA, GitHub Issue)
- Oznacz draft jeśli nie gotowe

**Ułatw review:**
```markdown
## Co zmienia ten PR?
Dodaje endpoint do rejestracji użytkownika

## Dlaczego?
TRAN-123: Potrzebujemy rejestracji dla nowych użytkowników

## Jak przetestować?
1. POST /api/users/register
2. Sprawdź email weryfikacyjny
3. Kliknij link aktywacyjny

## Checklist
- [x] Dodane testy
- [x] Zaktualizowana dokumentacja
- [x] Sprawdzone na staging
```

**Reaguj na feedback:**
- Odpowiadaj na komentarze
- Nie bierz do siebie krytyki
- Pytaj jeśli nie rozumiesz
- Dziękuj za sugestie

#### ❌ Złe praktyki

- Nie rób PR >1000 linii (nikt tego nie zreviewuje dobrze)
- Nie mieszaj refactoringu z nowym feature (osobne PR)
- Nie pushuj bez testów
- Nie ignoruj komentarzy reviewera

### Proces review

#### 1. Pierwszy przegląd (5-10 min)
- Przeczytaj opis PR
- Sprawdź rozmiar (jeśli >500 linii, poproś o podział)
- Sprawdź czy testy przechodzą
- Sprawdź czy nie ma oczywistych błędów

#### 2. Szczegółowy przegląd (20-30 min)
- Przejrzyj kod linia po linii
- Sprawdź logikę biznesową
- Sprawdź testy
- Sprawdź bezpieczeństwo
- Dodaj komentarze

#### 3. Feedback (5 min)
- Podsumuj główne uwagi
- Oznacz poziom (MUST FIX / SUGGESTION)
- Approve lub Request Changes

#### 4. Follow-up
- Sprawdź czy autor odpowiedział na komentarze
- Sprawdź czy poprawki są OK
- Approve i merge

---

## Podsumowanie - Quick Reference

### Przed zatwierdzeniem PR sprawdź:

```
✅ Kod działa i robi to co powinien
✅ Są testy dla nowego kodu
✅ Testy przechodzą
✅ Brak hardcodowanych secrets
✅ Dane wejściowe są walidowane
✅ Nazwy są jasne i opisowe
✅ Funkcje są krótkie (<50 linii)
✅ Brak duplikacji kodu
✅ Brak oczywistych problemów wydajnościowych
✅ Commit messages są opisowe
✅ Brak red flags
```

### Pytania do zadania sobie:

1. **Czy rozumiem co ten kod robi?**
2. **Czy mogę go łatwo przetestować?**
3. **Czy będzie łatwy w utrzymaniu za 6 miesięcy?**
4. **Czy nie wprowadza regresji?**
5. **Czy jest bezpieczny?**

Jeśli odpowiedź na którekolwiek pytanie to "nie" → Request Changes.

---

## Narzędzia automatyzacji

### Pre-commit hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### CI/CD checks
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
      - name: Check coverage
        run: pytest --cov=. --cov-fail-under=80
      - name: Lint
        run: flake8 .
      - name: Type check
        run: mypy .
```

---

*Dokument wersja 1.0 | Data: 2025-01-20*
