import re
import time

import pytest
from playwright.sync_api import expect

from api.market_data_api import MarketDataApi
from data.price_data import MAIN_COINS, MAX_PRICE_AGE_MINUTES, PRICE_TOLERANCE_PERCENT
from data.spot_data import PAIRS_PER_CATEGORY
from pages.coin_page import CoinPage
from pages.explore_page import ExplorePage


def test_prices_api_has_data_for_every_coin_on_screen(page):
    """TC-PRICE-01: Prices API responds OK and has data for every coin shown in the table."""
    explore = ExplorePage(page)
    explore.open()
    expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)

    api = MarketDataApi(page)
    response = api.get_prices_response()
    assert response.status == 200

    api_symbols = [coin["base"] for coin in response.json()]
    for symbol in explore.pair_symbols():
        assert symbol in api_symbols, f"{symbol} is on screen but missing from the prices API"


def test_screen_price_matches_api_price(page):
    """TC-PRICE-02: The price customers see matches the price from the API (within 1%)."""
    explore = ExplorePage(page)
    explore.open()
    expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)
    api = MarketDataApi(page)

    for symbol in MAIN_COINS:
        screen_price = explore.pair_price(symbol)
        api_price = float(api.get_coin(symbol)["close"])

        difference_percent = abs(screen_price - api_price) / api_price * 100
        assert difference_percent <= PRICE_TOLERANCE_PERCENT, (
            f"{symbol}: screen ${screen_price} vs API ${api_price} ({difference_percent:.2f}% apart)"
        )


@pytest.mark.xfail(reason="BUG-002 (to confirm): MBG price in the API is hours old")
def test_prices_on_screen_are_fresh(page):
    """TC-PRICE-03: Every coin shown on screen has a price updated in the last 60 minutes."""
    explore = ExplorePage(page)
    explore.open()
    expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)
    api = MarketDataApi(page)

    now = time.time()
    stale_coins = []
    for symbol in explore.pair_symbols():
        age_minutes = (now - api.get_coin(symbol)["timestamp"]) / 60
        if age_minutes > MAX_PRICE_AGE_MINUTES:
            stale_coins.append(f"{symbol} ({age_minutes:.0f} min old)")

    assert stale_coins == [], f"Stale prices: {stale_coins}"


def test_coin_page_opens_from_table(page):
    """TC-PRICE-04: Clicking a coin in the table opens that coin's page."""
    explore = ExplorePage(page)
    explore.open()
    expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)

    explore.click_pair("BTC")

    expect(page).to_have_url(re.compile("/explore/BTC"))
    # Only check the coin name: the "(BTC)" part is sometimes "(undefined)" - see BUG-001
    expect(CoinPage(page).get_about_heading()).to_contain_text("About Bitcoin")


@pytest.mark.xfail(reason="BUG-001: coin page returns HTTP 500 and shows 'undefined' when opened by direct link")
def test_coin_page_opens_by_direct_link(page):
    """TC-PRICE-05: A coin page opened from a link (Google, bookmark) loads correctly."""
    coin = CoinPage(page)

    for symbol, name in MAIN_COINS.items():
        response = coin.open(symbol)
        assert response.status == 200, f"/explore/{symbol} returned HTTP {response.status}"
        expect(coin.get_about_heading()).to_have_text(f"About {name} ({symbol})")