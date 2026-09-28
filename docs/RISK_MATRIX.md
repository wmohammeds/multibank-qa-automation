# Risk Matrix

**Risk score = Likelihood × Impact** (each rated 1 = low to 5 = high).

| Score | Level | What it means |
|---|---|---|
| 15–25 | 🔴 High | Test first and deepest; blocks release if not covered |
| 8–14 | 🟠 Medium | Test thoroughly after the high risks |
| 1–7 | 🟢 Low | Light or exploratory testing |

---

## Part A – Web platform (mb.io, Task 1)

| # | Risk | Likelihood | Impact | Score | Level | How this suite covers it |
|---|---|---|---|---|---|---|
| W1 | Prices shown to customers are wrong or out of date | 3 | 5 | 15 | 🔴 | TC-PRICE-01, 02, 03 (found BUG-002) |
| W2 | Coin pages broken for visitors from Google or shared links | 4 | 4 | 16 | 🔴 | TC-PRICE-04, 05 (found BUG-001) |
| W3 | Price service outage breaks the whole page | 2 | 5 | 10 | 🟠 | TC-EDGE-04 |
| W4 | Risk warning or licence missing (regulatory breach) | 2 | 5 | 10 | 🟠 | TC-EDGE-05 |
| W5 | App download links send users to the wrong or a dead app page | 2 | 4 | 8 | 🟠 | TC-CONTENT-02, 03 |
| W6 | Navigation broken or links dead | 2 | 4 | 8 | 🟠 | TC-NAV-01–04, TC-EDGE-02 |
| W7 | Spot market table missing data or wrongly grouped | 2 | 4 | 8 | 🟠 | TC-SPOT-01–03 |
| W8 | Layout broken on phones | 3 | 3 | 9 | 🟠 | TC-EDGE-03 |
| W9 | Arabic (right-to-left) version broken for UAE users | 2 | 3 | 6 | 🟢 | TC-EDGE-06 |
| W10 | Wrong-address pages show an error instead of help | 2 | 2 | 4 | 🟢 | TC-EDGE-01 |
| W11 | Accessibility gaps (no H1, missing alt text) | 4 | 2 | 8 | 🟠 | BUG-003 (manual) |

---

## Part B – Mobile trading app release (Task 2)

| # | Risk | Likelihood | Impact | Score | Level | Mitigation |
|---|---|---|---|---|---|---|
| M1 | Wrong balance after buy / sell / deposit | 3 | 5 | 15 | 🔴 | Manual + API tests with exact expected values; reconcile screen vs back end |
| M2 | Duplicate order or payment (double tap, retry after timeout) | 3 | 5 | 15 | 🔴 | Double-tap and network-drop tests; check the back end ignores duplicates |
| M3 | Withdrawal fails or funds go missing | 2 | 5 | 10 | 🟠 | End-to-end withdrawal tests on staging; controlled production check |
| M4 | Account takeover: weak session handling or 2FA bypass | 2 | 5 | 10 | 🟠 | Session, logout, 2FA and multi-device tests; security review |
| M5 | Prices wrong or stale in the app | 3 | 5 | 15 | 🔴 | Compare app prices with the price source; freshness checks |
| M6 | App crashes on some devices or OS versions | 4 | 3 | 12 | 🟠 | Agreed device matrix; crash monitoring from day one |
| M7 | Poor network causes stuck or unclear transactions | 4 | 4 | 16 | 🔴 | Offline, slow and switching-network tests during orders |
| M8 | Identity verification (KYC) blocks genuine users | 3 | 4 | 12 | 🟠 | Test common document types and failure messages |
| M9 | Missing regulatory content (risk warnings, disclosures) | 2 | 5 | 10 | 🟠 | Compliance checklist reviewed with the compliance team |
| M10 | Launch-day traffic overloads the back end | 2 | 4 | 8 | 🟠 | Basic load check on staging; monitoring and scaling plan |
| M11 | A serious bug is found after release and can't be rolled back fast | 3 | 5 | 15 | 🔴 | Feature flags / kill switch, staged rollout, hotfix process |
| M12 | Visual issues and small text errors | 4 | 1 | 4 | 🟢 | Exploratory testing, fixed if time allows |
