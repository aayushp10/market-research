# Credit Research Wiki

Personal credit research knowledge base. Inspired by Karpathy's LLM Wiki pattern. Local files, git-tracked, Obsidian-native, LLM-maintained.

## What this is

A persistent, compounding research artifact for credit markets. An LLM agent ingests sources (articles, research, desk notes, PDFs), integrates them into structured wiki pages, runs a daily market briefing, and maintains a live list of tradeable setups. You curate sources, direct analysis, and hold views. The agent does the bookkeeping.

## How it's organized

```
research/
├── CLAUDE.md              ← Universal rules (agent reads this first)
├── README.md              ← This file
├── index.md               ← Catalog of all wiki pages
├── log.md                 ← Chronological record of every session
│
├── _raw/                  ← Immutable source documents
│   ├── inbox/             ← Drop new sources here; agent processes and moves them
│   ├── credit/            ← Permanent home for credit sources
│   ├── bdc/               ← Permanent home for BDC sources
│   └── shared/            ← Permanent home for macro/cross-cutting sources
│
├── _templates/            ← Page templates the agent uses when creating new pages
│
├── credit/                ← IG / HY / crossover world
│   ├── CLAUDE.md          ← Credit-world-specific rules (templates, classification)
│   ├── issuers/           ← One page per researched name (ORCL, FLO, JPM, ...)
│   ├── sectors/           ← Sector pages (banks-big-6, life-insurers, technology, ...)
│   ├── universe/          ← IG sector map as reference (for classification help)
│   └── situations/        ← Dated theses on specific names or events
│
├── bdc/                   ← BDC / private credit complex world
│   ├── CLAUDE.md          ← BDC-world-specific rules (different primitives)
│   ├── issuers/           ← OBDC, OTF, ARCC, BXSL, ...
│   ├── segments/          ← bdc-unsecured, pe-holdco, pe-insurance-sub
│   └── situations/
│
└── shared/                ← Cross-world layer
    ├── frameworks/        ← Masters (Marks, Klarman, Fridson, ...)
    ├── concepts/          ← Technical references (CDX mechanics, mark staleness, ...)
    └── macro/
        ├── briefing-scope.md  ← Agent's standing instructions on what's in scope
        ├── setups.md          ← Live curated list of tradeable setups
        ├── daily/             ← Morning briefings, append-only
        ├── state/             ← Monthly regime snapshots, never overwritten
        └── events/            ← Discrete shock analyses (Iran, Fed events, ...)
```

## How to use it

### Morning (15 minutes, most days)

1. Drop any overnight sources (PDFs, clipped articles, links) into `_raw/inbox/`.
2. Agent runs automatically: reads scope, reads inbox, searches the web, drafts `shared/macro/daily/YYYY-MM-DD.md` as an unreviewed draft.
3. Open the draft. Read it. Mark up what's wrong, missing, or noise.
4. Rule on any proposed setup updates in the draft. Accept, reject, or modify.
5. Agent finalizes: updates setups.md, touches affected issuer/sector pages, commits to git.

### When sources arrive ad-hoc

Drop them in `_raw/inbox/` anytime. Next agent session processes them, either into the daily briefing or as a standalone ingest.

### When you want to dig

Ask the agent anything. It searches the wiki, pulls relevant pages, synthesizes an answer with citations. Good answers can be filed back as new wiki pages so they compound.

### Weekly (30–45 min, Friday afternoon)

Review the week's dailies. Agent generates a weekly rollup: what setups moved, what got promoted to state, what you may have missed. This is the calibration loop.

### Monthly (1 hour)

Lint pass. Fresh agent session reads the wiki with no context and flags: claims without raw sources, stale pages, contradictions, orphans, setups to score. This is the epistemic hygiene loop.

## What's here today (day 1)

- Rules and schema (`CLAUDE.md` files)
- Initial briefing scope reflecting your day-1 coverage list
- One live setup (BDC unsecured decompression) from the 2026-04-04 prototype briefing
- One finalized daily briefing (`shared/macro/daily/2026-04-04.md`)
- Page templates for credit issuers, BDC issuers, and sectors
- Empty folders for everything else — they'll grow with use

## What's NOT here yet

- Any actual issuer pages. These get created as you do real work.
- Any sector pages. Same.
- Frameworks (Marks, Klarman, etc.), concepts (CDX mechanics, etc.). Same.
- The IG sector map reference. Drop your existing sector map file into `credit/universe/` and the agent will use it.
- A built IG/HY decompression metric (flagged in the 2026-04-04 Gaps section).

The vault grows with use. The goal is not to front-load scaffolding — it's to build the structure that matches how you actually work, one ingest at a time.

## Principles (the non-negotiables)

1. **Wiki pages are never evidence.** Only raw sources are evidence. The agent cannot cite one wiki page as support for a claim on another wiki page.
2. **Facts and views are separated.** Issuer and sector pages are facts layer. "View" pages are your thesis layer. They never mix.
3. **Provenance is mandatory.** Every claim traces to a specific raw file.
4. **Disagreement is preserved, not smoothed.** When sources disagree, the disagreement is documented, not blended.
5. **The wiki should make it easy to disbelieve itself.** Every mechanism — reviewed flags, cold-read lint, setup scoring — exists so the wiki tells you when it's wrong.

See `CLAUDE.md` for the full rules.
