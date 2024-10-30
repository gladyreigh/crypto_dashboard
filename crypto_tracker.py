import requests
import sqlite3
import time
from datetime import datetime

class CryptoTracker:
    def __init__(self, database_name="crypto_data.db"):
        """Initialize the tracker with a database connection"""
        # Connect to SQLite database (creates it if it doesn't exist)
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.setup_database()
    
    def setup_database(self):
        """Create the database table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cryptocurrency TEXT,
                price_usd REAL,
                market_cap_usd REAL,
                volume_usd REAL,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()
        print("Database setup complete!")

    def fetch_crypto_data(self):
        """Fetch cryptocurrency data from CoinGecko"""
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def save_to_database(self, crypto_data):
        """Save the cryptocurrency data to the database"""
        if not crypto_data:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare data for both cryptocurrencies
        cryptos = ['bitcoin', 'ethereum']
        for crypto in cryptos:
            data = crypto_data[crypto]
            self.cursor.execute('''
                INSERT INTO crypto_prices 
                (cryptocurrency, price_usd, market_cap_usd, volume_usd, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                crypto,
                data['usd'],
                data['usd_market_cap'],
                data['usd_24h_vol'],
                timestamp
            ))
        
        self.conn.commit()

    def display_current_prices(self, crypto_data):
        """Display the current cryptocurrency prices"""
        if not crypto_data:
            return
            
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nTime: {current_time}")
        
        for crypto in ['bitcoin', 'ethereum']:
            data = crypto_data[crypto]
            print(f"\n{crypto.capitalize()}:")
            print(f"Price: ${data['usd']:,.2f}")
            print(f"Market Cap: ${data['usd_market_cap']:,.2f}")
            print(f"24h Volume: ${data['usd_24h_vol']:,.2f}")

    def display_latest_stored_data(self):
        """Display the most recent data from the database"""
        print("\nLatest stored data from database:")
        
        for crypto in ['bitcoin', 'ethereum']:
            self.cursor.execute('''
                SELECT price_usd, timestamp 
                FROM crypto_prices 
                WHERE cryptocurrency = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''', (crypto,))
            
            result = self.cursor.fetchone()
            if result:
                price, timestamp = result
                print(f"{crypto.capitalize()}: ${price:,.2f} at {timestamp}")

    def run(self, interval=60):
        """Run the tracker continuously"""
        print("Starting cryptocurrency price tracker...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                # Fetch and process data
                crypto_data = self.fetch_crypto_data()
                if crypto_data:
                    self.save_to_database(crypto_data)
                    self.display_current_prices(crypto_data)
                    self.display_latest_stored_data()
                
                # Wait for the next update
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nStopping price tracker...")
        finally:
            self.conn.close()

# Run the tracker
if __name__ == "__main__":
    tracker = CryptoTracker()
    tracker.run()