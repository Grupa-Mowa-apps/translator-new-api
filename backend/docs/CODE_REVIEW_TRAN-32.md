# CODE REVIEW: TRAN-32 Files Endpoints

**Branch**: TRAN-32-files-endpoints  
**Reviewer**: Amazon Q  
**Date**: 2024  
**Scope**: File entity, repository, commands, queries, API endpoints

---

## BLOCKER Issues

### 1. **Inconsistent import paths in File entity**
**File**: `backend/src/app/domain/entities/file.py`  
**Lines**: 4-5  
**Issue**: Mixed import styles - uses `app.domain.*` and `domain.*`
```python
from app.domain.value_objects.file_kind import FileKind
from domain.constants import INITIAL_VERSION  # <- should be app.domain
from domain.errors import FileErrors  # <- should be app.domain
```
**Impact**: Import errors, inconsistent with codebase standard  
**Fix**: Change to `from app.domain.constants` and `from app.domain.errors`

---

### 2. **Repository violates Unit of Work pattern - commit in repository**
**File**: `backend/src/app/infrastructure/db/repositories/file_repo_sqlalchemy.py`  
**Lines**: 25, 44, 51  
**Issue**: Repository calls `self.session.commit()` directly
```python
def add(self, file: File) -> None:
    file_row = _domain_to_row_file(file)
    self.session.add(file_row)
    self.session.commit()  # <- BLOCKER: commit should be in Command layer
```
**Impact**: Violates established pattern from TRAN-29, breaks transaction control  
**Fix**: Remove all `commit()` calls from repository, add to Command layer

---

### 3. **Repository get() raises exception instead of returning None**
**File**: `backend/src/app/infrastructure/db/repositories/file_repo_sqlalchemy.py`  
**Line**: 30  
**Issue**: Violates established pattern - get() should return `Optional[File]`
```python
def get(self, file_id: str) -> Optional[File]:
    file_row = self.session.get(FileDB, file_id)
    if not file_row:
        raise ValueError(FileErrors.FILE_NOT_FOUND)  # <- BLOCKER
    return _row_to_domain_file(file_row)
```
**Impact**: Inconsistent with UserRepository pattern from TRAN-29  
**Fix**: Return `None` when not found, handle in Command/Query layer

---

### 4. **Bug in File.rename() - assigns to wrong attribute**
**File**: `backend/src/app/domain/entities/file.py`  
**Line**: 25  
**Issue**: Assigns to `self.title` instead of `self.filename`
```python
def rename(self, new_filename: str) -> None:
    if not new_filename or not new_filename.strip():
        raise ValueError(FileErrors.FILENAME_CANNOT_BE_EMPTY)
    self.title = new_filename.strip()  # <- BLOCKER: should be self.filename
    self._update_version()
```
**Impact**: Critical bug - attribute doesn't exist, will crash  
**Fix**: Change to `self.filename = new_filename.strip()`

---

### 5. **Typo in FileKind enum value**
**File**: `backend/src/app/domain/value_objects/file_kind.py`  
**Line**: 6  
**Issue**: Typo "TRANSALTED" instead of "TRANSLATED"
```python
TRANSALTED_MARKDOWN = "translated_md"  # <- BLOCKER: typo
```
**Impact**: Wrong enum name, inconsistent naming  
**Fix**: Rename to `TRANSLATED_MARKDOWN`

---

## MAJOR Issues

### 6. **Missing commit in Commands**
**Files**: `upload_file.py`, `delete_file.py`  
**Issue**: Commands don't call `commit()` after repository operations
```python
def run(self, dto: UploadFileRequest) -> FileResponse:
    # ... create file
    self.repo.add(file)
    # <- MAJOR: missing self.repo.session.commit() or similar
    return FileResponse(...)
```
**Impact**: Changes won't be persisted to database  
**Fix**: Add commit after repository operations in Command layer

---

### 7. **Missing logging in Commands**
**Files**: All command files  
**Issue**: No logging for important operations (upload, delete)
**Impact**: No audit trail, hard to debug  
**Fix**: Add logging like in TRAN-29 commands

---

### 8. **Controller endpoint has unused file upload**
**File**: `file_controller.py`  
**Line**: 20-22  
**Issue**: Reads file content but never uses it
```python
async def upload_file(dto: UploadFileRequest, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()  # <- MAJOR: read but never used
    return UploadFileCommand(file_repo(db)).run(dto)
```
**Impact**: Misleading code, file upload doesn't actually work  
**Fix**: Either use content or remove UploadFile parameter

---

