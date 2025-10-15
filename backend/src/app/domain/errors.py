class TranslationTaskErrors:
    CANNOT_START_FROM_STATUS = "Cannot start from status {status}"
    PROGRESS_ONLY_IN_PROGRESS = "Progress can be updated only when IN_PROGRESS"
    MUST_BE_IN_PROGRESS_BEFORE_DONE = "Must be IN_PROGRESS before DONE"
    CANNOT_CANCEL_FINISHED = "Cannot cancel a finished task"

class AnnotationSetErrors:
    MUST_BE_EXTRACTED_BEFORE_TRANSLATED = "Must be EXTRACTED before TRANSALTED"
    MUST_BE_TRANSLATED_BEFORE_REVIEWED = "Must be TRANSLATED before REVIEWED"
    MUST_BE_REVIEWED_BEFORE_APPLIED = "Must be TRANSLATED before APPLIED"

class UserErrors:
    EMAIL_CANNOT_BE_EMPTY = "Email cannot be empty"
    EMAIL_ALREADY_IN_USE = "This email is already in use"
    USER_NOT_FOUND = "There is no user with such id"