# Research — Folder Rules

Read the root `CLAUDE.md` first; this file extends it with folder-specific rules for the research area.

---

## Purpose

`research/` holds working research: raw sources, work products (issuer pages, sector pages, deep dives, situations, themes), macro state tracking, and daily briefings. This is where the vault's day-to-day analytical work lives.

---

## Retrieval scoping

Agents doing analysis in `research/` read from:
- `research/` — raw sources, existing work products, macro state
- `concepts/` — concept stubs for wikilink resolution
- The loaded skill — compiled methodology from `training/`

They do NOT retrieve from `training/` directly. The loaded skill is the interface to training content. Reaching into `training/` bypasses the compile pipeline's weighting and synthesis — that's a discipline violation.

---

## Raw source rules

### Immutability

Files in `research/_raw/` MUST NOT be moved, edited, renamed, or reorganized after filing. They are the audit trail. If a raw source needs correction or supersession, file a new source alongside it with a newer `as_of_date`.

### Ingestion flow

1. Files arrive in `research/_raw/inbox/to-tag/` via file drops in `#research`.
2. Every file goes through the inference-review pattern before moving to a content folder.
3. On confirmation, files move: `to-tag/` → `to-file/` → final subfolder in `_raw/`.

### Raw source frontmatter (required)

```yaml
source_type: research_report    # REQUIRED — closed vocabulary, see below
source_name: "Citi IG Snapshot" # REQUIRED — human-readable name
date_added: 2026-04-05          # REQUIRED — when added to vault
as_of_date: 2026-04-03          # REQUIRED — when the data was captured (critical for time-sensitive material)
tags: [ig, spreads, weekly]     # REQUIRED
tickers: [OBDC, OTF]           # REQUIRED — can be empty list []
sectors: [bdc-unsecured]        # REQUIRED — can be empty list []
```

### Raw source frontmatter (optional)

```yaml
publisher: Citi
author: Citi Credit Strategy
supersedes: _raw/credit/markets/older-version.md
paywalled: true
url: https://example.com/article
```

### Source type vocabulary (closed)

`filing`, `earnings_release`, `news_article`, `research_report`, `trace_data`, `market_data`, `press_release`, `court_doc`, `rating_action`, `transcript`, `web_page`, `other`

### Binary file sidecars

For non-markdown files (PDFs, images, etc.), create a companion `.md` sidecar with the same name containing the frontmatter and a brief description. The sidecar lives next to the binary file.

### Raw subfolder routing

- Credit issuers → `_raw/credit/issuers/`
- Credit sectors → `_raw/credit/sectors/`
- Credit markets (broad credit data, indices, ETFs) → `_raw/credit/markets/`
- Credit themes → `_raw/credit/themes/`
- Credit special situations → `_raw/credit/special-situations/`
- Macro narrative → `_raw/macro/narrative/`
- Macro credit-specific (spreads, flows, ETFs, CDX) → `_raw/macro/credit/`
- Macro equities → `_raw/macro/equities/`
- Macro rates → `_raw/macro/rates/`
- Macro commodities → `_raw/macro/commodities/`
- Macro events → `_raw/macro/events/`
- Briefing-related sources → `_raw/briefings/`

---

## Facts/views firewall

This is the v1 firewall, carried forward and strengthened.

**Facts layer** (no opinions, no "looks cheap"):
- Issuer pages in `credit/issuers/`
- Sector pages in `credit/sectors/`
- Market pages in `credit/markets/`
- Macro state files in `macro/`
- Raw source sidecars

**Views layer** (dated theses with kill criteria):
- Themes in `credit/themes/`
- Special situations in `credit/special-situations/`
- Briefing `## Setups` and `## Dig` sections
- Any content that says "we should," "this looks," or "I expect"

If you find yourself writing view content on a facts page, STOP. Create a separate theme or situation file.

---

## Deep dive agent discipline

When producing a deep dive:

1. Check `research/_raw/` for existing sources first.
2. If insufficient (fewer than 3 relevant files, or all >30 days old), propose web search to Aayush in the thread with specific queries.
3. Fetched web sources go through the full ingestion tagging flow before use. No shortcuts.
4. Every claim in the deep dive cites a specific raw source via wikilink.
5. Concept stubs are created inline for any concept from the loaded skill that the deep dive invokes — wikilink to `concepts/<slug>.md` and create the stub if missing.
6. The deep dive MUST end with `## Confidence and what would change my mind`.

---

## Concept stub invocation

Any time a deep dive, situation, issuer page, or sector page invokes a concept from the loaded skill:

1. Check whether `concepts/<slug>.md` exists.
2. If yes, wikilink to it.
3. If no, create the stub using the template in root CLAUDE.md, then wikilink.
4. Post a brief notification: "Created new concept stub: `[[concept-name]]`." Aayush can review at any time.

Stubs created during research are committed as part of the same operation.

---

## Briefing workflow

Morning briefings land in `research/briefings/` with `status: draft, reviewed: false`.

### Standing context

Read at the start of every briefing run:
- `research/briefing-scope.md` — active coverage, themes, sector sensitivities
- Last 3 daily files in `research/briefings/`
- Current macro state in `research/macro/*`

### Skip-day protection

If a daily file exists with `status: draft` and `reviewed: false` that is more than 24 hours old:
- Do NOT promote it to final.
- Do NOT update any wiki content based on it.
- It stays as a record of what was seen that day.

Next morning Aayush engages after a skip:
- Ask whether to batch-review skipped drafts or move on.
- For 1–2 day gaps, batch review is usually fast.
- For longer gaps, default to moving on.

### Briefing scope amendments

`research/briefing-scope.md` is the standing instructions for the briefing agent. Amendments are propose-and-approve via Slack — agents MUST NOT edit briefing-scope.md directly.

---

## Macro substructure

The `research/macro/` tree tracks macro state across domains:

- `macro/narrative/` — regime-level narrative snapshots, dated
- `macro/credit/spreads/` — credit spread state snapshots
- `macro/credit/flows/` — ETF and fund flow data
- `macro/credit/etfs/` — ETF-specific analysis
- `macro/credit/cdx/` — CDX index analysis
- `macro/equities/` — equity market context relevant to credit
- `macro/rates/` — rates, curve shape, Fed path
- `macro/commodities/` — oil, gas, other commodities
- `macro/events/` — discrete shock analyses (Iran, Fed events, tariff events)

Briefing agents update the relevant subfolders with dated snapshots of what they covered. The macro layer grows over time — it's not just the briefings folder.

---

## Templates

Templates live in `research/_templates/`. Use these when creating new pages:

- `issuer-credit.md` — for IG/HY/crossover credit issuers
- `issuer-bdc.md` — for BDC issuers (public, non-traded, semi-liquid)
- `sector.md` — for sector-level pages

Templates are updated via the rule evolution flow, not directly edited by agents during tasks.

---

## Things specific to this folder you must never do

- Read from `training/` during research tasks (use the loaded skill).
- Edit or move files in `_raw/` after they've been filed.
- Edit `briefing-scope.md` directly (propose-and-approve only).
- Write view content on issuer or sector pages.
- Promote a stale draft (>24h, unreviewed) to final.
- Use a raw source in research without it being fully tagged and filed first.
