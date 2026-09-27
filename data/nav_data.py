# Test data for the top navigation, shared by all navigation tests.

# The menu items we expect, in the same order as on the website
EXPECTED_NAV_ITEMS = ["Explore", "Features", "OTC Desk", "Company", "Support", "Blog", "$MBG"]

# Menu item -> text the page URL should contain after clicking it
NAV_LINKS = {
    "Explore": "/explore",
    "Features": "/features",
    "OTC Desk": "/otc-desk",
    "Company": "/company",
    "Support": "/support",
    "Blog": "/blog",
}

# Common desktop screen sizes (width, height)
DESKTOP_SIZES = [
    (1280, 720),
    (1366, 768),
    (1440, 900),
    (1920, 1080),
]