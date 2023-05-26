import pandas as pd
import pytest
from src.modules.stocks import get_stocks_data

@pytest.fixture(scope="module")
def api_key():
    return "YOUR_API_KEY_HERE"

def test_get_stocks_data():
    data = get_stocks_data(api_key)
    assert isinstance(data, pd.DataFrame)
    expected_columns = ['Symbol', 'Price', 'Price Change', '1 Year Price Change']
    assert all(col in data.columns for col in expected_columns)
    assert data.dtypes['Symbol'] == 'object'
    assert data.dtypes['Price'] == 'float64'
    assert data.dtypes['Price Change'] == 'float64'
    assert data.dtypes['1 Year Price Change'] == 'float64'
