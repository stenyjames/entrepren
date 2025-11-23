import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from user_manager import UserManager

# Configure page
st.set_page_config(
    page_title="Menu - StockUp",
    page_icon="🏠",
    layout="wide"
)

# Add custom CSS for better logo styling
st.markdown("""
<style>
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 150px;
        padding: 15px;
        background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%);
        border-radius: 10px;
        margin: 10px 0;
    }
    .logo-container img {
        max-height: 120px;
        max-width: 100%;
        object-fit: contain;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .brand-card {
        border-radius: 10px;
        padding: 15px;
        background: #f9f9f9;
    }
    .brand-name {
        font-size: 1.1em;
        font-weight: bold;
        text-align: center;
        margin: 10px 0 5px 0;
    }
    .brand-desc {
        text-align: center;
        color: #666;
        font-size: 0.85em;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Check authentication
if not st.session_state.logged_in:
    st.error("❌ Please log in first")
    st.switch_page("login.py")

username = st.session_state.get("username")
user_manager = UserManager()

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    try:
        st.image("logo-icon.svg", width=80)
    except:
        st.write("🏠")
with col2:
    st.title("StockUp Menu")
    st.markdown("Navigate to your favorite features")
with col3:
    if st.button("👤 Account", use_container_width=True):
        st.switch_page("pages/settings.py")

st.divider()

# User info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👤 User", username)
with col2:
    has_location = user_manager.has_location_permission(username)
    location_status = "Enabled 📍" if has_location else "Disabled 🔕"
    st.metric("📍 Location", location_status)
with col3:
    user_prefs = user_manager.get_user_preferences(username)
    theme = user_prefs.get('theme', 'Light') if user_prefs else 'Light'
    st.metric("🎨 Theme", theme)

st.divider()

# Main navigation menu
st.subheader("📱 Main Features")

col1, col2, col3 = st.columns(3, gap="medium")

# Dashboard
with col1:
    with st.container(border=True):
        st.markdown("# 📊 Dashboard")
        st.markdown("""
        View price comparisons across stores with:
        - Interactive charts and graphs
        - Best deals highlighting
        - Store performance analysis
        - Live data scraping or saved data
        """)
        if st.button("Go to Dashboard", use_container_width=True, key="dashboard_btn"):
            st.switch_page("pages/dashboard.py")

# Search Products
with col2:
    with st.container(border=True):
        st.markdown("# 🔍 Search Products")
        st.markdown("""
        Find and filter products by:
        - Product name
        - Price range
        - Store availability
        - Savings percentage
        - Company brand
        """)
        if st.button("Open Search", use_container_width=True, key="search_btn"):
            st.switch_page("pages/search.py")

# Settings
with col3:
    with st.container(border=True):
        st.markdown("# ⚙️ Settings")
        st.markdown("""
        Manage your account:
        - Location permissions
        - Theme preferences
        - Favorite products
        - Password management
        - Export data
        """)
        if st.button("Go to Settings", use_container_width=True, key="settings_btn"):
            st.switch_page("pages/settings.py")

st.divider()

# Quick access section
st.subheader("⚡ Quick Access")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 View Charts", use_container_width=True):
        st.switch_page("pages/dashboard.py")
        
with col2:
    if st.button("🎁 Best Deals", use_container_width=True):
        st.switch_page("pages/dashboard.py")
        
with col3:
    if st.button("🔍 Find Products", use_container_width=True):
        st.switch_page("pages/search.py")
        
with col4:
    if st.button("👤 My Account", use_container_width=True):
        st.switch_page("pages/settings.py")

st.divider()

# Company brands section
st.subheader("🏢 Browse by Brand")
st.markdown("Click on a brand to view all their products and find the best deals!")

brands = [
    {
        "name": "Apple",
        "emoji": "🍎",
        "desc": "Premium tech products",
        "logo": "brands/apple-logo.svg"
    },
    {
        "name": "Samsung",
        "emoji": "🔵",
        "desc": "Diverse electronics",
        "logo": "brands/samsung-logo.svg"
    },
    {
        "name": "Google",
        "emoji": "🔴",
        "desc": "Android & smart devices",
        "logo": "brands/google-logo.svg"
    },
    {
        "name": "Sony",
        "emoji": "⚫",
        "desc": "Audio & entertainment",
        "logo": "brands/sony-logo.svg"
    },
    {
        "name": "Dell",
        "emoji": "💚",
        "desc": "Computers & peripherals",
        "logo": "brands/dell-logo.svg"
    },
    {
        "name": "LG",
        "emoji": "🟦",
        "desc": "Displays & monitors",
        "logo": "brands/lg-logo.svg"
    },
    {
        "name": "Logitech",
        "emoji": "🎮",
        "desc": "Input devices & gaming",
        "logo": "brands/logitech-logo.svg"
    },
    {
        "name": "Razer",
        "emoji": "🔴",
        "desc": "Gaming peripherals",
        "logo": "brands/razer-logo.svg"
    },
    {
        "name": "Corsair",
        "emoji": "🔷",
        "desc": "Gaming gear",
        "logo": "brands/corsair-logo.svg"
    },
]

col_width = 3
cols = st.columns(col_width, gap="large")

for idx, brand in enumerate(brands):
    with cols[idx % col_width]:
        with st.container(border=True):
            # Create a container for the logo with better styling
            try:
                # Try to display logo
                st.markdown(f"<div class='logo-container'>", unsafe_allow_html=True)
                st.image(brand["logo"], width=200, use_column_width=False)
                st.markdown("</div>", unsafe_allow_html=True)
            except:
                # Fallback to large emoji
                st.markdown(f"""
                <div style='
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 150px;
                    font-size: 80px;
                    background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%);
                    border-radius: 10px;
                    margin: 10px 0;
                '>
                {brand['emoji']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"<div class='brand-name'>{brand['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='brand-desc'>{brand['desc']}</div>", unsafe_allow_html=True)
            
            if st.button("🔍 Browse", use_container_width=True, key=f"brand_{idx}"):
                st.session_state.brand_filter = brand['name']
                st.switch_page("pages/search.py")

