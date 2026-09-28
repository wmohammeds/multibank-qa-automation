import re

from playwright.sync_api import expect

from data.content_data import MOBILE_SIZE, REGULATED_PAGES
from data.nav_data import EXPECTED_NAV_ITEMS
from data.spot_data import PAIRS_PER_CATEGORY
from pages.explore_page import ExplorePage
from pages.home_page import HomePage
from pages.not_found_page import NotFoundPage


def test_invalid_page_shows_friendly_404(page):
    """TC-EDGE-01: A wrong address shows a 'Page not found' page with a way back home."""
    not_found = NotFoundPage(page)
    response = not_found.goto("/this-page-does-not-exist")

    assert response.status == 404
    expect(not_found.get_heading()).to_be_visible()

    not_found.get_back_home_link().click()
    expect(page).not_to_have_url(re.compile("this-page-does-not-exist"))
    expect(HomePage(page).get_hero_title()).to_be_visible()


def test_no_broken_links_in_menu_and_footer(page):
    """TC-EDGE-02: Every internal link in the header menu and footer opens without an error."""
    home = HomePage(page)
    home.open()

    broken_links = []
    for url in home.internal_link_urls():
        status = page.request.get(url).status
        if status >= 400:
            broken_links.append(f"{url} -> HTTP {status}")

    assert broken_links == [], f"Broken links: {broken_links}"


def test_mobile_screen_shows_menu_button(page):
    """TC-EDGE-03: On a phone screen the menu collapses into a button that still opens all items."""
    page.set_viewport_size(MOBILE_SIZE)
    home = HomePage(page)
    home.open()

    expect(home.get_menu_button()).to_be_visible()
    assert not home.has_horizontal_scroll(), "Page scrolls sideways on a phone screen"

    home.get_menu_button().click()
    for name in EXPECTED_NAV_ITEMS:
        expect(page.get_by_role("link", name=name, exact=True)).to_be_visible()


def test_page_still_works_when_price_service_times_out(page):
    """TC-EDGE-04: If the price service times out, the page still loads and can be used."""
    # Make every call to the price service fail with a timeout (only in this test's browser)
    page.route("**/marketdata/**", lambda route: route.abort("timedout"))

    explore = ExplorePage(page)
    explore.open()

    expect(explore.get_spot_market_heading()).to_be_visible()
    expect(HomePage(page).get_nav_item("Explore")).to_be_visible()
    expect(explore.get_pair_rows()).not_to_have_count(PAIRS_PER_CATEGORY)


def test_risk_warning_and_licence_on_every_key_page(page):
    """TC-EDGE-05: Risk warning and VARA licence number are shown on every key page."""
    home = HomePage(page)

    for path in REGULATED_PAGES:
        home.goto(path)
        expect(home.get_risk_warning()).to_be_visible()
        expect(home.get_vara_licence()).to_be_visible()


def test_arabic_version_reads_right_to_left(browser):
    """TC-EDGE-06: An Arabic browser gets the Arabic site, shown right to left."""
    arabic_browser = browser.new_context(locale="ar-AE", base_url="https://mb.io")
    page = arabic_browser.new_page()
    home = HomePage(page)
    home.open()

    expect(page).to_have_url(re.compile("/ar-"))
    assert home.text_direction() == "rtl"
    expect(home.get_nav_items()).to_have_count(len(EXPECTED_NAV_ITEMS))

    arabic_browser.close()