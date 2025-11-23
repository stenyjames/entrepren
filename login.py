"""
StockUp Authentication Dashboard
Login and registration interface with location tracking permission.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from user_manager import UserManager

# Compatibility wrapper for st.switch_page
def switch_page(page_path):
    """Navigate to another page with fallback for older Streamlit versions"""
    try:
        st.switch_page(page_path)
    except AttributeError:
        # Fallback for Streamlit < 1.28
        st.session_state['redirect_to'] = page_path
        st.rerun()


def initialize_auth_session():
    """Initialize authentication session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "location_permission" not in st.session_state:
        st.session_state.location_permission = False
    if "show_location_prompt" not in st.session_state:
        st.session_state.show_location_prompt = False


def show_login_page(user_manager: UserManager):
    """Display login page."""
    # Logo and header
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        try:
            st.image("logo-icon.svg", width=80)
        except:
            st.write("💰")
    with col2:
        st.title("StockUp")
        st.markdown("**Stock Up on Savings!**")
    
    st.divider()
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Welcome Back!")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_username = st.text_input(
                "Username",
                key="login_username",
                placeholder="Enter your username"
            )
        with col2:
            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password",
                placeholder="Enter your password"
            )
        
        if st.button("🔓 Login", use_container_width=True, type="primary"):
            if login_username and login_password:
                success, message = user_manager.authenticate(login_username, login_password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.session_state.show_location_prompt = True
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter both username and password")
        
        # Demo login option
        st.divider()
        st.caption("💡 **Demo:** Username: demo | Password: demo123")
        if st.button("Demo Login", use_container_width=True):
            if not user_manager.user_exists("demo"):
                user_manager.register_user("demo", "demo123", "demo@stockup.app")
            success, msg = user_manager.authenticate("demo", "demo123")
            if success:
                st.session_state.logged_in = True
                st.session_state.username = "demo"
                st.session_state.show_location_prompt = True
                st.success("Demo login successful!")
                st.rerun()
    
    with tab2:
        st.subheader("Create New Account")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            reg_username = st.text_input(
                "Choose a username",
                key="reg_username",
                placeholder="At least 3 characters"
            )
        with col2:
            reg_email = st.text_input(
                "Email (optional)",
                key="reg_email",
                placeholder="your@email.com"
            )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            reg_password = st.text_input(
                "Choose a password",
                type="password",
                key="reg_password",
                placeholder="At least 6 characters"
            )
        with col2:
            reg_password_confirm = st.text_input(
                "Confirm password",
                type="password",
                key="reg_password_confirm",
                placeholder="Repeat password"
            )
        
        if st.button("✅ Register", use_container_width=True, type="primary"):
            if not reg_username or not reg_password:
                st.warning("Username and password are required")
            elif reg_password != reg_password_confirm:
                st.error("Passwords do not match")
            else:
                success, message = user_manager.register_user(
                    reg_username, 
                    reg_password, 
                    reg_email
                )
                if success:
                    st.success(message)
                    st.info("✅ Account created! Please login with your credentials.")
                else:
                    st.error(message)


def show_location_permission_dialog(user_manager: UserManager):
    """Show location permission request dialog."""
    username = st.session_state.username
    
    st.warning("📍 **Location Tracking Permission**")
    st.markdown("""
    StockUp would like to access your location to:
    - 🏪 Show nearby stores
    - 📍 Suggest local deals
    - 🗺️ Optimize price comparisons for your area
    
    Your location data is:
    - ✅ Used only for store recommendations
    - ✅ Never shared with third parties
    - ✅ Removable at any time from settings
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Grant Permission", use_container_width=True):
            user_manager.grant_location_tracking(username)
            st.session_state.location_permission = True
            st.session_state.show_location_prompt = False
            st.success("✅ Location permission granted!")
            st.rerun()
    
    with col2:
        if st.button("❌ Deny Permission", use_container_width=True):
            st.session_state.location_permission = False
            st.session_state.show_location_prompt = False
            st.info("You can enable location tracking later in Settings")
            st.rerun()


def main():
    """Main authentication application."""
    # Set page config
    st.set_page_config(
        page_title="StockUp - Login",
        page_icon="💰",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session
    initialize_auth_session()
    
    # Create user manager
    user_manager = UserManager()
    
    # Check if user is logged in
    if st.session_state.logged_in:
        # Show location permission prompt if needed
        if st.session_state.show_location_prompt:
            st.markdown(f"### Welcome, **{st.session_state.username}**! 👋")
            st.divider()
            show_location_permission_dialog(user_manager)
        else:
            # User is logged in and has handled location prompt
            st.success(f"✅ Logged in as: **{st.session_state.username}**")
            st.info("🚀 You can now access StockUp!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🏠 Go to Menu", use_container_width=True):
                    st.switch_page("pages/menu.py")
            with col2:
                if st.button("📊 Dashboard", use_container_width=True):
                    st.switch_page("pages/dashboard.py")
            with col3:
                if st.button("🚪 Logout", use_container_width=True):
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.session_state.location_permission = False
                    st.session_state.show_location_prompt = False
                    st.success("Logged out successfully!")
                    st.rerun()
    else:
        # Show login page
        show_login_page(user_manager)
        
        # Footer
        st.divider()
        st.markdown("""
        <div style='text-align: center; color: gray; font-size: 12px;'>
            <p>💰 StockUp - Smart Price Comparison</p>
            <p>Stock Up on Savings!</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
