from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.annotation_set import AnnotationSet
from app.domain.ports.annotation_set_repository import AnnotationSetRepository
from app.infrastructure.db.models import AnnotationSetDB
from app.domain.value_objects.annotation_status import AnnotationStatus
from app.domain.errors import AnnotationSetErrors

def _to_domain(annotation_model: AnnotationSetDB) -> AnnotationSet:
    return AnnotationSet(
        id=annotation_model.id,
        book_id=annotation_model.book_id,
        file_path=annotation_model.file_path,
        status=annotation_model.status,
        version=annotation_model.version,
    )

def _to_orm(annotation_entity: AnnotationSet) -> AnnotationSetDB:
    return AnnotationSetDB(
        id=annotation_entity.id,
        book_id=annotation_entity.book_id,
        file_path=annotation_entity.file_path,
        status=str(annotation_entity.status),
        version=annotation_entity.version,
    )

class SqlAlchemyAnnotationSetRepository(AnnotationSetRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def add(self, annotation_set: AnnotationSet) -> None:
        annotation_row = _to_orm(annotation_set)
        self.session.add(annotation_row)

    def get(self, annotation_set_id: str) -> Optional[AnnotationSet]:
        annotation_row = self.session.get(AnnotationSetDB, annotation_set_id)
        if annotation_row is None:
            raise ValueError(AnnotationSetErrors.ANNOTATION_SET_NOT_FOUND)
        return _to_domain(annotation_row)

    def get_by_file_path(self, file_path: str) -> Optional[AnnotationSet]:
        annotation_row = self.session.query(AnnotationSetDB).filter(AnnotationSetDB.file_path == file_path).first()
        if annotation_row is None:
            raise ValueError(AnnotationSetErrors.ANNOTATION_SET_NOT_FOUND)
        return _to_domain(annotation_row)

    def update(self, annotation_set: AnnotationSet) -> bool:
        annotation_row = self.session.get(AnnotationSetDB, annotation_set.id)

        if annotation_row is None:
            raise ValueError(AnnotationSetErrors.ANNOTATION_SET_NOT_FOUND)

        annotation_row.book_id = annotation_set.book_id
        annotation_row.file_path = annotation_set.file_path
        annotation_row.status = str(annotation_set.status)
        annotation_row.version = annotation_set.version

        return True

    def delete(self, annotation_set: AnnotationSet) -> bool:
        annotation_row = self.session.get(AnnotationSetDB, annotation_set.id)

        if annotation_row is None:
            raise ValueError(AnnotationSetErrors.ANNOTATION_SET_NOT_FOUND)
        
        self.session.delete(annotation_row)
        return True
    
    def list_for_book(self, book_id: str) -> List[AnnotationSet]:
        annotation_rows = self.session.query(AnnotationSetDB).filter(AnnotationSetDB.book_id == book_id)
        return [_to_domain(annotation_model=annotation_row) for annotation_row in annotation_rows]
