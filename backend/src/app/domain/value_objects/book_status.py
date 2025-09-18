from enum import Enum

class BookStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSED = "parsed"   # mamy excela z wyciagnietymi cytatami&przypisami
    READY_TO_TRANSLATE = "ready_to_translate"   # albo mamy excela z gotowymi tlumaczeniami, albo nie, w kazdym razie jestesmy gotowi do tlumaczenia ksiazki
    IN_TRANSLATION = "in_translation"
    TRANSLATED = "translated"
    FAILED = "failed"