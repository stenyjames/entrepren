# 🚀 StockUp - Setup & Deployment Guide

## 📋 System Requirements

- **Python:** 3.7 or higher
- **OS:** Windows, macOS, or Linux
- **RAM:** 2GB minimum
- **Disk Space:** 500MB

## 🔧 Installation

### 1. Clone/Navigate to Project
```bash
cd price-comparison-app
# or your project directory
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv

# macOS/Linux
python3 -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Running StockUp

### Start Application
```bash
streamlit run login.py
```

### Access in Browser
- **Local:** http://localhost:8502
- **Network:** http://192.168.x.x:8502

### Demo Login
- **Username:** demo
- **Password:** demo123

## 📁 Project Structure

```
stockup/
├── login.py                    # Authentication entry point
├── src/
│   ├── main.py                 # CLI application
│   ├── user_manager.py         # Authentication system
│   ├── price_scraper.py        # Price data retrieval
│   ├── comparison_engine.py    # Price comparison logic
│   └── report_generator.py     # Report generation
├── pages/
│   ├── dashboard.py            # Main dashboard
│   └── settings.py             # User settings
├── data/
│   ├── users.json              # User accounts
│   ├── prices.json             # Price data
│   └── price_report.txt        # Reports
├── products.json               # Product configuration
├── requirements.txt            # Python dependencies
├── logo.svg                    # App icon
├── logo-stockup.svg            # Branding logo
├── README.md                   # Main documentation
├── QUICK_START.md              # Quick start guide
├── LOGIN_GUIDE.md              # Authentication guide
├── AUTHENTICATION_SUMMARY.md   # Summary of auth features
└── BRAND_GUIDELINES.md         # Brand standards
```

## 🎯 Features Overview

### 🔐 Authentication
- User registration and login
- Secure password hashing
- Demo account access
- Multi-user support

### 📍 Location Tracking
- Optional permission system
- Privacy-focused design
- User-controlled settings
- Local data storage

### 📊 Dashboard
- Interactive price charts
- Best deals finder
- Savings calculator
- Data export (CSV/JSON)

### ⚙️ Settings
- User preferences
- Theme selection
- Favorite stores
- Location management

## 🔑 First-Time Setup

1. **Start the app:**
   ```bash
   streamlit run login.py
   ```

2. **Create account or login:**
   - New user: Click "📝 Register" tab
   - Existing: Click "🔑 Login" tab
   - Demo: Click "Demo Login" button

3. **Grant permissions:**
   - Review location permission dialog
   - Click "✅ Grant" or "❌ Deny"

4. **Explore dashboard:**
   - View price comparisons
   - Check best deals
   - Adjust settings

## 🔄 Configuration

### Products to Compare
Edit `products.json`:
```json
[
  {
    "name": "Product Name",
    "stores": ["Amazon", "Walmart", "Best Buy", "Target", "eBay"]
  }
]
```

### User Preferences
Managed through Settings interface:
- Theme (Light/Dark)
- Notifications
- Favorite stores
- Favorite products

## 📊 Running CLI Version

For command-line interface:
```bash
python src/main.py
```

Output:
- Console display with best deals
- `data/prices.json` - Price data
- `data/price_report.txt` - Report

## 🌐 Deployment Options

### Local Development
```bash
streamlit run login.py
```

### Remote Server (Linux/macOS)
```bash
# Background process
nohup streamlit run login.py > logs/stockup.log 2>&1 &

# With supervisor
[program:stockup]
command=streamlit run login.py
directory=/path/to/stockup
```

### Docker Container
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "login.py"]
```

## 🔒 Security Checklist

- ✅ Change demo password in production
- ✅ Use HTTPS for remote access
- ✅ Secure database credentials
- ✅ Regular backups of data/users.json
- ✅ Monitor access logs
- ✅ Update dependencies regularly

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
streamlit run login.py --server.port 8503
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\Activate.ps1  # Windows
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Streamlit Cache Issues
```bash
streamlit cache clear
```

## 📊 Monitoring

### Logs Location
- Streamlit: Console output
- User data: `data/users.json`
- Price data: `data/prices.json`

### Check Application Health
```bash
# Test Python environment
python -c "import streamlit; print(streamlit.__version__)"

# Verify users file
cat data/users.json
```

## 🔄 Backup & Restore

### Backup User Data
```bash
# Linux/macOS
cp -r data/ data_backup_$(date +%Y%m%d)

# Windows
xcopy data data_backup_%date:~10,4%%date:~4,2%%date:~7,2% /E
```

### Restore Data
```bash
cp -r data_backup_YYYYMMDD/* data/
```

## 📈 Performance Tips

1. **Limit Products**
   - Keep products list under 20 items
   - Large lists slow down dashboard

2. **Cache Results**
   - Use "Load Saved Data" option
   - Reduces API calls

3. **Browser Cache**
   - Clear browser cache if issues occur
   - Use Ctrl+Shift+Delete (Windows/Linux) or Cmd+Shift+Delete (macOS)

4. **Server Resources**
   - Monitor system memory
   - Close unused applications
   - Restart application if needed

## 🔐 Database Security

### User Data Protection
- Passwords hashed with SHA256
- No plaintext storage
- Local file storage only
- JSON format

### Privacy Features
- Location tracking optional
- User-controlled permissions
- Data never shared
- Easy to disable

## 📚 Additional Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Python Docs:** https://python.org/doc
- **Project README:** README.md
- **Login Guide:** LOGIN_GUIDE.md

## 🆘 Support Channels

1. Check documentation
2. Review troubleshooting section
3. Check application logs
4. Verify data/users.json exists
5. Test with demo account

## ✅ Verification Checklist

- [ ] Python 3.7+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Application runs: `streamlit run login.py`
- [ ] Login page loads
- [ ] Demo account works
- [ ] Can register new account
- [ ] Can access dashboard
- [ ] Settings page works
- [ ] Can logout

---

**Setup Version:** 1.0
**Last Updated:** November 22, 2025
**Status:** ✅ Ready for Deployment
