import yfinance as yf
import pandas as pd

# Retrieve a list of all available stock symbols from a text file
with open('stock_symbols.txt') as f:
    stock_symbols = [line.strip() for line in f]

# Initialize an empty list to store the filtered data for each stock
filtered_data = []

# Loop through each stock symbol and retrieve historical data
for symbol in stock_symbols:
    # Retrieve historical data for the past 20 years
    data = yf.download(symbol, start='2008-01-01', end='2023-05-02')

    # Calculate the percentage change between the opening and closing prices for each day
    data['pct_change'] = (data['Close'] - data['Open']) / data['Open'] * 100

    # Filter the data to show only days where the percentage change was greater than 10%
    data = data[data['pct_change'] >= 10]

    # Add the filtered data to the list
    if not data.empty:
        filtered_data.append(data)

# Concatenate the filtered data for all stocks into a single dataframe
all_filtered_data = pd.concat(filtered_data)

# Print the filtered data for all stocks
print(all_filtered_data)