st.divider()

# Stats section
st.subheader("📈 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

import json
try:
    with open("data/prices.json", "r") as f:
        price_data = json.load(f)
        num_products = len(price_data.get('prices', {}))
        num_stores = len(set([store for product in price_data.get('prices', {}).values() for store in product.keys()]))
        
        with col1:
            st.metric("📦 Products", num_products)
        with col2:
            st.metric("🏪 Stores", num_stores)
        with col3:
            st.metric("💰 Last Updated", price_data.get('timestamp', 'Never')[:10])
        with col4:
            st.metric("📊 Tracked", f"{num_products * num_stores} prices")
except:
    with col1:
        st.metric("📦 Products", "—")
    with col2:
        st.metric("🏪 Stores", "—")
    with col3:
        st.metric("💰 Last Updated", "—")
    with col4:
        st.metric("📊 Tracked", "—")

st.divider()

# Help section
with st.expander("❓ Help & Tips", expanded=False):
    st.markdown("""
    ### How to use StockUp:
    
    1. **Dashboard** - Scrape prices and view comparisons
       - Use "Live Scraping" for current prices
       - Use "Load Saved Data" for previously scraped prices
       - View charts to analyze trends
    
    2. **Search** - Find specific products
       - Search by product name
       - Filter by price range and company
       - Sort by best price or savings
       - Export results
    
    3. **Settings** - Manage your account
       - Update profile information
       - Control location tracking
       - Manage preferences
       - Export your data
    
    ### Tips:
    - 💡 Use the search filters to find great deals
    - 💡 Sort by "Most Savings %" to find the best bargains
    - 💡 Filter by your preferred stores to compare prices
    - 💡 Enable location tracking for personalized recommendations
    """)

st.divider()

# Footer
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("login.py")
with col2:
    st.caption("🔐 Your data is secure and private")
with col3:
    st.caption("Made with ❤️ by StockUp Team")
