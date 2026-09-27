from playwright.sync_api import expect

from data.spot_data import CATEGORIES, PAIRS_PER_CATEGORY
from pages.explore_page import ExplorePage


def test_spot_market_shows_trading_pairs(page):
    """TC-SPOT-01: Spot market section is shown with a full list of trading pairs."""
    explore = ExplorePage(page)
    explore.open()

    expect(explore.get_spot_market_heading()).to_be_visible()
    # expect waits until all pairs have loaded (the table fills in over a few seconds)
    expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)


def test_trading_pairs_are_grouped_into_categories(page):
    """TC-SPOT-02: Hot, Gainers and Losers tabs each show their own list of pairs."""
    explore = ExplorePage(page)
    explore.open()

    # Every category tab is visible and shows a full list when clicked
    for category in CATEGORIES:
        expect(explore.get_category_tab(category)).to_be_visible()
        explore.click_category(category)
        expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)

    # Gainers and Losers must show different lists
    explore.click_category("Gainers")
    gainers = explore.pair_symbols()
    explore.click_category("Losers")
    losers = explore.pair_symbols()

    assert gainers != losers, "Gainers and Losers show the same pairs"
    assert gainers[0] != losers[0], f"{gainers[0]} is both top gainer and top loser"


def test_trading_pairs_have_expected_data_fields(page):
    """TC-SPOT-03: Every trading pair shows a symbol, name, price and % change."""
    explore = ExplorePage(page)
    explore.open()
    expect(explore.get_pair_rows()).to_have_count(PAIRS_PER_CATEGORY)

    symbols = explore.pair_symbols()
    names = explore.pair_names()
    prices = explore.pair_prices()
    changes = explore.pair_changes()

    # Every row must have all four fields (no missing values)
    assert len(symbols) == len(names) == len(prices) == len(changes) == PAIRS_PER_CATEGORY

    # Check each field has the expected format
    for symbol, name, price, change in zip(symbols, names, prices, changes):
        assert symbol != "", "Symbol is empty"
        assert name != "", f"Name is empty for {symbol}"
        assert price.startswith("$"), f"{symbol} price '{price}' does not start with $"
        assert change.endswith("%"), f"{symbol} change '{change}' does not end with %"