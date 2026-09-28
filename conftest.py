import base64
from pathlib import Path

import pytest
import pytest_html
from playwright.sync_api import expect

SCREENSHOT_FOLDER = Path("reports/screenshots")

# The site loads its price table in stages and can be slow when busy (up to about 5 seconds),
# so every expect() check waits up to 15 seconds instead of Playwright's default 5.
expect.set_options(timeout=15_000)


def pytest_html_report_title(report):
    """Set the title shown at the top of the HTML report."""
    report.title = "MultiBank QA Automation - Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each test: if it failed or hit a known bug, save a screenshot and add it to the HTML report."""
    outcome = yield
    report = outcome.get_result()

    page = item.funcargs.get("page")
    failed = report.failed or hasattr(report, "wasxfail")

    if report.when == "call" and failed and page is not None:
        # 1. Save the screenshot as a file, named after the test
        SCREENSHOT_FOLDER.mkdir(parents=True, exist_ok=True)
        file_name = item.name.replace("[", "_").replace("]", "") + ".png"
        screenshot = page.screenshot(path=SCREENSHOT_FOLDER / file_name, full_page=True)

        # 2. Show the same screenshot inside the HTML report
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(base64.b64encode(screenshot).decode()))
        report.extras = extras