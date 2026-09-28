# MultiBank QA Automation Challenge

UI and API test automation for the MultiBank crypto platform (**https://mb.io**), built with **Python + Playwright + pytest**.

**24 tests** covering every scenario in the brief, plus the areas a regulated trading platform can't afford to get wrong: **prices, compliance and outages**. They run in **Chromium, Firefox and WebKit**, locally and in **GitHub Actions**.

While building the suite I found **real issues on the live site**, including coin pages that return **HTTP 500** ([BUG-001](docs/BUG_REPORTS.md#bug-001--coin-page-returns-http-500-and-shows-undefined--empty-data)) and **stale prices** in the market data API ([BUG-002](docs/BUG_REPORTS.md#bug-002--prices-api-returns-stale-prices-for-some-coins-to-confirm)).

---

## Run it

**Requirements:** Python 3.12+ and Git.

```bash
git clone https://github.com/wmohammeds/multibank-qa-automation.git
cd multibank-qa-automation
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS / Linux: source .venv/bin/activate)
pip install -r requirements.txt
playwright install
```

**Run the whole suite (one command):**
```bash
pytest
```

**Run in all three browsers:**
```bash
pytest --browser chromium --browser firefox --browser webkit
```

**Useful options**

| Command | What it does |
|---|---|
| `pytest --headed --slowmo 500` | Watch the browser, slowed down |
| `pytest tests/test_price_data.py` | Run one test file |
| `pytest -k navigation` | Run tests with "navigation" in their name |

**Expected result:** `22 passed, 2 xfailed` per browser. The 2 `xfailed` are tests for known bugs (BUG-001, BUG-002). They check the correct behaviour and are marked as expected failures, so the build stays green and the bugs stay visible. If a bug is fixed, the test shows `XPASS`.

---

## Reports and evidence

| What | Where |
|---|---|
| HTML report (every run) | `reports/report.html` |
| Screenshots of failed tests **and known bugs** | inside the HTML report, and `reports/screenshots/` |
| Playwright traces of failed tests (step-by-step replay) | `test-results/` → open with `playwright show-trace <file>.zip` |
| Sample cross-browser report | [`docs/test-report-cross-browser.html`](docs/test-report-cross-browser.html) (download and open in a browser) |
| CI runs (3 browsers in parallel) | GitHub → **Actions** tab → each run has a downloadable report |

---

## What is tested

| Area | Tests | File |
|---|---|---|
| Smoke | TC-SMOKE-01, 02 | `test_smoke.py` |
| Navigation: items, links, external link | TC-NAV-01, 02, 03 | `test_navigation.py` |
| Navigation at 4 desktop screen sizes | TC-NAV-04 | `test_desktop_viewports.py` |
| Spot trading: pairs, categories, data fields | TC-SPOT-01, 02, 03 | `test_spot_trading.py` |
| Price data: API, screen vs API, freshness, coin pages | TC-PRICE-01 – 05 | `test_price_data.py` |
| Content: hero banner, App Store, Google Play, Why MultiBank | TC-CONTENT-01 – 04 | `test_content.py` |
| Edge cases: 404, broken links, mobile, price service timeout, risk warning + licence, Arabic | TC-EDGE-01 – 06 | `test_edge_cases.py` |

The full requirement-to-test mapping is in the [Test Plan](docs/TEST_PLAN.md#a5-traceability--requirement-to-test).

**Highlights**
- **Price accuracy:** the price on screen is compared with the market data API the site uses (1% tolerance, because prices move while the test runs), and price timestamps are checked for freshness.
- **Resilience:** the price service is made to time out (`page.route`), and the page must still load and stay usable.
- **App download link:** requests pretending to be an iPhone and an Android phone check that each is sent to the right store, and that the store page exists.
- **Compliance:** the risk warning and VARA licence number must appear on every key page.
- **UAE market:** an Arabic browser must get the Arabic site, displayed right to left.

---

## Project structure

```
multibank-qa-automation/
├── pages/                  Page objects: one class per page (locators + actions)
│   ├── base_page.py        Shared by all pages: goto, footer compliance text, layout checks
│   ├── home_page.py
│   ├── explore_page.py     Spot market table
│   ├── coin_page.py
│   ├── company_page.py     About Us > Why MultiBank
│   └── not_found_page.py
├── api/                    Helpers that call services directly (no browser tab)
│   ├── market_data_api.py  Prices API used by the site
│   └── app_download_api.py Where the app download link sends iPhone / Android users
├── data/                   Test data: expected values, kept apart from test logic
├── tests/                  Test files: what to check
├── docs/                   Test plan, risk matrix, release checklist, bug reports, Task 2 answers
├── conftest.py             Adds a screenshot to the report for failed tests and known bugs
├── pytest.ini              Base URL, report and evidence settings
└── .github/workflows/      CI: runs the suite in 3 browsers on every push
```

---

## Design decisions

- **Page Object Model.** Locators and page actions live in one class per page. When the site changes, one file changes, not every test.
- **Separate test data (`data/`).** Tests say *what* to check; data files say *with which values*. Adding a menu item or coin is a one-line change.
- **API helpers (`api/`).** Services are kept apart from pages, so the same code checks the API and compares it with the UI.
- **Stable tests.** No `sleep()`. Playwright's `expect` waits and retries. Locators use roles and visible text. Live data is checked for **format and business rules** (for example "the top gainer is never the top loser"), not exact values.
- **Independent tests.** Each test gets a fresh browser page and opens its own starting page, so tests can run alone or in any order.
- **Known bugs stay visible.** Tests for open bugs use pytest's built-in `xfail` with the bug ID, instead of being deleted or weakened.
- **Evidence like a manual tester.** Every failure and known bug has a screenshot in the report; failed tests also keep a Playwright trace.
- **Kept simple on purpose.** Plain pytest functions and fixtures, no custom frameworks or heavy plugins, so any tester can read and extend it.

## Assumptions

- **Target URL.** The brief's URL, `https://trade.multibank.io/`, redirects to a login page. The brief says not to create accounts, so the suite tests the public site **https://mb.io**, which has all the required features.
- **About Us > Why MultiBank** is the **Company** page (`/company`), whose main heading is "Why MultiBank Group?".
- **Region.** mb.io redirects to a language + region path (for example `/en-AE`) based on the browser language and the visitor's location. Tests use neutral URLs and check that the URL *contains* the expected path, so they work from any region. The iPhone app is listed in the **UAE** App Store only, so the test checks the UAE store page.
- **Marketing banner** = the home page hero section ("Crypto for everyone" with its "Download the app" and "Open an account" buttons), which must appear within the first screen.
- **Out of scope:** sign-up, login and trading flows (not allowed by the brief), load testing and security attacks on production (no permission), and pixel-based visual comparison (not built into Playwright for Python).

- **Regional content.** mb.io shows a different regulated company by visitor location: MBIO FZE with a VARA licence in the UAE, and MB.IO Pty Ltd with an Australian licence (AFSL) elsewhere, including GitHub's US servers. The compliance test checks that the risk warning and the regulator licence *for the visitor's region* are shown.
---

## Documents

| Document | Contents |
|---|---|
| [Task 2 – QA Strategy](docs/QA_STRATEGY.md) | Answers to the five Task 2 questions |
| [Test Plan](docs/TEST_PLAN.md) | Plan for this suite (with traceability) and a two-week plan for the mobile app release |
| [Risk Matrix](docs/RISK_MATRIX.md) | Likelihood × impact for the web platform and the mobile app |
| [Release Readiness Checklist](docs/RELEASE_CHECKLIST.md) | Go / no-go checklist for the mobile app release |
| [Bug Reports](docs/BUG_REPORTS.md) | Issues found on the live site, with steps, impact and evidence |

## Tools

Python 3 · Playwright 1.63 · pytest 9 · pytest-playwright · pytest-html · GitHub Actions
