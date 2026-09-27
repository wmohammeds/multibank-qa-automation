from .base_page import BasePage


class ExplorePage(BasePage):
    """Page object for the Explore page, which holds the spot market section."""

    PAIR_ROWS = "table tbody tr"
    PAIR_SYMBOLS = "table tbody tr td[id$='_displayName-td'] span:first-child"
    PAIR_NAMES = "table tbody tr td[id$='_displayName-td'] span:last-child"
    PAIR_PRICES = "table tbody tr td[id$='_price-td']"
    PAIR_CHANGES = "table tbody tr td[id$='_change-td'] span"

    def open(self):
        """Open the Explore page."""
        self.goto("/explore")

    def get_spot_market_heading(self):
        """Return the 'Spot market' heading."""
        return self.page.get_by_role("heading", name="Spot market")

    def get_pair_rows(self):
        """Return all trading pair rows in the table."""
        return self.page.locator(self.PAIR_ROWS)

    def get_category_tab(self, name):
        """Return a category tab (Hot, Gainers, Losers) by its text."""
        return self.page.get_by_role("button", name=name, exact=True)

    def click_category(self, name):
        """Click a category tab by its text."""
        self.get_category_tab(name).click()

    def pair_symbols(self):
        """Return the symbol of every pair, e.g. ['BTC', 'ETH']."""
        return self.page.locator(self.PAIR_SYMBOLS).all_inner_texts()

    def pair_names(self):
        """Return the full name of every pair, e.g. ['Bitcoin', 'Ethereum']."""
        return self.page.locator(self.PAIR_NAMES).all_inner_texts()

    def pair_prices(self):
        """Return the price of every pair, e.g. ['$84,452.45']."""
        return self.page.locator(self.PAIR_PRICES).all_inner_texts()

    def pair_changes(self):
        """Return the 24h change of every pair, e.g. ['0.33%']."""
        return self.page.locator(self.PAIR_CHANGES).all_inner_texts()
        