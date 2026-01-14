import pytest
from app.domain.entities.annotation_set import AnnotationSet
from app.domain.value_objects.annotation_status import AnnotationStatus
from app.domain.errors import AnnotationSetErrors

def test_annotation_set_right_path():
    annotation_set = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")
    assert annotation_set.status == AnnotationStatus.EXTRACTED_FROM_MD_TO_XLSX

    annotation_set.mark_translated()
    assert annotation_set.status == AnnotationStatus.TRANSLATED

    annotation_set.mark_applied()
    assert annotation_set.status == AnnotationStatus.APPLIED

def test_invalid_transitions_raise():
    annotation_set1 = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")

    with pytest.raises(ValueError) as e1:
        annotation_set1.mark_applied()
    assert AnnotationSetErrors.MUST_BE_TRANSLATED_BEFORE_APPLIED in str(e1.value)

def test_version_increments_on_status_changes():
    annotation_set = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")
    initial_version = annotation_set.version
    
    annotation_set.mark_translated()
    assert annotation_set.version == initial_version + 1
    
    annotation_set.mark_applied()
    assert annotation_set.version == initial_version + 2

def test_cannot_mark_translated_twice():
    annotation_set = AnnotationSet(id="a1", book_id="b1", file_path="/tmp/x.xlsx")
    annotation_set.mark_translated()
    
    with pytest.raises(ValueError):
        annotation_set.mark_translated()