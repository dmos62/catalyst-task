from flask import Flask, jsonify, abort, request
from flask_httpauth import HTTPBasicAuth
import utility
from ticker_service import TickerService
from user_service import UserService

app = Flask(__name__)
auth = HTTPBasicAuth()

def get_user_token(auth):
    return auth.current_user()

ticker_service = TickerService()
user_service = UserService(ticker_service)

@auth.verify_password
def verify_password(user_token, _):
    is_user_token_provided = bool(user_token)
    if is_user_token_provided:
        return user_token


@app.route('/tickers')
@auth.login_required
def handle_get_portfolio():
    user_token = get_user_token(auth)
    today = utility.get_today()
    portfolio_snapshot = \
        user_service.get_portfolio_snapshot(today, user_token)
    return jsonify(portfolio_snapshot)

def parse_pagination_parameter(request):
    page = request.args.get('page')
    try:
        return int(page)
    except:
        return

@app.route('/tickers/<ticker_symbol>/history')
@auth.login_required
def handle_get_history(ticker_symbol):
    if not ticker_service.is_known_ticker_symbol(ticker_symbol):
        abort(404)
    pagination_parameter = parse_pagination_parameter(request)
    page_ix = pagination_parameter or 1
    user_token = get_user_token(auth)

    page_length = 90
    today = utility.get_today()
    data_points = ticker_service.get_history(
        page_length = page_length,
        date = today,
        page_ix = page_ix,
        ticker_symbol = ticker_symbol,
    )
    return jsonify(data_points)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
