import sqlite3
from datetime import datetime, timedelta

def query_crypto_history(database_name="crypto_data.db", hours=24):
    """Query the cryptocurrency price history for the last specified hours"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Calculate the timestamp for hours ago
    time_threshold = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Query data for both cryptocurrencies
        for crypto in ['bitcoin', 'ethereum']:
            print(f"\n{crypto.capitalize()} price history for the last {hours} hours:")
            
            cursor.execute('''
                SELECT timestamp, price_usd
                FROM crypto_prices
                WHERE cryptocurrency = ? AND timestamp >= ?
                ORDER BY timestamp ASC
            ''', (crypto, time_threshold))
            
            results = cursor.fetchall()
            
            if results:
                for timestamp, price in results:
                    print(f"{timestamp}: ${price:,.2f}")
                
                # Calculate price change
                first_price = results[0][1]
                last_price = results[-1][1]
                price_change = ((last_price - first_price) / first_price) * 100
                
                print(f"\nPrice change: {price_change:.2f}%")
            else:
                print("No data available for this time period")
    
    finally:
        conn.close()

if __name__ == "__main__":
    # Query the last 24 hours of data
    query_crypto_history()