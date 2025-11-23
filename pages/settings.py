"""
StockUp Settings Page
User preferences and account settings.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from user_manager import UserManager


def check_authentication():
    """Check if user is authenticated."""
    if not st.session_state.get("logged_in", False):
        st.error("❌ Please login first")
        if st.button("Go to Login"):
            st.switch_page("login.py")
        st.stop()


def main():
    """Settings page."""
    # Check authentication
    check_authentication()
    
    # Page configuration
    st.set_page_config(
        page_title="StockUp - Settings",
        page_icon="⚙️",
        layout="wide"
    )
    
    username = st.session_state.username
    user_manager = UserManager()
    
    # Header
    st.title("⚙️ Settings")
    st.markdown(f"Account settings for **{username}**")
    st.divider()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["👤 Account", "📍 Location", "🏪 Preferences", "🔒 Security"]
    )
    
    with tab1:
        st.subheader("Account Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Username", username)
        with col2:
            st.metric("Account Status", "✅ Active")
        
        st.divider()
        
        st.subheader("Account Actions")
        if st.button("🗑️ Delete Account", help="Permanently delete your account"):
            if st.checkbox("I understand this action cannot be undone"):
                st.error("❌ Account deletion is not available in this version")
    
    with tab2:
        st.subheader("📍 Location & Currency Settings")
        
        # Get user preferences for location
        prefs = user_manager.get_user_preferences(username)
        current_location = prefs.get('location', 'United States') if prefs else 'United States'
        
        # Currency conversion rates (USD as base)
        currency_rates = {
            'United States': {'currency': 'USD', 'rate': 1.0},
            'Canada': {'currency': 'CAD', 'rate': 1.36},
            'United Kingdom': {'currency': 'GBP', 'rate': 0.79},
            'Europe': {'currency': 'EUR', 'rate': 0.92},
            'Australia': {'currency': 'AUD', 'rate': 1.54},
            'Japan': {'currency': 'JPY', 'rate': 149.50},
            'India': {'currency': 'INR', 'rate': 83.12},
            'Mexico': {'currency': 'MXN', 'rate': 17.05},
            'Brazil': {'currency': 'BRL', 'rate': 4.97},
            'China': {'currency': 'CNY', 'rate': 7.24},
        }
        
        st.write("Select your location to convert prices to your local currency:")
        
        st.divider()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            selected_location = st.selectbox(
                "📍 Select Your Location",
                options=list(currency_rates.keys()),
                index=list(currency_rates.keys()).index(current_location) if current_location in currency_rates else 0,
                help="Choose your location for currency conversion"
            )
            
            currency_info = currency_rates[selected_location]
            st.metric("Currency", f"{currency_info['currency']}")
            st.metric("Conversion Rate", f"1 USD = {currency_info['rate']:.2f} {currency_info['currency']}")
        
        with col2:
            st.info(f"""
            **Location: {selected_location}**
            
            Currency: {currency_info['currency']}
            
            With this setting, all prices will be displayed in **{currency_info['currency']}**
            
            Example:
            - $100 USD → {currency_info['rate'] * 100:.2f} {currency_info['currency']}
            """)
        
        st.divider()
        
        # Location tracking section
        has_location = user_manager.has_location_permission(username)
        
        st.subheader("🗺️ Location Tracking")
        st.write("Enable location tracking to get:")
        st.markdown("""
        - 🏪 Nearby store recommendations
        - 📍 Location-specific deals
        - 🗺️ Optimized price comparisons
        """)
        
        st.divider()
        
        if has_location:
            st.success("✅ Location tracking is **ENABLED**")
            if st.button("❌ Disable Location Tracking"):
                user_manager.revoke_location_tracking(username)
                st.success("Location tracking disabled!")
                st.rerun()
        else:
            st.info("📍 Location tracking is **DISABLED**")
            if st.button("✅ Enable Location Tracking"):
                user_manager.grant_location_tracking(username)
                st.success("Location tracking enabled!")
                st.rerun()
        
        st.divider()
        
        st.info("""
        **Privacy Notice:**
        - Your location is never shared
        - Data is stored securely
        - You can change this at any time
        """)
        
        # Save location preference
        if st.button("💾 Save Location & Currency", use_container_width=True, type="primary"):
            new_prefs = prefs if prefs else {}
            new_prefs['location'] = selected_location
            user_manager.update_user_preferences(username, new_prefs)
            st.success(f"✅ Location set to {selected_location}! Prices will now show in {currency_info['currency']}")
    
    with tab3:
        st.subheader("🎯 User Preferences")
        
        # Get user preferences
        prefs = user_manager.get_user_preferences(username)
        
        # Theme preference
        theme = st.radio(
            "Theme",
            ["light", "dark"],
            index=0 if prefs.get('theme') == 'light' else 1
        )
        
        # Notifications
        notifications = st.checkbox(
            "Enable Notifications",
            value=prefs.get('notifications', True)
        )
        
        st.divider()
        
        st.subheader("🏪 Favorite Stores")
        st.write("Select your preferred stores for better recommendations:")
        
        all_stores = ["Amazon", "Walmart", "Best Buy", "Target", "eBay"]
        favorite_stores = prefs.get('favorite_stores', [])
        
        selected_stores = []
        cols = st.columns(3)
        for idx, store in enumerate(all_stores):
            with cols[idx % 3]:
                is_selected = st.checkbox(
                    store,
                    value=store in favorite_stores,
                    key=f"store_{store}"
                )
                if is_selected:
                    selected_stores.append(store)
        
        st.divider()
        
        st.subheader("⭐ Favorite Products")
        st.write("Products you want to track regularly:")
        
        favorite_products = prefs.get('favorite_products', [])
        product_text = st.text_area(
            "Enter products (one per line)",
            value="\n".join(favorite_products),
            height=100
        )
        
        st.divider()
        
        if st.button("💾 Save Preferences", use_container_width=True, type="primary"):
            new_prefs = {
                'theme': theme,
                'notifications': notifications,
                'favorite_stores': selected_stores,
                'favorite_products': [p.strip() for p in product_text.split('\n') if p.strip()]
            }
            user_manager.update_user_preferences(username, new_prefs)
            st.success("✅ Preferences saved!")
    
    with tab4:
        st.subheader("🔒 Security")
        
        st.write("Password & Security Settings")
        
        st.divider()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            current_password = st.text_input(
                "Current Password",
                type="password",
                key="current_pass"
            )
        with col2:
            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_pass"
            )
        
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            key="confirm_pass"
        )
        
        if st.button("🔐 Change Password", use_container_width=True):
            if not current_password or not new_password or not confirm_password:
                st.warning("Please fill all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                # Verify current password
                success, _ = user_manager.authenticate(username, current_password)
                if success:
                    st.info("✅ Password change functionality coming soon")
                else:
                    st.error("❌ Current password is incorrect")
        
        st.divider()
        
        st.subheader("Active Sessions")
        st.info(f"📱 Current Session: {username}")
        st.caption("You have 1 active session")
    
    st.divider()
    
    # Bottom navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📊 Back to Dashboard"):
            st.switch_page("pages/dashboard.py")
    with col2:
        st.empty()
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.success("Logged out successfully!")
            st.switch_page("login.py")


if __name__ == "__main__":
    main()
