import random
from toolz.curried import pipe, map
import utility

class UserService:

    def __init__(self, ticker_service):
        self.ticker_service = ticker_service

    def get_ticker_symbols_in_portfolio(self, user_token):
        seed = user_token
        random.seed(seed)
        number_of_tickers_in_portfolio = random.randint(1, 10)
        deterministically_selected_ticker_symbols = \
            random.sample(
                self.ticker_service.get_known_ticker_symbols(),
                k = number_of_tickers_in_portfolio
            )
        return set(deterministically_selected_ticker_symbols)

    def get_portfolio_snapshot(self, date, user_token):
        ticker_symbols = self.get_ticker_symbols_in_portfolio(user_token)
        make_ticker = lambda ticker_symbol: \
            {
                "symbol": ticker_symbol,
                "price": self.ticker_service.get_price(ticker_symbol, date),
            }
        return pipe(
            ticker_symbols,
            map(make_ticker),
            list
        )
