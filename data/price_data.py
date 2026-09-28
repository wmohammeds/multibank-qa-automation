# Test data for price checks.

# Coins used for price checks: symbol -> full name
MAIN_COINS = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
}

# Screen price may differ from API price by up to 1% (prices move while the test runs)
PRICE_TOLERANCE_PERCENT = 1

# A price older than this is stale
MAX_PRICE_AGE_MINUTES = 60