import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

class CryptoDashboard:
    def __init__(self, database_name="crypto_data.db"):
        """Initialize the dashboard with database connection"""
        self.conn = sqlite3.connect(database_name)
        
    def fetch_latest_prices(self):
        """Fetch the most recent price for each cryptocurrency"""
        query = """
        SELECT cryptocurrency, price_usd, timestamp
        FROM crypto_prices
        WHERE (cryptocurrency, timestamp) IN (
            SELECT cryptocurrency, MAX(timestamp)
            FROM crypto_prices
            GROUP BY cryptocurrency
        )
        """
        return pd.read_sql_query(query, self.conn)
    
    def fetch_historical_data(self, hours=24):
        """Fetch historical data for the specified time period"""
        time_threshold = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
        SELECT cryptocurrency, timestamp, price_usd, market_cap_usd, volume_usd
        FROM crypto_prices
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
        """
        
        return pd.read_sql_query(
            query,
            self.conn,
            params=(time_threshold,),
            parse_dates=['timestamp']
        )
    
    def create_price_chart(self, df, title):
        """Create an interactive price chart using Plotly"""
        fig = px.line(
            df,
            x='timestamp',
            y='price_usd',
            color='cryptocurrency',
            title=title
        )
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            hovermode='x unified'
        )
        
        return fig
    
    def create_market_metrics(self, df, crypto):
        """Create market metrics visualization for a single cryptocurrency"""
        crypto_data = df[df['cryptocurrency'] == crypto]
        
        fig = go.Figure()
        
        # Add price trace
        fig.add_trace(go.Scatter(
            x=crypto_data['timestamp'],
            y=crypto_data['price_usd'],
            name='Price',
            line=dict(color='blue')
        ))
        
        # Add volume trace on secondary y-axis
        fig.add_trace(go.Scatter(
            x=crypto_data['timestamp'],
            y=crypto_data['volume_usd'],
            name='Volume',
            line=dict(color='red'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=f'{crypto.capitalize()} Price and Volume',
            xaxis_title='Time',
            yaxis_title='Price (USD)',
            yaxis2=dict(
                title='Volume (USD)',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified'
        )
        
        return fig

def main():
    st.set_page_config(
        page_title="Crypto Dashboard",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize session state for auto-refresh
    if 'refresh_count' not in st.session_state:
        st.session_state.refresh_count = 0
    
    st.title("Cryptocurrency Real-Time Dashboard")
    st.write("Tracking Bitcoin and Ethereum prices, volumes, and trends")
    
    # Initialize dashboard
    dashboard = CryptoDashboard()
    
    # Create two columns for latest prices
    col1, col2 = st.columns(2)
    
    # Fetch and display latest prices
    latest_prices = dashboard.fetch_latest_prices()
    
    for idx, row in latest_prices.iterrows():
        with col1 if idx == 0 else col2:
            st.metric(
                label=f"{row['cryptocurrency'].capitalize()} Price",
                value=f"${row['price_usd']:,.2f}",
                delta=None
            )
    
    # Time period selector
    time_period = st.selectbox(
        "Select Time Period",
        options=[
            "Last 1 Hour",
            "Last 24 Hours",
            "Last 7 Days"
        ],
        index=1
    )
    
    # Convert selection to hours
    hours_map = {
        "Last 1 Hour": 1,
        "Last 24 Hours": 24,
        "Last 7 Days": 168
    }
    hours = hours_map[time_period]
    
    # Fetch historical data
    historical_data = dashboard.fetch_historical_data(hours=hours)
    
    # Create and display price chart
    price_chart = dashboard.create_price_chart(
        historical_data,
        f"Price Trends - {time_period}"
    )
    st.plotly_chart(price_chart, use_container_width=True)
    
    # Create tabs for individual cryptocurrency metrics
    tab1, tab2 = st.tabs(["Bitcoin Metrics", "Ethereum Metrics"])
    
    with tab1:
        btc_chart = dashboard.create_market_metrics(historical_data, 'bitcoin')
        st.plotly_chart(btc_chart, use_container_width=True)
    
    with tab2:
        eth_chart = dashboard.create_market_metrics(historical_data, 'ethereum')
        st.plotly_chart(eth_chart, use_container_width=True)
    
    # Display summary statistics
    st.subheader("Summary Statistics")
    
    # Calculate statistics for each cryptocurrency
    stats = []
    for crypto in ['bitcoin', 'ethereum']:
        crypto_data = historical_data[historical_data['cryptocurrency'] == crypto]
        if not crypto_data.empty:
            first_price = crypto_data['price_usd'].iloc[0]
            last_price = crypto_data['price_usd'].iloc[-1]
            price_change = ((last_price - first_price) / first_price) * 100
            
            stats.append({
                'Cryptocurrency': crypto.capitalize(),
                'Current Price': f"${last_price:,.2f}",
                'Price Change': f"{price_change:.2f}%",
                'Highest Price': f"${crypto_data['price_usd'].max():,.2f}",
                'Lowest Price': f"${crypto_data['price_usd'].min():,.2f}",
                'Average Volume': f"${crypto_data['volume_usd'].mean():,.2f}"
            })
    
    st.table(pd.DataFrame(stats))
    
    # Add auto-refresh button and status
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Refresh Data"):
            st.session_state.refresh_count += 1
            st.rerun()
    
    with col2:
        st.markdown("Data updates when refreshed • Last updated: " + 
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()