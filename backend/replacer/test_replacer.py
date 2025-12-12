"""Test script for footnote replacer"""

import pandas as pd
from pathlib import Path
from service import FootnoteReplacer
from verifier import ReplacementVerifier


def test_footnote_replacement():
    # Load files
    uploads_dir = Path(__file__).parent / 'uploads'
    md_path = uploads_dir / 'Kalisciak_md.md'
    excel_path = uploads_dir / 'Kalisciak_quotes.xlsx'
    
    # Read files
    md_text = md_path.read_text(encoding='utf-8')
    excel_df = pd.read_excel(excel_path)
    
    print(f"Loaded MD: {len(md_text)} chars")
    print(f"Loaded Excel: {len(excel_df)} rows")
    
    # Replace footnotes
    replacer = FootnoteReplacer(md_text, excel_df)
    result_text, successful, failed, output_path = replacer.replace_footnotes('test_output.md')
    
    print(f"\nReplacement completed!")
    print(f"Output saved to: {output_path}")
    
    # Verify results
    verifier = ReplacementVerifier()
    stats = verifier.verify_replacements(successful, failed)
    
    print(f"\n{verifier.generate_report(successful, failed)}")
    
    return stats


if __name__ == '__main__':
    test_footnote_replacement()
