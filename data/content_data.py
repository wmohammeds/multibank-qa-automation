# Test data for content, links and edge case tests.

# About Us > Why MultiBank (the Company page): headings in the order they appear
WHY_MULTIBANK_HEADINGS = [
    "Why MultiBank Group?",
    "A tradition of global leadership",
    "Innovation with purpose",
    "Integrity built into every decision",
    "The strength behind MultiBank Group",
    "Community & Media",
]
WHY_MULTIBANK_INTRO = "regulation, transparency, and technological excellence"

# Phone "user agents": how a browser tells a website which device it is
IPHONE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
ANDROID_USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36"
)

# App store pages (the app is listed in the UAE App Store only)
APP_STORE_APP_ID = "id1592119946"
APP_STORE_UAE_URL = "https://apps.apple.com/ae/app/id1592119946"
GOOGLE_PLAY_APP_ID = "com.multibank.app"
GOOGLE_PLAY_URL = "https://play.google.com/store/apps/details?id=com.multibank.app"

# Pages that must show the risk warning and VARA licence (regulatory requirement)
REGULATED_PAGES = ["/", "/explore", "/company"]

# A mobile phone screen size (iPhone 12/13/14)
MOBILE_SIZE = {"width": 390, "height": 844}