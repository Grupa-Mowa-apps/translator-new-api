# Code Review - Branch TRAN-29-user-endpoints

**Data:** 2025-01-20  
**Reviewer:** AI Assistant  
**Bazowy branch:** develop  
**Typ zmian:** User endpoints + repositories + DTOs

---

## Podsumowanie

| Kategoria | Ilość |
|-----------|-------|
| 🚨 BLOCKER | 3 |
| 🚩 MAJOR | 4 |
| 💡 SUGGESTION | 6 |
| 📝 NIT | 5 |
| ✅ PRAISE | 7 |

---

## 🚨 BLOCKER - Muszą być poprawione przed mergem

### 1. Brak zwracania wartości w create_user endpoint
**Plik:** `backend/src/app/api/http/controllers/users_controller.py:27`  
**Linia:** 27-30

```python
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(dto: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        CreateUserCommand(user_repo(db)).run(dto)  # ❌ Brak return!
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
```

**Problem:** Endpoint deklaruje `response_model=UserResponse` ale nie zwraca wartości. FastAPI zwróci `null`.

**Rekomendacja:**
```python
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(dto: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        return CreateUserCommand(user_repo(db)).run(dto)  # ✅ Zwróć UserResponse
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
```

**Priorytet:** 🚨 CRITICAL - endpoint nie działa poprawnie

---

### 2. Nieprawidłowa logika w get_by_email - rzuca ValueError zamiast zwracać None
**Plik:** `backend/src/app/infrastructure/db/repositories/user_repo_sqlalchemy.py:25`  
**Linia:** 25-29

```python
def get_by_email(self, email: str) -> Optional[User]:
    user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
    if not user_row:
        raise ValueError(UserErrors.USER_NOT_FOUND)  # ❌ Powinno być return None
    return User(id=user_row.id, email=user_row.email, name=user_row.name)
```

**Problem:** 
- Metoda deklaruje `Optional[User]` ale rzuca wyjątek zamiast zwracać `None`
- W `CreateUserCommand.run()` używane jest: `if self.repo.get_by_email(dto.email):` co spowoduje ValueError zamiast sprawdzenia czy user istnieje

**Rekomendacja:**
```python
def get_by_email(self, email: str) -> Optional[User]:
    user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
    if not user_row:
        return None  # ✅ Zwróć None zgodnie z type hint
    return User(id=user_row.id, email=user_row.email, name=user_row.name)
```

**Priorytet:** 🚨 CRITICAL - CreateUserCommand nie działa poprawnie

---

### 3. Brak walidacji email w User entity
**Plik:** `backend/src/app/domain/entities/user.py:11`  
**Linia:** 11-18

```python
def change_email(self, new_email: str) -> None:
    if not new_email or not new_email.strip():
        raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
    self.email = new_email.strip()  # ❌ Brak walidacji formatu email
```

**Problem:** 
- Metoda sprawdza tylko czy email nie jest pusty
- Nie waliduje formatu email (np. "abc" przejdzie)
- DTO używa `EmailStr` ale entity nie waliduje

**Rekomendacja:**
```python
import re
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def change_email(self, new_email: str) -> None:
    email = new_email.strip()
    if not email:
        raise ValueError(UserErrors.EMAIL_CANNOT_BE_EMPTY)
    if not re.match(EMAIL_REGEX, email):
        raise ValueError(UserErrors.INVALID_EMAIL_FORMAT)
    self.email = email
```

**Priorytet:** 🚨 HIGH - dane mogą być niespójne

---

## 🚩 MAJOR - Poważne problemy do poprawy

### 1. Inconsistent error handling - get() vs get_by_email()
**Plik:** `backend/src/app/infrastructure/db/repositories/user_repo_sqlalchemy.py`  
**Linie:** 19-29

```python
def get(self, user_id: str) -> Optional[User]:
    user_row = self.session.get(UserDB, user_id)
    if not user_row:
        raise ValueError(UserErrors.USER_NOT_FOUND)  # ❌ Rzuca wyjątek
    return User(...)

def get_by_email(self, email: str) -> Optional[User]:
    user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
    if not user_row:
        raise ValueError(UserErrors.USER_NOT_FOUND)  # ❌ Rzuca wyjątek
    return User(...)
```

**Problem:** 
- Obie metody deklarują `Optional[User]` ale rzucają wyjątek zamiast zwracać `None`
- To jest **anty-pattern** - type hint mówi jedno, implementacja robi drugie
- Utrudnia użycie metod (trzeba zawsze owijać w try-except)

**Rekomendacja:** Zdecyduj się na jeden pattern:

