# Credit Research Vault (v2)

A personal credit research knowledge base maintained by an LLM agent,
built natively in Obsidian, and tracked in git. The vault covers five
content areas -- training, research, journal, ledger, and concepts --
plus a thin graph layer that links them. The compounding model is
cyclical: training produces compiled skill, skill sharpens research,
research generates ledger predictions, ledger outcomes feed back into
training.

---

## Architecture

```
Market Research/
  training/          source corpus -> compiled skill
    _compiled/         versioned skill bundles (credit-trading, bdc-knowledge)
    _transcripts/      raw conversation logs
    conversations/     curated training dialogues
    frameworks/        mental-model references
    primers/           onboarding primers
    inbox/             unprocessed material
    post-mortems/      trade and decision reviews

  research/          raw sources + work products
    credit/
      issuers/         per-name pages (OBDC, OTF, CCLFX, FLO, ADS, BCRED)
      sectors/         sector-level analysis
      markets/         market structure and technicals
      themes/          thematic research threads
      special-situations/
    macro/             rates, flows, positioning
    briefings/         date-stamped morning briefings
    _raw/              unprocessed source material
    _provenance/       source metadata

  journal/           append-only, Slack-first daily log
    _index/            date and tag indices
    entries/           individual journal entries

  ledger/            prediction scoreboard, promotion-only
    _index/            lookup indices
    open/              active predictions awaiting resolution
    resolved/          scored outcomes
    reviews/           periodic accuracy reviews

  concepts/          thin stub graph layer, lazy-created
                     (13 stubs: spread-duration, rating-migration,
                      redemption-gating, unitranche-subordination, etc.)

  _agent/            operations config and playbooks
```

---

## Daily Workflow

1. **Morning briefing** auto-runs at 6:00 AM ET. The agent pulls
   overnight data, scores open ledger items, and drafts a briefing
   into `research/briefings/`.
2. **Review in Slack.** The briefing posts to the #briefings thread.
   Comments, questions, and new observations are captured in-thread.
3. **Agent finalizes.** After review, the agent updates issuer pages,
   promotes any confirmed predictions in the ledger, and appends the
   journal entry.

---

## Slack Channels

- **#research** -- new issuer pages, sector updates, and deep-dive links
- **#training** -- skill compilation results, primer additions, post-mortems
- **#journal** -- daily journal entry notifications
- **#ledger** -- new predictions posted, resolutions scored
- **#briefings** -- morning briefing delivery and review thread
- **#agent-ops** -- agent health, errors, config changes

---

## Key Commands

| Command          | Purpose                                        |
| ---------------- | ---------------------------------------------- |
| `/dive <ticker>` | Open or create an issuer deep-dive page        |
| `/compile`       | Compile training corpus into a versioned skill |
| `/brief`         | Generate an ad-hoc briefing now                |
| `/open`          | List all open ledger predictions               |
| `/review`        | Run a ledger accuracy review                   |
| `/rule propose`  | Propose a new vault or agent rule              |

---

## What's Here Today

- **6 issuer pages:** OBDC, OTF, CCLFX, FLO, ADS (stub), BCRED
- **1 event playbook:** Iran special-situation
- **13 concept stubs:** spread-duration, rating-migration, redemption-gating,
  unitranche-subordination, non-traded-bdc-structure, price-nav,
  fallen-angel-framework, macro-credit-transmission, nii-coverage,
  mark-staleness, energy-sub-industry-decomposition,
  bdc-unsecured-notes, software-ai-bdc-exposure
- **1 briefing:** 2026-04-04
- **1 ledger entry**
- **credit-trading skill v1.0** (compiled)

---

## Principles

1. **Provenance mandatory.** Every fact links to a source; no orphan claims.
2. **Facts/views firewall.** Objective data and subjective views live in clearly separated sections.
3. **Inference-review pattern.** The agent drafts, a human reviews; nothing publishes unreviewed.
4. **Append-only journal.** Journal entries are never edited after the day closes.
5. **Promotion-only ledger.** Predictions move forward (open -> resolved) but never backward.
