"""
Test script to verify yfinance data fetching
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def test_data_fetch():
    """Test data fetching with error handling"""
    
    # Test symbols
    test_symbols = ['AAPL', 'GOOGL', 'MSFT', 'INVALID_SYMBOL']
    
    for symbol in test_symbols:
        print(f"\n{'='*50}")
        print(f"Testing symbol: {symbol}")
        print(f"{'='*50}")
        
        try:
            # Fetch data
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
            print(f"Fetching data from {start_date} to {end_date}")
            
            data = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True, progress=False)
            
            # Check if data is empty
            if data.empty:
                print(f"❌ No data found for {symbol}")
                continue
            
            # Handle multi-index columns
            if isinstance(data.columns, pd.MultiIndex):
                print("📋 Multi-index columns detected, flattening...")
                data.columns = [col[0] for col in data.columns.values]
            
            print(f"✅ Data fetched successfully!")
            print(f"Shape: {data.shape}")
            print(f"Columns: {list(data.columns)}")
            print(f"Date range: {data.index[0]} to {data.index[-1]}")
            
            # Test data access
            try:
                latest_close = data['Close'].iloc[-1]
                first_close = data['Close'].iloc[0]
                print(f"Latest price: ${latest_close:.2f}")
                print(f"First price: ${first_close:.2f}")
                print(f"Change: {((latest_close/first_close - 1) * 100):+.2f}%")
            except Exception as e:
                print(f"⚠️ Error accessing price data: {e}")
            
            # Test technical indicators
            try:
                data['MA20'] = data['Close'].rolling(20).mean()
                ma20_latest = data['MA20'].iloc[-1]
                if not pd.isna(ma20_latest):
                    print(f"20-day MA: ${ma20_latest:.2f}")
                else:
                    print("20-day MA: Not enough data")
            except Exception as e:
                print(f"⚠️ Error calculating MA: {e}")
                
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("🔍 Testing yfinance data fetching...")
    test_data_fetch()
    print("\n✅ Test completed!")
