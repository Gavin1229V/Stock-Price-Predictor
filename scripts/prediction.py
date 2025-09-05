import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_stock_data(symbol, days=365):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns.values]
    
    return data

def prepare_features(data):
    features = pd.DataFrame()
    
    # Basic price features
    features['price'] = data['Close']
    features['volume'] = data['Volume']
    features['high'] = data['High']
    features['low'] = data['Low']
    
    # Simple moving averages
    features['ma5'] = data['Close'].rolling(5).mean()
    features['ma20'] = data['Close'].rolling(20).mean()
    
    # Price changes
    features['price_change'] = data['Close'].pct_change()
    features['volume_change'] = data['Volume'].pct_change()
    
    # Simple trend indicator
    features['trend'] = (features['ma5'] - features['ma20']) / features['ma20']
    
    # Day of week (0=Monday, 6=Sunday)
    features['day_of_week'] = pd.to_datetime(data.index).dayofweek
    
    features = features.dropna()
    
    return features

def train_model(features):
    # Prepare data for training
    X = features[['volume', 'high', 'low', 'ma5', 'ma20', 'price_change', 'volume_change', 'trend', 'day_of_week']]
    y = features['price'].shift(-1).dropna()  # Next day's price
    X = X.iloc[:-1]
    
    # Split into train and test
    split_point = int(len(X) * 0.8)
    X_train = X.iloc[:split_point]
    X_test = X.iloc[split_point:]
    y_train = y.iloc[:split_point]
    y_test = y.iloc[split_point:]
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Test accuracy
    test_score = model.score(X_test, y_test)
    
    return model, test_score, X.columns

def predict_future_prices(model, features, feature_names, days=30):
    predictions = []
    last_row = features.iloc[-1:][feature_names].copy()
    
    for day in range(days):
        # Make prediction
        pred_price = model.predict(last_row)[0]
        predictions.append(pred_price)
        
        # Update features for next prediction
        new_row = last_row.copy()
        new_row['volume'] = last_row['volume'].iloc[0]  # Keeping volume same
        new_row['high'] = pred_price * 1.02
        new_row['low'] = pred_price * 0.98
        new_row['ma5'] = np.mean(predictions[-5:]) if len(predictions) >= 5 else pred_price
        new_row['ma20'] = np.mean(predictions[-20:]) if len(predictions) >= 20 else pred_price
        new_row['price_change'] = (pred_price - (predictions[-2] if len(predictions) > 1 else features['price'].iloc[-1])) / features['price'].iloc[-1]
        new_row['volume_change'] = 0
        new_row['trend'] = (new_row['ma5'] - new_row['ma20']) / new_row['ma20']
        new_row['day_of_week'] = (last_row['day_of_week'].iloc[0] + 1) % 7
        
        last_row = new_row
    
    return predictions

def analyze_stock(symbol='AAPL', prediction_days=30):
    print(f"Analyzing {symbol}...")
    
    # Get data
    data = get_stock_data(symbol)
    print(f"Got {len(data)} days of data")
    
    # Prepare features
    features = prepare_features(data)
    print(f"Prepared {len(features)} feature rows")
    
    # Train model
    model, accuracy, feature_names = train_model(features)
    print(f"Model trained with accuracy: {accuracy:.2%}")
    
    # Make predictions
    predictions = predict_future_prices(model, features, feature_names, prediction_days)
    
    # Current info
    current_price = float(data['Close'].iloc[-1])
    predicted_price = predictions[-1]
    change_percent = ((predicted_price - current_price) / current_price) * 100
    
    print(f"\nCurrent Price: ${current_price:.2f}")
    print(f"Predicted Price ({prediction_days} days): ${predicted_price:.2f}")
    print(f"Expected Change: {change_percent:+.1f}%")
    
    # Create prediction dates
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=prediction_days, freq='B')
    
    # Plot results
    plt.figure(figsize=(12, 6))
    
    # Plot historical (last 60 days)
    recent_data = data.tail(60)
    plt.plot(recent_data.index, recent_data['Close'], label='Historical Price', color='blue', linewidth=2)
    
    # Plot predictions
    plt.plot(future_dates, predictions, label='Predicted Price', color='red', linestyle='--', linewidth=2)
    
    # 10% confidence band
    confidence = np.array(predictions) * 0.1  
    plt.fill_between(future_dates, 
                     np.array(predictions) - confidence, 
                     np.array(predictions) + confidence, 
                     color='red', alpha=0.2, label='Confidence Band')
    
    plt.title(f'{symbol} Price Prediction', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    return {
        'current_price': current_price,
        'predicted_price': predicted_price,
        'change_percent': change_percent,
        'predictions': predictions,
        'accuracy': accuracy,
        'dates': future_dates
    }

if __name__ == "__main__":
    result = analyze_stock('AAPL', 30)
    
    print(f"\nSummary:")
    print(f"Model Accuracy: {result['accuracy']:.2%}")
    print(f"Prediction: ${result['current_price']:.2f} -> ${result['predicted_price']:.2f}")
    print(f"Expected change: {result['change_percent']:+.1f}%")
