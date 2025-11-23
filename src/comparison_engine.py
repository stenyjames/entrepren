"""
Comparison Engine Module
Handles comparing prices and finding best deals.
"""

from typing import Dict, Any


class ComparisonEngine:
    """Compares prices across stores and finds best deals."""
    
    def compare(self, prices: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
        Compare prices for all products.
        
        Args:
            prices: Dictionary with product names as keys and store prices as values
            
        Returns:
            Dictionary with comparison results including best deals
        """
        results = {}
        
        for product_name, store_prices in prices.items():
            if not store_prices:
                continue
            
            # Find best deal
            best_store = min(store_prices, key=store_prices.get)
            best_price = store_prices[best_store]
            
            # Calculate statistics
            prices_list = list(store_prices.values())
            average_price = sum(prices_list) / len(prices_list)
            max_price = max(prices_list)
            price_range = max_price - best_price
            savings_percentage = (price_range / max_price * 100) if max_price > 0 else 0
            
            results[product_name] = {
                'best_deal': {
                    'store': best_store,
                    'price': best_price
                },
                'all_prices': store_prices,
                'statistics': {
                    'average_price': round(average_price, 2),
                    'max_price': max_price,
                    'min_price': best_price,
                    'price_range': round(price_range, 2),
                    'savings_percentage': round(savings_percentage, 2)
                }
            }
        
        return results
    
    def get_best_deals_by_store(self, comparison_results: Dict[str, Any]) -> Dict[str, list]:
        """Get all best deals grouped by store."""
        deals_by_store = {}
        
        for product, result in comparison_results.items():
            store = result['best_deal']['store']
            if store not in deals_by_store:
                deals_by_store[store] = []
            
            deals_by_store[store].append({
                'product': product,
                'price': result['best_deal']['price']
            })
        
        return deals_by_store
    
    def filter_by_price_range(self, comparison_results: Dict[str, Any], 
                             min_price: float, max_price: float) -> Dict[str, Any]:
        """Filter products by price range."""
        filtered = {}
        
        for product, result in comparison_results.items():
            best_price = result['best_deal']['price']
            if min_price <= best_price <= max_price:
                filtered[product] = result
        
        return filtered
    
    def find_price_drops(self, old_prices: Dict[str, Any], 
                        new_prices: Dict[str, Any]) -> Dict[str, Any]:
        """Find products with price drops."""
        drops = {}
        
        for product in new_prices:
            if product in old_prices:
                old_best = old_prices[product]['best_deal']['price']
                new_best = new_prices[product]['best_deal']['price']
                
                if new_best < old_best:
                    drop_amount = old_best - new_best
                    drop_percentage = (drop_amount / old_best * 100)
                    
                    drops[product] = {
                        'old_price': old_best,
                        'new_price': new_best,
                        'drop_amount': round(drop_amount, 2),
                        'drop_percentage': round(drop_percentage, 2)
                    }
        
        return drops
