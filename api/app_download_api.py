import time

from playwright.sync_api import Error

# The link service sometimes can't be found for a few seconds (a network / DNS hiccup),
# so each request is tried up to 3 times, 5 seconds apart, before the test fails.
ATTEMPTS = 3
WAIT_SECONDS = 5


class AppDownloadApi:
    """Checks where the 'Download the app' link sends iPhone and Android users."""

    def __init__(self, playwright):
        """Store Playwright so we can send requests that pretend to be a phone."""
        self.playwright = playwright

    def redirect_target(self, link, user_agent):
        """Open the link as the given device and return the address it redirects to."""
        response = self.get(link, user_agent=user_agent, max_redirects=0)
        return response.headers.get("location")

    def page_status(self, url):
        """Return the HTTP status code of a web page, e.g. 200 or 404."""
        return self.get(url).status

    def get(self, url, user_agent=None, max_redirects=20):
        """Send a request, trying again if the network fails for a moment."""
        request = self.playwright.request.new_context(user_agent=user_agent)
        for attempt in range(1, ATTEMPTS + 1):
            try:
                return request.get(url, max_redirects=max_redirects)
            except Error:
                if attempt == ATTEMPTS:
                    raise
                time.sleep(WAIT_SECONDS)