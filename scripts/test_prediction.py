"""
Test script for prediction functionality
"""
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta

def test_prediction_pipeline():
    """Test the complete prediction pipeline"""
    
    print("🧪 Testing Stock Prediction Pipeline")
    print("=" * 50)
    
    # Fetch test data
    print("📊 Fetching test data...")
    try:
        data = yf.download('AAPL', start='2024-01-01', end='2025-08-22', auto_adjust=True, progress=False)
        
        # Handle multi-index columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns.values]
            
        print(f"✅ Data fetched: {data.shape}")
        print(f"Columns: {list(data.columns)}")
        
    except Exception as e:
        print(f"❌ Data fetch failed: {e}")
        return False
    
    # Prepare features (simplified version)
    print("\n🔧 Preparing features...")
    try:
        features = pd.DataFrame(index=data.index)
        
        # Basic features
        features['Close'] = data['Close']
        features['Volume'] = data['Volume']
        features['High'] = data['High']
        features['Low'] = data['Low']
        features['Open'] = data['Open']
        
        # Technical indicators
        features['MA5'] = data['Close'].rolling(5, min_periods=3).mean()
        features['MA20'] = data['Close'].rolling(20, min_periods=10).mean()
        features['Daily_Return'] = data['Close'].pct_change()
        features['Volatility'] = features['Daily_Return'].rolling(10, min_periods=5).std()
        features['Price_Change'] = data['Close'].diff()
        
        # Price ratios
        features['Close_MA5_Ratio'] = features['Close'] / features['MA5']
        features['High_Low_Ratio'] = features['High'] / features['Low']
        
        # Time features
        features['DayOfWeek'] = pd.to_datetime(data.index).dayofweek
        
        # Clean data
        features = features.fillna(method='ffill').fillna(method='bfill')
        features = features.dropna()
        
        print(f"✅ Features prepared: {features.shape}")
        print(f"Feature columns: {len(features.columns)}")
        
    except Exception as e:
        print(f"❌ Feature preparation failed: {e}")
        return False
    
    # Prepare target
    print("\n🎯 Preparing target variable...")
    try:
        aligned_data = data.loc[features.index]
        target = aligned_data['Close'].shift(-1).dropna()
        
        # Align features and target
        min_length = min(len(features), len(target))
        features = features.iloc[:min_length]
        target = target.iloc[:min_length]
        
        print(f"✅ Target prepared: {len(target)} samples")
        
    except Exception as e:
        print(f"❌ Target preparation failed: {e}")
        return False
    
    # Test model training
    print("\n🤖 Testing model training...")
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
    }
    
    results = {}
    
    for model_name, model in models.items():
        try:
            print(f"\nTesting {model_name}...")
            
            # Split data
            split_point = int(len(features) * 0.8)
            X_train = features.iloc[:split_point]
            X_test = features.iloc[split_point:]
            y_train = target.iloc[:split_point]
            y_test = target.iloc[split_point:]
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            results[model_name] = {
                'R²': r2,
                'RMSE': rmse,
                'MSE': mse
            }
            
            print(f"  R²: {r2:.3f}")
            print(f"  RMSE: ${rmse:.2f}")
            print(f"  Status: {'✅ Good' if r2 > 0.3 else '⚠️ Fair' if r2 > 0 else '❌ Poor'}")
            
            # Test future predictions
            print(f"  Testing future predictions...")
            last_features = features.iloc[-1:].copy()
            future_preds = []
            
            for i in range(5):  # Test 5-day prediction
                pred = model.predict(last_features)[0]
                future_preds.append(pred)
                
                # Simple feature update
                new_features = last_features.copy()
                new_features['Close'] = pred
                new_features['Price_Change'] = pred - (future_preds[-2] if len(future_preds) > 1 else features['Close'].iloc[-1])
                last_features = new_features
            
            current_price = float(aligned_data['Close'].iloc[-1])
            pred_change = ((future_preds[-1] / current_price) - 1) * 100
            
            print(f"  5-day prediction: ${future_preds[-1]:.2f} ({pred_change:+.1f}%)")
            results[model_name]['predictions'] = future_preds
            
        except Exception as e:
            print(f"❌ {model_name} failed: {e}")
            results[model_name] = {'error': str(e)}
    
    # Summary
    print("\n📊 PREDICTION TEST SUMMARY")
    print("=" * 30)
    for model_name, result in results.items():
        if 'error' in result:
            print(f"{model_name}: ❌ Failed - {result['error']}")
        else:
            print(f"{model_name}:")
            print(f"  R²: {result['R²']:.3f}")
            print(f"  RMSE: ${result['RMSE']:.2f}")
            if 'predictions' in result:
                print(f"  Future predictions: {len(result['predictions'])} days")
    
    print("\n✅ Prediction pipeline test completed!")
    return True

if __name__ == "__main__":
    test_prediction_pipeline()
