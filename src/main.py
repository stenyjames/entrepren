"""
Price Comparison App
A simple Python application to compare prices across different stores and products.
"""

import json
from datetime import datetime
from pathlib import Path
from price_scraper import PriceScraper
from comparison_engine import ComparisonEngine
from report_generator import ReportGenerator


class PriceComparisonApp:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.scraper = PriceScraper()
        self.engine = ComparisonEngine()
        self.reporter = ReportGenerator()
        self.prices_file = self.data_dir / "prices.json"

    def load_products(self, products_file: str) -> list:
        """Load products from a JSON file."""
        try:
            with open(products_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Products file '{products_file}' not found.")
            return []

    def scrape_prices(self, products: list) -> dict:
        """Scrape prices for all products."""
        print("Scraping prices from stores...")
        prices = {}
        
        for product in products:
            product_name = product.get('name', 'Unknown')
            print(f"  Scraping {product_name}...")
            
            product_prices = {}
            for store in product.get('stores', []):
                # Simulate price scraping (in real app, this would scrape actual websites)
                price = self.scraper.get_price(product_name, store)
                if price:
                    product_prices[store] = price
            
            if product_prices:
                prices[product_name] = product_prices
        
        return prices

    def save_prices(self, prices: dict) -> None:
        """Save prices to a JSON file with timestamp."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'prices': prices
        }
        with open(self.prices_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Prices saved to {self.prices_file}")

    def compare_prices(self, prices: dict) -> dict:
        """Compare prices and find best deals."""
        print("Comparing prices...")
        return self.engine.compare(prices)

    def generate_report(self, comparison_results: dict) -> str:
        """Generate a price comparison report."""
        return self.reporter.generate(comparison_results)

    def display_best_deals(self, comparison_results: dict) -> None:
        """Display best deals in a formatted way."""
        print("\n" + "="*60)
        print("BEST DEALS".center(60))
        print("="*60)
        
        for product, deals in comparison_results.items():
            best_deal = deals['best_deal']
            print(f"\n{product}")
            print(f"  Best Price: ${best_deal['price']:.2f} at {best_deal['store']}")
            print(f"  Other prices:")
            for store, price in deals['all_prices'].items():
                if store != best_deal['store']:
                    savings = price - best_deal['price']
                    print(f"    {store}: ${price:.2f} (+${savings:.2f})")

    def run(self, products_file: str = "products.json") -> None:
        """Run the price comparison process."""
        print("Starting Price Comparison App...")
        
        # Load products
        products = self.load_products(products_file)
        if not products:
            print("No products to compare. Please create a products.json file.")
            return
        
        # Scrape prices
        prices = self.scrape_prices(products)
        if not prices:
            print("No prices found.")
            return
        
        # Save prices
        self.save_prices(prices)
        
        # Compare prices
        comparison_results = self.compare_prices(prices)
        
        # Display results
        self.display_best_deals(comparison_results)
        
        # Generate report
        report = self.generate_report(comparison_results)
        report_file = self.data_dir / "price_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {report_file}")


if __name__ == "__main__":
    app = PriceComparisonApp()
    app.run()
