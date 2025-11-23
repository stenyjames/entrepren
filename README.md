# 💰 StockUp - Smart Price Comparison

**StockUp** is a Python application that compares product prices across multiple stores and identifies the best deals. Save money by finding the lowest prices instantly!

## Features

- **Price Scraping**: Fetch prices for products from multiple stores
- **Price Comparison**: Compare prices and find the best deals
- **Detailed Reports**: Generate comprehensive price comparison reports
- **Statistics**: Calculate average prices, ranges, and potential savings
- **Price Tracking**: Save historical price data for trend analysis
- **Multiple Export Formats**: Generate reports in text, CSV, and JSON formats
- **Interactive Dashboard**: Streamlit-based visual interface with charts and analytics
- **Live or Saved Data**: Choose between real-time scraping or analyzing historical data

## Project Structure

```
.
├── dashboard.py                # Streamlit dashboard application
├── src/
│   ├── main.py                 # Main CLI application entry point
│   ├── price_scraper.py        # Price scraping module
│   ├── comparison_engine.py    # Price comparison logic
│   └── report_generator.py     # Report generation
├── data/                       # Directory for storing price data
├── products.json               # Product and store configuration
├── logo.svg                    # Application logo
├── README.md                   # This file
├── PROFILE.md                  # Project profile
├── BRAND_GUIDELINES.md         # Branding guidelines
└── .github/
    └── copilot-instructions.md # Development instructions
```

## Installation

1. Clone or download the project
2. Ensure you have Python 3.7+ installed
3. No external dependencies required for the basic version

## Usage

### Command Line Interface

Run the application:

```bash
python src/main.py
```

### Interactive Dashboard with Login

Launch the StockUp dashboard with authentication:

```bash
streamlit run login.py
```

**Features:**
- 🔐 User registration and login
- 📍 Location tracking permissions
- 🎨 Interactive price comparison charts
- 🎁 Best deals visualization
- 💰 Savings percentage analysis
- 🏆 Store performance metrics
- 📑 Detailed data tables
- ⚙️ User settings and preferences
- 📥 Export to CSV/JSON

### Login Credentials

For quick testing, use the demo account:
- **Username:** demo
- **Password:** demo123

### Configuration

Edit `products.json` to add or modify products and stores:

```json
[
  {
    "name": "Product Name",
    "stores": ["Store1", "Store2", "Store3"]
  }
]
```

### Supported Stores

- Amazon
- Walmart
- Best Buy
- Target
- eBay

## Modules

### main.py
The main application that orchestrates the price comparison workflow:
- Loads products from configuration
- Scrapes prices
- Compares prices
- Generates reports

### price_scraper.py
Handles price data retrieval:
- Simulates price scraping from multiple stores
- Manages store configurations
- Generates realistic price variations

### comparison_engine.py
Performs price analysis:
- Compares prices across stores
- Finds best deals
- Calculates statistics (average, range, savings)
- Compares historical prices to find drops

### report_generator.py
Generates formatted reports:
- Text format reports
- CSV format for spreadsheets
- JSON format for data integration

## Output

The application generates:
- Console output with best deals
- `data/prices.json` - Historical price data with timestamps
- `data/price_report.txt` - Detailed price comparison report

## Future Enhancements

- Real web scraping using BeautifulSoup or Selenium
- Database integration for historical price tracking
- Web interface using Flask or Django
- Email notifications for price drops
- Price prediction using machine learning
- Support for discount codes and coupons

## License

This project is open source and available under the MIT License.
