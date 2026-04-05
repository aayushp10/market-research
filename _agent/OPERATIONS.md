# Market Research Agent — Operations

## Daily operation

**6:00 AM (automatic)**
- Adapter reads briefing-scope.md, setups.md, last 3 dailies
- Processes any files in _raw/inbox/
- Runs 5–10 targeted web searches
- Drafts shared/macro/daily/YYYY-MM-DD.md (status: draft, reviewed: false)
- Moves inbox files to permanent _raw/ homes
- Commits: `daily: YYYY-MM-DD draft — {summary}`
- Posts summary to #briefings in Slack

**Your 15 minutes (whenever you have time)**
- Read the draft in Obsidian (laptop or phone)
- Reply in the #briefings thread with feedback — freeform is fine:
  - "approve the BDC setup, cut the refiner line, add X"
  - "reject all proposed setups, rest looks good, reviewed"
- The agent applies corrections, finalizes the file, updates setups.md, commits, posts summary back

**If you skip a day**
- The draft stays as-is, never promoted to final
- On your next engagement, the agent will ask: batch-review skipped drafts or move on?
- For 1–2 day gaps: batch review is usually fast
- For longer gaps: default to moving on

---

## Weekly operation (Friday afternoon or Sunday evening)

Post in #agent:
```
run the weekly review
```

The agent generates:
- Dailies reviewed vs skipped this week
- Setups moved (new / reinforced / killed / matured)
- Pages touched most
- Themes that recurred
- Quality flags (repetitive briefings? Dig section producing anything?)

---

## Monthly operation (lint pass)

Post in #agent:
```
run the monthly lint pass
```

The agent does a cold-read of the entire wiki:
- Flags claims without raw source citations
- Flags stale content (>60 days, newer contradicting sources exist)
- Flags contradictions between pages
- Scores matured/dead setups: was the thesis right?
- Flags orphan pages and stub pages
- Proposes briefing-scope.md amendments

This is the most important epistemic control. Do it once a month.

---

## Adding new coverage

Edit `shared/macro/briefing-scope.md` — add the name under the relevant section. The agent picks it up on the next briefing run. No other changes needed.

To create the issuer page: drop a source file for that name in #inbox (or _raw/inbox/), then ask the agent to ingest it. The agent creates the page from the appropriate template (_templates/issuer-credit.md or _templates/issuer-bdc.md) on first ingest.

---

## Retiring or adding a setup

**Adding:** Propose setups arise from the morning briefing. The agent surfaces them in the draft under ## Setups. You approve or reject during review. Approved setups are added to setups.md. You never add directly to setups.md.

**Retiring:** Tell the agent during review: "kill the [name] setup — [outcome notes]." The agent moves it to the Closed section of setups.md with your outcome notes. It is never deleted.

**Re-evaluating:** Each setup has a re-evaluate date. The agent flags these in daily briefings when the date arrives.

---

## Promoting a drift-watch theme to state

Themes in briefing-scope.md have a status (drift-watch, active, closed). To promote one, tell the agent during any review or in #agent: "promote [theme] from drift-watch to active state — [reason]." The agent will propose a briefing-scope.md amendment; you approve it in the next daily review.

---

## Updating Claude Code path

When VS Code updates the Claude Code extension, the version number in the path changes. Update CLAUDE_PATH in .env:

1. Open PowerShell and run:
   ```
   ls "$env:USERPROFILE\.vscode\extensions\" | Where-Object { $_ -like "anthropic.claude-code*" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
   ```
2. Copy the new extension folder name
3. Edit C:\Data\Code\Market Research\.env — update CLAUDE_PATH to the new path
4. Restart the adapter
