import json
from src.modules.weather import get_weather_forecast
from src.modules.stocks import get_top_stocks, get_top_10_etfs, get_crypto_data, get_currency_exchange_data
from src.modules.soccer import get_fixtures
from src.utils.email_sender import send_email
from src.utils.email_content import create_email_content
from src.modules.newcode import get_new_product_announcements


def send_daily_digest(email_credentials_file, recipients):
    with open(email_credentials_file, "r") as f:
        email_credentials = json.load(f)

    fixtures = get_fixtures(140, 2022, email_credentials["SOCCER_API_KEY"])
    stocks = get_top_stocks(email_credentials["ALPHA_VANTAGE_API_KEY"])
    etf = get_top_10_etfs()
    exchange = get_currency_exchange_data(email_credentials["CURRENCY_LAYER_API_KEY"])
    crypto = get_crypto_data(email_credentials["COINMARKETCAP_API_KEY"])
    products=get_new_product_announcements('VvtRKjTiZbjSg8C3h0oQFbY3AjpIFSpeTA0wHzkppF8', 'KFuVZ1WbQLkSvvwr6CcJ1fSSrYUwKW_tAwpPfr1h84E')
    email_content = create_email_content(
        fixtures, stocks, etf, exchange, crypto, products
    )

    send_email(email_credentials, recipients, email_credentials["subject"], email_content)

    print("Daily digest sent successfully!")


if __name__ == '__main__':
    email_credentials_file = "src/modules/credentials.json"
    recipients = ["avetik.babayan@gmail.com"]
    send_daily_digest(email_credentials_file, recipients)
