from pathlib import Path
from typing import Any
import pandas as pd
from typing import Optional, Tuple, Dict

from app.domain.ports.excel_quotes_footnotes import ExcelQuotesFootnotesPort
from app.domain.ports.markdown_analyzer import MarkdownAnalyzerPort
from app.domain.value_objects.quotation_marks import QuoteType

from app.domain.services.parser.parser_extraction import (
    build_footnotes_dict,
    extract_quotes_with_related_footnotes,
    extract_blockquotes,
)

from app.domain.services.parser.footnotes_inserter import apply_footnotes_translations_with_report
from app.domain.services.parser.quotes_inserter import apply_quotes_translations_with_report
from app.domain.services.parser.blockquotes_inserter import apply_blockquotes_translations_with_report

from app.domain.constants import PARSER_COLUMNS
from app.infrastructure.parsing.markdown_analyzer_adapter import MarkdownAnalyzerAdapter

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


class ParserAdapter(ExcelQuotesFootnotesPort):
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def export_from_markdown(
        self,
        md_path: str,
        quote_type: QuoteType,
        excel_path: str | None = None,
    ) -> tuple[str, dict]:
        md_path = self._resolve_path(path=md_path)

        analyzer = MarkdownAnalyzerAdapter(file_path=str(md_path))
        md_text = analyzer.load_text()
        headers = analyzer.identify_headers()
        footnotes_raw = analyzer.identify_footnotes()

        footnotes_dict = build_footnotes_dict(footnotes_raw=footnotes_raw)

        quotes_pl, related_footnotes = extract_quotes_with_related_footnotes(
            markdown_text=md_text,
            headers=headers,
            quote_type=quote_type,
            footnotes_dict=footnotes_dict,
        )
        blockquotes_pl = extract_blockquotes(markdown_text=md_text)

        footnote_items = list(footnotes_dict.items())

        df_footnotes = pd.DataFrame(
            [{"footnote number": k, "footnotes PL": v, "footnotes EN": ""} for k, v in footnote_items]
        )
        df_quotes = pd.DataFrame(
            [{"quotes PL": q, "przypis powiązany": (fn or ""), "quotes EN": ""} for q, fn in zip(quotes_pl, related_footnotes)]
        )
        df_blockquotes = pd.DataFrame(
            [{"blockquotes PL": bq, "blockquotes EN": ""} for bq in blockquotes_pl]
        )

        max_len = max(len(df_footnotes), len(df_quotes), len(df_blockquotes), 1)
        df_footnotes = df_footnotes.reindex(range(max_len)).fillna("")
        df_quotes = df_quotes.reindex(range(max_len)).fillna("")
        df_blockquotes = df_blockquotes.reindex(range(max_len)).fillna("")

        df_final = pd.concat([df_footnotes, df_quotes, df_blockquotes], axis=1)
        for c in PARSER_COLUMNS:
            if c not in df_final.columns:
                df_final[c] = ""
        df_final = df_final[PARSER_COLUMNS]

        out_dir = self.base_dir / "exports"
        out_dir.mkdir(parents=True, exist_ok=True)

        filename = excel_path or f"{md_path.stem}_quotes_footnotes.xlsx"
        out_path = out_dir / filename

        text_cols = df_final.select_dtypes(include=["object"]).columns
        df_final[text_cols] = df_final[text_cols].map(self._clean_text_for_excel_cell)

        df_final.to_excel(out_path, index=False)

        stats = {"footnotes": len(footnotes_dict), "quotes": len(quotes_pl), "blockquotes": len(blockquotes_pl)}
        return str(out_path), stats
    
    def apply_translations_from_excel(
            self, 
            excel_path: str,
            md_input_path: str, 
            md_output_path: Optional[str] = None
    ) -> tuple[str, list[dict]]:
        excel_path = self._resolve_path(excel_path)
        md_input_path = self._resolve_path(md_input_path)

        df = pd.read_excel(excel_path)

        quotes = {}
        for _, r in df.iterrows():
            pl = str(r.get("quotes PL", "")).strip()
            en = str(r.get("quotes EN", "")).strip()
            if pl and en and pl.lower() != "nan" and en.lower() != "nan":
                quotes[pl] = en

        blockquotes = {}
        for _, r in df.iterrows():
            pl = str(r.get("blockquotes PL", "")).strip()
            en = str(r.get("blockquotes EN", "")).strip()
            if pl and en and pl.lower() != "nan" and en.lower() != "nan":
                blockquotes[pl] = en

        footnotes = {}
        for _, r in df.iterrows():
            fid = r.get("footnote number", "")
            pl = str(r.get("footnotes PL", "")).strip()
            en = str(r.get("footnotes EN", "")).strip()
            if str(fid).strip() and pl and en:
                footnotes[(str(fid).strip(), pl)] = en

        md_text = md_input_path.read_text(encoding="utf-8")

        all_failed = []

        md_text, _, failed_footnotes = apply_footnotes_translations_with_report(md_text, footnotes)
        all_failed.extend(failed_footnotes)

        md_text, _, failed_quotes = apply_quotes_translations_with_report(md_text, quotes)
        all_failed.extend(failed_quotes)

        md_text, _, failed_blockquotes = apply_blockquotes_translations_with_report(md_text, blockquotes)
        all_failed.extend(failed_blockquotes)

        out_dir = self.base_dir / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)

        out_name = md_output_path or f"{md_input_path.stem}_REPLACED.md"
        if not out_name.lower().endswith(".md"):
            out_name += ".md"
        out_path = out_dir / out_name
        out_path.write_text(md_text, encoding="utf-8")

        return str(out_path), all_failed
    
    def _resolve_path(self, path: str | Path) -> Path:
        p = Path(path)
        if p.is_absolute():
            return p
        return (self.base_dir / p).resolve()

    def _clean_text_for_excel_cell(self, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        sanitized = value.replace("\v", "\n")
        sanitized = sanitized.replace("\r\n", "\n").replace("\r", "\n")
        sanitized = ILLEGAL_CHARACTERS_RE.sub("", sanitized)
        return sanitized
