import re
class BasePage:
    """Parent class for every page object. Holds the shared Playwright page."""

    RISK_WARNING = "Risk Warning"
        # The site shows the regulator of the visitor's region: UAE (VARA) or Australia (AFSL)
    REGULATOR_LICENCE = re.compile("VL/24/06/001|AFSL 416279")

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

    def get_regulator_licence(self):
        """Return the regulator licence number in the footer (UAE or Australian)."""
        return self.page.get_by_text(self.REGULATOR_LICENCE).first