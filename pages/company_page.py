from .base_page import BasePage


class CompanyPage(BasePage):
    """Page object for the Company page (About Us > Why MultiBank)."""

    INTRO_TEXT = "For nearly two decades"

    def open(self):
        """Open the Company page."""
        self.goto("/company")

    def get_heading(self, name):
        """Return a heading on the page by its exact text."""
        return self.page.get_by_role("heading", name=name, exact=True)

    def get_intro_text(self):
        """Return the introduction paragraph under the main heading."""
        return self.page.get_by_text(self.INTRO_TEXT)