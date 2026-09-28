from playwright.sync_api import expect

from api.app_download_api import AppDownloadApi
from data.content_data import (
    ANDROID_USER_AGENT,
    APP_STORE_APP_ID,
    APP_STORE_UAE_URL,
    GOOGLE_PLAY_APP_ID,
    GOOGLE_PLAY_URL,
    IPHONE_USER_AGENT,
    WHY_MULTIBANK_HEADINGS,
    WHY_MULTIBANK_INTRO,
)
from pages.company_page import CompanyPage
from pages.home_page import HomePage


def test_hero_banner_is_in_top_region(page):
    """TC-CONTENT-01: Main banner and its buttons are shown at the top of the home page."""
    home = HomePage(page)
    home.open()

    expect(home.get_hero_title()).to_be_visible()
    expect(home.get_download_app_link()).to_be_visible()
    expect(home.get_open_account_link()).to_be_visible()

    # The banner must be inside the first screen, without scrolling
    banner_top = home.get_hero_title().bounding_box()["y"]
    screen_height = page.viewport_size["height"]
    assert banner_top < screen_height, f"Banner starts at {banner_top}px, below the first screen"


def test_download_link_opens_app_store_on_iphone(page, playwright):
    """TC-CONTENT-02: 'Download the app' sends iPhone users to the mb.io app in the App Store."""
    home = HomePage(page)
    home.open()
    download_link = home.get_download_app_link().get_attribute("href")

    app_links = AppDownloadApi(playwright)
    target = app_links.redirect_target(download_link, IPHONE_USER_AGENT)

    assert "apps.apple.com" in target and APP_STORE_APP_ID in target, f"iPhone sent to {target}"
    assert app_links.page_status(APP_STORE_UAE_URL) == 200


def test_download_link_opens_google_play_on_android(page, playwright):
    """TC-CONTENT-03: 'Download the app' sends Android users to the mb.io app in Google Play."""
    home = HomePage(page)
    home.open()
    download_link = home.get_download_app_link().get_attribute("href")

    app_links = AppDownloadApi(playwright)
    target = app_links.redirect_target(download_link, ANDROID_USER_AGENT)

    assert "play.google.com" in target and GOOGLE_PLAY_APP_ID in target, f"Android sent to {target}"
    assert app_links.page_status(GOOGLE_PLAY_URL) == 200


def test_why_multibank_page_shows_all_sections(page):
    """TC-CONTENT-04: About Us > Why MultiBank page shows every section heading and the intro text."""
    company = CompanyPage(page)
    company.open()

    for heading in WHY_MULTIBANK_HEADINGS:
        expect(company.get_heading(heading)).to_be_visible()
    expect(company.get_intro_text()).to_contain_text(WHY_MULTIBANK_INTRO)