import streamlit as st
import yfinance as yf
import pandas as pd

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# App title
st.title("RSI Fetcher for Indian Stocks")

# User input for stock symbol
st.markdown("""
- For **NSE** stocks, append `.NS` to the stock symbol (e.g., `RELIANCE.NS`).
- For **BSE** stocks, append `.BO` to the stock symbol (e.g., `500325.BO` for Reliance).
""")
stock_symbol = st.text_input("Enter the stock symbol (e.g., RELIANCE.NS):", "RELIANCE.NS")
window = st.number_input("Enter the RSI window (default is 14):", min_value=1, value=14, step=1)

# Fetch data button
if st.button("Fetch RSI"):
    try:
        # Fetch stock data for the last 2 years
        stock_data = yf.download(stock_symbol, period="2y", interval="1d")
        
        if stock_data.empty:
            st.error("No data found for the given symbol. Please check the symbol and try again.")
        else:
            # Calculate RSI
            stock_data['RSI'] = calculate_rsi(stock_data, window)
            
            # Save to Excel
            file_name = f"{stock_symbol}_RSI.xlsx"
            stock_data.to_excel(file_name, index=True)
            
            st.success(f"RSI data for {stock_symbol} calculated and saved successfully!")
            st.download_button(
                label="Download RSI Excel File",
                data=open(file_name, "rb").read(),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")
