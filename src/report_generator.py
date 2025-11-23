"""
Report Generator Module
Generates formatted reports of price comparisons.
"""

from datetime import datetime
from typing import Dict, Any


class ReportGenerator:
    """Generates price comparison reports."""
    
    def generate(self, comparison_results: Dict[str, Any]) -> str:
        """Generate a comprehensive price comparison report."""
        report = []
        
        # Header
        report.append("=" * 70)
        report.append("PRICE COMPARISON REPORT".center(70))
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        total_products = len(comparison_results)
        total_savings = sum(
            r['statistics']['price_range'] 
            for r in comparison_results.values()
        )
        
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Total Products: {total_products}")
        report.append(f"Total Potential Savings: ${total_savings:.2f}")
        report.append("")
        
        # Detailed comparisons
        report.append("DETAILED COMPARISONS")
        report.append("-" * 70)
        
        for product, result in sorted(comparison_results.items()):
            report.append(f"\n{product.upper()}")
            report.append("  Best Deal:")
            best = result['best_deal']
            report.append(f"    Store: {best['store']}")
            report.append(f"    Price: ${best['price']:.2f}")
            
            report.append("  All Prices:")
            for store, price in sorted(result['all_prices'].items(), key=lambda x: x[1]):
                report.append(f"    {store}: ${price:.2f}")
            
            stats = result['statistics']
            report.append("  Statistics:")
            report.append(f"    Average Price: ${stats['average_price']:.2f}")
            report.append(f"    Price Range: ${stats['min_price']:.2f} - ${stats['max_price']:.2f}")
            report.append(f"    Potential Savings: ${stats['price_range']:.2f} ({stats['savings_percentage']:.1f}%)")
        
        # Footer
        report.append("\n" + "=" * 70)
        report.append("END OF REPORT".center(70))
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def generate_csv(self, comparison_results: Dict[str, Any]) -> str:
        """Generate a CSV format report."""
        lines = ["Product,Best Store,Best Price,Average Price,Max Price,Savings Amount,Savings %"]
        
        for product, result in sorted(comparison_results.items()):
            best = result['best_deal']
            stats = result['statistics']
            
            line = (
                f"{product},"
                f"{best['store']},"
                f"${best['price']:.2f},"
                f"${stats['average_price']:.2f},"
                f"${stats['max_price']:.2f},"
                f"${stats['price_range']:.2f},"
                f"{stats['savings_percentage']:.1f}%"
            )
            lines.append(line)
        
        return "\n".join(lines)
    
    def generate_json(self, comparison_results: Dict[str, Any]) -> str:
        """Generate a JSON format report."""
        import json
        return json.dumps(comparison_results, indent=2)
