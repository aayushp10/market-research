# BDC / Private Credit World — Agent Instructions

This file extends the root `CLAUDE.md` with rules specific to the BDC and private credit complex world. Read this when ingesting or updating content in `bdc/`.

## Scope

This world covers:
- Public BDCs (OBDC, OTF, ARCC, BXSL, MAIN, etc.)
- Non-traded BDCs (OTIC, OCIC, BCRED, CCLFX, etc.)
- BDC managers as credit counterparties (OWL, ARES, KKR, BX, APO, CG, BAM, TPG — specifically their BDC sponsor roles)
- BDC unsecured notes complex (Aayush's private credit complex trading book thesis)
- PE holdco paper (where it trades with BDC-adjacent characteristics)
- PE-affiliated insurance sub debt (life insurers heavy into private credit)
- Private credit stress events, gating, redemption cycles

Not in scope here (routes to credit world):
- Public HY/IG issuers that happen to have private credit exposure but aren't primarily BDC-related.
- PE holdcos where the analysis is purely about their equity/credit as operating companies, not as BDC sponsors.
- Traditional HY distressed names held by BDCs (analyze the name in `credit/`, link from BDC holdings pages).

## Different primitives

BDC analysis is a genuinely different vocabulary from public credit. The analytical lens and templates reflect that:

**BDC-specific fields that don't apply to public credit:**
- NAV and NAV/share trajectory
- Price/NAV (premium or discount)
- Non-accruals (current count, trend, sector concentration)
- PIK ratio (payment-in-kind interest as % of total income)
- NII coverage of distribution
- Leverage (debt-to-equity, regulatory cap 2.0x)
- Fee structure (management fee, incentive fee, hurdle, high water mark)
- Spillover income (prior-year earnings carried forward for distribution)
- Mark staleness (how old are the Level 3 valuations driving NAV)
- Sector concentration in the portfolio (software, healthcare, business services)
- Liability stack (SBIC debentures, unsecured notes, revolver draws)
- Maturity walls and refinancing risk on the BDC's own debt

**Public-credit fields that still apply:**
- Spreads on the BDC's unsecured notes (this is where Aayush's trading sits)
- Rating actions on the BDC
- New issue analysis for BDC unsecured notes
- Liquidity and trading characteristics of the unsecured complex

## Issuer classification

YAML frontmatter for a BDC issuer page:

```yaml
ticker: OBDC
name: Blue Owl Capital Corp
sponsor: blue-owl
structure: public           # public | non-traded | semi-liquid | bdc-fund
rating_sp: BBB-
rating_moodys: Baa3
rating_fitch: BBB-
nav_per_share: 15.10
price_nav_ratio: 0.93
non_accrual_rate: 1.8
pik_ratio: 8.2
nii_coverage: 1.02
sector_concentration_top: software, healthcare, business-services
coverage_priority: core | secondary | monitoring
last_updated: 2026-04-04
```

**Structure field** distinguishes:
- `public`: exchange-traded, no redemption gating risk (OBDC, OTF, ARCC, BXSL, MAIN).
- `non-traded`: gateable, quarterly tender offers, subject to redemption cycles (OTIC, OCIC, BCRED, NCDL).
- `semi-liquid`: intermittent liquidity, typically monthly or quarterly (CCLFX).
- `bdc-fund`: BDC-focused funds or ETFs.

This is critical because the analytical questions differ sharply — gating risk doesn't exist for public BDCs but dominates non-traded analysis.

## The private credit complex segments

`bdc/segments/` holds pages for cross-issuer thematic analysis that doesn't fit on any single BDC page:

- `bdc-unsecured-notes.md` — the HY-market complex of BDC unsecured notes, where Aayush's trading sits.
- `pe-holdco-paper.md` — BX, APO, KKR, ARES, OWL, CG, BAM, TPG as credit issuers of holdco paper that trades in IG/HY spread markets.
- `pe-insurance-sub.md` — life insurers affiliated with PE/alt managers, their sub debt, and private credit asset concentration (Athene/Apollo, Global Atlantic/KKR, F&G/Blackstone, etc.).

These segment pages are where the private credit complex trading book thesis lives. They're the clearest examples of the seam between this world and the credit world — every segment page links heavily to names in `credit/` (BX the equity, APO the equity) or to specific insurance issuer pages.

## Non-traded BDC stress tracking

Non-traded BDCs are subject to redemption cycles that public BDCs don't face. Track these explicitly:

- **Quarterly tender offers:** scheduled redemption windows with a stated cap (typically 5% of NAV).
- **Gate events:** when tender requests exceed the cap and the manager limits redemptions.
- **Tender at discount:** when third parties (Saba, Cox, etc.) offer to buy shares from locked-up holders at a discount.

When a gate event or historic-level tender lands, it's almost always material enough for the daily briefing AND a touch on affected BDC issuer pages AND a touch on the `bdc-unsecured-notes.md` segment page. The 2026-04-04 Blue Owl event is the archetype.

## Read-across rules

When a non-traded BDC sponsored by a given manager hits stress, check the public BDC from the same sponsor:
- OTIC/OCIC stress → check OBDC (same sponsor, Blue Owl)
- BCRED stress → check BXSL (same sponsor, Blackstone)
- ARCC never had non-traded issues, but their sponsor Ares has non-traded funds worth watching.

The transmission is NOT automatic — public BDCs are structurally immune to redemption gating. But:
1. Sponsor-brand contagion is real in the unsecured note market.
2. The underlying portfolio exposure thesis (e.g., software/AI concentration) may apply to both.
3. NAV methodology concerns at one vehicle raise questions about the sponsor's marks generally.

When flagging read-across, be explicit about which transmission channel you're invoking (brand, portfolio, methodology) and cite raw sources.

## Situations

`bdc/situations/` holds dated BDC-specific theses. Same format as credit situations. Common situation types:

- NAV stress / mark staleness theses
- Non-accrual migration theses
- Dividend coverage / cut risk theses
- BDC unsecured note RV theses (these are the most actionable for Aayush's trading)
- Private credit complex seam theses (bridging to credit world names)

## Rules specific to this world

- Every BDC issuer touch should check whether it warrants an update to `bdc/segments/bdc-unsecured-notes.md` — this segment page is the trading-relevant rollup.
- Never blend non-traded and public BDC analysis into one lens. They're structurally different.
- When a manager press release lands about a non-traded vehicle, DO NOT assume symmetric read-through to the public vehicle without evidence. Check sponsor-brand contagion at the unsecured note level (this is the actual transmission channel for Aayush's trading).
- PE holdco paper (BX, APO, etc.) analyzed here is about the credit issuance; the same entities as operating/equity stories belong in `credit/` or not in the wiki at all.
