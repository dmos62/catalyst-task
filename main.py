from flask import Flask
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

known_ticker_symbols = \
    {
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
    }

def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')

def get_ticker_symbols_in_portfolio(user_token):
    # TODO
    return

def get_price_for_symbol_at_date(ticker, date):
    # TODO
    return

@auth.verify_password
def verify_password(username, _password):
    return username

@app.route('/')
@auth.login_required
def index():
    return {"Hello": auth.current_user()}

if __name__ == '__main__':
    app.run()
