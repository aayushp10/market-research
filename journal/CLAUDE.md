# Journal — Folder Rules

Read the root `CLAUDE.md` first; this file extends it with folder-specific rules for the journal.

---

## Purpose

`journal/` is Aayush's in-the-moment thinking log. Fast, append-only, Slack-first. It captures trades, conversations, reading reactions, observations, and anything else worth recording as it happens. The value is in the honest state-of-mind record, not in polished prose.

---

## Folder structure

```
journal/
├── CLAUDE.md     ← this file
├── _index/       ← system-generated rollups (never hand-edit)
└── entries/      ← flat folder of dated entries
```

---

## Append-only discipline

This is a protected rule (see root CLAUDE.md). No substantive edits to journal entries after 24 hours.

- **Within 24 hours:** typo fixes and minor formatting corrections are permitted.
- **After 24 hours:** the entry is frozen. If new information changes the picture, write a NEW entry that links back to the original. Do not edit history.
- **Why this matters:** the journal's calibration value comes from honest capture of what Aayush thought at the time. Retroactive edits destroy that signal.

---

## Entry frontmatter (required)

Every journal entry MUST have:

```yaml
date: 2026-04-05                    # REQUIRED — defaults to today
entry_type: trade                    # REQUIRED — closed vocabulary, see below
tickers: [OBDC, OTF]               # REQUIRED — can be empty list []
sectors: [bdc-unsecured]             # REQUIRED — can be empty list []
tags: [mark-staleness, contagion]    # REQUIRED
links: []                            # REQUIRED — wikilinks to related entries or research artifacts
```

### Entry type vocabulary (closed)

`trade`, `conversation`, `reading`, `observation`, `daily`, `other`

- **`trade`** — a position entry, exit, adjustment, or sizing decision
- **`conversation`** — notes from a conversation with a colleague, trader, salesperson
- **`reading`** — reaction to something read (article, research note, book)
- **`observation`** — a market observation, pattern noticed, or hypothesis forming
- **`daily`** — end-of-day summary or reflection
- **`other`** — anything that doesn't fit the above

---

## Slack-first ingestion

The default write path for journal entries is a Slack message in `#journal`.

### Flow

1. Aayush posts a message in `#journal` (not a file upload — journal is text-first).
2. The ingestion agent reads the message and infers frontmatter fields via the inference-review pattern.
3. The agent infers `entry_type` from message content, extracts tickers and sectors, proposes tags, and presents the proposed entry for confirmation.
4. Aayush confirms or corrects in the thread.
5. On confirmation, the entry is written to `journal/entries/<date>-<short-slug>.md` with the original message as the body and confirmed frontmatter.
6. Git commit: `v2-journal: <date> <entry_type> — <one-line summary>`.

### Naming convention

`<YYYY-MM-DD>-<short-slug>.md`

Examples:
- `2026-04-05-obdc-long-entry.md`
- `2026-04-05-iran-hormuz-observation.md`
- `2026-04-05-end-of-day.md`

---

## Index folder

`journal/_index/` holds system-generated rollups (weekly, monthly). These are produced by automated agents and MUST NOT be hand-edited.

Rollups serve retrieval: deep dive agents and ledger promotion agents query `journal/entries/` via frontmatter filters on `tickers`, `sectors`, and `entry_type`. The index makes this efficient.

---

## Retrieval usage

Other agents read journal entries for context:

- **Ledger promotion agent** scans recent entries for falsifiable predictions to propose for promotion.
- **Deep dive agent** checks recent journal entries on the target ticker for Aayush's current thinking.
- **Monthly review agent** reads entries tagged with resolved ledger tickers to find lessons.

Journal entries are read-only for these agents — they never edit entries.

---

## Things specific to this folder you must never do

- Substantively edit an entry after 24 hours.
- Accept file uploads in `#journal` (journal is text-only; files go to `#research` or `#training`).
- Hand-edit files in `_index/`.
- Create entries without going through the inference-review pattern.
- Use entry types not in the closed vocabulary without a rule evolution proposal.
- Write entries directly to the folder without Slack confirmation (the Slack-first flow is the only valid write path for agents).
