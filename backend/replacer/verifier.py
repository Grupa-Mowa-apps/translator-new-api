from typing import List, Dict


class ReplacementVerifier:
    """Verify and analyze replacement results"""
    
    def verify_replacements(self, successful: List[dict], failed: List[dict]) -> Dict:
        """Calculate replacement statistics"""
        total = len(successful) + len(failed)
        success_rate = (len(successful) / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': round(success_rate, 2)
        }
    
    def generate_report(self, successful: List[dict], failed: List[dict]) -> str:
        """Generate text report"""
        stats = self.verify_replacements(successful, failed)
        
        report = f"""
=== Replacement Report ===
Total footnotes: {stats['total']}
Successful: {stats['successful']}
Failed: {stats['failed']}
Success rate: {stats['success_rate']}%
========================
"""
        
        if failed:
            report += "\nFailed replacements:\n"
            for item in failed:
                report += f"- {item['original_text'][:50]}...\n"
        
        return report
