"""Test script for quote replacer"""

import pandas as pd
from pathlib import Path
from service import QuoteReplacer
from verifier import ReplacementVerifier
import time


def test_quote_replacement():
    # Load files
    uploads_dir = Path(__file__).parent / 'uploads'
    md_path = uploads_dir / 'Kalisciak_md.md'
    excel_path = uploads_dir / 'Kalisciak_quotes.xlsx'
    
    # Read files
    md_text = md_path.read_text(encoding='utf-8')
    excel_df = pd.read_excel(excel_path)
    
    print(f"Loaded MD: {len(md_text)} chars")
    print(f"Loaded Excel: {len(excel_df)} rows")
    
    # Replace quotes
    start_time = time.time()
    replacer = QuoteReplacer(md_text, excel_df)
    result_text, successful, failed, output_path = replacer.replace_quotes('test_quotes_output.md')
    elapsed = time.time() - start_time
    
    print(f"\nReplacement completed in {elapsed:.2f}s")
    print(f"Output saved to: {output_path}")
    
    # Verify results
    verifier = ReplacementVerifier()
    stats = verifier.verify_replacements(successful, failed)
    
    print(f"\n{verifier.generate_report(successful, failed)}")
    
    return stats


if __name__ == '__main__':
    test_quote_replacement()
