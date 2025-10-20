import pytest
from app.domain.entities.annotation_set import AnnotationSet
from app.domain.value_objects.annotation_status import AnnotationStatus
from app.domain.errors import AnnotationSetErrors

def test_annotation_set_right_path():
    annotation_set = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")
    assert annotation_set.status == AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX

    annotation_set.mark_translated()
    assert annotation_set.status == AnnotationStatus.TRANSLATED

    annotation_set.mark_reviewed()
    assert annotation_set.status == AnnotationStatus.REVIEWED

    annotation_set.mark_applied()
    assert annotation_set.status == AnnotationStatus.APPLIED

def test_invalid_transitions_raise():
    annotation_set1 = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")

    with pytest.raises(ValueError) as e1:
        annotation_set1.mark_reviewed()
    assert AnnotationSetErrors.MUST_BE_TRANSLATED_BEFORE_REVIEWED in str(e1.value)

    annotation_set2 = AnnotationSet(id="a2", book_id="b1", file_path="/tmp/y.xlsx")
    with pytest.raises(ValueError) as e2:
        annotation_set2.mark_applied()
    assert AnnotationSetErrors.MUST_BE_REVIEWED_BEFORE_APPLIED in str(e2.value)