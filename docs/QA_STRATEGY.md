# Task 2 – QA Strategy & Thinking

**Scenario:** I have just joined a fintech startup as a QA Engineer. There is a mobile trading app (iOS and Android), two weeks from its first public release. There is no test suite, no QA documentation, and the team has been shipping fast. Real user funds are involved.

Related documents: [Test Plan](TEST_PLAN.md) · [Risk Matrix](RISK_MATRIX.md) · [Release Readiness Checklist](RELEASE_CHECKLIST.md)

---

## 1. Where do you start?

With two weeks and real money involved, I can't test everything, so I start by **understanding the product and the risks**, not by writing automation.

**Days 1–2: learn and map**
- Talk to the product owner, the developers and support: what does the app do, what changed recently, what are they worried about?
- Use the app myself, like a new customer: sign up, verify identity, deposit, buy, sell, withdraw. I note everything confusing or broken. That exploratory session is my first bug list.
- List the **critical user journeys**, the ones that touch money or trust:
  1. Sign up, login, 2FA and identity verification (KYC)
  2. Deposit funds (card, bank transfer)
  3. Place a buy / sell order and see the correct balance afterwards
  4. Withdraw funds
  5. Prices and portfolio values shown correctly
- Check what already exists: unit tests, a staging environment, test accounts, crash reporting, logs.

**Day 3: agree priorities**
- Build a simple [risk matrix](RISK_MATRIX.md): likelihood × impact for each area.
- Agree with the team and product owner **what "ready to release" means** (the [release checklist](RELEASE_CHECKLIST.md)): for example, "no open critical or high bugs in money flows".

Starting this way means that in the first days I'm already finding the bugs that matter most, and everyone agrees on the goal.

---

## 2. How would you approach testing this app?

**Risk-based**: the most testing time goes to what can lose customers money or break trust.

| Priority | Area | How I test it |
|---|---|---|
| P1 | Money flows: deposit, buy/sell, withdraw, balances | Manual test cases with exact expected values; check the balance on screen matches the back end; edge cases like insufficient funds, double tap on "Buy", losing network mid-order, app killed mid-transaction |
| P1 | Security & access: login, 2FA, session timeout, KYC | Wrong passwords, expired sessions, logging in on two devices, what a logged-out user can see |
| P1 | Price data | Prices match the source, update in time, and are labelled clearly when stale or unavailable |
| P2 | Onboarding and navigation | Happy paths plus common mistakes |
| P2 | Devices | A small, agreed device list: recent and older iPhones and Android phones, small and large screens, different OS versions |
| P3 | Look and feel, content, notifications | Exploratory testing, screenshots against designs |

**Types of testing**
- **Exploratory testing** every day on new builds. With no documentation it finds the most bugs fastest.
- **Structured test cases** for the critical journeys, so they are repeatable and anyone can run them.
- **API testing** of the back end (for example with Postman or Python): money logic is best checked below the UI, where it's faster and more precise.
- **Automation**, started small: a smoke suite of the critical journeys on the API and web, then mobile UI later. In two weeks, I wouldn't try to automate everything.
- **Non-functional basics**: slow or no network, app in the background, low battery, app updates over an older version.

**Environments**: test on staging with test money first, and do a small, controlled check in production at release (for example a tiny real deposit and withdrawal with an internal account).

---

## 3. What does QA look like inside a sprint, from ticket creation through to regression?

QA is involved at **every** step, not only at the end.

1. **Ticket creation / refinement**: I review the story before it's started and ask "how will we know it works?" I help write clear **acceptance criteria**, including negative cases ("what if the payment fails?").
2. **Sprint planning**: testing effort is part of the estimate. A story isn't done until it's tested.
3. **During development**: I write test cases or charters in parallel with the developer, and prepare test data and accounts. Developers write unit tests; I review what they cover.
4. **Testing the story**: when a build is ready, I test against the acceptance criteria and explore around it. Bugs are logged with steps, expected vs actual, severity, device/OS and evidence (screenshot or video).
5. **Bug fix and retest**: fixes are retested, and I check nearby features for side effects.
6. **Automation**: stable, important checks from the story are added to the automated suite, so the regression suite grows every sprint.
7. **Regression**: before release, the automated suite runs on every build (CI), plus a focused manual regression of the critical journeys on real devices.
8. **Sprint review / retro**: I share quality information (bugs found, where they came from, escaped bugs) so the team can improve.

---

## 4. What does your ideal regression suite look like?

- **Layered, like a pyramid**: many fast unit tests (developers), a good set of API tests for business rules and money logic, and a **small** number of end-to-end UI tests for the critical journeys only.
- **Risk-based and focused**: every test is there for a reason. The money flows, login and prices are always covered. It's better to have 50 reliable tests than 500 flaky ones.
- **Tiered**:
  - **Smoke** (minutes): runs on every build. Can users log in, see prices, and open buy/sell?
  - **Full regression** (under an hour): runs nightly and before every release.
- **Automated in CI**, with clear reports and evidence (screenshots, logs) on failure, and results that the whole team looks at.
- **Reliable**: no fixed sleeps, independent tests, stable test data, and flaky tests are fixed or removed quickly, because a suite nobody trusts is useless.
- **Traceable**: each test links to a requirement or risk, so we know what a failure means for customers.
- **Maintained**: reviewed every sprint. New features add tests; removed features remove them.
- **Plus a short manual checklist** on real devices for things automation can't judge well (look and feel, real payment cards, app store install).

This project follows the same ideas on a small scale: page objects, separate test data, known bugs tracked with `xfail`, reports with screenshots, three browsers and CI.

---

## 5. What would keep you up at night about this app and releasing to the public?

1. **Money being wrong.** A balance that doesn't update, a double charge from tapping "Buy" twice, an order placed at a different price than shown, or a withdrawal that leaves the account but never arrives. With real funds, one such bug can lose customers and trigger regulatory action.
2. **Wrong or stale prices.** On the website I found prices in the API that were hours or days old (BUG-002). In a trading app, customers act on the number they see.
3. **Security and account takeover.** Weak session handling, 2FA that can be skipped, or personal/KYC data exposed.
4. **No time to recover.** No test suite and fast shipping mean we don't know what's already broken. A mobile release can't be rolled back instantly: users must update from the app store, and review takes time. So I'd want **feature flags** or a server-side "kill switch" for risky features, and crash monitoring from day one.
5. **Real-world conditions.** Poor mobile network, the app killed during a transaction, old phones, and many users at once on launch day.
6. **Regulation.** Missing risk warnings, disclosures or complaint routes in the app (the website shows these on every page; the app must too).

**What I'd do about it**: focus the two weeks on these risks, agree clear go/no-go criteria, plan a staged rollout (for example a small percentage of users first), and make sure monitoring and a support process are in place on release day.
