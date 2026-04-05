---
ticker: TICKER
name: Full BDC Name
sponsor: sponsor-slug
structure: public | non-traded | semi-liquid | bdc-fund
rating_sp: BBB-
rating_moodys: Baa3
rating_fitch: BBB-
nav_per_share: 0.00
price_nav_ratio: 0.00
non_accrual_rate_pct: 0.0
pik_ratio_pct: 0.0
nii_coverage: 0.00
leverage_d_to_e: 0.00
sector_concentration_top: software, healthcare, business-services
coverage_priority: core | secondary | monitoring
tags:
  - issuer
  - bdc/{public|non-traded|semi-liquid}
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# {TICKER} — {Full Name}

> One-sentence description: sponsor, structure (public/non-traded), strategy focus, and why it's in coverage.

## Snapshot

*Updated every touch. Current state only.*

- **NAV per share:** current, trajectory (QoQ, YoY).
- **Price/NAV:** current premium or discount. For public BDCs only; non-traded always trade at NAV by construction.
- **Non-accrual rate:** % of portfolio, current and 2-quarter trend.
- **PIK ratio:** % of total income paid in kind. Flag if >10% or accelerating.
- **NII coverage of distribution:** current quarter. Flag if <1.0x or trending down.
- **Leverage:** debt-to-equity, regulatory cap 2.0x. Headroom commentary if near cap.
- **Sector concentration:** top 3 portfolio sectors by fair value %.
- **Unsecured notes:** outstanding tranches, OAS, recent spread move. This is the tradeable expression.

## Portfolio characteristics

- Total investments at fair value
- Number of portfolio companies
- Weighted average yield
- Floating vs. fixed
- Senior secured % of portfolio
- Sector breakdown (top 10)
- Top 10 investments by size
- Vintage composition (origination year buckets — important for mark reliability)

## Liability stack

*Critical for BDC unsecured note analysis since this is where Aayush trades.*

- Senior secured revolver: size, drawn, rate, maturity
- SBIC debentures: size, rate, maturity (if applicable)
- Unsecured notes: list every tranche with coupon, maturity, size, OAS
- Maturity ladder visualization
- Refinancing risk commentary

## Sponsor context

- Sponsor: full name, AUM, BDC family (if multiple vehicles)
- Sibling vehicles: any non-traded BDCs from the same sponsor? Link to them.
- Sponsor stress events: any gating, redemption issues, reputational events. Critical read-across channel.

See [[bdc/segments/bdc-unsecured-notes]] for the complex-level view.

## Recent developments

*Dated bullets with raw source citations, most recent first.*

- **2026-04-04:** ... Citation: `_raw/bdc/source-file.md`
- **2026-03-15:** ...

## Mark validation notes

*Specific to BDCs. Track the quality and staleness of Level 3 marks.*

- Last third-party mark validation date
- Any methodology notes or concerns
- Vintage skew (are the oldest vintages in the book representing stale marks?)
- Any discrepancies between similar names held by other BDCs

## Open questions

- Question 1
- Question 2

## Sources

- `_raw/bdc/source-file-YYYY-MM-DD.md` — contribution summary
- ...

## Views

- [[bdc/situations/YYYY-MM-DD-ticker-thesis-name]] — dated thesis

---

**Template notes (delete when instantiating):**

1. Non-traded BDCs get additional tracking around tender windows and redemption cycles. Add a "Redemption history" section to the snapshot for non-traded vehicles.
2. Public BDCs get more attention to Price/NAV and equity market signals. Add an "Equity signals" section if relevant.
3. When a sponsor stress event hits (like Blue Owl 2026-04-02), every BDC from that sponsor gets a touch, even if structurally immune (public BDCs). Note what channel the read-across runs through.
4. Sector concentration is critical — software exposure was the specific driver of the 2026 Q1 Blue Owl tech BDC bleed. Track changes in top sectors quarterly.
5. PIK ratio and NII coverage are the two most important leading indicators of BDC stress. Watch for acceleration.
