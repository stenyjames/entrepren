"""
Authentication and User Management Module
Handles user login, registration, and session management.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Tuple


class UserManager:
    """Manages user accounts and authentication."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize user manager."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.load_users()
    
    def load_users(self) -> Dict:
        """Load users from file."""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
        return self.users
    
    def save_users(self) -> None:
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = "") -> Tuple[bool, str]:
        """
        Register a new user.
        
        Returns:
            (success: bool, message: str)
        """
        # Validate input
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check if user exists
        if username in self.users:
            return False, "Username already exists"
        
        # Create new user
        self.users[username] = {
            'password': self.hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'location_tracking': False,
            'location_permission': False,
            'preferences': {
                'theme': 'light',
                'notifications': True,
                'favorite_stores': [],
                'favorite_products': []
            }
        }
        
        self.save_users()
        return True, f"User '{username}' registered successfully"
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate a user.
        
        Returns:
            (success: bool, message: str)
        """
        if username not in self.users:
            return False, "Username not found"
        
        user = self.users[username]
        if user['password'] != self.hash_password(password):
            return False, "Invalid password"
        
        return True, "Authentication successful"
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self.users
    
    def get_user_preferences(self, username: str) -> Optional[Dict]:
        """Get user preferences."""
        if username in self.users:
            return self.users[username].get('preferences', {})
        return None
    
    def update_user_preferences(self, username: str, preferences: Dict) -> bool:
        """Update user preferences."""
        if username in self.users:
            self.users[username]['preferences'].update(preferences)
            self.save_users()
            return True
        return False
    
    def request_location_permission(self, username: str) -> bool:
        """Request location tracking permission from user."""
        if username in self.users:
            self.users[username]['location_permission'] = True
            self.save_users()
            return True
        return False
    
    def grant_location_tracking(self, username: str) -> bool:
        """Grant location tracking permission."""
        if username in self.users:
            self.users[username]['location_tracking'] = True
            self.save_users()
            return True
        return False
    
    def revoke_location_tracking(self, username: str) -> bool:
        """Revoke location tracking permission."""
        if username in self.users:
            self.users[username]['location_tracking'] = False
            self.save_users()
            return True
        return False
    
    def has_location_permission(self, username: str) -> bool:
        """Check if user has granted location tracking permission."""
        if username in self.users:
            return self.users[username].get('location_tracking', False)
        return False
    
    def add_favorite_store(self, username: str, store: str) -> bool:
        """Add a store to user's favorites."""
        if username in self.users:
            if store not in self.users[username]['preferences']['favorite_stores']:
                self.users[username]['preferences']['favorite_stores'].append(store)
                self.save_users()
            return True
        return False
    
    def add_favorite_product(self, username: str, product: str) -> bool:
        """Add a product to user's favorites."""
        if username in self.users:
            if product not in self.users[username]['preferences']['favorite_products']:
                self.users[username]['preferences']['favorite_products'].append(product)
                self.save_users()
            return True
        return False
    
    def get_favorite_stores(self, username: str) -> list:
        """Get user's favorite stores."""
        if username in self.users:
            return self.users[username]['preferences'].get('favorite_stores', [])
        return []
    
    def get_favorite_products(self, username: str) -> list:
        """Get user's favorite products."""
        if username in self.users:
            return self.users[username]['preferences'].get('favorite_products', [])
        return []
