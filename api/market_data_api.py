PRICES_URL = "https://mbg-market-data-service.mb.io/api/io/v1/marketdata/prices?quote=USDT"


class MarketDataApi:
    """Reads prices straight from the market data service the website uses."""

    def __init__(self, page):
        """Store the Playwright page; page.request sends API calls without a browser tab."""
        self.page = page

    def get_prices_response(self):
        """Call the prices API and return the raw response."""
        return self.page.request.get(PRICES_URL)

    def get_prices(self):
        """Return the price list as Python dictionaries, one per coin."""
        return self.get_prices_response().json()

    def get_coin(self, symbol):
        """Return the price data for one coin, e.g. 'BTC'."""
        for coin in self.get_prices():
            if coin["base"] == symbol:
                return coin
        return None