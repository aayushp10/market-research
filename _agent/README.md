# Market Research Agent — Runtime

The `_agent/` directory contains the Slack adapter and supporting scripts
that connect Claude Code to the Slack workspace. The markdown vault itself
lives in the parent directory.

---

## Starting the adapter

Double-click `slack_adapter\run.bat`, or from a terminal:

```
cd "C:\Data\Code\Market Research\_agent\slack_adapter"
.venv\Scripts\activate
python app.py
```

The adapter connects to Slack via Socket Mode. You should see:
```
Starting Market Research Agent (Socket Mode)
⚡️ Bolt app is running!
```

Keep this window open (or let it run via Task Scheduler — see Phase 7 of the
setup plan).

---

## Checking logs

All activity is logged to `_agent\logs\adapter.log` (rotating, max 10 MB × 5 files).

To tail in real time:
```
Get-Content "C:\Data\Code\Market Research\_agent\logs\adapter.log" -Wait -Tail 50
```

---

## Updating Python dependencies

```
cd "C:\Data\Code\Market Research\_agent\slack_adapter"
.venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

---

## Testing the Slack connection

Send `status` in the `#agent` channel. You should receive a health report
with uptime, last git commit, disk space, unreviewed draft count, and
active setup count.

---

## Disabling the scheduled briefing temporarily

Open Task Scheduler → `Market Research Morning Briefing` → right-click →
Disable. Re-enable when you're back.

Alternatively, just don't review the draft — skip-day protection in CLAUDE.md
ensures stale drafts are never promoted to ground truth.

---

## Common troubleshooting

**Adapter won't start — "Missing required environment variables"**
Check that `C:\Data\Code\Market Research\.env` exists and all fields are
populated. Compare against `.env.example`.

**Adapter won't start — Slack token errors**
Tokens expire if the Slack app is reinstalled or the workspace disconnects.
Go to `https://api.slack.com/apps`, regenerate tokens, update `.env`.

**"claude: command not found" or subprocess error**
`CLAUDE_PATH` in `.env` points to a specific Claude Code version. If you've
updated VS Code and the extension upgraded, find the new path:
```
ls "$env:USERPROFILE\.vscode\extensions\" | Where-Object { $_ -like "anthropic.claude-code*" }
```
Update `CLAUDE_PATH` in `.env` to point to the new version's `claude.exe`.

**Briefing takes too long / times out**
Default timeout is 15 minutes for briefings. On days with many inbox files
or heavy web search load this can stretch. If it consistently times out,
increase `_BRIEFING_TIMEOUT` in `briefing.py`.

**Obsidian Sync conflict**
Obsidian will show a conflict banner. Open the conflicted file, review both
versions, keep the correct one, and delete the conflict copy. The vault is
single-writer (only Claude Code and you), so conflicts are rare and always
resolvable by inspection.

**Git merge conflict**
Shouldn't happen in a single-user setup. If it does:
```
cd "C:\Data\Code\Market Research"
git status        # see which files are conflicted
git diff          # review
# Edit the file to resolve, then:
git add <file>
git commit -m "fix: resolve merge conflict in <file>"
```
