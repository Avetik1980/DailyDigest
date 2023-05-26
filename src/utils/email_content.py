from src.modules.stocks import create_stocks_table, create_etf_table, create_crypto_table, create_exchange_table
from src.modules.newcode import get_new_product_announcements

def create_email_content(fixtures, stocks, etf, exchange, crypto, products):
    content = "<html><body>"
    content += "<h1>Daily Digest</h1>"
    content += fixtures
    content += create_stocks_table(stocks)
    content += create_etf_table(etf)
    content += create_exchange_table(exchange)
    content += create_crypto_table(crypto)
    content += get_new_product_announcements()
    content += "</body></html>"
    return content
