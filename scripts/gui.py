
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd
from prediction import get_stock_data, prepare_features, train_model, predict_future_prices
import numpy as np

class SimpleStockGUI:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Simple Stock Analysis")
        self.window.geometry("1000x800")
        
        title = tk.Label(self.window, text="Stock Price Analyser", 
                        font=('Arial', 24), pady=10)
        title.pack()
        
        # Sections
        self.create_input_section()
        self.create_chart_area()
        self.create_info_section()
    
    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.window, text="Enter Stock Details", padding=10)
        input_frame.pack(fill='x', padx=10)
        
        # Stock symbol input
        symbol_frame = ttk.Frame(input_frame)
        symbol_frame.pack(fill='x', pady=5)
        
        ttk.Label(symbol_frame, text="Stock Symbol:").pack(side='left')
        self.symbol_entry = ttk.Entry(symbol_frame, width=10)
        self.symbol_entry.insert(0, "AAPL")  # Default
        self.symbol_entry.pack(side='left', padx=5)
        
        # Date range input
        date_frame = ttk.Frame(input_frame)
        date_frame.pack(fill='x', pady=5)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        ttk.Label(date_frame, text="Start Date:").pack(side='left')
        self.start_date = ttk.Entry(date_frame, width=10)
        self.start_date.insert(0, start_date.strftime("%Y-%m-%d"))
        self.start_date.pack(side='left', padx=5)
        
        ttk.Label(date_frame, text="End Date:").pack(side='left')
        self.end_date = ttk.Entry(date_frame, width=10)
        self.end_date.insert(0, end_date.strftime("%Y-%m-%d"))
        self.end_date.pack(side='left', padx=5)
        
        # Analyze button
        self.analyze_btn = ttk.Button(input_frame, text="Analyse Stock", 
                                    command=self.analyze_stock)
        self.analyze_btn.pack(pady=5)
        
        # Predict button
        self.predict_btn = ttk.Button(input_frame, text="Predict Future Price", 
                                    command=self.predict_stock)
        self.predict_btn.pack(pady=5)
    
    def create_chart_area(self):
        self.chart_frame = ttk.LabelFrame(self.window, text="Stock Price Chart", 
                        padding=10)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.canvas = None
    
    def create_info_section(self):
        self.info_frame = ttk.LabelFrame(self.window, text="Stock Information", 
                                       padding=10)
        self.info_frame.pack(fill='x', padx=10, pady=5)
        
        # Labels for displaying information
        self.current_price_label = ttk.Label(self.info_frame, text="")
        self.current_price_label.pack()
        
        self.change_label = ttk.Label(self.info_frame, text="")
        self.change_label.pack()
        
        self.volume_label = ttk.Label(self.info_frame, text="")
        self.volume_label.pack()
        
        # Prediction info labels
        self.prediction_label = ttk.Label(self.info_frame, text="", foreground="blue")
        self.prediction_label.pack()
        
        self.accuracy_label = ttk.Label(self.info_frame, text="", foreground="green")
        self.accuracy_label.pack()
    
    def analyze_stock(self):
        try:
            # Get values from inputs
            symbol = self.symbol_entry.get().upper()
            start = self.start_date.get()
            end = self.end_date.get()
            
            # Download data
            self.analyze_btn.config(text="Downloading...", state='disabled')
            data = yf.download(symbol, start=start, end=end)
            
            if len(data) == 0:
                messagebox.showerror("Error", "No data found for this stock!")
                return
            
            # Calculate moving averages
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()
            
            # Update chart
            self.update_chart(data)
            
            # Update information
            self.update_info(data)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.analyze_btn.config(text="Analyze Stock", state='normal')
    
    def update_chart(self, data):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        # Create new chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot stock price and moving averages
        ax.plot(data.index, data['Close'], label='Stock Price', linewidth=2)
        ax.plot(data.index, data['MA20'], label='20-day Average', alpha=0.7)
        ax.plot(data.index, data['MA50'], label='50-day Average', alpha=0.7)
        
        ax.set_title(f'Stock Price Analysis', pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add chart
        self.canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def update_info(self, data):
        current_price = float(data['Close'].iloc[-1])
        first_price = float(data['Close'].iloc[0])
        price_change = ((current_price - first_price) / first_price) * 100
        avg_volume = float(data['Volume'].mean()) / 1_000_000
        
        self.current_price_label.config(
            text=f"Current Price: ${current_price:.2f}")
        self.change_label.config(
            text=f"Total Price Change: {price_change:.1f}%")
        self.volume_label.config(
            text=f"Average Daily Volume: {avg_volume:.1f}M shares")
    
    def predict_stock(self):
        try:
            symbol = self.symbol_entry.get().upper()
            
            self.predict_btn.config(text="Predicting...", state='disabled')
            
            # Get data using prediction module
            data = get_stock_data(symbol, 365)
            
            if len(data) == 0:
                messagebox.showerror("Error", "No data found for prediction!")
                return
            
            # Prepare features and train model
            features = prepare_features(data)
            model, accuracy, feature_names = train_model(features)
            
            # Make 30-day predictions
            predictions = predict_future_prices(model, features, feature_names, 30)
            
            # Create prediction dates
            last_date = data.index[-1]
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=30, freq='B')
            
            # Update chart with predictions
            self.update_chart_with_prediction(data, predictions, future_dates)
            
            # Update prediction info
            current_price = float(data['Close'].iloc[-1])
            predicted_price = predictions[-1]
            change_percent = ((predicted_price - current_price) / current_price) * 100
            
            self.prediction_label.config(
                text=f"30-day Prediction: ${predicted_price:.2f} ({change_percent:+.1f}%)")
            self.accuracy_label.config(
                text=f"Model Accuracy: {accuracy:.1%}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
        finally:
            self.predict_btn.config(text="Predict Future Price", state='normal')
    
    def update_chart_with_prediction(self, data, predictions, future_dates):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot historical data (last 60 days)
        recent_data = data.tail(60)
        ax.plot(recent_data.index, recent_data['Close'], label='Historical Price', 
                linewidth=2, color='blue')
        
        # Plot moving averages
        if 'MA20' in data.columns:
            ax.plot(recent_data.index, recent_data['MA20'], label='20-day MA', 
                    alpha=0.7, color='orange')
        
        # Plot predictions
        ax.plot(future_dates, predictions, label='Predicted Price', 
                linewidth=2, color='red', linestyle='--')
        
        # Add confidence band
        confidence = np.array(predictions) * 0.1
        ax.fill_between(future_dates, 
                       np.array(predictions) - confidence, 
                       np.array(predictions) + confidence, 
                       color='red', alpha=0.2, label='Confidence Band')
        
        ax.set_title('Stock Price Analysis with Prediction', pad=20)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SimpleStockGUI()
    app.run()
