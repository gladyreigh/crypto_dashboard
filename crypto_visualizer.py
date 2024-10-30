import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns

class CryptoVisualizer:
    def __init__(self, database_name="crypto_data.db"):
        """Initialize the visualizer with database connection"""
        self.conn = sqlite3.connect(database_name)
        # Set style for better-looking graphs
        plt.style.use('seaborn')
        sns.set_palette("husl")
    
    def fetch_data(self, hours=24):
        """Fetch cryptocurrency data from database for the specified time period"""
        time_threshold = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
        SELECT cryptocurrency, timestamp, price_usd, market_cap_usd, volume_usd
        FROM crypto_prices
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
        """
        
        # Read data into a pandas DataFrame
        df = pd.read_sql_query(
            query, 
            self.conn, 
            params=(time_threshold,),
            parse_dates=['timestamp']
        )
        return df
    
    def plot_price_trends(self, hours=24):
        """Create a line plot showing price trends for both cryptocurrencies"""
        df = self.fetch_data(hours)
        
        plt.figure(figsize=(12, 6))
        
        # Plot each cryptocurrency
        for crypto in ['bitcoin', 'ethereum']:
            crypto_data = df[df['cryptocurrency'] == crypto]
            plt.plot(
                crypto_data['timestamp'], 
                crypto_data['price_usd'],
                label=crypto.capitalize(),
                linewidth=2,
                marker='o',
                markersize=1
            )
        
        plt.title(f'Cryptocurrency Prices - Last {hours} Hours')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('price_trends.png')
        plt.close()
    
    def plot_price_comparison(self, hours=24):
        """Create a normalized price comparison plot"""
        df = self.fetch_data(hours)
        
        plt.figure(figsize=(12, 6))
        
        # Normalize prices for comparison
        for crypto in ['bitcoin', 'ethereum']:
            crypto_data = df[df['cryptocurrency'] == crypto]
            initial_price = crypto_data['price_usd'].iloc[0]
            normalized_prices = (crypto_data['price_usd'] / initial_price) * 100
            
            plt.plot(
                crypto_data['timestamp'],
                normalized_prices,
                label=crypto.capitalize(),
                linewidth=2
            )
        
        plt.title(f'Normalized Price Comparison - Last {hours} Hours (Starting at 100)')
        plt.xlabel('Time')
        plt.ylabel('Normalized Price')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig('price_comparison.png')
        plt.close()
    
    def plot_market_metrics(self, crypto='bitcoin', hours=24):
        """Create a multi-metric visualization for a single cryptocurrency"""
        df = self.fetch_data(hours)
        crypto_data = df[df['cryptocurrency'] == crypto]
        
        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # Price trend
        ax1.plot(crypto_data['timestamp'], crypto_data['price_usd'], 
                color='blue', linewidth=2)
        ax1.set_title(f'{crypto.capitalize()} Price (USD)')
        ax1.grid(True)
        
        # Market cap
        ax2.plot(crypto_data['timestamp'], crypto_data['market_cap_usd'],
                color='green', linewidth=2)
        ax2.set_title('Market Cap (USD)')
        ax2.grid(True)
        
        # Volume
        ax3.plot(crypto_data['timestamp'], crypto_data['volume_usd'],
                color='red', linewidth=2)
        ax3.set_title('24h Volume (USD)')
        ax3.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{crypto}_metrics.png')
        plt.close()
    
    def generate_summary_statistics(self, hours=24):
        """Generate summary statistics for the specified period"""
        df = self.fetch_data(hours)
        
        summary = []
        for crypto in ['bitcoin', 'ethereum']:
            crypto_data = df[df['cryptocurrency'] == crypto]
            
            if not crypto_data.empty:
                first_price = crypto_data['price_usd'].iloc[0]
                last_price = crypto_data['price_usd'].iloc[-1]
                price_change = ((last_price - first_price) / first_price) * 100
                
                stats = {
                    'Cryptocurrency': crypto.capitalize(),
                    'Current Price': f"${last_price:,.2f}",
                    'Price Change (%)': f"{price_change:.2f}%",
                    'Highest Price': f"${crypto_data['price_usd'].max():,.2f}",
                    'Lowest Price': f"${crypto_data['price_usd'].min():,.2f}",
                    'Average Volume': f"${crypto_data['volume_usd'].mean():,.2f}"
                }
                summary.append(stats)
        
        return pd.DataFrame(summary)
    
    def close(self):
        """Close the database connection"""
        self.conn.close()

def main():
    """Main function to demonstrate the visualizer"""
    print("Generating cryptocurrency visualizations...")
    
    visualizer = CryptoVisualizer()
    
    try:
        # Generate various visualizations
        visualizer.plot_price_trends(hours=24)
        print("✓ Generated price trends plot")
        
        visualizer.plot_price_comparison(hours=24)
        print("✓ Generated price comparison plot")
        
        visualizer.plot_market_metrics('bitcoin', hours=24)
        print("✓ Generated Bitcoin market metrics")
        
        visualizer.plot_market_metrics('ethereum', hours=24)
        print("✓ Generated Ethereum market metrics")
        
        # Display summary statistics
        print("\nSummary Statistics (Last 24 Hours):")
        print(visualizer.generate_summary_statistics().to_string(index=False))
        
    finally:
        visualizer.close()

if __name__ == "__main__":
    main()