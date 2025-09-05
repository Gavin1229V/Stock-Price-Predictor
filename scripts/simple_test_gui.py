import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd

class SimpleTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Data Fetch Test")
        self.root.geometry("600x400")
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self.root, text="Stock Symbol:").pack(pady=5)
        self.symbol_var = tk.StringVar(value="AAPL")
        ttk.Entry(self.root, textvariable=self.symbol_var).pack(pady=5)
        # Fetch button
        ttk.Button(self.root, text="Fetch Data", command=self.fetch_data).pack(pady=10)
        # Results text
        self.result_text = tk.Text(self.root, height=20, width=70)
        self.result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
    def fetch_data(self):
        try:
            symbol = self.symbol_var.get().upper().strip()
            
            if not symbol:
                messagebox.showerror("Error", "Please enter a stock symbol")
                return
                
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Fetching data for {symbol}...\n")
            self.root.update()
            data = yf.download(symbol, start='2024-01-01', end='2025-08-22', 
                             auto_adjust=True, progress=False)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = [col[0] for col in data.columns.values]
                self.result_text.insert(tk.END, "Multi-index columns detected and flattened\n")
            
            if data.empty:
                self.result_text.insert(tk.END, f"No data found for symbol {symbol}\n")
                return
            required_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                self.result_text.insert(tk.END, f"Missing columns: {missing_columns}\n")
                return
                
            # Test data access
            try:
                latest_price = data['Close'].iloc[-1]
                first_price = data['Close'].iloc[0]
                price_change = ((latest_price / first_price) - 1) * 100
                
                result = f"""
Data fetched successfully for {symbol}
Shape: {data.shape}
Columns: {list(data.columns)}
Date range: {data.index[0].date()} to {data.index[-1].date()}
Latest price: ${latest_price:.2f}
First price: ${first_price:.2f}
Price change: {price_change:+.2f}%

All data access tests passed
"""
                self.result_text.insert(tk.END, result)
                
            except Exception as e:
                self.result_text.insert(tk.END, f"Error accessing data: {e}\n")
                
        except Exception as e:
            error_msg = f"Error fetching data: {str(e)}"
            self.result_text.insert(tk.END, error_msg + "\n")
            print(f"Detailed error: {type(e).__name__}: {e}")

def main():
    root = tk.Tk()
    app = SimpleTestGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
