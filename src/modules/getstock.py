import pandas as pd
import requests
import time

def get_stocks_data(api_key):
    # Define the endpoints and parameters for the Alpha Vantage API
    url_stocks = 'https://www.alphavantage.co/query'
    params_stocks = {
        'function': 'GLOBAL_QUOTE',
        'apikey': "RK0U9XZ20OJ4XO2A"
    }

    # Define the symbols to fetch
    symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'FB', 'TSLA', 'JPM', 'JNJ', 'V', 'PG']

    stocks_df_list = []
    for symbol in symbols:
        # Send a GET request to the Alpha Vantage API for each symbol and get the JSON response
        params_stocks['symbol'] = symbol
        response = requests.get(url_stocks, params=params_stocks)
        data = response.json()

        # Extract the relevant information from the JSON response and create a pandas dataframe
        if 'Global Quote' in data and '05. price' in data['Global Quote']:
            price = float(data['Global Quote']['05. price'])
            price_change = float(data['Global Quote']['09. change'])
            year_change = float(data['Global Quote']['10. change percent'][:-1])
            stocks_df_list.append({
                'Symbol': symbol,
                'Price': price,
                'Price Change': price_change,
                '1 Year Price Change': year_change
            })

        # Add a delay between API calls to avoid hitting the rate limit
        time.sleep(15)

    # Concatenate the dataframes and return the result
    stocks_df = pd.concat([pd.DataFrame(item, index=[0]) for item in stocks_df_list], ignore_index=True)
    return stocks_df
