from io import BytesIO
import pandas as pd
from app.infrastructure.db.repositories.failed_annotation_application_repo_sqlalchemy import FailedAnnotationApplicationRepoSQLAlchemy


class FailedAnnotationApplicationService:
    def __init__(self, repo: FailedAnnotationApplicationRepoSQLAlchemy):
        self.repo = repo
    
    def save_batch(self, annotation_set_id: str, failed_list: list[dict]):
        if not failed_list:
            return
        self.repo.save_batch(annotation_set_id, failed_list)
    
    def export_to_excel(self, annotation_set_id: str) -> BytesIO:
        failed_list = self.repo.get_by_annotation_set(annotation_set_id)
        
        data = [{
            "Type": self._format_type(f.type),
            "Original Text (PL)": f.original_text,
            "Translation (EN)": f.translation
        } for f in failed_list]
        
        df = pd.DataFrame(data)
        
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
    
    def _format_type(self, type_value: str) -> str:
        """Formatuje typ zgodnie ze wzorcem: quote -> Quote, blockquote -> BlockQuote"""
        if type_value.lower() == "blockquote":
            return "BlockQuote"
        return type_value.capitalize()
