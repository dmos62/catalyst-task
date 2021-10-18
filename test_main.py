import main
from operator import itemgetter

def http_get_history_for_symbol(user_token, symbol):
    with main.app.test_client() as c:
        response = c.get(
            f'/tickers/{symbol}/history',
            auth = (user_token, ""),
        )
        return response

def http_get_portfolio(user_token):
    with main.app.test_client() as c:
        response = c.get(
            '/tickers',
            auth = (user_token, ""),
        )
        return response

def is_price_right(ticker, date):
    symbol = ticker["symbol"]
    actual_price = main.get_price_for_symbol_at_date(symbol, date)
    reported_price = ticker["price"]
    assert actual_price == reported_price

def test_portfolio():
    user_token = "123"
    response = http_get_portfolio(user_token)
    assert response.status_code == 200
    portfolio = response.get_json()

    for ticker in portfolio:
        is_string = lambda x: type(x) is str
        assert "symbol" in ticker
        assert is_string(ticker["symbol"])
        assert "price" in ticker
        assert is_string(ticker["price"])
        current_date = main.get_current_date()
        assert is_price_right(ticker, current_date)

    expected_ticker_symbols_in_portfolio = \
        main.get_ticker_symbols_in_portfolio(user_token)
    ticker_symbols_in_portfolio = set(map(itemgetter("symbol"), portfolio))
    assert ticker_symbols_in_portfolio == expected_ticker_symbols_in_portfolio

def test_unknown_symbol():
    user_token = "561"
    unknown_symbol = "XYZXYZ"
    assert unknown_symbol not in main.known_ticker_symbols
    symbol = unknown_symbol
    response = http_get_history_for_symbol(user_token, symbol)
    assert response.status_code == 404

def test_history():
    user_token = "321"
    symbol = "AAPL"
    response = http_get_history_for_symbol(user_token, symbol)
    assert response.status_code == 200
    history = response.get_json()
    for data_point in history:
        is_string = lambda x: type(x) is str
        assert "date" in data_point
        assert "price" in data_point
        date = date_point["date"]
        price = date_point["price"]
        assert is_string(date)
        assert is_string(price)
        assert is_price_right({"symbol": symbol, "price": price}, date)
    history_in_descending_order = \
        sorted(history, key=itemgetter("date"), reverse=True)
    assert history_in_descending_order == history
