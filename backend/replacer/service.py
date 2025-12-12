import pandas as pd
import re
from typing import Dict, Tuple, List
from pathlib import Path


class QuoteReplacer:
    """Service for replacing quotes in Markdown files"""
    
    def __init__(self, md_text: str, excel_data: pd.DataFrame):
        self.md_text = md_text
        self.excel_data = excel_data
        self.successful = []
        self.failed = []
    
    def _normalize(self, text: str) -> str:
        """Normalize text for matching - same as Excel extraction"""
        text = text.strip()
        text = re.sub(r'\\([\\[\]()*_{}~`>#+\-.!|=])', r'\1', text)  # Remove backslashes
        # DON'T replace \xa0 - Excel keeps it!
        return text.lower()
    
    def _load_translations(self, column_pl: str, column_en: str) -> Dict[str, str]:
        """Load PL→EN translation pairs from Excel"""
        if column_pl not in self.excel_data.columns or column_en not in self.excel_data.columns:
            return {}
        
        pairs = {}
        for _, row in self.excel_data.iterrows():
            orig = row.get(column_pl, '')
            trans = row.get(column_en, '')
            
            if pd.isna(orig) or pd.isna(trans):
                continue
            
            orig = str(orig).strip()
            trans = str(trans).strip()
            
            if orig and trans:
                normalized = self._normalize(orig)
                pairs[normalized] = (orig, trans)
        
        return pairs
    
    def replace_quotes(self) -> Tuple[str, List[dict], List[dict]]:
        """Replace quotes - all quote types"""
        translations = self._load_translations('quotes PL', 'quotes EN')
        
        if not translations:
            return self.md_text, [], []
        
        # All quote patterns from quotes_processing.py (fr + ge)
        patterns = [
            r'"(.*?)"',
            r"'(.*?)'",
            r'“(.*?)”',
            r'„(.*?)”',
            r'‚(.*?)’',
            r'‘(.*?)’',
            r'«(.*?)»',
            r'»(.*?)«',
            r'‹(.*?)›',
        ]
        
        replacements = []
        
        for pattern in patterns:
            for match in re.finditer(pattern, self.md_text, re.DOTALL):
                content = match.group(1).strip()
                content_cleaned = re.sub(r'\\([\\[\]()*_{}~`>#+\-.!|=])', r'\1', content)
                normalized = self._normalize(content_cleaned)
                
                if normalized in translations:
                    original, translation = translations[normalized]
                    opening = match.group(0)[0]
                    closing = match.group(0)[-1]
                    replacement = f"{opening}{translation}{closing}"
                    
                    replacements.append({
                        'start': match.start(),
                        'end': match.end(),
                        'replacement': replacement,
                        'original': original,
                        'translation': translation
                    })
        
        # Apply replacements from end to start
        replacements.sort(key=lambda x: x['start'], reverse=True)
        
        for repl in replacements:
            self.md_text = self.md_text[:repl['start']] + repl['replacement'] + self.md_text[repl['end']:]
            self.successful.append({
                'type': 'quote',
                'original_text': repl['original'],
                'translation': repl['translation'],
                'occurrences': 1
            })
        
        # Track failed
        for normalized, (original, translation) in translations.items():
            if not any(s['original_text'] == original for s in self.successful):
                self.failed.append({
                    'type': 'quote',
                    'original_text': original,
                    'translation': translation
                })
        
        return self.md_text, self.successful, self.failed


