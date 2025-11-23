# StockUp - Development Instructions

## Project Overview
**StockUp** is a Python application for comparing product prices across multiple stores and identifying best deals, with both CLI and interactive Streamlit dashboard interfaces. Stock up on savings!

## Architecture
- **Main Application**: `src/main.py` - CLI application orchestrating the comparison workflow
- **Dashboard**: `dashboard.py` - Streamlit-based interactive visualization interface
- **Price Scraper**: `src/price_scraper.py` - Retrieves price data from stores
- **Comparison Engine**: `src/comparison_engine.py` - Analyzes and compares prices
- **Report Generator**: `src/report_generator.py` - Creates formatted reports

## Key Features
- Multi-store price comparison (Amazon, Walmart, Best Buy, Target, eBay)
- Best deal identification and highlighting
- Statistical analysis of prices (average, range, savings percentage)
- Report generation in multiple formats (TXT, CSV, JSON)
- Price tracking with timestamps
- Interactive Streamlit dashboard with charts and visualizations
- Live price scraping or historical data analysis

## Development Guidelines
- Keep modules focused and single-responsibility
- Maintain compatibility with Python 3.7+
- Use type hints for function signatures
- Document public functions and classes
- Add unit tests when adding new features
- Follow PEP 8 style guidelines

## Running the Application

### CLI Mode
```bash
python src/main.py
```

### Dashboard Mode (Recommended)
```bash
streamlit run dashboard.py
```
Opens at: http://localhost:8501

## Configuration
Edit `products.json` to change products and stores being compared.

## Dependencies
Install with: `pip install -r requirements.txt`
- streamlit >= 1.28.1
- pandas >= 2.1.3
- plotly >= 5.18.0

## Output Files
- `data/prices.json` - Raw price data with timestamps
- `data/price_report.txt` - Formatted comparison report
- CSV/JSON exports from dashboard
