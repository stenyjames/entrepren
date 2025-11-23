import streamlit as st
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from price_scraper import PriceScraper
from comparison_engine import ComparisonEngine
from user_manager import UserManager

# Configure page
st.set_page_config(
    page_title="Product Search - StockUp",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Check authentication
if not st.session_state.logged_in:
    st.error("❌ Please log in first")
    st.switch_page("login.py")

username = st.session_state.get("username")
user_manager = UserManager()

# Load data functions
@st.cache_data
def load_products():
    try:
        with open("products.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@st.cache_data
def load_price_history():
    try:
        with open("data/prices.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def create_search_filters(comparison_results):
    """Extract filter options from comparison results"""
    stores = set()
    price_ranges = {"min": float('inf'), "max": 0}
    
    for product, result in comparison_results.items():
        for store_price in result['all_prices'].values():
            if store_price:
                price_ranges["min"] = min(price_ranges["min"], store_price)
                price_ranges["max"] = max(price_ranges["max"], store_price)
        for store in result['all_prices'].keys():
            stores.add(store)
    
    return sorted(list(stores)), price_ranges

def filter_results(comparison_results, search_query, min_price, max_price, selected_stores, savings_filter):
    """Filter comparison results based on search and filters"""
    filtered = {}
    
    for product, result in comparison_results.items():
        # Search query filter - case insensitive, search in product name and company
        if search_query:
            search_lower = search_query.lower()
            product_lower = product.lower()
            company_lower = result.get('company', '').lower()
            if search_lower not in product_lower and search_lower not in company_lower:
                continue
        
        best_price = result['best_deal']['price']
        savings_pct = result['statistics']['savings_percentage']
        
        # Price filter
        if not (min_price <= best_price <= max_price):
            continue
        
        # Store filter
        if selected_stores and result['best_deal']['store'] not in selected_stores:
            continue
        
        # Savings filter
        if savings_filter > 0 and savings_pct < savings_filter:
            continue
        
        filtered[product] = result
    
    return filtered

# Header
col1, col2, col3, col4, col5 = st.columns([0.1, 0.65, 0.08, 0.08, 0.09])
with col1:
    try:
        with open("logo-icon.svg", "r") as f:
            st.image("logo-icon.svg", width=80)
    except:
        st.write("🔍")
with col2:
    st.title("Product Search")
    st.markdown("Find the best deals on products across multiple stores")
with col3:
    if st.button("🏠"):
        st.switch_page("pages/menu.py")
with col4:
    if st.button("📊"):
        st.switch_page("pages/dashboard.py")
with col5:
    if st.button("👤"):
        st.switch_page("pages/settings.py")

st.divider()

# Load data
products = load_products()
price_history = load_price_history()

if not price_history or 'prices' not in price_history:
    st.warning("⚠️ No price data available. Please scrape prices from the dashboard first.")
    st.stop()

# Prepare comparison data from categories
scraper = PriceScraper()
engine = ComparisonEngine()
category_results = engine.compare(price_history['prices'])

# Create comparison results for individual products
comparison_results = {}
for product in products:
    product_name = product.get('name', 'Unknown')
    category = product.get('category', 'Product')
    company = product.get('company', 'Unknown')
    
    # Get prices for this product's category from the category results
    if category in category_results:
        cat_result = category_results[category]
        comparison_results[product_name] = {
            'best_deal': cat_result['best_deal'],
            'all_prices': cat_result['all_prices'],
            'statistics': cat_result['statistics'],
            'company': company,
            'image': product.get('image', ''),
            'category': category
        }
    else:
        # If category not found, create empty entry
        comparison_results[product_name] = {
            'best_deal': {'store': 'N/A', 'price': 0},
            'all_prices': {},
            'statistics': {'average_price': 0, 'max_price': 0, 'min_price': 0, 'price_range': 0, 'savings_percentage': 0},
            'company': company,
            'image': product.get('image', ''),
            'category': category
        }

if not comparison_results:
    st.error("❌ No products found in price data.")
    st.stop()

# Get filter options
stores, price_ranges = create_search_filters(comparison_results)
if price_ranges["min"] == float('inf'):
    price_ranges["min"] = 0

# Advanced Search Section
st.subheader("🔎 Advanced Search Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    search_query = st.text_input(
        "📝 Product Name",
        placeholder="e.g., Laptop, iPhone...",
        help="Search by product name"
    )

with col2:
    min_price = st.number_input(
        "💰 Min Price ($)",
        min_value=0.0,
        value=0.0,
        step=10.0
    )

with col3:
    max_price = st.number_input(
        "💰 Max Price ($)",
        min_value=0.0,
        value=max(price_ranges["max"], 10000.0),
        step=10.0
    )

with col4:
    savings_filter = st.number_input(
        "📊 Min Savings %",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0,
        help="Filter by minimum savings percentage"
    )

col1, col2 = st.columns(2)

with col1:
    selected_stores = st.multiselect(
        "🏪 Filter by Store",
        options=stores,
        default=stores,
        help="Select stores to include in results"
    )

with col2:
    sort_by = st.selectbox(
        "📊 Sort By",
        options=["Best Price", "Most Savings %", "Price Range", "Alphabetical"],
        help="How to sort the results"
    )

col1, col2 = st.columns(2)

with col1:
    # Get unique companies
    all_companies = sorted(set(p.get('company', 'Unknown') for p in comparison_results.values()))
    selected_companies = st.multiselect(
        "🏢 Filter by Company",
        options=all_companies,
        default=all_companies,
        help="Filter by product company/brand"
    )

with col2:
    st.empty()  # Spacer

st.divider()

# Apply filters
filtered_results = filter_results(
    comparison_results,
    search_query,
    min_price,
    max_price,
    selected_stores,
    savings_filter
)

# Filter by selected companies
filtered_results = {
    p: v for p, v in filtered_results.items()
    if v.get('company', 'Unknown') in selected_companies
}

# Sort results
if sort_by == "Best Price":
    filtered_results = dict(sorted(
        filtered_results.items(),
        key=lambda x: x[1]['best_deal']['price']
    ))
elif sort_by == "Most Savings %":
    filtered_results = dict(sorted(
        filtered_results.items(),
        key=lambda x: x[1]['statistics']['savings_percentage'],
        reverse=True
    ))
elif sort_by == "Price Range":
    filtered_results = dict(sorted(
        filtered_results.items(),
        key=lambda x: x[1]['statistics']['price_range'],
        reverse=True
    ))
else:  # Alphabetical
    filtered_results = dict(sorted(filtered_results.items()))

# Results
st.subheader(f"🎯 Search Results ({len(filtered_results)} products found)")

if not filtered_results:
    st.info("❌ No products match your search criteria. Try adjusting your filters.")
else:
    # Group results by company
    companies = {}
    for product, result in filtered_results.items():
        company = result.get('company', 'Unknown')
        if company not in companies:
            companies[company] = {}
        companies[company][product] = result
    
    # Create tabs for each company
    company_list = sorted(companies.keys())
    company_tabs = st.tabs([f"🏢 {company} ({len(companies[company])})" for company in company_list])
    
    for tab_idx, company in enumerate(company_list):
        with company_tabs[tab_idx]:
            products_in_company = companies[company]
            
            # Create columns for product cards
            cols = st.columns(min(4, len(products_in_company)))
            
            for idx, (product, result) in enumerate(products_in_company.items()):
                with cols[idx % len(cols)]:
                    with st.container(border=True):
                        # Product image
                        try:
                            st.image(result.get('image', ''), use_column_width=True, width=500)
                        except:
                            st.write("📦 No image available")
                        
                        # Product name and category
                        st.markdown(f"**{product}**")
                        category = result.get('category', 'Product')
                        st.caption(f"📂 {category}")
                        
                        # Best deal - prominent
                        best_deal = result['best_deal']
                        st.markdown(f"### 🏆 ${best_deal['price']:.2f}")
                        st.caption(f"at {best_deal['store']}")
                        
                        # Savings info
                        savings = result['statistics']['price_range']
                        savings_pct = result['statistics']['savings_percentage']
                        col_s1, col_s2 = st.columns(2)
                        with col_s1:
                            st.metric("Save", f"${savings:.2f}")
                        with col_s2:
                            st.metric("Save %", f"{savings_pct:.1f}%")
                        
                        # Price comparison dropdown
                        with st.expander("📊 All Prices"):
                            for store, price in sorted(result['all_prices'].items()):
                                if price:
                                    is_best = "✅ BEST" if store == best_deal['store'] else ""
                                    st.write(f"**{store}**: ${price:.2f} {is_best}")
        
        st.divider()

# Export section
st.subheader("📥 Export Results")

col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Export as CSV", use_container_width=True):
        import pandas as pd
        
        export_data = []
        for product, result in filtered_results.items():
            export_data.append({
                "Product": product,
                "Best Price": f"${result['best_deal']['price']:.2f}",
                "Best Store": result['best_deal']['store'],
                "Savings": f"${result['statistics']['price_range']:.2f}",
                "Savings %": f"{result['statistics']['savings_percentage']:.1f}%",
                "Price Range": f"${result['statistics']['min_price']:.2f} - ${result['statistics']['max_price']:.2f}"
            })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="stockup_search_results.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📊 Export as JSON", use_container_width=True):
        import json
        json_data = json.dumps(filtered_results, indent=2, default=str)
        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name="stockup_search_results.json",
            mime="application/json"
        )

st.divider()

# Search tips
with st.expander("💡 Search Tips", expanded=False):
    st.markdown("""
    ### How to use the search page:
    
    1. **Product Name** - Search for specific products (e.g., "Laptop", "iPhone 15", "Monitor")
    2. **Price Range** - Set minimum and maximum price filters
    3. **Minimum Savings %** - Only show products with at least this much savings potential
    4. **Store Filter** - Select which stores to include in the comparison
    5. **Sort By** - Choose how to sort the results:
       - **Best Price**: Lowest price first
       - **Most Savings %**: Highest savings percentage first
       - **Price Range**: Largest price difference between stores first
       - **Alphabetical**: Product name A-Z
    
    ### Tips:
    - Leave product name empty to see all products
    - Use the store filter to focus on specific retailers
    - Sort by "Most Savings %" to find the best deals
    - Export results to share with others or for your records
    """)
