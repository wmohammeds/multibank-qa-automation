# Release Readiness Checklist

Used at the **go / no-go** meeting before the first public release of the mobile trading app (Task 2).
Every item needs an owner and a ✅ or a documented, accepted risk.

## 1. Quality
- [ ] No open **Critical** bugs
- [ ] All **High** bugs fixed, or accepted in writing by the product owner
- [ ] All P1 journeys pass on the release candidate build: sign up, login + 2FA, KYC, deposit, buy, sell, withdraw, balances, prices
- [ ] Full regression run completed on the release candidate; results shared
- [ ] Automated smoke suite green in CI on the release candidate
- [ ] Known issues listed, with workarounds for support

## 2. Money and data
- [ ] Balances reconcile between the app and the back end after test trades
- [ ] Duplicate orders/payments prevented (double tap, retry, network drop)
- [ ] Prices match the price source and update on time; stale prices are clearly shown
- [ ] Fees and limits displayed and applied correctly

## 3. Security and compliance
- [ ] Session timeout, logout and 2FA verified
- [ ] No sensitive data in logs, screenshots or notifications
- [ ] Risk warnings, terms and privacy policy shown and linked
- [ ] Compliance team sign-off

## 4. Devices and conditions
- [ ] Tested on the agreed iOS and Android device and OS list
- [ ] Tested on slow network, offline and switching networks
- [ ] Interruptions tested: phone call, app in background, app killed mid-transaction
- [ ] Fresh install and upgrade from the previous build tested

## 5. Release and operations
- [ ] App Store and Google Play listings, screenshots and age rating approved
- [ ] Crash reporting and monitoring dashboards live, with alerts
- [ ] Feature flags / kill switch in place for risky features
- [ ] Staged rollout plan agreed (for example 5% → 25% → 100%)
- [ ] Rollback / hotfix process agreed; on-call people named for launch day
- [ ] Customer support briefed: known issues, FAQs, escalation route

## 6. Post-release (first 48 hours)
- [ ] Smoke test in production with an internal account (small real deposit and withdrawal)
- [ ] Monitor crashes, failed transactions and support tickets
- [ ] Daily quality check-in with the team

---

**Decision:** ☐ Go ☐ Go with accepted risks ☐ No-go

**Signed off by:** QA ______ Product ______ Engineering ______ Compliance ______ **Date:** ______
