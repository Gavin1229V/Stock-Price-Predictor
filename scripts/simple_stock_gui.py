
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd

class SimpleStockGUI:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Simple Stock Analysis")
        self.window.geometry("1000x800")
        
        # Add a title at the top
        title = tk.Label(self.window, text="Stock Price Analyzer", 
                        font=('Arial', 24), pady=10)
        title.pack()
        
        # Create input section
        self.create_input_section()
        
        # Create chart area
        self.create_chart_area()
        
        # Create info section
        self.create_info_section()
    
    def create_input_section(self):
        """Create the section for user inputs"""
        input_frame = ttk.LabelFrame(self.window, text="Enter Stock Details", padding=10)
        input_frame.pack(fill='x', padx=10)
        
        # Stock symbol input
        symbol_frame = ttk.Frame(input_frame)
        symbol_frame.pack(fill='x', pady=5)
        
        ttk.Label(symbol_frame, text="Stock Symbol:").pack(side='left')
        self.symbol_entry = ttk.Entry(symbol_frame, width=10)
        self.symbol_entry.insert(0, "AAPL")  # Default value
        self.symbol_entry.pack(side='left', padx=5)
        
        # Date range input
        date_frame = ttk.Frame(input_frame)
        date_frame.pack(fill='x', pady=5)
        
        # Calculate default dates (1 year of data)
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
        self.analyze_btn = ttk.Button(input_frame, text="Analyze Stock", 
                                    command=self.analyze_stock)
        self.analyze_btn.pack(pady=10)
    
    def create_chart_area(self):
        """Create the area where charts will be displayed"""
        self.chart_frame = ttk.LabelFrame(self.window, text="Stock Price Chart", 
                                        padding=10)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # We'll create the actual chart when data is loaded
        self.canvas = None
    
    def create_info_section(self):
        """Create the section for displaying stock information"""
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
    
    def analyze_stock(self):
        """Analyze the stock and update the display"""
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
        """Update the stock price chart"""
        # Clear previous chart
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
        
        # Add chart to GUI
        self.canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def update_info(self, data):
        """Update the stock information display"""
        current_price = data['Close'].iloc[-1]
        price_change = ((current_price - data['Close'].iloc[0]) / 
                       data['Close'].iloc[0] * 100)
        avg_volume = data['Volume'].mean() / 1_000_000  # Convert to millions
        
        self.current_price_label.config(
            text=f"Current Price: ${current_price:.2f}")
        self.change_label.config(
            text=f"Total Price Change: {price_change:.1f}%")
        self.volume_label.config(
            text=f"Average Daily Volume: {avg_volume:.1f}M shares")
    
    def run(self):
        """Start the GUI application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = SimpleStockGUI()
    app.run()
