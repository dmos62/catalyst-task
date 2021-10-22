import datetime
import random
from toolz.curried import pipe, map, tail, partial
import utility

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

def generate_price_deterministically(symbol, date):
    distribution_seed = symbol
    random.seed(distribution_seed)
    mu = random.randint(100, 1000)
    sigma = mu / 4
    ticker_referenced_price = \
        random.gauss(mu, sigma)

    sample_seed = str(date)
    random.seed(sample_seed)
    mu = 0
    sigma = 10
    delta_for_date = \
        random.gauss(mu, sigma)

    price_for_date = \
        ticker_referenced_price + delta_for_date

    string_number = str("%.2f" % price_for_date)
    return string_number

def date_with_days_subtracted(date, days_to_subtract):
    timedelta = datetime.timedelta(days=days_to_subtract)
    return date - timedelta

class TickerService:

    def get_price(self, symbol, date):
        return generate_price_deterministically(symbol, date)

    def get_data_point_for_ticker_and_date(self, ticker_symbol, date):
        data_point = {
            "date": utility.to_iso8601(date),
            "price": self.get_price(symbol = ticker_symbol, date = date)
        }
        return data_point

    def get_known_ticker_symbols(self):
        return known_ticker_symbols

    def is_known_ticker_symbol(self, ticker_symbol):
        return ticker_symbol in self.get_known_ticker_symbols()

    def get_history(
        self,
        page_ix,
        ticker_symbol,
        page_length = 90,
        date = utility.get_today(),
    ):
        whole_date_range = range(page_length * page_ix)
        a_90_day_page = pipe(
            whole_date_range,
            tail(page_length),
            map(partial(date_with_days_subtracted, date)),
        )
        get_data_point_for_date = \
            partial(self.get_data_point_for_ticker_and_date, ticker_symbol)
        data_points = pipe(
            a_90_day_page,
            map(get_data_point_for_date),
            list
        )
        return data_points