**Opcja A: Zwracaj None (lepsze dla Optional)**
```python
def get(self, user_id: str) -> Optional[User]:
    user_row = self.session.get(UserDB, user_id)
    if not user_row:
        return None  # ✅ Zgodne z type hint
    return _row_to_domain_user(user_row)

def get_by_email(self, email: str) -> Optional[User]:
    user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
    if not user_row:
        return None  # ✅ Zgodne z type hint
    return _row_to_domain_user(user_row)
```

**Opcja B: Rzucaj wyjątek (zmień type hint)**
```python
def get(self, user_id: str) -> User:  # ✅ Usuń Optional
    user_row = self.session.get(UserDB, user_id)
    if not user_row:
        raise ValueError(UserErrors.USER_NOT_FOUND)
    return _row_to_domain_user(user_row)
```

**Priorytet:** 🚩 HIGH - niespójność API

---

### 2. Brak transakcji w repository - commit po każdej operacji
**Plik:** `backend/src/app/infrastructure/db/repositories/user_repo_sqlalchemy.py`  
**Linie:** 15-42

```python
def add(self, user: User) -> None:
    self.session.add(UserDB(id=user.id, email=user.email, name=user.name))
    self.session.commit()  # ❌ Commit w repository

def update(self, user: User) -> None:
    # ...
    self.session.commit()  # ❌ Commit w repository

def delete(self, user_id: str) -> None:
    # ...
    self.session.commit()  # ❌ Commit w repository
```

**Problem:**
- Repository nie powinno commitować transakcji
- Uniemożliwia transakcje obejmujące wiele operacji
- Narusza Single Responsibility Principle
- Utrudnia testowanie (trzeba mockować commit)

**Rekomendacja:** Przenieś commit do warstwy aplikacji (Command/Query) lub użyj Unit of Work pattern:

```python
# Repository - bez commit
def add(self, user: User) -> None:
    self.session.add(UserDB(id=user.id, email=user.email, name=user.name))
    # ✅ Brak commit

# Command - z commit
class CreateUserCommand:
    def run(self, dto: CreateUserRequest) -> UserResponse:
        if self.repo.get_by_email(dto.email):
            raise ValueError(UserErrors.EMAIL_ALREADY_IN_USE)
        user = User(id=uuid.uuid4().hex, email=dto.email, name=dto.name)
        self.repo.add(user)
        self.repo.session.commit()  # ✅ Commit w Command
        return UserResponse(id=user.id, email=user.email, name=user.name)
```

**Priorytet:** 🚩 MEDIUM - utrudnia rozbudowę

---

### 3. Brak walidacji parametrów w list_users
**Plik:** `backend/src/app/api/http/controllers/users_controller.py:40`  
**Linia:** 40-41

```python
@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(limit: int, email_like: Optional[str], db: Session=Depends(get_db)):
    return ListUsersQuery(user_repo(db)).run(limit, email_like)
```

**Problem:**
- Brak walidacji `limit` - może być ujemny lub bardzo duży (DoS)
- Brak domyślnej wartości dla `limit`
- Brak maksymalnego limitu

**Rekomendacja:**
```python
from fastapi import Query

@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    limit: int = Query(default=10, ge=1, le=100),  # ✅ Walidacja
    email_like: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return ListUsersQuery(user_repo(db)).run(limit, email_like)
```

**Priorytet:** 🚩 MEDIUM - potencjalne DoS

---

### 4. Duplikacja kodu w repository - _row_to_domain_user nie jest używany
**Plik:** `backend/src/app/infrastructure/db/repositories/user_repo_sqlalchemy.py`  
**Linie:** 8-48

```python
def _row_to_domain_user(user: UserDB) -> User:  # ✅ Funkcja helper
    return User(id=user.id, email=user.email, name=user.name)

class SqlAlchemyUserRepository(UserRepository):
    def get(self, user_id: str) -> Optional[User]:
        user_row = self.session.get(UserDB, user_id)
        if not user_row:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        return User(id=user_row.id, email=user_row.email, name=user_row.name)  # ❌ Duplikacja
    
    def get_by_email(self, email: str) -> Optional[User]:
        user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
        if not user_row:
            raise ValueError(UserErrors.USER_NOT_FOUND)
        return User(id=user_row.id, email=user_row.email, name=user_row.name)  # ❌ Duplikacja
```

**Problem:** Funkcja `_row_to_domain_user` istnieje ale nie jest używana w `get()` i `get_by_email()`.

**Rekomendacja:**
```python
def get(self, user_id: str) -> Optional[User]:
    user_row = self.session.get(UserDB, user_id)
    if not user_row:
        return None
    return _row_to_domain_user(user_row)  # ✅ Użyj helper

def get_by_email(self, email: str) -> Optional[User]:
    user_row = self.session.query(UserDB).filter(UserDB.email == email).first()
    if not user_row:
        return None
    return _row_to_domain_user(user_row)  # ✅ Użyj helper
```

