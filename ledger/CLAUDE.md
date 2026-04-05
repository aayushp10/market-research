# Ledger — Folder Rules

Read the root `CLAUDE.md` first; this file extends it with folder-specific rules for the prediction ledger.

---

## Purpose

`ledger/` is the scoreboard. It holds falsifiable predictions graded against reality. The ledger's job is honest calibration: what did Aayush predict, what actually happened, and what does the pattern say about where his edge is and isn't.

---

## Folder structure

```
ledger/
├── CLAUDE.md        ← this file
├── _index/          ← system-generated rollups (never hand-edit)
├── open/            ← live predictions awaiting resolution
├── resolved/        ← graded predictions, organized by domain
│   ├── credit/
│   │   ├── issuers/
│   │   ├── sectors/
│   │   ├── markets/
│   │   ├── themes/
│   │   └── special-situations/
│   └── macro/
│       ├── narrative/
│       ├── credit/
│       ├── rates/
│       ├── equities/
│       └── commodities/
└── reviews/         ← monthly review ritual outputs
```

The `resolved/` substructure mirrors `research/` exactly so retrieval scopes translate cleanly.

---

## Promotion-only discipline

This is a protected rule (see root CLAUDE.md). Ledger entries are NEVER written directly.

Every entry originates from one of:
- A journal entry (most common — Aayush logs a prediction in `#journal`)
- A research artifact (a deep dive concludes with a falsifiable view)
- A briefing (the `## Setups` or `## Dig` section contains a prediction)

And arrives in the ledger via the inference-review pattern:
1. A promotion agent detects the falsifiable prediction in the source.
2. The agent drafts a ledger entry with inferred fields.
3. The proposal posts to `#ledger` for Aayush's confirmation.
4. On confirmation, the entry is filed to `ledger/open/`.

---

## Entry frontmatter — open entries (required)

```yaml
predicted_date: 2026-04-05           # REQUIRED — when the prediction was made
revisit_date: 2026-04-15             # REQUIRED — when to check the outcome
prediction: "OBDC unsecured tightens 15bps by mid-April on mark staleness clearing"  # REQUIRED
confidence: medium                    # REQUIRED — low | medium | high
source: "[[journal/entries/2026-04-05-obdc-long-entry]]"  # REQUIRED — wikilink to originating artifact
domain_path: credit/issuers           # REQUIRED — where this lives in resolved/ after grading
tickers: [OBDC]                       # REQUIRED — can be empty list
sectors: [bdc-unsecured]              # REQUIRED — can be empty list
tags: [mark-staleness, spread-compression]  # REQUIRED
```

---

## Resolution fields (added on resolve)

When an open entry is resolved, these fields are added to the frontmatter:

```yaml
resolved_date: 2026-04-16
outcome: played_out                   # played_out | partial | wrong | expired | canceled
delta: "OBDC tightened 18bps, exceeding the 15bps target. Mark staleness did clear as expected."
lessons: "Mark staleness clearing is a stronger catalyst than expected when combined with quarterly reporting."
promoted_to_post_mortem: false        # true if this resolution led to a training post-mortem
```

### Outcome vocabulary (closed)

- **`played_out`** — the prediction materialized substantially as described
- **`partial`** — the direction was right but the magnitude or timing was materially off
- **`wrong`** — the prediction did not materialize or went the opposite direction
- **`expired`** — the revisit date passed without a clear resolution; the prediction became stale
- **`canceled`** — the setup conditions changed enough that the prediction is no longer testable

### Resolution flow

1. The revisit-date watcher (daily, early morning) scans `ledger/open/` for entries past their `revisit_date`.
2. For each overdue entry, the agent pulls current market data via web search.
3. The agent drafts a resolution proposal with inferred `outcome` and `delta`.
4. `lessons` is ALWAYS marked `[needs input]` — only Aayush can say what he learned.
5. The proposal posts to `#ledger` in a thread.
6. Aayush confirms or corrects. The `lessons` field is the key input.
7. On confirmation, the entry moves from `open/` to `resolved/<domain_path>/`.

---

## Backfill flag

For predictions that existed before the v2 ledger was built (e.g., the v1 setups that migrated), entries SHOULD be tagged:

```yaml
backfilled: true
backfilled_date: 2026-04-05
```

This ensures backfilled entries are honestly distinguishable from natively-recorded predictions in calibration analysis.

---

## Monthly review ritual

Trigger: manual via `/review` in `#ledger`, or scheduled on the first Monday of each month.

### Review steps

1. Agent reads `ledger/resolved/` entries since the last review (or last 30 days if no prior review).
2. Computes aggregate stats: total resolved, outcome breakdown, win rate by domain, win rate by confidence level.
3. Identifies patterns: repeated misses in a specific area, systematic over/underconfidence, themes that played out well.
4. Drafts a review document at `ledger/reviews/<YYYY-MM>-review.md`.
5. Posts the draft to `#ledger` in a thread.
6. Aayush reviews and confirms or edits each proposed post-mortem promotion.
7. On confirmation, each approved post-mortem promotion produces a new file in `training/post-mortems/` via the training ingestion flow (full inference-review for each post-mortem).

### Post-mortem promotion criteria

Not every resolved entry deserves a post-mortem. Promote ONLY when:
- The resolution revealed a **methodological** insight (not just a situational one)
- The insight would change how a playbook is executed or how a framework is applied
- The pattern recurs across multiple entries (a single miss is data, a pattern is signal)

### Review document frontmatter

```yaml
review_period: 2026-04
entries_reviewed: 12
outcomes:
  played_out: 5
  partial: 3
  wrong: 2
  expired: 1
  canceled: 1
post_mortems_proposed: 2
post_mortems_approved: 1
```

---

## Commands in `#ledger`

- `/open` — list all open predictions, sorted by revisit date
- `/resolved <filter>` — list resolved entries; filter by ticker, sector, date range, outcome
- `/review` — kick off the monthly review ritual
- `/ledger <wikilink>` — show a specific entry

---

## Things specific to this folder you must never do

- Write directly to `ledger/open/` or `ledger/resolved/` without going through promotion or resolution flows.
- Hand-edit files in `_index/`.
- Mark `lessons` as `[inferred]` — it is ALWAYS `[needs input]` because only Aayush knows what he learned.
- Skip the inference-review pattern for promotions or resolutions.
- Promote every resolved entry to a post-mortem. Most don't warrant it.
- Use outcome values not in the closed vocabulary.
- Ad-hoc promote from ledger to training outside the monthly review ritual (this skips the calibration step).
