import re

from playwright.sync_api import expect

from pages.home_page import HomePage


def test_home_page_loads(page):
    """TC-SMOKE-01: Home page opens with the correct title."""
    home = HomePage(page)
    home.open()
    expect(page).to_have_title(re.compile("mb.io"))


def test_header_and_logo_are_visible(page):
    """TC-SMOKE-02: Header and logo are visible on the home page."""
    home = HomePage(page)
    home.open()
    expect(home.get_header()).to_be_visible()
    expect(home.get_logo()).to_be_visible()