**Priorytet:** 🚩 LOW - DRY principle

---

## 💡 SUGGESTION - Zalecane do poprawy

### 1. Brak dependency injection dla repositories w controller
**Plik:** `backend/src/app/api/http/controllers/users_controller.py:19-23`

```python
def user_repo(db: Session):
    return SqlAlchemyUserRepository(db)

def book_repo(db: Session):
    return SqlAlchemyBookRepository(db)
```

**Problem:** Funkcje helper zamiast proper dependency injection.

**Rekomendacja:** Użyj FastAPI Depends:
```python
def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(db)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    dto: CreateUserRequest,
    repo: UserRepository = Depends(get_user_repo)
):
    return CreateUserCommand(repo).run(dto)
```

---

### 2. Brak logowania w repository i commands
**Pliki:** Wszystkie commands i repositories

**Problem:** Brak logów dla operacji CRUD, trudne debugowanie.

**Rekomendacja:**
```python
import logging

logger = logging.getLogger(__name__)

class CreateUserCommand:
    def run(self, dto: CreateUserRequest) -> UserResponse:
        logger.info(f"Creating user with email: {dto.email}")
        # ...
        logger.info(f"User created with id: {user.id}")
        return UserResponse(...)
```

---

### 3. Brak testów dla nowych endpointów
**Brak plików:** `tests/integration/test_users_api.py`

**Problem:** Nowe endpointy nie mają testów integracyjnych.

**Rekomendacja:** Dodaj testy:
```python
def test_create_user_success(client, db_session):
    response = client.post("/users", json={"email": "test@test.com", "name": "Test"})
    assert response.status_code == 201
    assert response.json()["email"] == "test@test.com"

def test_create_user_duplicate_email(client, db_session):
    # Create first user
    client.post("/users", json={"email": "test@test.com", "name": "Test"})
    # Try to create duplicate
    response = client.post("/users", json={"email": "test@test.com", "name": "Test2"})
    assert response.status_code == 409
```

---

### 4. Brak paginacji w list_users - tylko limit
**Plik:** `backend/src/app/api/http/controllers/users_controller.py:40`

**Problem:** Endpoint ma tylko `limit` bez `offset` - nie można przeglądać kolejnych stron.

**Rekomendacja:**
```python
@router.get("", response_model=List[UserResponse])
def list_users(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    email_like: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return ListUsersQuery(user_repo(db)).run(limit, offset, email_like)
```

---

### 5. Inconsistent naming - owner_id vs user_id
**Plik:** `backend/src/app/api/http/controllers/users_controller.py:58`

```python
@router.get("/{user_id}/books", response_model=List[BookResponse])
def list_user_books(owner_id: str, db: Session=Depends(get_db)):  # ❌ owner_id zamiast user_id
    return GetUserBooksCommand(book_repo(db)).run(owner_id)
```

**Problem:** Path parameter to `user_id` ale argument funkcji to `owner_id`.

**Rekomendacja:**
```python
@router.get("/{user_id}/books", response_model=List[BookResponse])
def list_user_books(user_id: str, db: Session=Depends(get_db)):  # ✅ Spójne nazewnictwo
    return GetUserBooksCommand(book_repo(db)).run(user_id)
```

---

### 6. Brak docstringów w publicznych metodach
**Pliki:** Wszystkie commands, queries, repositories

**Problem:** Brak dokumentacji API.

**Rekomendacja:**
```python
class CreateUserCommand:
    """Command to create a new user in the system.
    
    Validates that email is unique before creating user.
    
    Raises:
        ValueError: If email is already in use
    """
    
    def run(self, dto: CreateUserRequest) -> UserResponse:
        """Execute user creation.
        
        Args:
            dto: User data from request
            
        Returns:
            UserResponse with created user data
            
        Raises:
            ValueError: If email already exists
        """
```

---

## 📝 NIT - Drobne uwagi

### 1. Inconsistent spacing w parametrach funkcji
**Plik:** `backend/src/app/api/http/controllers/users_controller.py`

```python
def get_user(user_id: str, db: Session=Depends(get_db)):  # ❌ Brak spacji przed =
def list_users(limit: int, email_like: Optional[str], db: Session=Depends(get_db)):  # ❌
```

**Rekomendacja:** PEP 8 - spacja przed i po `=` w default values:
```python
def get_user(user_id: str, db: Session = Depends(get_db)):  # ✅
```

---

### 2. Nieużywany import w models.py
**Plik:** `backend/src/app/infrastructure/db/models.py:2`

```python
from sqlalchemy import Column, String, Integer, Text, ForeignKey, UniqueConstraint
```

**Problem:** Wszystkie importy są używane, ale można je pogrupować.

**Rekomendacja:** Grupuj importy logicznie:
```python
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship, backref
```

---

