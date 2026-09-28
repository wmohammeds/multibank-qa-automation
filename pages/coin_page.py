import re

from .base_page import BasePage


class CoinPage(BasePage):
    """Page object for a single coin page, e.g. /explore/BTC."""

    ABOUT_HEADING = re.compile("^About ")

    def open(self, symbol):
        """Open the coin page directly by its symbol and return the server response."""
        return self.goto(f"/explore/{symbol}")

    def get_about_heading(self):
        """Return the 'About <coin> (<symbol>)' heading, e.g. 'About Bitcoin (BTC)'."""
        return self.page.get_by_role("heading", name=self.ABOUT_HEADING)