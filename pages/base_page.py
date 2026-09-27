class BasePage:
    """Parent class for every page object. Holds the shared Playwright page."""

    def __init__(self, page):
        """Store the Playwright page so every method can use it."""
        self.page = page

    def goto(self, url):
        """Open a URL. A path like "/" is added to the base_url in pytest.ini."""
        self.page.goto(url)