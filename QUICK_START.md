# Quick Start Guide - StockUp

## 🚀 Getting Started with StockUp

### Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)

### Installation

1. **Clone/Navigate to project**
   ```bash
   cd price-comparison-app
   ```

2. **Create virtual environment** (if not already created)
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: CLI Mode
For command-line interface with text-based output:

```bash
python src/main.py
```

**Output:**
- Console display with best deals  
- `data/prices.json` - Price data with timestamps
- `data/price_report.txt` - Detailed report

#### Option 2: Interactive StockUp Dashboard (Recommended)
For visual, interactive price comparison:

```bash
streamlit run dashboard.py
```

**Opens in browser at:** `http://localhost:8501`

**Dashboard features:**
- 📊 Interactive charts and visualizations
- 🎁 Best deals showcase
- 💰 Savings analysis
- 🏆 Store performance metrics
- 📋 Detailed data tables
- 📥 Export to CSV/JSON

### Configuration

Edit `products.json` to customize what you're comparing:

```json
[
  {
    "name": "Product Name",
    "stores": ["Amazon", "Walmart", "Best Buy", "Target", "eBay"]
  }
]
```

### Dashboard Walkthrough

#### 1. **Settings Sidebar**
   - Choose between "Live Scraping" or "Load Saved Data"
   - Click "Scrape Prices Now" to fetch current prices
   - Filter view: All Products, Top Deals, or Best by Store

#### 2. **Summary Metrics**
   - Quick overview: Number of products, total savings, average savings %
   - Store count for transparency

#### 3. **Analysis Tabs**

   **📋 All Prices Tab**
   - Bar chart showing all prices by product and store
   - Easily compare prices across retailers
   - Color-coded by store

   **🎁 Best Deals Tab**
   - Scatter plot showing best prices vs potential savings
   - Bubble size represents savings amount
   - Color intensity shows savings magnitude

   **💰 Savings % Tab**
   - Horizontal bar chart showing percentage savings
   - Identifies products with highest savings potential
   - Color gradient from red to green

   **🏆 Store Performance Tab**
   - Shows which store has the most best deals
   - Quick indicator of store competitiveness
   - Bar chart with count of best deals

   **📑 Details Table Tab**
   - Complete data table with all information
   - Sortable and filterable columns
   - Best for detailed analysis

#### 4. **Best Deals Section**
   - Cards showing your best deals
   - Includes: Best Price, Store, Average Price, Savings Amount
   - Savings percentage indicator

#### 5. **Export Options**
   - Download as CSV for Excel/spreadsheet use
   - Download as JSON for integration/analysis

### Supported Stores

- 🛒 Amazon
- 🏬 Walmart
- 🎮 Best Buy
- 🎯 Target
- 🛍️ eBay

### Tips & Tricks

1. **Set a Schedule**: Run the CLI version via cron (Linux/macOS) or Task Scheduler (Windows) to track price changes over time

2. **Compare Historically**: Use "Load Saved Data" to compare prices from different times

3. **Export Reports**: Download CSV for further analysis in spreadsheets

4. **Add Products**: Edit `products.json` to add new products to track

5. **Performance**: Dashboard works best with 5-20 products; large datasets may take longer to load

### Troubleshooting

**Dashboard won't start?**
- Ensure Streamlit is installed: `pip install streamlit`
- Check port 8501 isn't in use
- Try: `streamlit run dashboard.py --server.port 8502`

**No price data?**
- Click "Scrape Prices Now" button in sidebar
- Check that products.json has valid store names
- Ensure all stores in products.json are supported

**Plots not showing?**
- Ensure Plotly is installed: `pip install plotly`
- Refresh browser page
- Clear Streamlit cache: `streamlit cache clear`

**Installation issues?**
- Try upgrading pip: `pip install --upgrade pip`
- Delete `.venv` folder and reinstall
- Use Python 3.9+ for best compatibility

### Project Structure

```
price-comparison-app/
├── dashboard.py           # Streamlit app
├── src/
│   ├── main.py           # CLI application
│   ├── price_scraper.py
│   ├── comparison_engine.py
│   └── report_generator.py
├── data/                 # Price data output
├── products.json         # Configuration
├── requirements.txt      # Dependencies
└── README.md
```

### Next Steps

1. Run the dashboard: `streamlit run dashboard.py`
2. Customize products in `products.json`
3. Analyze price trends
4. Export reports for further analysis
5. Schedule regular price checks

---

**Need help?** Check README.md or BRAND_GUIDELINES.md for more information.
