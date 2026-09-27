import re

from playwright.sync_api import expect

from data.nav_data import EXPECTED_NAV_ITEMS, NAV_LINKS
from pages.home_page import HomePage


def test_all_nav_items_are_visible(page):
    """TC-NAV-01: Top navigation shows all expected items in the correct order."""
    home = HomePage(page)
    home.open()

    # Check each expected menu item can be seen
    for name in EXPECTED_NAV_ITEMS:
        expect(home.get_nav_item(name)).to_be_visible()

    # Check there are no extra or missing items, and the order is correct
    assert home.nav_item_names() == EXPECTED_NAV_ITEMS


def test_nav_items_open_correct_pages(page):
    """TC-NAV-02: Each navigation item opens the correct page."""
    home = HomePage(page)

    for name, url_part in NAV_LINKS.items():
        home.open()
        home.click_nav_item(name)
        expect(page).to_have_url(re.compile(url_part))


def test_mbg_link_points_to_token_site(page):
    """TC-NAV-03: $MBG link goes to the MultiBank token site in a new tab."""
    home = HomePage(page)
    home.open()

    mbg_link = home.get_nav_item("$MBG")
    expect(mbg_link).to_have_attribute("href", re.compile("token.multibankgroup.com"))
    expect(mbg_link).to_have_attribute("target", "_blank")