### 9. **Missing type hints in File entity methods**
**File**: `file.py`  
**Lines**: 54, 60  
**Issue**: `__repr__` and `__str__` missing return type hints
```python
def __repr__(self):  # <- should be -> str
def __str__(self):   # <- should be -> str
```
**Impact**: Inconsistent with other entities (User, Chapter)  
**Fix**: Add `-> str` return type hints

---

### 10. **Repository methods raise exceptions inconsistently**
**File**: `file_repo_sqlalchemy.py`  
**Lines**: 36, 48  
**Issue**: `update()` and `delete()` raise exceptions, but should follow get() pattern
**Impact**: Inconsistent error handling across repository  
**Fix**: Make consistent - either all raise or all return None

---

### 11. **Missing validation in UploadFileCommand**
**File**: `upload_file.py`  
**Issue**: No validation for dto fields (owner_id, filename, kind)
**Impact**: Can create invalid File entities  
**Fix**: Add validation before creating File entity

---

### 12. **Duplicate file_id generation**
**File**: `upload_file.py`  
**Lines**: 12-13  
**Issue**: Generates `file_id` but then generates another `uuid.uuid4().hex` for File.id
```python
file_id = uuid.uuid4().hex
file_path = f"{file_id}/{dto.filename}/{dto.kind}"
file = File(
    id=uuid.uuid4().hex,  # <- MAJOR: different ID than in path
```
**Impact**: Path contains different ID than entity  
**Fix**: Use same `file_id` for both

---

## SUGGESTION Issues

### 13. **FileRepository has unclear methods**
**File**: `file_repository.py`  
**Lines**: 11-12  
**Issue**: Methods `save()` and `open()` are unclear and not implemented
```python
def save(self, destination_name: str) -> str: ...
def open(self, path: str) -> str: ...
```
**Suggestion**: Remove if not needed, or clarify purpose and implement

---

### 14. **Missing tests for File entity**
**Issue**: No unit tests for File entity methods  
**Suggestion**: Add tests like `test_file_entity.py` covering validation, version updates

---

### 15. **Missing integration tests for file endpoints**
**Issue**: No integration tests for file API endpoints  
**Suggestion**: Add `test_files_api.py` similar to `test_users_api.py`

---

### 16. **File.detach_from_book() doesn't update version**
**File**: `file.py`  
**Line**: 47  
**Issue**: Doesn't call `_update_version()` like other methods
```python
def detach_from_book(self) -> None:
    self.book_id = None
    # <- SUGGESTION: add self._update_version()
```
**Suggestion**: Add version update for consistency

---

### 17. **Missing pagination in list queries**
**File**: `list_files.py`  
**Issue**: Has `limit` but no `offset` parameter  
**Suggestion**: Add offset for proper pagination like in ListUsersQuery

---

### 18. **Controller path parameter mismatch**
**File**: `file_controller.py`  
**Line**: 32  
**Issue**: Path says `/by-owner/{book_id}` but parameter is `owner_id`
```python
@router.get("/by-owner/{book_id}", ...)  # <- should be {owner_id}
def list_files_for_owner(owner_id: str, ...):
```
**Suggestion**: Fix path to `/by-owner/{owner_id}`

---

### 19. **Missing validation for limit parameter**
**File**: `file_controller.py`  
**Issue**: No validation for limit (should be 1-100 like in users_controller)  
**Suggestion**: Add Query validation: `limit: int = Query(10, ge=1, le=100)`

---

## NIT Issues

### 20. **Inconsistent spacing in File entity**
**File**: `file.py`  
**Line**: 16  
**Issue**: Extra space in `book_id: Optional[str] = None`  
**Nit**: Remove extra space for consistency

---

### 21. **Missing docstrings**
**Files**: All new files  
**Nit**: Consider adding docstrings for complex methods

---

## PRAISE

### ✓ **Good separation of concerns**
File entity, repository, commands, queries properly separated

### ✓ **Follows Clean Architecture**
Proper layering: API → Application → Domain → Infrastructure

### ✓ **Alembic migration included**
Database schema changes properly versioned

### ✓ **FileKind enum for type safety**
Good use of enum instead of strings

---

## Summary

**BLOCKER**: 5 issues - MUST fix before merge  
**MAJOR**: 7 issues - SHOULD fix before merge  
**SUGGESTION**: 7 issues - Consider fixing  
**NIT**: 2 issues - Optional

**Critical Issues**:
1. Import inconsistencies (BLOCKER #1)
2. Repository pattern violations (BLOCKER #2, #3)
3. Critical bug in rename() (BLOCKER #4)
4. Missing commits in Commands (MAJOR #6)
5. Unused file upload (MAJOR #8)

**Recommendation**: Fix all BLOCKER and MAJOR issues before merging to develop.
