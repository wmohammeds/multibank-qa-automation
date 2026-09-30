# Test Plan

This document has two parts:
- **Part A** – the plan for the web automation suite in this repository (Task 1).
- **Part B** – a two-week test plan for the mobile trading app release (Task 2 scenario).

---

## Part A – Web UI automation suite (Task 1)

### A1. Objective
Automatically check that the core public features of the MultiBank crypto platform work and catch problems that would hurt customers: navigation, trading data, key content and links, compliance information and behaviour when things go wrong.

### A2. Scope

**In scope** (public pages, no login):
- Top navigation and layout at desktop and mobile sizes
- Spot market: trading pairs, categories, data fields, coin pages
- Price data: API response, screen vs API, freshness
- Content: hero banner, app download links, About Us > Why MultiBank
- Compliance: risk warning and VARA licence on key pages
- Negative / edge cases: invalid page, broken links, mobile, price service timeout, Arabic (right to left)

**Out of scope** (and why):
- Sign up, login, deposits, trading: the brief says not to create accounts or enter personal or financial data.
- Load / performance and security attack testing: this is a live production site and we have no permission.
- Pixel-by-pixel visual comparison: not built into Playwright for Python.

### A3. Approach
- **Tool:** Python + Playwright + pytest, Page Object Model, test data in `data/`, API helpers in `api/`.
- **Risk-based:** tests are prioritised by customer and business impact (see [Risk Matrix](RISK_MATRIX.md)).
- **Stable by design:** automatic waiting with `expect` (no `sleep`), user-facing locators, check format and rules rather than live values, no dependency on third-party sites being clicked.
- **Known bugs:** tests for known bugs are marked `xfail` with the bug ID, so they stay visible without breaking the build.

### A4. Environments
| Item | Value |
|---|---|
| Site | https://mb.io (the brief's URL, trade.multibank.io, redirects to a login page) |
| Browsers | Chromium, Firefox, WebKit (Safari engine) |
| Screen sizes | 1280×720, 1366×768, 1440×900, 1920×1080, mobile 390×844 |
| Locales | English (en-AE), Arabic (ar-AE) |
| Run locations | Local (Windows 11), GitHub Actions (Ubuntu) |

### A5. Traceability – requirement to test

| Requirement (from the brief) | Test IDs |
|---|---|
| Top navigation renders with all expected items | TC-SMOKE-02, TC-NAV-01 |
| Each navigation item links to the correct destination | TC-NAV-02, TC-NAV-03 |
| Navigation at standard desktop viewport sizes | TC-NAV-04 |
| Spot trading section renders and shows trading pairs | TC-SPOT-01 |
| Trading pairs are grouped into categories | TC-SPOT-02 |
| Trading pair entries contain the expected data fields | TC-SPOT-03 |
| Marketing banners render in the expected page region | TC-CONTENT-01 |
| App Store and Google Play download links resolve | TC-CONTENT-02, TC-CONTENT-03 |
| About Us > Why MultiBank page components, headings, text | TC-CONTENT-04 |
| Negative: invalid route handling | TC-EDGE-01 |
| Negative: broken link detection | TC-EDGE-02 |
| Negative: viewport regression at a mobile breakpoint | TC-EDGE-03 |
| Negative: content loading timeout handling | TC-EDGE-04 |
| Bonus: validate API / network responses | TC-PRICE-01, 02, 03, TC-CONTENT-02, 03 |
| Bonus: parameterised test data | `data/` folder used by all tests |
| Bonus: CI | `.github/workflows/tests.yml` |
| Extra: compliance (risk warning, licence) | TC-EDGE-05 |
| Extra: localisation (Arabic, right to left) | TC-EDGE-06 |
| Extra: coin pages (found BUG-001) | TC-PRICE-04, TC-PRICE-05 |

### A6. Entry and exit criteria
- **Entry:** site reachable, test environment set up (`pip install -r requirements.txt`, `playwright install`).
- **Exit:** all tests pass or are `xfail` with a documented bug ID; the report is generated; new bugs are logged in [BUG_REPORTS.md](BUG_REPORTS.md).

### A7. Deliverables
Test suite, HTML report with screenshots, cross-browser results, bug reports, this plan, risk matrix, release checklist, Task 2 answers.

---

## Part B – Mobile trading app: two-week release test plan (Task 2)

### B1. Objective
Give the team and the business an honest picture of the app's quality and its biggest risks before the first public release and make sure the money flows are safe.

### B2. Scope and priorities

| Priority | Area |
|---|---|
| P1 | Deposits, buy/sell orders, balances, withdrawals |
| P1 | Login, 2FA, session handling, identity verification (KYC) |
| P1 | Price data: correct, up to date, clear when unavailable |
| P2 | Onboarding, navigation, portfolio views, notifications |
| P2 | Device and OS coverage (agreed list of iOS and Android devices) |
| P3 | Visual polish, content, minor settings |

**Out of scope for the first release:** full performance testing (a basic launch-day load check only), full accessibility audit (smoke check only) and full test automation (smoke only).

### B3. Timeline

| Days | Activity |
|---|---|
| 1–2 | Learn the product; exploratory testing of the critical journeys; first bug list |
| 3 | Risk matrix, release criteria and device list agreed with the team |
| 3–8 | Structured testing of P1 areas (manual + API); daily bug triage with developers |
| 5–9 | Automated smoke suite (API + critical UI journeys) running in CI |
| 9–11 | P2 areas; device and network-condition testing; fix verification |
| 12–13 | Full regression on the release candidate; production readiness checks |
| 14 | Go / no-go meeting using the [Release Readiness Checklist](RELEASE_CHECKLIST.md) |

### B4. Test types
Exploratory, structured manual test cases for money flows, API tests, automated smoke, device/OS matrix, network conditions (offline, slow, switching), interruption (calls, app killed, background), upgrade/install and a basic security review (sessions, 2FA, data exposure).

### B5. Environments and data
Staging with test money and test accounts; production verification with internal accounts on release day; real devices plus cloud devices if available.

### B6. Bug management
Every bug gets steps, expected vs actual, severity, device/OS and evidence. Daily triage. Severity guide:
- **Critical:** money lost or wrong, security hole, app unusable → blocks release.
- **High:** core journey broken with no workaround → blocks release unless the business accepts the risk in writing.
- **Medium / Low:** fixed if time allows, otherwise logged as known issues.

### B7. Exit criteria
- No open Critical bugs; High bugs fixed or formally accepted.
- All P1 journeys pass on the agreed devices.
- Smoke suite green on the release candidate.
- Release checklist signed off.

### B8. Risks to the plan
Only two weeks; no documentation; unstable builds. Mitigations: focus on P1, daily triage, early agreement on release criteria and clear reporting so decisions are made on facts.
