# StockUp Authentication System - Documentation

## 🔐 Login & Registration

StockUp now features a complete authentication system with user management and location tracking permissions.

## 🚀 Getting Started

### Start the Application

```bash
streamlit run login.py
```

The app will open at: `http://localhost:8502`

### Demo Account

For quick testing, use:
- **Username:** demo
- **Password:** demo123

Click "Demo Login" button for instant access.

## 📝 User Features

### 1. Registration

Create a new StockUp account:

1. Click the **"📝 Register"** tab
2. Enter:
   - **Username** (minimum 3 characters)
   - **Email** (optional)
   - **Password** (minimum 6 characters)
   - **Confirm Password**
3. Click **"✅ Register"**

**Password Requirements:**
- Minimum 6 characters
- Case-sensitive
- Can include numbers and special characters

### 2. Login

Access your StockUp account:

1. Click the **"🔑 Login"** tab
2. Enter your username and password
3. Click **"🔓 Login"**

### 3. Location Permission

After login, StockUp requests location tracking permission:

**Grant permission for:**
- 🏪 Nearby store recommendations
- 📍 Location-specific deals
- 🗺️ Optimized price comparisons

You can change this setting anytime in **Settings → Location**

## ⚙️ User Settings

Access settings by clicking the **👤** icon in the dashboard header.

### Account Tab
- View account information
- Account status

### Location Tab (📍)
- Enable/disable location tracking
- View privacy information
- Manage location permissions

### Preferences Tab (🎯)
- **Theme:** Light or Dark mode
- **Notifications:** Enable/disable alerts
- **Favorite Stores:** Select preferred retailers
- **Favorite Products:** Add products to track

### Security Tab (🔒)
- Change password
- View active sessions
- Account security settings

## 🔐 Authentication System

### User Data Storage

User accounts are stored in: `data/users.json`

**Stored Information:**
```json
{
  "username": {
    "password": "hashed_password",
    "email": "user@email.com",
    "created_at": "2025-11-22T...",
    "location_tracking": false,
    "location_permission": false,
    "preferences": {
      "theme": "light",
      "notifications": true,
      "favorite_stores": ["Amazon", "Walmart"],
      "favorite_products": ["Laptop", "Headphones"]
    }
  }
}
```

### Security Features

✅ **Password Hashing**
- Passwords are hashed with SHA256
- Plaintext passwords never stored

✅ **Session Management**
- Secure session state management
- Automatic logout capability

✅ **Privacy Controls**
- Location tracking is optional
- Users can revoke permissions anytime
- No data shared with third parties

## 🗺️ Location Tracking

### What It Does
- Identifies nearby stores
- Suggests location-specific deals
- Optimizes price comparisons for your area

### Privacy Assurance
- ✅ Your location is never shared
- ✅ Data stored securely and locally
- ✅ Can be disabled at any time
- ✅ Removable from account settings

### How to Enable/Disable

**During Login:**
- Accept or deny in the permission dialog

**After Login:**
- Go to **Settings → Location**
- Click "Enable" or "Disable" button

## 📱 Dashboard Access

After login and permission setup, you can access:

### Main Dashboard
- 📊 Price comparisons
- 🎁 Best deals
- 💰 Savings analysis
- 📥 Data export

### Settings
- ⚙️ Account preferences
- 📍 Location settings
- 🎯 Favorites management
- 🔒 Security options

## 🔑 Password Management

### Changing Your Password

1. Go to **Settings → Security**
2. Enter current password
3. Enter new password (min. 6 characters)
4. Confirm new password
5. Click **"🔐 Change Password"**

**Note:** Password change functionality coming in next update

### Forgot Password

Currently, there is no password recovery feature. For demo purposes, re-register with a new account.

## 👥 Multi-User Support

StockUp supports multiple user accounts:

- Each user has separate preferences
- Personalized price tracking
- Individual location settings
- Custom favorite stores and products

## 📊 User Data Files

```
data/
├── users.json          # User accounts and preferences
├── prices.json         # Price comparison data
└── price_report.txt    # Generated reports
```

## 🔄 Logout

To logout:

1. Click **"⚙️ Settings"** icon (👤) in dashboard
2. Or use **"🚪 Logout"** button in sidebar
3. You'll be returned to login page

## 🐛 Troubleshooting

### "Username not found"
- Check spelling of username
- Register if you don't have an account
- Try demo account (demo/demo123)

### "Invalid password"
- Passwords are case-sensitive
- Check Caps Lock
- Re-enter password carefully

### "Username already exists"
- Choose a different username
- Username must be unique
- Or login with existing account

### Location Permission Not Showing
- Reload the page
- Try logging out and back in
- Check browser permissions

### Can't Access Dashboard
- Ensure you're logged in
- Check that authentication passed
- Try demo account

## 🔐 Security Best Practices

✅ **DO:**
- Use strong, unique passwords
- Review location permissions
- Keep your account secure
- Check privacy settings regularly

❌ **DON'T:**
- Share your password
- Use simple passwords
- Leave session logged in on shared computers
- Grant unnecessary permissions

## 🚀 Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| Registration | ✅ Active | Create new accounts |
| Login | ✅ Active | Secure authentication |
| Location Permission | ✅ Active | Optional tracking |
| User Preferences | ✅ Active | Customizable settings |
| Password Change | 🔄 Coming | Future update |
| Password Recovery | 🔄 Coming | Future update |
| Email Verification | 🔄 Coming | Future update |
| Two-Factor Auth | 🔄 Coming | Future update |

## 📚 Related Modules

- **user_manager.py** - Core authentication logic
- **login.py** - Login interface
- **pages/dashboard.py** - Protected dashboard
- **pages/settings.py** - User settings

## 🆘 Support

For issues or questions:
1. Check this documentation
2. Review troubleshooting section
3. Use demo account to test
4. Check data/users.json file permissions

---

**Version:** 1.0 - Authentication System
**Last Updated:** November 22, 2025
**Status:** ✅ Production Ready
