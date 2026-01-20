import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.infrastructure.db.models import FailedAnnotationApplicationDB


class FailedAnnotationApplicationRepoSQLAlchemy:
    def __init__(self, session: Session):
        self.session = session
    
    def save_batch(self, annotation_set_id: str, failed_list: list[dict]):
        for item in failed_list:
            db_obj = FailedAnnotationApplicationDB(
                id=str(uuid.uuid4()),
                annotation_set_id=annotation_set_id,
                type=item["type"],
                original_text=item["original_text"],
                translation=item["translation"],
                created_at=datetime.utcnow().isoformat()
            )
            self.session.add(db_obj)
        self.session.commit()
    
    def get_by_annotation_set(self, annotation_set_id: str) -> list[FailedAnnotationApplicationDB]:
        return self.session.query(FailedAnnotationApplicationDB)\
            .filter_by(annotation_set_id=annotation_set_id)\
            .all()
    
    def delete_by_annotation_set(self, annotation_set_id: str):
        self.session.query(FailedAnnotationApplicationDB)\
            .filter_by(annotation_set_id=annotation_set_id)\
            .delete()
        self.session.commit()
