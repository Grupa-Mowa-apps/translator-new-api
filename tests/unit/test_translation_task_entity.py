import pytest
from app.domain.entities.translation_task import TranslationTask
from app.domain.value_objects.translation_status import TranslationStatus
from app.domain.errors import TranslationTaskErrors

def test_task_right_path_progress():
    translation_task = TranslationTask(id="t1", book_id="b1", total_chapters=10)
    assert translation_task.status == TranslationStatus.QUEUED

    translation_task.start_translation_task()
    assert translation_task.status == TranslationStatus.IN_PROGRESS
    assert translation_task.progress == 0

    translation_task.update_progress(30, "ok", translated_chapters=3)
    assert translation_task.progress == 30
    assert translation_task.translated_chapters == 3
    assert translation_task.message == "ok"

    translation_task.update_progress(10)
    assert translation_task.progress == 30

    translation_task.complete_task("done")
    assert translation_task.status == TranslationStatus.DONE
    assert translation_task.progress == 100
    assert translation_task.message == "done"

def test_invalid_flows():
    translation_task = TranslationTask(id="t2", book_id="b1")

    with pytest.raises(ValueError) as e1:
        translation_task.update_progress(10)
    assert TranslationTaskErrors.PROGRESS_ONLY_IN_PROGRESS in str(e1.value)

    with pytest.raises(ValueError) as e2:
        translation_task.complete_task()
    assert TranslationTaskErrors.MUST_BE_IN_PROGRESS_BEFORE_DONE in str(e2.value)

    translation_task.start_translation_task()
    translation_task.complete_task()
    with pytest.raises(ValueError) as e3:
        translation_task.cancel("nope")
    assert TranslationTaskErrors.CANNOT_CANCEL_FINISHED in str(e3.value)

def test_reset_progress_and_cancel():
    translation_task = TranslationTask(id="t3", book_id="b1", total_chapters=5)
    translation_task.start_translation_task()
    translation_task.update_progress(50, translated_chapters=2)

    translation_task.reset_progress(new_total_chapters=7, msg="Reset")
    assert translation_task.status == TranslationStatus.QUEUED
    assert translation_task.progress == 0
    assert translation_task.translated_chapters == 0
    assert translation_task.total_chapters == 7
    assert translation_task.message == "Reset"

    translation_task.cancel("bye")
    assert translation_task.status == TranslationStatus.CANCELED
    assert translation_task.message == "bye"

def test_fail_from_any_state():
    translation_task = TranslationTask(id="t4", book_id="b1")
    translation_task.fail("error")
    assert translation_task.status == TranslationStatus.FAILED
    assert translation_task.message == "error"

def test_progress_boundaries():
    translation_task = TranslationTask(id="t5", book_id="b1")
    translation_task.start_translation_task()
    
    translation_task.update_progress(150)
    assert translation_task.progress == 100
    
    translation_task.update_progress(-10)
    assert translation_task.progress == 100

def test_cannot_start_twice():
    translation_task = TranslationTask(id="t6", book_id="b1")
    translation_task.start_translation_task()
    
    with pytest.raises(ValueError):
        translation_task.start_translation_task()