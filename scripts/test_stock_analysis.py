"""
Basic tests for stock analysis functionality
"""
import unittest
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

class TestStockAnalysis(unittest.TestCase):
    def setUp(self):
        # Use a short date range for testing
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        self.test_symbol = "AAPL"
        self.data = yf.download(self.test_symbol, start=start_date, end=end_date)

    def test_data_download(self):
        """Test if we can download stock data"""
        self.assertIsNotNone(self.data)
        self.assertGreater(len(self.data), 0)
        self.assertTrue('Close' in self.data.columns)

    def test_moving_average_calculation(self):
        """Test moving average calculations"""
        # Calculate 5-day moving average (using small window for testing)
        ma5 = self.data['Close'].rolling(window=5).mean()
        
        # Check if MA was calculated correctly
        self.assertEqual(len(ma5), len(self.data))
        # First 4 values should be NaN (not enough data for 5-day average)
        self.assertTrue(pd.isna(ma5.iloc[3]).item())
        # 5th value onwards should not be NaN
        self.assertFalse(pd.isna(ma5.iloc[5]).item())

    def test_price_change_calculation(self):
        """Test price change percentage calculation"""
        first_price = float(self.data['Close'].iloc[0])
        last_price = float(self.data['Close'].iloc[-1])
        price_change = ((last_price - first_price) / first_price) * 100
        
        # Price change should be a number
        self.assertIsInstance(price_change, float)

if __name__ == '__main__':
    unittest.main()
