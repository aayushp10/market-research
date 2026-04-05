# Provenance Backfill Guide

## When to run a backfill

Run a backfill for the v1.0 baseline skill only when:
- v2 has been operational for 4+ weeks
- At least one native-provenance version (v2.0+) has been compiled and published
- You want historical audit capability for decisions that were shaped by v1.0

Backfill is never urgent. The system works without it.

## The procedure

1. Open `training/_compiled/credit-trading/v1.0/SKILL.md`
2. For each section, identify candidate source material from: your memory, prior Claude conversations, primers/books you've read, framework sources you've drawn on
3. For each identified source, add a retroactive entry to `training/_provenance/credit-trading/v1.0.md` with frontmatter `backfilled: true, backfilled_date: <today>, confidence: low|medium|high`
4. Work incrementally. A partial backfill is valuable. Don't wait until you can do the whole thing.
5. Commit each backfill step with message `v2-provenance-backfill: v1.0 section <name>`

## What not to do

- Do NOT modify the v1.0 skill itself during backfill. v1.0 is frozen.
- Do NOT mark backfilled entries as if they were native. The honesty of the backfill flag is what makes this useful.
- Do NOT skip writing `confidence: low` when that's the truth. Low-confidence backfill is better than no backfill, but it must be labeled.
