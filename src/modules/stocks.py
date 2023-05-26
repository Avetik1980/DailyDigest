import yfinance as yf
import pandas as pd
import requests
import time
from tabulate import tabulate

def get_top_stocks(api_key):
    # Define the endpoints and parameters for the Alpha Vantage API
    url_stocks = 'https://www.alphavantage.co/query'
    params_stocks = {
        'function': 'GLOBAL_QUOTE',
        'apikey': api_key
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

    # Sort the stocks by price in descending order
    stocks_df = stocks_df.sort_values(by='Price', ascending=False)

    # Format the columns
    stocks_df['Price'] = stocks_df['Price'].map('${:,.2f}'.format)
    stocks_df['Price Change'] = stocks_df['Price Change'].map('{:+,.2f}%'.format)
    stocks_df['1 Year Price Change'] = stocks_df['1 Year Price Change'].map('{:+,.2f}%'.format)

    # Return the top 10 stocks as a table
    return stocks_df.head(10).to_html(index=False, classes='table table-striped')

def create_stocks_table(stocks):
    table = '<h2>Top 10 Stocks</h2>'
    table += stocks
    return table

def get_currency_exchange_data(api_key):
    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {"symbols": "EUR,JPY,GBP,AUD,CAD,CHF,CNY,HKD,NZD,SEK",
              "access_key": api_key,
              "base": "USD"}
    headers = {"apikey": api_key}
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        exchange_rates = {}
        for currency, rate in data['rates'].items():
            exchange_rates[currency] = round(rate, 4)

        # Sort the exchange rates by value in descending order
        sorted_rates = {k: v for k, v in sorted(exchange_rates.items(), key=lambda item: item[1], reverse=True)}

        # Get the top 10 currencies
        top_currencies = list(sorted_rates.keys())[:10]

        # Initialize the table headers and data
        tab_names = ['Currency', 'Exchange Rate']
        data = []

        # Add the exchange rate for each currency to the data list
        for currency in top_currencies:
            data.append([currency, f"1 USD = {exchange_rates[currency]:.4f} {currency}"])

        # Return the table as a string
        return tabulate(data, headers=tab_names, tablefmt='html')
    except requests.exceptions.Timeout:
        print("Connection timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error")
        return None
    except KeyError:
        print("Invalid response format")
        return None

def create_exchange_table(exchange_data):
    if exchange_data is None:
        return "Error: Unable to fetch exchange rates."

    return exchange_data

def get_top_10_etfs():
    # Define the ETFs to fetch
    etfs = ['SPY', 'QQQ', 'VTI', 'GLD', 'EEM', 'IWM', 'XLF', 'XLE', 'XLK', 'XLI']
    etf_prices = []

    # Fetch the ETF prices
    for etf in etfs:
        try:
            # Fetch the data from Yahoo Finance
            data = yf.download(etf, period='2d', interval='1d')

            # Calculate the price changes
            current_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2]
            price_change = current_price / previous_price - 1

            # Add the data to the list
            etf_prices.append({
                'ETF': etf,
                'Price': round(current_price, 2),
                'Price Change': f"{round(price_change * 100, 2)}%"
            })
        except:
            pass

    # Sort the ETFs by price in descending order
    etf_prices = sorted(etf_prices, key=lambda x: x['Price'], reverse=True)

    # Return the list of dictionaries containing ETF information
    return etf_prices

def create_etf_table(etf_data):
    # Initialize the table headers and data
    tab_names = ['ETF', 'Price', 'Price Change']
    data = []

    # Add the ETF data to the data list
    for etf_price in etf_data:
        data.append([etf_price['ETF'], etf_price['Price'], etf_price['Price Change']])

    # Return the table as a string
    return tabulate(data, headers=tab_names, tablefmt='html')

def get_crypto_data(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }
    params = {
        "limit": 10,
        "convert": "USD",
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        crypto_list = []
        for symbol in data['data']:
            name = symbol['name']
            price = symbol['quote']['USD']['price']
            percent_change = symbol['quote']['USD']['percent_change_24h']
            arrow = '↑' if percent_change >= 0 else '↓'
            percent_change = f"{percent_change:.2f}% {arrow}"
            crypto_list.append({
                'Symbol': symbol['symbol'],
                'Name': name,
                'Price': price,
                '24H % Change': percent_change
            })

        # Sort the cryptocurrencies by price in descending order
        crypto_list = sorted(crypto_list, key=lambda x: x['Price'], reverse=True)
        return crypto_list
    except requests.exceptions.Timeout:
        print("Connection timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error")
        return None
    except KeyError:
        print("Invalid response format")
        return None

def create_crypto_table(crypto_list):
    # Initialize the table headers and data
    tab_names = ['Symbol', 'Name', 'Price', '24H % Change']
    data = []

    # Add the cryptocurrency data to the data list
    for crypto in crypto_list:
        data.append([crypto['Symbol'], crypto['Name'], f"${crypto['Price']:.2f}", crypto['24H % Change']])

    # Return the table as a string
    return tabulate(data, headers=tab_names, tablefmt='html')
