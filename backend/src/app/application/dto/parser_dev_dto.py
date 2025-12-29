# app/application/dto/parser_dev_dto.py
from pydantic import BaseModel

class ParserExportResponse(BaseModel):
    excel_path: str
    stats: dict

class ParserApplyResponse(BaseModel):
    output_md_path: str