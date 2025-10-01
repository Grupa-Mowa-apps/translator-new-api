import pytest
from app.domain.entities.annotation_set import AnnotationSet
from app.domain.value_objects.annotation_status import AnnotationStatus
from app.domain.errors import AnnotationSetErrors

def test_annotation_set_right_path():
    a = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")
    assert a.status == AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX

    a.mark_translated()
    assert a.status == AnnotationStatus.TRANSLATED

    a.mark_reviewed()
    assert a.status == AnnotationStatus.REVIEWED

    a.mark_applied()
    assert a.status == AnnotationStatus.APPLIED

def test_invalid_transitions_raise():
    a = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")

    with pytest.raises(ValueError) as e1:
        a.mark_reviewed()
    assert AnnotationSetErrors.MUST_BE_TRANSLATED_BEFORE_REVIEWED in str(e1.value)

    a2 = AnnotationSet(id="a2", book_id="b1", file_path="/tmp/y.xlsx")
    with pytest.raises(ValueError) as e2:
        a2.mark_applied()
    assert AnnotationSetErrors.MUST_BE_REVIEWED_BEFORE_APPLIED in str(e2.value)