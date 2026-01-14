class TranslationTaskErrors:
    CANNOT_START_FROM_STATUS = "Cannot start from status {status}"
    PROGRESS_ONLY_IN_PROGRESS = "Progress can be updated only when IN_PROGRESS"
    MUST_BE_IN_PROGRESS_BEFORE_DONE = "Must be IN_PROGRESS before DONE"
    CANNOT_CANCEL_FINISHED = "Cannot cancel a finished task"

class AnnotationSetErrors:
    MUST_BE_EXTRACTED_BEFORE_TRANSLATED = "Must be EXTRACTED before TRANSLATED"
    MUST_BE_TRANSLATED_BEFORE_REVIEWED = "Must be TRANSLATED before REVIEWED"
    MUST_BE_REVIEWED_BEFORE_APPLIED = "Must be REVIEWED before APPLIED"
    ANNOTATION_SET_NOT_FOUND_FOR_BOOK = "Annotation set not found for the book"
    ANNOTATION_SET_NOT_FOUND = "There is no annotaation set with such id"

class UserErrors:
    EMAIL_CANNOT_BE_EMPTY = "Email cannot be empty"
    INVALID_EMAIL_FORMAT = "Invalid email format"
    EMAIL_ALREADY_IN_USE = "This email is already in use"
    NAME_CANNOT_BE_AN_EMPTY_STRING = "Username cannot be an empty string"
    USER_NOT_FOUND = "There is no user with such id"

class BookErrors:
    TITLE_CANNOT_BE_EMPTY = "Title cannot be empty"
    GENRE_CANNOT_BE_EMPTY = "Genre cannot be empty"
    BOOK_NOT_FOUND = "There is no book with such id"
    BOOK_FILE_PATH_NOT_SET = "Book file path is not set"
    BOOK_FILE_PATH_NOT_SET = "Book file path is not set"
    TITLE_ALREADY_EXISTS = "Book with this title already exists"
    FILE_NOT_FOUND = "Book file not found"
    BOOK_MAPPING_FAILED = "Book mapping failed"

class ChapterErrors:
    CHAPTER_NOT_FOUND = "Chapter not found"

class FileErrors:
    FILENAME_CANNOT_BE_EMPTY = "Filename cannot be empty"
    PATH_CANNOT_BE_EMPTY = "Path cannot be empty"
    OWNER_ID_CANNOT_BE_EMPTY = "Owner id cannot be empty"
    BOOK_ID_CANNOT_BE_EMPTY = "Book id cannot be empty"
    INVALID_FILE_KIND = "Invalid file kind"
    FILE_NOT_FOUND = "File not found"
    INVALID_STORAGE_PATH = "Invalid storage path"

class QuoteTypeErrors:
    INVALID_QUOTE_TYPE = "Invalid quote type"

class LLMErrors:
    LLM_REQUEST_FAILED = "LLM request failed"
    NO_CHOICES_IN_LLM_RESPONSE = "No choices in LLM response"