"""
Price Scraper Module
Handles scraping prices from different stores.
"""

import random
from typing import Optional


class PriceScraper:
    """Scrapes prices from various stores."""
    
    def __init__(self):
        """Initialize the price scraper."""
        self.stores = {
            'Amazon': {'delay': 0.5, 'variance': 1.2},
            'Walmart': {'delay': 0.5, 'variance': 1.0},
            'Best Buy': {'delay': 0.5, 'variance': 1.1},
            'Target': {'delay': 0.5, 'variance': 0.95},
            'eBay': {'delay': 0.5, 'variance': 1.15},
        }
    
    def get_price(self, product_name: str, store: str) -> Optional[float]:
        """
        Get the price of a product from a specific store.
        In a real application, this would scrape actual websites.
        For demo purposes, we generate mock prices.
        """
        try:
            # Generate a realistic mock price
            base_price = self._get_base_price(product_name)
            if base_price is None:
                return None
            
            variance = self.stores.get(store, {}).get('variance', 1.0)
            fluctuation = random.uniform(0.9, 1.1)
            
            final_price = base_price * variance * fluctuation
            return round(final_price, 2)
        except Exception as e:
            print(f"Error scraping price from {store}: {e}")
            return None
    
    def _get_base_price(self, product_name: str) -> Optional[float]:
        """Get base price for a product."""
        # Mock product prices
        product_prices = {
            'laptop': 899.99,
            'smartphone': 699.99,
            'headphones': 199.99,
            'usb cable': 9.99,
            'keyboard': 79.99,
            'monitor': 299.99,
            'mouse': 29.99,
        }
        
        product_lower = product_name.lower()
        for key, price in product_prices.items():
            if key in product_lower:
                return price
        
        return None
    
    def is_store_available(self, store: str) -> bool:
        """Check if a store is available for scraping."""
        return store in self.stores


# Mock function to demonstrate adding custom stores
def add_store(scraper: PriceScraper, store_name: str, delay: float = 0.5, variance: float = 1.0) -> None:
    """Add a new store to the scraper."""
    scraper.stores[store_name] = {'delay': delay, 'variance': variance}
