import pytest
from app.domain.entities.translation_task import TranslationTask
from app.domain.value_objects.translation_status import TranslationStatus
from app.domain.errors import TranslationTaskErrors

def test_task_right_path_progress():
    t = TranslationTask(id="t1", book_id="b1", total_chapters=10)
    assert t.status == TranslationStatus.QUEUED

    t.start_translation_task()
    assert t.status == TranslationStatus.IN_PROGRESS
    assert t.progress == 0

    t.update_progress(30, "ok", translated_chapters=3)
    assert t.progress == 30
    assert t.translated_chapters == 3
    assert t.message == "ok"

    t.update_progress(10)
    assert t.progress == 30

    t.complete_task("done")
    assert t.status == TranslationStatus.DONE
    assert t.progress == 100
    assert t.message == "done"

def test_invalid_flows():
    t = TranslationTask(id="t2", book_id="b1")

    with pytest.raises(ValueError) as e1:
        t.update_progress(10)
    assert TranslationTaskErrors.PROGRESS_ONLY_IN_PROGRESS in str(e1.value)

    with pytest.raises(ValueError) as e2:
        t.complete_task()
    assert TranslationTaskErrors.MUST_BE_IN_PROGRESS_BEFORE_DONE in str(e2.value)

    t.start_translation_task()
    t.complete_task()
    with pytest.raises(ValueError) as e3:
        t.cancel("nope")
    assert TranslationTaskErrors.CANNOT_CANCEL_FINISHED in str(e3.value)

def test_reset_progress_and_cancel():
    t = TranslationTask(id="t3", book_id="b1", total_chapters=5)
    t.start_translation_task()
    t.update_progress(50, translated_chapters=2)

    t.reset_progress(new_total_chapters=7, msg="Reset")
    assert t.status == TranslationStatus.QUEUED
    assert t.progress == 0
    assert t.translated_chapters == 0
    assert t.total_chapters == 7
    assert t.message == "Reset"

    t.cancel("bye")
    assert t.status == TranslationStatus.CANCELED
    assert t.message == "bye"