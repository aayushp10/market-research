# First-Week Orientation

Work through one section per day. Each step should take 5-10 minutes.

---

## Day 1 — Verify the adapter and first briefing

1. Post `/ping` in #agent-ops. Confirm the agent responds.
2. Post `/brief` in #briefings to trigger a manual briefing run.
3. Review the draft that appears. Reply in-thread with at least one edit and one approval to confirm the feedback loop works.
4. Verify the finalized daily file appears in `shared/macro/daily/`.

## Day 2 — Ingestion from training

1. Drop a training source (PDF, link, or doc) in #training.
2. Agent posts an inference-review proposal (filename, folder, tags).
3. Approve or modify in-thread.
4. Confirm the file lands in the correct location and a commit is created.

## Day 3 — Journal entry

1. Post a freeform journal entry in #journal (a short market thought is fine).
2. Agent runs inference-review and proposes a date-stamped entry.
3. Approve in-thread.
4. Verify the entry appears in `shared/journal/`.

## Day 4 — Deep dive

1. Post `/dive <ticker>` in #research using a seeded name already in the vault.
2. Review the proposed scope (questions, sources, page structure).
3. Approve or trim, then let the agent execute.
4. Confirm new/updated pages and a commit appear.

## Day 5 — Ledger and compile status

1. Post `/open` in #ledger to see any open predictions.
2. If the ledger is empty, note that promotion detection will populate it over time.
3. Post `/compile status` in #training to check compile readiness.
4. Review the output — no action needed yet unless 5+ training files are queued.

## End of week — Weekly review

1. Post `run the weekly review` in #agent-ops.
2. Review the generated summary: dailies, setups, pages touched, quality flags.
3. Note anything that looks off — missing briefings, stuck ingestions, empty sections.

---

## After week 1

Once the basics are verified:

- Run a real deep dive on a fresh name not yet in the vault.
- Drop 2-3 real training sources over a few days and let ingestion run naturally.
- Let the ledger promotion detector run across a few briefings and journal entries; check `/open` after a week to see what it captured.
- When 5+ training files accumulate or 14 days pass, the agent will hint at a compile — try it.
