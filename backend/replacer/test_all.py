import pandas as pd
from service import CombinedReplacer

# Wczytaj dane
excel_path = '/Users/gmtomasz/PycharmProjects/translator/backend/replacer/uploads/Kalisciak_quotes.xlsx'
md_path = '/Users/gmtomasz/PycharmProjects/translator/backend/replacer/uploads/Kalisciak_md.md'

df = pd.read_excel(excel_path)
md_text = open(md_path, 'r', encoding='utf-8').read()

print("=== TEST COMBINED REPLACER ===\n")
print(f"MD length: {len(md_text)} chars")
print(f"Excel rows: {len(df)}\n")

# Uruchom replacer
replacer = CombinedReplacer(md_text, df)
result_md, results, output_path = replacer.replace_all('Kalisciak_REPLACED.md')

# Podsumowanie
print("=== WYNIKI ===\n")

print("QUOTES:")
print(f"  ✅ Successful: {results['quotes']['success_count']}")
print(f"  ❌ Failed: {results['quotes']['failed_count']}")

print("\nFOOTNOTES:")
print(f"  ✅ Successful: {results['footnotes']['success_count']}")
print(f"  ❌ Failed: {results['footnotes']['failed_count']}")

print("\nBLOCKQUOTES:")
print(f"  ✅ Successful: {results['blockquotes']['success_count']}")
print(f"  ❌ Failed: {results['blockquotes']['failed_count']}")

total_success = results['quotes']['success_count'] + results['footnotes']['success_count'] + results['blockquotes']['success_count']
total_failed = results['quotes']['failed_count'] + results['footnotes']['failed_count'] + results['blockquotes']['failed_count']

print(f"\nTOTAL:")
print(f"  ✅ Successful: {total_success}")
print(f"  ❌ Failed: {total_failed}")
print(f"  Success rate: {total_success/(total_success+total_failed)*100:.1f}%")

print(f"\n=== OUTPUT FILES ===")
print(f"MD: {output_path}")

# Export failed
failed_path = replacer.export_failed_to_excel(results, 'Kalisciak_FAILED.xlsx')
print(f"Failed Excel: {failed_path}")
