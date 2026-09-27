from playwright.sync_api import expect

from data.nav_data import DESKTOP_SIZES, EXPECTED_NAV_ITEMS
from pages.home_page import HomePage


def test_nav_works_on_desktop_screen_sizes(page):
    """TC-NAV-04: Top navigation shows all items at common desktop screen sizes."""
    home = HomePage(page)

    for width, height in DESKTOP_SIZES:
        page.set_viewport_size({"width": width, "height": height})
        home.open()

        # Header and every menu item must be visible at this screen size
        expect(home.get_header()).to_be_visible()
        for name in EXPECTED_NAV_ITEMS:
            expect(home.get_nav_item(name)).to_be_visible()

        # Page must not scroll sideways (a sign the layout is broken)
        assert not home.has_horizontal_scroll(), f"Horizontal scroll at {width}x{height}"