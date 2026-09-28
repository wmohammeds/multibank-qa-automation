class BasePage:
    """Parent class for every page object. Holds the shared Playwright page."""

    RISK_WARNING = "Risk Warning"
    VARA_LICENCE = "VL/24/06/001"

    def __init__(self, page):
        """Store the Playwright page so every method can use it."""
        self.page = page

    def goto(self, url):
        """Open a URL and return the server response (holds the status code, e.g. 200)."""
        return self.page.goto(url)

    def has_horizontal_scroll(self):
        """Return True if the page is wider than the browser window."""
        return self.page.evaluate("document.documentElement.scrollWidth > window.innerWidth")

    def text_direction(self):
        """Return the page text direction: 'ltr' (left to right) or 'rtl' (right to left)."""
        return self.page.evaluate("document.documentElement.dir")

    def get_risk_warning(self):
        """Return the risk warning text in the footer."""
        return self.page.get_by_text(self.RISK_WARNING)

    def get_vara_licence(self):
        """Return the VARA licence number text in the footer."""
        return self.page.get_by_text(self.VARA_LICENCE)