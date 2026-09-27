from .base_page import BasePage


class HomePage(BasePage):
    """Page object for the mb.io home page."""

    HEADER = "header"
    LOGO = "header a[href='/']"

    def open(self):
        """Open the home page."""
        self.goto("/")

    def get_header(self):
        """Return the top header bar."""
        return self.page.locator(self.HEADER)

    def get_logo(self):
        """Return the logo link in the header."""
        return self.page.locator(self.LOGO)