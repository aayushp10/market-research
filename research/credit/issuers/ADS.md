---
ticker: ADS
name: Apollo Debt Solutions BDC
sponsor: apollo
structure: non-traded
coverage_priority: secondary
status: stub
refresh_priority: high
tags: [issuer, bdc/non-traded, apollo, stub]
origin: seeded-from-prior-conversations
seeded_date: 2026-04-05
created: 2026-04-05
last_updated: 2026-04-05
---

# Apollo Debt Solutions BDC (ADS)

> **Stub file** -- seeded from prior conversation notes. Low fidelity. Needs full refresh against primary sources before any claims here are actionable.

## Overview

Apollo Debt Solutions BDC is a non-traded BDC managed by Apollo Global Management. Coverage priority is secondary, but refresh priority is high given recent facility activity and NAV trajectory. [from prior conversation -- no raw source available]

## Reporting Cadence

- Monthly 8-K filings, typically on the **23rd of each month**. [from prior conversation -- no raw source available]
- This cadence makes ADS one of the more transparent non-traded BDCs in terms of NAV reporting frequency.

## NAV Trajectory

Recent NAV per share readings show a modest but persistent downward drift:

| Period | NAV / Share |
|--------|-------------|
| T-2    | $24.86      |
| T-1    | $24.44      |
| T-0    | $24.40      |

[from prior conversation -- no raw source available]

The trajectory is shallow but directional. Need to determine whether the decline is driven by realized losses, unrealized marks, or distribution policy exceeding NII. Cannot assess without full data pull.

## Recent Facility Activity

Two credit facilities flagged in prior conversations:

1. **Grouse Funding LLC** -- facility with **Goldman Sachs**. [from prior conversation -- no raw source available]
2. **Bald Eagle Funding LLC** -- facility with **Bank of America + Citi**. [from prior conversation -- no raw source available]

Details on facility size, pricing, advance rates, covenants, and maturity are not yet captured. These SPV names suggest standard BDC warehouse/leverage structures.

## What We Do NOT Have

This stub is missing critical analytical components:

- **Full portfolio composition** -- sector, issuer, and position-level detail
- **Fee structure** -- management fee, incentive fee, fee waivers, total expense ratio
- **Non-accrual trajectory** -- current non-accruals as % of portfolio, trend over time
- **NII / distribution coverage** -- net investment income vs. declared distributions, spillover income
- **Software exposure** -- % of portfolio in software/SaaS credits (relevant for current cycle positioning)
- **Redemption data** -- tender offer history, pricing, completion rates, queue dynamics
- **Mark staleness analysis** -- how frequently underlying positions are re-marked, lag vs. traded BDC comps

[from prior conversation -- no raw source available]

## Refresh Plan

1. Pull the most recent **10-K** filing from SEC EDGAR
2. Pull trailing **monthly 8-Ks** (at least 6 months of NAV history)
3. Run the **BDC playbook** analysis framework against ADS filings
4. Build a **BCRED-vs-ADS comparison** (Apollo's two main credit vehicles, traded vs. non-traded, fee/structure/performance delta)
5. Populate all "What We Do NOT Have" items above
6. Upgrade status from `stub` to `draft` once primary source data is incorporated
