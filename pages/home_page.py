from .base_page import BasePage


class HomePage(BasePage):
    """Page object for the mb.io home page."""

    HEADER = "header"
    LOGO = "header a[href='/']"
    MAIN_NAV = "header nav[aria-label='Main']"
    NAV_ITEMS = "header nav[aria-label='Main'] a"
    HERO_TITLE = "Crypto for everyone"
    INTERNAL_LINKS = "header nav a[href^='/'], footer a[href^='/']"

    def open(self):
        """Open the home page."""
        self.goto("/")

    def get_header(self):
        """Return the top header bar."""
        return self.page.locator(self.HEADER)

    def get_logo(self):
        """Return the logo link in the header."""
        return self.page.locator(self.LOGO)

    def get_nav_items(self):
        """Return all links in the main navigation."""
        return self.page.locator(self.NAV_ITEMS)

    def get_nav_item(self, name):
        """Return one navigation link by its visible text."""
        return self.page.locator(self.MAIN_NAV).get_by_role("link", name=name, exact=True)

    def click_nav_item(self, name):
        """Click a navigation link by its visible text."""
        self.get_nav_item(name).click()

    def nav_item_names(self):
        """Return the visible text of every navigation link as a list."""
        return self.get_nav_items().all_inner_texts()

    def get_hero_title(self):
        """Return the main banner title at the top of the page."""
        return self.page.get_by_text(self.HERO_TITLE)

    def get_download_app_link(self):
        """Return the 'Download the app' button in the main banner."""
        return self.page.get_by_role("link", name="Download the app")

    def get_open_account_link(self):
        """Return the 'Open an account' button in the main banner."""
        return self.page.get_by_role("link", name="Open an account")

    def get_menu_button(self):
        """Return the menu button shown on small (mobile) screens."""
        return self.page.get_by_role("button", name="Open menu")

    def internal_link_urls(self):
        """Return the full URL of every internal link in the header menu and footer."""
        return self.page.locator(self.INTERNAL_LINKS).evaluate_all("links => links.map(link => link.href)")