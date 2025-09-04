# Stock Price Predictor

A comprehensive stock analysis and prediction application with both Jupyter notebook analysis and an advanced GUI interface.

## Features

### Jupyter Notebook Analysis (`notebooks/stock_analysis.ipynb`)
- ✅ **Fixed Data Display**: Proper handling of yfinance data structure
- ✅ **Improved Visualizations**: 
  - Stock price with moving averages (20, 50, 200-day)
  - Trading volume analysis
  - Daily returns analysis
- ✅ **Technical Analysis**:
  - Moving averages calculation
  - Daily returns and volatility metrics
  - Risk metrics (max loss/gain, annualized volatility)
  - Correlation matrix analysis

### Advanced GUI Application (`scripts/stock_gui.py`)
- 🎨 **Modern Interface**: Clean, professional layout with ttk styling
- 📊 **Interactive Charts**: 
  - Matplotlib integration with navigation toolbar
  - Real-time chart updates
  - Toggle technical indicators
- 🔍 **Comprehensive Analysis**:
  - Multiple stock symbols support
  - Customizable date ranges
  - Technical indicators (Moving Averages, Volume)
  - Risk and performance metrics
- 🤖 **Machine Learning Predictions**:
  - Linear Regression and Random Forest models
  - 10-day price forecasting
  - Model performance metrics (R², RMSE)
- 💾 **Export Features**:
  - Export data to CSV
  - Save charts as high-resolution images
- 📈 **Real-time Data**: Integration with Yahoo Finance API

## Installation & Setup

### Requirements
```bash
pip install yfinance pandas matplotlib scikit-learn numpy seaborn
```

### For Jupyter Notebook
1. Open `notebooks/stock_analysis.ipynb`
2. Run all cells to see the analysis

### For GUI Application
1. Run the launcher: `python scripts/launch_gui.py`
2. Or run directly: `python scripts/stock_gui.py`

## GUI Usage Guide

### Getting Started
1. **Launch the Application**: Run the GUI launcher or the main script
2. **Enter Stock Symbol**: Type any valid stock ticker (e.g., AAPL, GOOGL, TSLA)
3. **Set Date Range**: Choose your analysis period
4. **Fetch Data**: Click "📊 Fetch Data" to download stock information

### Analysis Features
- **📈 Analyze**: Get comprehensive technical analysis and statistics
- **🔮 Predict**: Use machine learning to forecast future prices
- **Toggle Indicators**: Enable/disable moving averages and volume charts
- **Export Options**: Save your data and charts for later use

### Prediction Models
- **Linear Regression**: Simple, fast predictions based on historical trends
- **Random Forest**: More complex ensemble model for potentially better accuracy

## Key Improvements Made

### Notebook Fixes
1. ✅ **Fixed yfinance data structure handling** - Properly flattened multi-index columns
2. ✅ **Corrected visualization errors** - Fixed matplotlib plotting issues
3. ✅ **Enhanced charts** - Better styling and more informative plots
4. ✅ **Added comprehensive analysis** - Risk metrics, correlation matrix
5. ✅ **Improved data display** - Proper formatting and statistics

### GUI Enhancements
1. 🎨 **Professional Design**: Modern ttk styling with intuitive layout
2. 📊 **Interactive Charts**: Matplotlib integration with zoom/pan capabilities
3. 🔧 **User Controls**: 
   - Stock symbol input
   - Date range selection
   - Model selection dropdown
   - Technical indicator toggles
4. 📈 **Advanced Analytics**:
   - Real-time technical analysis
   - Support/resistance levels
   - Trend analysis
   - Volatility metrics
5. 🤖 **Machine Learning Integration**:
   - Multiple prediction models
   - Feature engineering
   - Performance evaluation
   - Future price forecasting
6. 💾 **Export Capabilities**:
   - CSV data export
   - High-resolution chart export
   - Professional formatting

### Code Quality Improvements
- 🔧 **Error Handling**: Comprehensive exception handling
- 📝 **Documentation**: Detailed comments and docstrings
- 🎯 **Modularity**: Well-structured, reusable code
- 🔒 **Validation**: Input validation and data checking

## File Structure
```
stockPricePredictor/
├── notebooks/
│   └── stock_analysis.ipynb    # Fixed and enhanced analysis notebook
├── scripts/
│   ├── stock_gui.py           # Advanced GUI application
│   └── launch_gui.py          # GUI launcher with requirements check
├── data/                      # Data storage directory
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Screenshots & Demo

The GUI provides:
- **Left Panel**: Controls for stock selection, date ranges, and options
- **Right Panel**: Interactive charts with navigation toolbar
- **Bottom Panel**: Detailed analysis results and statistics

## Troubleshooting

### Common Issues
1. **Import Errors**: Make sure all required packages are installed
2. **Data Fetch Errors**: Check internet connection and stock symbol validity
3. **GUI Not Starting**: Ensure tkinter is properly installed with Python

### Getting Help
- Check the terminal output for error messages
- Verify stock symbols are valid (use Yahoo Finance tickers)
- Ensure date ranges are reasonable (not too far in the past/future)

## Future Enhancements
- 📱 Web-based interface
- 🔔 Real-time alerts and notifications
- 📊 More advanced technical indicators
- 🎯 Portfolio optimization features
- 📈 Backtesting capabilities

---

**Happy Trading! 📈💰**