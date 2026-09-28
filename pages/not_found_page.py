from .base_page import BasePage


class NotFoundPage(BasePage):
    """Page object for the 'Page not found' (404) page."""

    def get_heading(self):
        """Return the 'Page not found' heading."""
        return self.page.get_by_role("heading", name="Page not found")

    def get_back_home_link(self):
        """Return the 'Back to Homepage' link."""
        return self.page.get_by_role("link", name="Back to Homepage")