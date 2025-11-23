"""
StockUp Dashboard - DEPRECATED
This file is kept for backward compatibility.
Please use: streamlit run login.py

The main dashboard is now accessed through the login system.
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from price_scraper import PriceScraper
from comparison_engine import ComparisonEngine
from report_generator import ReportGenerator


# Page configuration
st.set_page_config(
    page_title="StockUp - Price Comparison Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)


def load_products(products_file: str = "products.json"):
    """Load products from configuration file."""
    try:
        with open(products_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Products file '{products_file}' not found.")
        return []


def load_price_history(data_dir: str = "data"):
    """Load historical price data if available."""
    data_file = Path(data_dir) / "prices.json"
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return None


def scrape_and_compare_prices(products):
    """Scrape prices and perform comparison."""
    scraper = PriceScraper()
    engine = ComparisonEngine()
    
    # Scrape prices
    prices = {}
    progress_bar = st.progress(0)
    
    for idx, product in enumerate(products):
        product_name = product.get('name', 'Unknown')
        product_prices = {}
        
        for store in product.get('stores', []):
            price = scraper.get_price(product_name, store)
            if price:
                product_prices[store] = price
        
        if product_prices:
            prices[product_name] = product_prices
        
        progress_bar.progress((idx + 1) / len(products))
    
    # Compare prices
    comparison_results = engine.compare(prices)
    return prices, comparison_results


def create_price_comparison_chart(comparison_results):
    """Create an interactive bar chart for price comparisons."""
    data = []
    
    for product, result in comparison_results.items():
        for store, price in result['all_prices'].items():
            is_best = store == result['best_deal']['store']
            data.append({
                'Product': product,
                'Store': store,
                'Price': price,
                'Best Deal': 'Yes' if is_best else 'No'
            })
    
    df = pd.DataFrame(data)
    
    fig = px.bar(
        df,
        x='Product',
        y='Price',
        color='Store',
        barmode='group',
        title='Price Comparison Across Stores',
        labels={'Price': 'Price ($)', 'Product': 'Product'},
        hover_data={'Price': ':.2f'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis_tickangle=-45
    )
    
    return fig


def create_best_deals_chart(comparison_results):
    """Create a chart showing best deals and savings."""
    data = []
    
    for product, result in comparison_results.items():
        best_deal = result['best_deal']
        stats = result['statistics']
        
        data.append({
            'Product': product,
            'Best Price': best_deal['price'],
            'Avg Price': stats['average_price'],
            'Max Price': stats['max_price'],
            'Savings': stats['price_range']
        })
    
    df = pd.DataFrame(data)
    
    fig = px.scatter(
        df,
        x='Product',
        y='Best Price',
        size='Savings',
        color='Savings',
        hover_data={'Avg Price': ':.2f', 'Max Price': ':.2f', 'Savings': ':.2f'},
        title='Best Deals & Potential Savings',
        labels={'Best Price': 'Best Price ($)', 'Savings': 'Potential Savings ($)'},
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(height=500)
    
    return fig


def create_savings_percentage_chart(comparison_results):
    """Create a chart showing savings percentage by product."""
    data = []
    
    for product, result in comparison_results.items():
        stats = result['statistics']
        data.append({
            'Product': product,
            'Savings %': stats['savings_percentage']
        })
    
    df = pd.DataFrame(data).sort_values('Savings %', ascending=True)
    
    fig = px.barh(
        df,
        x='Savings %',
        y='Product',
        title='Savings Percentage by Product',
        labels={'Savings %': 'Potential Savings (%)'},
        color='Savings %',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_store_performance_chart(comparison_results):
    """Create a chart showing store performance (best deals count)."""
    store_wins = {}
    
    for product, result in comparison_results.items():
        store = result['best_deal']['store']
        store_wins[store] = store_wins.get(store, 0) + 1
    
    df = pd.DataFrame(list(store_wins.items()), columns=['Store', 'Best Deals'])
    df = df.sort_values('Best Deals', ascending=False)
    
    fig = px.bar(
        df,
        x='Store',
        y='Best Deals',
        title='Best Deals by Store',
        labels={'Best Deals': 'Number of Best Deals'},
        color='Best Deals',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=400)
    
    return fig


def create_price_range_table(comparison_results):
    """Create a table showing price ranges for each product."""
    data = []
    
    for product, result in comparison_results.items():
        best = result['best_deal']
        stats = result['statistics']
        
        data.append({
            'Product': product,
            'Best Store': best['store'],
            'Best Price': f"${best['price']:.2f}",
            'Average Price': f"${stats['average_price']:.2f}",
            'Max Price': f"${stats['max_price']:.2f}",
            'Savings': f"${stats['price_range']:.2f}",
            'Savings %': f"{stats['savings_percentage']:.1f}%"
        })
    
    return pd.DataFrame(data)


def main():
    """Main Streamlit application."""
    
    # Header
    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        st.image("logo-icon.svg", width=80)
    with col2:
        st.title("💰 StockUp")
        st.markdown("Smart Price Comparison - Stock Up on Savings!")
    
    st.divider()
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        refresh_option = st.radio(
            "Data Source",
            ("Live Scraping", "Load Saved Data"),
            help="Choose whether to scrape live prices or load previously saved data"
        )
        
        if refresh_option == "Live Scraping":
            if st.button("🔄 Scrape Prices Now", use_container_width=True):
                st.session_state.scrape_now = True
        
        st.divider()
        
        st.subheader("Filter Options")
        filter_type = st.radio(
            "View",
            ("All Products", "Top Deals", "Best by Store"),
            help="Select what you want to analyze"
        )
        
        if filter_type == "Top Deals":
            top_n = st.slider("Show top N deals", 1, 20, 5)
        
        st.divider()
        st.caption("Last updated: Click 'Scrape Prices Now' to refresh data")
    
    # Main content
    products = load_products()
    
    if not products:
        st.error("❌ No products found. Please create a products.json file.")
        return
    
    # Check if we should scrape or load saved data
    if refresh_option == "Live Scraping" or st.session_state.get("scrape_now", False):
        st.info("📊 Scraping prices from stores...")
        prices, comparison_results = scrape_and_compare_prices(products)
        st.success("✅ Prices scraped successfully!")
    else:
        # Load saved data
        price_history = load_price_history()
        if price_history and 'prices' in price_history:
            scraper = PriceScraper()
            engine = ComparisonEngine()
            comparison_results = engine.compare(price_history['prices'])
            prices = price_history['prices']
            last_updated = price_history.get('timestamp', 'Unknown')
            st.info(f"📊 Loaded saved data from {last_updated}")
        else:
            st.warning("⚠️ No saved data found. Please scrape prices first.")
            if st.button("🔄 Scrape Prices Now"):
                st.session_state.scrape_now = True
                st.rerun()
            return
    
    # Display summary metrics
    st.subheader("📈 Summary Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_products = len(comparison_results)
    total_savings = sum(r['statistics']['price_range'] for r in comparison_results.values())
    avg_savings_pct = sum(r['statistics']['savings_percentage'] for r in comparison_results.values()) / total_products if total_products > 0 else 0
    
    with col1:
        st.metric("📦 Products", total_products)
    with col2:
        st.metric("💵 Total Savings Potential", f"${total_savings:.2f}")
    with col3:
        st.metric("📊 Avg Savings %", f"{avg_savings_pct:.1f}%")
    with col4:
        st.metric("🏪 Stores Analyzed", len(set([result['best_deal']['store'] for result in comparison_results.values()])))
    
    st.divider()
    
    # Charts
    st.subheader("📊 Price Comparisons")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 All Prices", "🎁 Best Deals", "💰 Savings %", "🏆 Store Performance", "📑 Details Table"]
    )
    
    with tab1:
        fig = create_price_comparison_chart(comparison_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = create_best_deals_chart(comparison_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = create_savings_percentage_chart(comparison_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        fig = create_store_performance_chart(comparison_results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.dataframe(
            create_price_range_table(comparison_results),
            use_container_width=True,
            hide_index=True
        )
    
    st.divider()
    
    # Best Deals Section
    st.subheader("🎁 Your Best Deals")
    
    if filter_type == "All Products":
        best_deals = {p: comparison_results[p] for p in comparison_results}
    elif filter_type == "Top Deals":
        best_deals = dict(sorted(
            comparison_results.items(),
            key=lambda x: x[1]['statistics']['price_range'],
            reverse=True
        )[:top_n])
    else:  # Best by Store
        best_deals = {}
        for product, result in comparison_results.items():
            store = result['best_deal']['store']
            best_deals[f"{product} ({store})"] = result
    
    # Display best deals in columns
    cols = st.columns(min(3, len(best_deals)))
    
    for idx, (product, result) in enumerate(best_deals.items()):
        with cols[idx % len(cols)]:
            best_deal = result['best_deal']
            stats = result['statistics']
            
            st.markdown(f"### {product}")
            
            col_price, col_store = st.columns([1, 1])
            with col_price:
                st.metric("💰 Best Price", f"${best_deal['price']:.2f}")
            with col_store:
                st.metric("🏪 Store", best_deal['store'])
            
            col_avg, col_save = st.columns([1, 1])
            with col_avg:
                st.metric("📊 Avg", f"${stats['average_price']:.2f}")
            with col_save:
                st.metric("💾 Save", f"${stats['price_range']:.2f}")
            
            st.caption(f"Save {stats['savings_percentage']:.1f}% vs highest price")
    
    st.divider()
    
    # Footer
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📥 Export Data as CSV"):
            df = create_price_range_table(comparison_results)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"price_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Export as JSON"):
            json_data = json.dumps(comparison_results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"price_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        st.caption("💡 Tip: Use the sidebar to switch between live scraping and saved data")


if __name__ == "__main__":
    # Initialize session state
    if "scrape_now" not in st.session_state:
        st.session_state.scrape_now = False
    
    main()