### 3. Magic string "users" w router prefix
**Plik:** `backend/src/app/api/http/controllers/users_controller.py:18`

```python
router = APIRouter(prefix="/users", tags=["users"])  # ❌ Magic string
```

**Rekomendacja:** Wydziel do stałej:
```python
USERS_PREFIX = "/users"
USERS_TAG = "users"

router = APIRouter(prefix=USERS_PREFIX, tags=[USERS_TAG])
```

---

### 4. Brak type hint dla session w repository
**Plik:** `backend/src/app/infrastructure/db/repositories/user_repo_sqlalchemy.py:11`

```python
class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session  # ❌ Brak type hint dla self.session
```

**Rekomendacja:**
```python
class SqlAlchemyUserRepository(UserRepository):
    session: Session  # ✅ Dodaj type hint
    
    def __init__(self, session: Session):
        self.session = session
```

---

### 5. Długa linia w UserDB constructor
**Plik:** `backend/src/app/infrastructure/db/repositories/user_repo_sqlalchemy.py:16`

```python
self.session.add(UserDB(id=user.id, email=user.email, name=user.name))  # 80+ znaków
```

**Rekomendacja:** Złam linię:
```python
self.session.add(UserDB(
    id=user.id,
    email=user.email,
    name=user.name
))
```

---

## ✅ PRAISE - Co jest dobrze zrobione

### 1. **Proper layering - Clean Architecture** 🎯
Kod jest podzielony na warstwy:
- API (controllers)
- Application (commands/queries/DTOs)
- Domain (entities/ports)
- Infrastructure (repositories)

To jest **wzorcowa implementacja Clean Architecture**!

### 2. **Protocol dla Repository** 🔒
```python
class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
```
Użycie `Protocol` zamiast ABC to świetny wybór - duck typing + type safety!

### 3. **Pydantic DTOs z walidacją** ✅
```python
class CreateUserRequest(BaseModel):
    email: EmailStr  # ✅ Walidacja email
    name: Optional[str]
```
EmailStr automatycznie waliduje format email!

### 4. **Proper HTTP status codes** 📡
```python
status_code=status.HTTP_201_CREATED  # POST
status_code=status.HTTP_200_OK       # GET
status_code=status.HTTP_204_NO_CONTENT  # DELETE
```
Poprawne użycie kodów HTTP!

### 5. **Command/Query separation** 🔄
Rozdzielenie Commands (write) i Queries (read) to CQRS pattern - świetnie!

### 6. **Dependency injection** 💉
```python
db: Session = Depends(get_db)
```
Proper DI z FastAPI Depends!

### 7. **Alembic migration** 🗄️
Dodanie migracji dla chapter_number i title - profesjonalne podejście do zmian w schemacie!

---

## Akcje do podjęcia (priorytet)

### Przed mergem (BLOCKER):
1. [ ] **CRITICAL** Dodaj `return` w `create_user` endpoint
2. [ ] **CRITICAL** Napraw `get_by_email()` - zwracaj `None` zamiast rzucać wyjątek
3. [ ] **HIGH** Dodaj walidację email w `User.change_email()`

### Po mergu (MAJOR):
4. [ ] Ujednolicić error handling w repository (Optional vs ValueError)
5. [ ] Przenieść commit z repository do Command/Query
6. [ ] Dodać walidację parametrów w `list_users` (limit: 1-100)
7. [ ] Użyć `_row_to_domain_user` helper w `get()` i `get_by_email()`

### Nice to have (SUGGESTION/NIT):
8. [ ] Dodać proper dependency injection dla repositories
9. [ ] Dodać logowanie w commands i repositories
10. [ ] Dodać testy integracyjne dla endpointów
11. [ ] Dodać paginację (offset) w `list_users`
12. [ ] Naprawić inconsistent naming (owner_id → user_id)
13. [ ] Dodać docstringi
14. [ ] Poprawić spacing w parametrach funkcji (PEP 8)

---

## Statystyki

- **Pliki zmienione:** 22
- **Nowe endpointy:** 6 (POST, GET, GET list, PUT, DELETE, GET books)
- **Nowe commands:** 4
- **Nowe queries:** 2
- **Nowe repositories:** 2
- **Nowe DTOs:** 3
- **Migracje:** 1

---

## Rekomendacja

**Status:** ⚠️ **APPROVE WITH CRITICAL CHANGES**

Branch ma solidną architekturę ale zawiera 3 BLOCKER-y które **muszą** być naprawione:
1. Brak return w create_user
2. Nieprawidłowa logika get_by_email
3. Brak walidacji email

Po poprawieniu BLOCKER-ów można mergować. MAJOR issues można naprawić w kolejnym PR.

---

*Review wykonane zgodnie z wytycznymi z `CODE_REVIEW_GUIDELINES.md`*
