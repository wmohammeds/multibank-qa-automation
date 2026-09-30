# Bug Reports

Issues found on the live site (https://mb.io) while building this suite, 27–28 Sep 2026.
The two most important ones are covered by tests, so the suite shows at once when they are fixed.

| ID | Title | Severity | Status | Covered by |
|---|---|---|---|---|
| BUG-001 | Coin page returns HTTP 500 and shows "undefined" / empty data | **High** | Open | TC-PRICE-05 (xfail), TC-PRICE-04 |
| BUG-002 | Prices API returns stale prices for some coins | Medium | **To confirm** with product team | TC-PRICE-03 (xfail) |
| BUG-003 | Home page has no H1 heading; some images have no alt text | Low | Open | Manual check |
| BUG-004 | Coin description shows outdated figures | Low | Open | Manual check |

---

## BUG-001 – Coin page returns HTTP 500 and shows "undefined" / empty data

**Severity:** High | **Priority:** High
**Environment:** Production (https://mb.io), Chromium / Firefox / WebKit, Windows 11

**Summary**
Opening a coin page directly (from Google, a bookmark or a shared link) returns a **server error (HTTP 500)**. The page the server sends has no data and in the browser the page shows broken placeholders.
Clicking the coin from the Explore table usually works, but about **1 time in 8** it shows the same broken state.

**Steps to reproduce (direct link)**
1. Open a new browser tab.
2. Go to `https://mb.io/en-AE/explore/BTC`.

**Expected result**
- HTTP status **200**.
- Heading "About Bitcoin (BTC)", sentiment percentage and "Overall Health" data filled in.

**Actual result**
- HTTP status **500** (also for ETH and SOL).
- The page sent by the server contains "No Data Found" and the unfilled template text `About {{displayName}} ({{code}})`.
- In the browser: heading **"About Bitcoin (undefined)"**, sentiment **0.00%**, "Overall Health" panel empty. Sometimes the page fills in a few seconds later, once scripts have loaded, but the status stays 500.

**Steps to reproduce (intermittent, by clicking)**
1. Go to `https://mb.io/en-AE/explore` and wait for the table to load.
2. Click "BTC".
3. About 1 time in 8, the heading shows **"About Bitcoin (undefined)"** and sentiment 0.00%. It stays like this after waiting 6 seconds and there is no page reload.

**Customer and business impact**
- Visitors arriving from search engines, bookmarks or shared links (often *new* customers) can see a broken page.
- Search engines see an error page with no data, which can hurt the ranking of every coin page.

**Evidence**
- `docs/evidence/BUG-001-direct-link.png` – direct link: "About Bitcoin (undefined)", sentiment 0.00%, empty Overall Health
- `docs/evidence/BUG-001-click-undefined.png` – same state after clicking BTC in the table
- The HTML report attaches a screenshot to TC-PRICE-05 on every run.

---

## BUG-002 – Prices API returns stale prices for some coins (to confirm)

**Severity:** Medium (High if confirmed)
**Environment:** `https://mbg-market-data-service.mb.io/api/io/v1/marketdata/prices?quote=USDT`

**Summary**
Each coin in the prices API has a `timestamp` of its last update. Most coins were updated seconds ago, but:
- **MBG** (MultiBank's own token, shown first in the "Hot" list) was about **14 hours old**.
- **USDC** was about **69 days old**.

**Steps to reproduce**
1. Call the prices API (link above).
2. For each coin, compare `timestamp` (seconds since 1970) with the current time.

**Expected result**
Every coin shown to customers has a recently updated price (the test uses 60 minutes).

**Actual result**
MBG and USDC prices are hours or days old.

**Why "to confirm"**
A token that trades rarely may legitimately have an older last price. This needs confirming with the product team: if it's expected, the site should show when the price was last updated; if not, it's a data feed problem.

**Customer impact**
Customers could make trading decisions based on an out-of-date price.

---

## BUG-003 – Home page has no H1 heading; images without alt text

**Severity:** Low | **Environment:** https://mb.io home page

**Summary**
- The home page has **no `<h1>` heading**. The main title "Crypto for everyone" is not marked up as a heading.
- **2 images** on the home page have no `alt` text.

**Expected result**
One H1 per page describing its main topic and alt text on every meaningful image.

**Impact**
- Screen reader users can't jump to the main heading or understand the images (accessibility).
- Search engines use the H1 to understand the page (SEO).

---

## BUG-004 – Coin description shows outdated figures

**Severity:** Low | **Environment:** https://mb.io/en-AE/explore/BTC

**Summary**
The "About Bitcoin (BTC)" text says *"The last known price of Bitcoin is 29,548.38 USD"*, while the same page shows a live price of about **$83,000**.

**Expected result**
The description doesn't contain numbers that go out of date, or they are updated automatically.

**Impact**
Conflicting prices on the same page confuse customers and reduce trust.


| BUG-005 | 404 page shows the Australian company's footer to UAE visitors | Medium | Open | Manual check |
---

## BUG-005 – 404 page shows the Australian company's footer to UAE visitors

**Severity:** Medium | **Environment:** https://mb.io/en-AE/this-page-does-not-exist (visited from the UAE)

**Summary**
Every normal page shown to a UAE visitor names the UAE company, **MBIO FZE**, with its **VARA** licence (VL/24/06/001) and the full set of UAE legal links. The "Page not found" page instead shows the **Australian** company MB.IO Pty Ltd (AFSL 416279) and only 5 legal links, even though the address is `/en-AE/...`.

**Expected result**
The 404 page shows the same regulated company, licence and legal links as the rest of the UAE site.

**Impact**
A regulated firm should show customers the correct licensed company and disclosures on every page. Showing another country's company can confuse customers and is a compliance risk.

**Evidence:** `docs/evidence/BUG-005-404-footer.png`