# v1 Archive Notes

## What v1 was

A Python Slack bot (slack-bolt, Socket Mode) bridging a Slack workspace to Claude Code against a local Obsidian vault. Three-world structure: `credit/`, `bdc/`, `shared/`. Morning briefing at 6 AM via Windows Task Scheduler. Three Slack channels: `#briefings`, `#inbox`, `#agent`.

Built on 2026-04-04 as a single-day prototype. One finalized daily briefing, one raw source (Citi IG snapshot), one closed setup, three templates, three CLAUDE.md files.

## Why it was replaced

v1 lacked:
- A compiled skill that learns from accumulated sources
- A ledger for grading predictions against reality
- A concepts layer for graph-based backlinks
- A structured journal
- A feedback loop from real experience back into skill refinement
- An ingestion tagging system (inference-review pattern)
- Multi-channel Slack topology for different content types

## What v2 does differently

- Five content areas (training, research, journal, ledger, concepts) instead of three worlds
- The skill is a compiled artifact with versioned history and provenance
- Ingestion uses the inference-review pattern across all paths
- Predictions are tracked and graded via the ledger
- Six Slack channels with command prefixes and thread-based task execution
- Rules evolve via an explicit approval flow

## Files archived here

- `CLAUDE-root-v1.md` — original root rules
- `credit-CLAUDE-v1.md` — credit world rules
- `bdc-CLAUDE-v1.md` — BDC world rules
- `README-v1.md` — original vault tour
- `index-v1.md` — original page catalog

Archived on 2026-04-05 during v2 migration.
