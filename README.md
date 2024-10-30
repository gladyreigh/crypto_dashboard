# Cryptocurrency Price Tracking and Analysis System

## Overview
This project is a real-time cryptocurrency tracking system that collects price data, stores it in a database, and visualizes it through an interactive web dashboard. The system consists of three main components:
1. Data Collector (crypto_tracker.py)
2. Data Visualizer (crypto_visualizer.py)
3. Web Dashboard (crypto_dashboard.py)

## Features
- Real-time price tracking for Bitcoin and Ethereum
- Automatic data collection and storage
- Interactive data visualizations
- Web-based dashboard with live updates
- Historical price analysis
- Market metrics visualization
- Summary statistics

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd cryptocurrency-tracker
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages (install them one by one manually to avoid errors):
```bash
pip install requests 
pip install pandas 
pip install sqlite3 
pip install matplotlib 
pip install seaborn 
pip install streamlit 
pip install plotly
```

## Project Structure
```
cryptocurrency-tracker/
│
├── crypto_tracker.py      # Data collection script
├── crypto_visualizer.py   # Data visualization script
├── crypto_dashboard.py    # Streamlit dashboard
├── requirements.txt       # Python dependencies
└── crypto_data.db        # SQLite database (created automatically)
```

## Usage

### 1. Data Collection
Run the data collector to start gathering cryptocurrency prices:
```bash
python crypto_tracker.py
```
This script will:
- Fetch prices every minute
- Store data in SQLite database
- Display current prices in the terminal
- Run continuously until stopped (Ctrl+C)

### 2. Data Visualization
Generate static visualizations of the collected data:
```bash
python crypto_visualizer.py
```
This will create:
- price_trends.png
- price_comparison.png
- bitcoin_metrics.png
- ethereum_metrics.png

### 3. Web Dashboard
Launch the interactive web dashboard:
```bash
streamlit run crypto_dashboard.py
```
The dashboard provides:
- Real-time price updates
- Interactive charts
- Multiple time period views
- Market metrics
- Summary statistics

## Dashboard Features
- **Price Display**: Current prices for Bitcoin and Ethereum
- **Time Period Selection**: View data for different time ranges
- **Interactive Charts**: 
  - Price trends
  - Volume analysis
  - Market metrics
- **Summary Statistics**: Key metrics and price changes
- **Auto-refresh**: Regular data updates

## Database Structure
The SQLite database (`crypto_data.db`) contains a single table:
```sql
CREATE TABLE crypto_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cryptocurrency TEXT,
    price_usd REAL,
    market_cap_usd REAL,
    volume_usd REAL,
    timestamp DATETIME
)
```

## Customization
You can modify the code to:
- Add more cryptocurrencies (modify the API parameters)
- Change update frequency (adjust the time.sleep() value)
- Add new visualizations
- Modify dashboard layout
- Add technical indicators

## Troubleshooting
1. **Database Issues**: 
   - If the database gets corrupted, delete `crypto_data.db` and restart the collector
   - The system will create a new database automatically

2. **API Rate Limits**: 
   - CoinGecko API has rate limits
   - Adjust the collection interval if needed

3. **Dashboard Not Updating**: 
   - Ensure the data collector is running
   - Check database permissions
   - Click the refresh button in the dashboard

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.