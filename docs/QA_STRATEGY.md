# Task 2 – QA Strategy & Thinking

**Scenario:** I've just joined a fintech startup as a QA Engineer. There's a mobile trading app (iOS and Android) two weeks from its first public release, with no test suite, no QA documentation, and a team that has been shipping fast. Real customer money is involved.

These answers come from my Quality Engineering and from what I learned building the automation suite in this repository.

Supporting documents: [Test Plan](TEST_PLAN.md) · [Risk Matrix](RISK_MATRIX.md) · [Release Readiness Checklist](RELEASE_CHECKLIST.md)

---

## 1. Where do you start?

I wouldn't start by writing automation. With only two weeks and real money involved, the first job is to understand the product and find the biggest risks quickly.

**First two days: learn the app and talk to people**
- I'd use the app myself exactly like a new customer would: sign up, verify my identity, add money, buy, sell and withdraw. I'd write down everything that breaks or confuses me. In my experience, this first hands-on session always finds real bugs, and it gives me the first bug list for the team.
- I'd talk to the product owner, the developers and customer support. I'd ask: what worries you most? What changed recently? Where have bugs appeared before? Developers usually know which areas are fragile.
- I'd find out what already exists: unit tests, a test environment, test accounts, logs and crash reporting.

**Day three: agree what matters most**
- I'd list the journeys where money moves or trust is at stake: login and 2FA, deposit, buy and sell, balances, withdrawal and prices.
- I'd put them in a simple [risk matrix](RISK_MATRIX.md) (how likely to fail × how bad if it fails) and agree priorities with the team.
- Most importantly, I'd agree with the product owner **what "ready to release" means** before the last week, not during it. For example: "no open critical bugs in any money flow". That's the [release checklist](RELEASE_CHECKLIST.md).

---

## 2. How would you approach testing this app?

I'd use a **risk-based** approach: most of my time goes to the areas that can lose customers' money or their trust.

**Highest priority: money and security**
- **Deposits, buy/sell orders, balances and withdrawals.** I'd write clear test cases with exact expected values. After every trade, the balance must be exactly right. I'd also test the things real users do: tapping "Buy" twice, losing signal in the middle of an order, closing the app during a payment, or not having enough funds.
- **Login, 2FA and sessions.** Wrong passwords, expired sessions, logging in on two phones, and what happens after logout.
- **Prices.** The price shown must match the source and be up to date. In this project I found prices in the website's API that were hours or even days old (BUG-002), so I know this can really happen.

**Next: everything customers use every day**
Onboarding, navigation, portfolio screens and notifications, tested on a small agreed list of real iPhones and Android phones, including older models and small screens.

**How I'd test**
- **Exploratory testing** every day on new builds. With no documentation, it's the fastest way to find important bugs.
- **Written test cases** for the critical journeys, so they're repeatable and anyone in the team can run them.
- **API testing** for the money logic. Checking the back end directly is faster and more precise than going through the screens.
- **A small automated smoke suite** for the critical journeys, like the one in this repository, running on every build. I wouldn't try to automate everything in two weeks.
- **Real-world conditions:** slow or no network, phone calls interrupting the app, the app in the background, and updating from an older version.

Every bug gets clear steps, expected and actual results, the device and OS, and evidence (a screenshot or video), so developers can fix it quickly.

---

## 3. What does QA look like inside a sprint, from ticket creation through to regression?

QA should be involved from the start of every ticket, not only at the end. Finding a problem in a ticket description is much cheaper than finding it in the app.

1. **Ticket creation and refinement.** I read the story before development starts and ask "how will we know this works?" I help write clear acceptance criteria, including the unhappy paths, for example "what happens if the payment fails?"
2. **Sprint planning.** Testing time is part of the estimate. A story isn't done until it has been tested.
3. **During development.** While the developer builds the feature, I prepare my test cases and test data. I also check which unit tests the developer is adding.
4. **Testing the story.** When the build is ready, I test against the acceptance criteria and then explore around the feature to find what wasn't thought of.
5. **Bugs and retesting.** I log bugs with clear evidence, retest fixes, and check nearby features for side effects.
6. **Automation.** The important, stable checks from the story are added to the automated suite, so the regression suite grows a little every sprint.
7. **Regression.** Before release, the automated suite runs in CI on every build, and I do a focused manual regression of the critical journeys on real devices.
8. **Sprint review and retro.** I share what we learned about quality, like where bugs came from and which ones escaped, so the whole team can improve.

---

## 4. What does your ideal regression suite look like?

- **Focused on risk, not size.** Every test is there for a reason. Money flows, login and prices are always covered. I'd rather have 50 reliable tests than 500 that nobody trusts. In this project I kept to 24 tests that cover every requirement.
- **Layered.** Many fast unit tests (written by developers), a good set of API tests for business rules and money logic, and only a small number of end-to-end UI tests for the most important journeys.
- **Two levels:**
  - a **smoke suite** that runs in minutes on every build ("can users log in, see prices and place an order?")
  - a **full regression** that runs every night and before every release.
- **Automated in CI**, with a clear report and evidence (screenshots, logs) for every failure, so anyone in the team can see what went wrong.
- **Stable.** No fixed waits, tests that don't depend on each other, and good test data. When a test is flaky, I find the real cause and fix it quickly. While building this project I found flaky results caused by slow loading, a network problem and regional differences, and I fixed the cause each time instead of just re-running.
- **Honest about known bugs.** Known bugs stay visible in the report, the way I use `xfail` in this project, instead of being deleted or hidden.
- **Traceable and maintained.** Each test links to a requirement or risk, and the suite is reviewed every sprint: new features add tests, and removed features remove them.
- **Plus a short manual checklist** on real devices for what automation can't judge well, like how the app looks and feels, real payment cards, and installing from the app store.

---

## 5. What would keep you up at night about this app and releasing it to the public?

1. **Money being wrong.** A balance that doesn't update, a double charge after tapping twice, an order filled at a different price than shown, or a withdrawal that leaves the account but never arrives. With real money, one of these bugs can lose customers' trust and cause problems with the regulator.
2. **Wrong or old prices.** Customers make decisions on the number they see. I've already seen stale prices in this company's website data, so I'd check this carefully in the app too.
3. **Security.** Someone getting into another person's account, 2FA that can be skipped, or personal and identity documents being exposed.
4. **No safety net.** With no test suite and fast shipping, nobody knows what's already broken. A mobile app also can't be rolled back instantly: users have to update from the app store, and store review takes time. I'd want a way to switch off risky features from the server, crash monitoring from day one, and a staged rollout to a small group of users first.
5. **Real life is messier than testing.** Weak mobile signal, old phones, the app being closed in the middle of a payment, and many users at once on launch day.
6. **Regulation.** Risk warnings, terms and complaint information must be shown correctly for each country. On the website I found the 404 page showing another country's company details (BUG-005), so I'd check this in the app as well.

**What I'd do about it:** spend the two weeks on these risks first, agree clear go / no-go criteria with the team, release gradually, and make sure monitoring, customer support and an on-call plan are ready on launch day.