class BlockquoteReplacer:
    """Service for replacing blockquotes in Markdown files"""
    
    def __init__(self, md_text: str, excel_data: pd.DataFrame):
        self.md_text = md_text
        self.excel_data = excel_data
        self.successful = []
        self.failed = []
    
    def _normalize(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
        text = re.sub(r'(\w)-(\w)', r'\1\2', text)
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        text = re.sub(r'\\([\\[\]()*_{}~`>#+\-.!|=])', r'\1', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower()
    
    def _load_translations(self, column_pl: str, column_en: str) -> Dict[str, Tuple[str, str]]:
        if column_pl not in self.excel_data.columns or column_en not in self.excel_data.columns:
            return {}
        
        pairs = {}
        for _, row in self.excel_data.iterrows():
            orig = row.get(column_pl, '')
            trans = row.get(column_en, '')
            
            if pd.isna(orig) or pd.isna(trans):
                continue
            
            orig = str(orig).strip()
            trans = str(trans).strip()
            
            if orig and trans:
                pairs[self._normalize(orig)] = (orig, trans)
        
        return pairs
    
    def replace_blockquotes(self, column_pl: str = 'blockquotes PL', column_en: str = 'blockquotes EN') -> Tuple[str, List[dict], List[dict]]:
        translations = self._load_translations(column_pl, column_en)
        
        if not translations:
            return self.md_text, [], []
        
        paragraphs = self.md_text.split('\n\n')
        
        # Pre-compute MD combinations
        md_combinations = []
        for n in range(1, 7):
            for i in range(len(paragraphs) - n + 1):
                combined = '\n\n'.join(paragraphs[i:i+n])
                md_combinations.append((self._normalize(combined), n, i, combined))
        
        matched_indices = set()
        
        # Find matches
        for excel_norm, (original, translation) in translations.items():
            found = False
            for md_norm, n, i, combined_text in md_combinations:
                if any(idx in matched_indices for idx in range(i, i + n)):
                    continue
                
                if md_norm.startswith(excel_norm):
                    paragraphs[i] = translation
                    for j in range(i + 1, i + n):
                        paragraphs[j] = ''
                        matched_indices.add(j)
                    matched_indices.add(i)
                    
                    self.successful.append({
                        'type': 'blockquote',
                        'original_text': original,
                        'translation': translation,
                        'occurrences': 1
                    })
                    found = True
                    break
            
            if not found:
                self.failed.append({
                    'type': 'blockquote',
                    'original_text': original,
                    'translation': translation
                })
        
        paragraphs = [p for p in paragraphs if p.strip()]
        self.md_text = '\n\n'.join(paragraphs)
        
        return self.md_text, self.successful, self.failed


class CombinedReplacer:
    """Service for replacing quotes, footnotes and blockquotes"""
    
    def __init__(self, md_text: str, excel_data: pd.DataFrame):
        self.md_text = md_text
        self.excel_data = excel_data
    
    def replace_all(self, output_filename: str = 'output_all_replaced.md') -> Tuple[str, dict, str]:
        """Replace quotes, footnotes and blockquotes"""
        quote_replacer = QuoteReplacer(self.md_text, self.excel_data)
        self.md_text, quote_success, quote_failed = quote_replacer.replace_quotes()
        
        footnote_replacer = FootnoteReplacer(self.md_text, self.excel_data)
        self.md_text, footnote_success, footnote_failed = footnote_replacer.replace_footnotes()
        
        blockquote_replacer = BlockquoteReplacer(self.md_text, self.excel_data)
        self.md_text, blockquote_success, blockquote_failed = blockquote_replacer.replace_blockquotes()
        
        output_dir = Path(__file__).parent / 'uploads'
        output_path = output_dir / output_filename
        output_path.write_text(self.md_text, encoding='utf-8')
        
        results = {
            'quotes': {
                'successful': quote_success,
                'failed': quote_failed,
                'success_count': len(quote_success),
                'failed_count': len(quote_failed)
            },
            'footnotes': {
                'successful': footnote_success,
                'failed': footnote_failed,
                'success_count': len(footnote_success),
                'failed_count': len(footnote_failed)
            },
            'blockquotes': {
                'successful': blockquote_success,
                'failed': blockquote_failed,
                'success_count': len(blockquote_success),
                'failed_count': len(blockquote_failed)
            }
        }
        
        return self.md_text, results, str(output_path)
    
    def export_failed_to_excel(self, results: dict, output_filename: str = 'failed_replacements.xlsx') -> str:
        """Export failed quotes, footnotes and blockquotes to Excel"""
        failed_quotes = [{
            'Type': 'Quote',
            'Original Text (PL)': item['original_text'],
            'Translation (EN)': item['translation']
        } for item in results['quotes']['failed']]
        
        failed_footnotes = [{
            'Type': 'Footnote',
            'Original Text (PL)': item['original_text'],
            'Translation (EN)': item['translation']
        } for item in results['footnotes']['failed']]
        
        failed_blockquotes = [{
            'Type': 'Blockquote',
            'Original Text (PL)': item['original_text'],
            'Translation (EN)': item['translation']
        } for item in results.get('blockquotes', {}).get('failed', [])]
        
        all_failed = failed_quotes + failed_footnotes + failed_blockquotes
        df = pd.DataFrame(all_failed)
        
        output_dir = Path(__file__).parent / 'uploads'
        output_path = output_dir / output_filename
        df.to_excel(output_path, index=False)
        
        return str(output_path)


class FootnoteReplacer:
    """Service for replacing footnotes in Markdown files"""
    
    def __init__(self, md_text: str, excel_data: pd.DataFrame):
        self.md_text = md_text
        self.excel_data = excel_data
        self.successful = []
        self.failed = []
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = ' '.join(text.split())
        text = re.sub(r'\\([\\[\]()*_{}~`>#+\-.!|=])', r'\1', text)
        return text.strip()
    
    def _load_translations(self, column_pl: str, column_en: str) -> Dict[str, str]:
        """Load PL→EN translation pairs from Excel"""
        if column_pl not in self.excel_data.columns or column_en not in self.excel_data.columns:
            return {}
        
        pairs = {}
        for _, row in self.excel_data.iterrows():
            orig = row.get(column_pl, '')
            trans = row.get(column_en, '')
            
            if pd.isna(orig) or pd.isna(trans):
                continue
            
            orig = str(orig).strip()
            trans = str(trans).strip()
            
            if not orig or not trans:
                continue
            
            orig_cleaned = self._clean_text(orig)
            trans_cleaned = self._clean_text(trans)
            
            if orig_cleaned and trans_cleaned:
                pairs[orig_cleaned] = trans_cleaned
        
        return dict(sorted(pairs.items(), key=lambda x: len(x[0]), reverse=True))
    
    def replace_footnotes(self) -> Tuple[str, List[dict], List[dict]]:
        """Replace footnotes [^1]: content"""
        translations = self._load_translations('footnotes PL', 'footnotes EN')
        
        if not translations:
            return self.md_text, [], []
        
        footnote_pattern = re.compile(
            r'^\[\^(\d+)\]:[ \t]*(.*?)(?=\n\[\^\d+\]:|\\Z)',
            re.MULTILINE | re.DOTALL
        )
        
        def replace_match(match):
            footnote_num = match.group(1)
            content = self._clean_text(match.group(2))
            
            translated = translations.get(content)
            
            if translated and pd.notna(translated):
                self.successful.append({
                    'type': 'footnote',
                    'original_text': content,
                    'translation': translated,
                    'occurrences': 1
                })
                return f"[^{footnote_num}]: {translated}"
            else:
                self.failed.append({
                    'type': 'footnote',
                    'original_text': content,
                    'translation': ''
                })
                return match.group(0)
        
        self.md_text = re.sub(footnote_pattern, replace_match, self.md_text)
        
        return self.md_text, self.successful, self.failed
