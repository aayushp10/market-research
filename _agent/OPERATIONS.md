# Market Research Agent — Operations (v2)

## 1. Daily briefing

**6:00 AM (automatic)**
- Agent reads briefing-scope.md, setups.md, last 3 dailies, ledger open items.
- Processes any files in _raw/inbox/.
- Runs targeted web searches.
- Drafts shared/macro/daily/YYYY-MM-DD.md (status: draft, reviewed: false).
- Commits: `daily: YYYY-MM-DD draft — {summary}`.
- Posts summary to #briefings.

**Your review (in-thread)**
- Read the draft, reply in the #briefings thread with freeform feedback:
  - "approve the BDC setup, cut the refiner line, add X"
  - "reject all proposed setups, rest looks good, reviewed"
- Agent applies corrections, finalizes the file, updates macro folders, commits.

**If you skip a day**
- Draft stays as-is, never promoted to final.
- Next engagement: agent asks batch-review or move-on.

---

## 2. Ingestion

**Sources (PDFs, links, docs)**
- Drop in #research or #training.
- Agent runs inference-review: proposes filename, folder, tags.
- You approve/modify in-thread.
- Agent files to the correct location, commits.

**Journal entries**
- Post freeform text in #journal.
- Agent runs inference-review (lighter): proposes date-stamped entry, tags.
- You approve; agent writes to shared/journal/, commits.

---

## 3. Deep dives

- Post `/dive <ticker>` in #research.
- Agent proposes scope (questions, sources, page structure).
- You approve or trim scope in-thread.
- Agent executes: searches, reads sources, writes/updates pages, commits.
- Final summary posted back to #research thread.

---

## 4. Ledger

Predictions are promoted from journal, research, or briefings into the ledger.

- **Open**: active predictions awaiting resolution.
- **Revisit**: flagged for re-evaluation (date-triggered or manual).
- **Resolve**: outcome recorded, scored.

Commands:
- `/open` in #ledger — list all open predictions.
- `/revisit` in #ledger — list items due for revisit.
- `/resolve <id> <outcome>` in #ledger — close a prediction with outcome.
- `/review` in #ledger — monthly review: accuracy stats, stale items, themes.

---

## 5. Compile

Training compilation bundles new training files into a structured set.

- Post `/compile` in #training to trigger.
- Auto-trigger hint: 5+ new training files or 14+ days since last compile.
- Agent posts proposed compilation (file list, structure, summary).
- You approve or reject in-thread.
- On approve: agent compiles, commits, posts confirmation.

Check status anytime: `/compile status` in #training.

---

## 6. Rule evolution

- Propose a rule change: `/rule propose <description>` in any channel.
- Agent drafts a formal proposal and posts it in #agent-ops.
- You respond: approve, modify, or reject.
- On approve: agent updates the relevant config/rule file, commits, logs to rule_changes.md.

---

## 7. Weekly review

Post in #agent-ops:
```
run the weekly review
```

Agent generates:
- Dailies reviewed vs skipped.
- Setups moved (new / reinforced / killed / matured).
- Ledger items opened, revisited, resolved.
- Pages touched most, recurring themes.
- Quality flags (repetitive briefings, dead dig sections).

---

## 8. Monthly lint

Post in #agent-ops:
```
run the monthly lint pass
```

Agent cold-reads the entire wiki:
- Claims without raw source citations.
- Stale content (>60 days, contradicting newer sources).
- Contradictions between pages.
- Matured/dead setup scoring.
- Orphan and stub pages.
- Proposes briefing-scope.md amendments.

---

## 9. Updating Claude Code path

When VS Code updates the Claude Code extension, the version in the path changes.

1. Open PowerShell and run:
   ```
   ls "$env:USERPROFILE\.vscode\extensions\" | Where-Object { $_ -like "anthropic.claude-code*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
   ```
2. Copy the new extension folder name.
3. Edit `C:\Data\Code\Market Research\.env` — update CLAUDE_PATH.
4. Restart the adapter.

---

## 10. Troubleshooting

**Adapter won't start**
- Check `.env` exists and all vars are set (CLAUDE_PATH, SLACK_BOT_TOKEN, channel IDs).
- Verify channel IDs match actual Slack channel IDs (not names).
- Verify CLAUDE_PATH points to a valid Claude Code executable (see section 9).

**Briefing fails or is empty**
- Check `_agent/logs/` for the latest run log.
- Confirm briefing-scope.md is not empty or malformed.
- Confirm _raw/inbox/ is readable.

**Ingestion stuck**
- Check for files stuck in to-tag/ folders under _raw/.
- Re-drop the file in the Slack channel to retry. Check logs for inference-review errors.
