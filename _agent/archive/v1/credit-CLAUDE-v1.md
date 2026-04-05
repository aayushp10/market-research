# Credit World — Agent Instructions

This file extends the root `CLAUDE.md` with rules specific to the credit world (IG, HY, crossover, distressed). Read this when ingesting or updating content in `credit/`.

## Scope

The credit world covers:
- Public IG issuers
- Public HY issuers
- Crossover and fallen-angel candidates
- Distressed and restructuring situations
- Sector-level credit analysis
- New issue analysis
- Event-driven credit (M&A, LBO, spin-offs, ratings actions)

Not in scope here (routes to other worlds):
- BDCs and private credit vehicles → `bdc/`
- Pure macro (rates, FX, commodities, Fed policy) → `shared/macro/`
- Masters and frameworks → `shared/frameworks/`
- Technical reference material → `shared/concepts/`

## Issuer classification

When ingesting a new issuer, classify it in YAML frontmatter:

```yaml
ticker: FLO
name: Flowers Foods Inc
sector: food-producers
sub_sector: bakery
rating_sp: BBB-
rating_moodys: Baa3
rating_fitch: BBB-
rating_status: stable      # stable | negative | positive | watch
status: ig | hy | crossover | distressed
coverage_priority: core | secondary | monitoring
last_updated: 2026-04-04
```

**Status rules:**
- `ig`: rated BBB- or higher across all three, not on negative watch for downgrade.
- `hy`: rated BB+ or lower across all three.
- `crossover`: split ratings spanning the IG/HY boundary, OR IG rating with negative watch that could trip it to HY, OR HY rating with positive watch toward upgrade. This is the most interesting bucket and deserves extra attention.
- `distressed`: trading materially distressed (spread >1000 over treasury, or restructuring in progress).

**Coverage priority:**
- `core`: names Aayush actively has views on and trades. Day-1 list: ORCL, DOW, FLO, KDP, JPM, OBDC, OTF.
- `secondary`: names in the broader research universe, updated when sources land but not proactively chased.
- `monitoring`: names on the watch list for a specific catalyst (e.g., rating action, earnings).

## Issuer page template

Use `_templates/issuer-credit.md` as the starting point. Every issuer page has these sections, populated based on status:

- **Snapshot** — current spreads, rating, key fundamentals. Updated on every touch.
- **Cap structure** — relevant for HY/crossover/distressed. Lines, seniority, covenants.
- **Recent developments** — dated bullets with raw source citations, most recent on top.
- **Sources** — list of `_raw/credit/` files that have contributed to this page.

IG-specific issuer pages emphasize curve/factor positioning, new issue concessions, and index inclusion. HY-specific pages emphasize cap structure, refinancing walls, covenants, and recovery. Crossover pages get BOTH treatments.

## Sector pages

Sector pages aggregate issuers and hold the sector-level view. Template in `_templates/sector.md`.

Day-1 sectors (create on first substantive ingest, not upfront):
- `technology-ig.md`
- `banks-big-6.md`
- `life-insurers.md`
- `food-producers.md` (for FLO and KDP)
- `chemicals-ig.md` (for DOW)
- `energy-ig-subsectors.md` (integrated, E&P, refiners, gas pipes — per energy decomposition rule in root CLAUDE.md)

Sector pages are where relative value lives. When updating an issuer page, ask whether the update has sector-level implications and update the sector page too.

## The universe reference

`credit/universe/` holds the IG sector map as a reference document. It catalogs 276 issuers across 15 mega-sectors as context for how names map to sectors and what comparables exist. This is NOT a deep-dive layer — most of those names never get their own page unless Aayush does work on them.

When ingesting a new name, consult the universe reference to:
1. Identify which sector the name belongs to.
2. Find the comparable names already covered.
3. Decide whether the new name warrants a full issuer page or just a mention on an existing sector page.

## Situations

`credit/situations/` holds dated theses on specific names or events. A situation is created when Aayush wants to track a specific setup or idea that doesn't belong on an issuer page (because it's a view, not a fact, and would violate the firewall).

Situation filename format: `YYYY-MM-DD-{name}-{thesis-short}.md`
- `2026-04-04-flo-fallen-angel.md`
- `2026-03-20-energy-hy-refiner-crack.md`

Situations are always dated, always have kill criteria, and get scored when they resolve. They're the credit-world equivalent of setups, but more developed — a setup becomes a situation when it graduates from "watching" to "positioned view."

## Rules specific to this world

- When ingesting a new issue announcement, create a brief entry on the issuer page under "recent developments" with the key terms (size, tenor, coupon, concession). Do not rewrite the snapshot unless the deal materially changes the cap structure.
- When a rating action lands, touch the issuer page AND the sector page (sector pages track rating distribution).
- Fallen angel candidates are a priority focus — if a source signals IG → HY migration risk, flag it clearly in the daily briefing even if the name isn't in Aayush's core coverage.
- When updating a crossover name, always ask whether the update should propagate to the IG sector page, the HY sector page, or both.
