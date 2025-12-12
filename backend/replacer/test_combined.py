import pandas as pd
from pathlib import Path
from service import CombinedReplacer

# Load files
uploads_dir = Path(__file__).parent / 'uploads'
md_path = uploads_dir / 'Kalisciak_md.md'
excel_path = uploads_dir / 'Kalisciak_quotes.xlsx'

md_text = md_path.read_text(encoding='utf-8')
excel_data = pd.read_excel(excel_path)

# Replace both quotes and footnotes
replacer = CombinedReplacer(md_text, excel_data)
result_text, results, output_path = replacer.replace_all('output_combined.md')

# Export failed to Excel
failed_excel_path = replacer.export_failed_to_excel(results, 'failed_replacements.xlsx')

# Print results
print("=== COMBINED REPLACEMENT RESULTS ===\n")
print(f"QUOTES:")
print(f"  ✓ Successful: {results['quotes']['success_count']}")
print(f"  ✗ Failed: {results['quotes']['failed_count']}")
print(f"\nFOOTNOTES:")
print(f"  ✓ Successful: {results['footnotes']['success_count']}")
print(f"  ✗ Failed: {results['footnotes']['failed_count']}")
print(f"\nOutput MD saved to: {output_path}")
print(f"Failed items Excel saved to: {failed_excel_path}")
