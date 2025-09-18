from enum import Enum

class QuotesStatus(str, Enum):
    """QuotesStatus w domysle Quotes i Footnotes"""
    DRAFT = "draft"   # excel powstal i jest pusty (czy to jest potrzebne??)
    EXTRACTED = "extracted"   # cytaty&przypisy zostaly zaciagniete z .md do .xlsx
    TRANSLATED = "translated"   # tlumaczenia zostaly wprowadzone
    REVIEWED = "reviewed"   # tlumaczenia zostaly zaakceptowane przez druga osobe (??obstawiam ze redakcja cytatow&przypisow jest, ale trzebaby sie zapytac tlumaczek)
    APPLIED = "applied"   # tlumaczenia zostaly wstrzykniete do .md