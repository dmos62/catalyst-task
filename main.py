from flask import Flask, jsonify, abort
from flask_httpauth import HTTPBasicAuth
import datetime
import random
from toolz.curried import pipe, map, partial

app = Flask(__name__)
auth = HTTPBasicAuth()

known_ticker_symbols = \
    [
        "AAPL",
        "MSFT",
        "GOOG",
        "AMZN",
        "FB",
        "TSLA",
        "NVDA",
        "JPM",
        "BABA",
        "JNJ",
        "WMT",
        "PG",
        "PYPL",
        "DIS",
        "ADBE",
        "PFE",
        "V",
        "MA",
        "CRM",
        "NFLX"
    ]

# https://docs.python.org/3/library/datetime.html#datetime.date
def get_today():
    return datetime.date.today()

def to_iso8601(date):
    return date.isoformat()

def generate_price_deterministically(symbol, date):
    seed = symbol + str(date)
    random.seed(seed)
    random_integer = random.randint(1, 1000)
    with_decimal = random_integer / 10
    string_number = str(with_decimal)
    return string_number

def get_price(symbol, date):
    return generate_price_deterministically(symbol, date)

def get_ticker_symbols_in_portfolio(user_token):
    seed = user_token
    random.seed(seed)
    number_of_tickers_in_portfolio = random.randint(1, 10)
    deterministically_selected_ticker_symbols = \
        random.sample(known_ticker_symbols, k=number_of_tickers_in_portfolio)
    return set(deterministically_selected_ticker_symbols)

def get_portfolio_snapshot(user_token):
    ticker_symbols = get_ticker_symbols_in_portfolio(user_token)
    today = get_today()
    make_ticker = lambda ticker_symbol: \
        {
            "symbol": ticker_symbol,
            "price": get_price(ticker_symbol, today),
        }
    return pipe(
        ticker_symbols,
        map(make_ticker),
        list
    )

@auth.verify_password
def verify_password(user_token, _):
    is_user_token_provided = bool(user_token)
    if is_user_token_provided:
        return user_token

def get_user_token(auth):
    return auth.current_user()

def date_with_days_subtracted(date, days_to_subtract):
    timedelta = datetime.timedelta(days=days_to_subtract)
    return date - timedelta

def get_data_point_for_ticker_and_date(ticker_symbol, date):
    data_point = {
        "date": to_iso8601(date),
        "price": get_price(symbol = ticker_symbol, date = date)
    }
    return data_point

@app.route('/tickers')
@auth.login_required
def handle_get_portfolio():
    user_token = get_user_token(auth)
    portfolio_snapshot = get_portfolio_snapshot(user_token)
    return jsonify(portfolio_snapshot)

@app.route('/tickers/<ticker_symbol>/history')
@auth.login_required
def handle_get_history(ticker_symbol):
    is_known_ticker = ticker_symbol in known_ticker_symbols
    if not is_known_ticker:
        abort(404)
    user_token = get_user_token(auth)
    today = get_today()
    last_90_days = pipe(
        range(90),
        map(partial(date_with_days_subtracted, today)),
    )
    get_data_point_for_date = \
        partial(get_data_point_for_ticker_and_date, ticker_symbol)
    data_points = pipe(
        last_90_days,
        map(get_data_point_for_date),
        list
    )
    return jsonify(data_points)

if __name__ == '__main__':
    app.run()
