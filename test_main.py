import main
from toolz.curried import pipe, map, sliding_window, concat
from operator import itemgetter
import datetime

def http_get_history_for_symbol(user_token, symbol):
    with main.app.test_client() as c:
        response = c.get(
            f'/tickers/{symbol}/history',
            auth = (user_token, ""),
        )
        return response

def http_get_history_for_symbol_with_page(user_token, symbol, page):
    with main.app.test_client() as c:
        response = c.get(
            f'/tickers/{symbol}/history?page={page}',
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
    actual_price = main.get_price(symbol = symbol, date = date)
    reported_price = ticker["price"]
    return actual_price == reported_price

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
        today_date = main.get_today()
        assert is_price_right(ticker, today_date)

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
        date = data_point["date"]
        price = data_point["price"]
        assert is_string(date)
        assert is_string(price)
        assert is_price_right({"symbol": symbol, "price": price}, date)
    history_in_descending_order = \
        sorted(history, key=itemgetter("date"), reverse=True)
    assert history_in_descending_order == history

def test_pagination():
    user_token = "444"
    symbol = "PYPL"
    def get_page(n):
        response = http_get_history_for_symbol_with_page(
            user_token, symbol, page = n
        )
        return response.get_json()
    number_of_pages_to_get = 3
    inclusive_range = lambda a,b: range(a,b+1)
    pages_to_get = inclusive_range(1, number_of_pages_to_get)
    concatenated_subsequent_pages = pipe(
        pages_to_get,
        map(get_page),
        concat,
        list
    )

    expected_number_of_datums = number_of_pages_to_get * 90
    number_of_datums = len(concatenated_subsequent_pages)

    assert expected_number_of_datums == number_of_datums
    parse_date = lambda date_str: \
        datetime.datetime.fromisoformat(date_str).date()
    dates = pipe(
        concatenated_subsequent_pages,
        map(itemgetter('date')),
        map(parse_date),
    )
    is_difference_between_dates_one_day = lambda two_dates: \
        (two_dates[0] - two_dates[1]) == datetime.timedelta(days=1)
    difference_between_every_two_subsequent_datums_is_one_day = \
        pipe(
            dates,
            sliding_window(2),
            map(is_difference_between_dates_one_day),
            all,
        )

    assert difference_between_every_two_subsequent_datums_is_one_day


