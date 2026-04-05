# Market Research Agent — Troubleshooting

## Briefing didn't arrive at 6 AM

Check in this order:

1. **Is the adapter running?**
   - Open Task Manager → Details tab → look for `python.exe`
   - If not running: open a terminal, run `run.bat`, check for startup errors
   - Or check Task Scheduler → "Market Research Slack Adapter" → Last Run Result

2. **Did the scheduled task fire?**
   - Task Scheduler → "Market Research Morning Briefing" → History tab
   - If it shows "Task was run but the program... exited with return code 1": check the log at `_agent\logs\adapter.log`

3. **Did Claude Code fail?**
   - Open `_agent\logs\adapter.log`, scroll to the 6 AM window
   - Look for `briefing: failed` or `RuntimeError`
   - Common cause: CLAUDE_PATH in .env is stale (Claude Code extension updated). See OPERATIONS.md → Updating Claude Code path.

4. **Slack token expired?**
   - Log shows `slack_sdk.errors.SlackApiError: invalid_auth`
   - Go to https://api.slack.com/apps → Market Research Agent → OAuth & Permissions → Reinstall
   - Update SLACK_BOT_TOKEN in .env, restart adapter

---

## Adapter won't start

**"Missing required environment variables"**
- .env file is missing or incomplete
- Check: `C:\Data\Code\Market Research\.env` exists and all 8 fields are populated
- Compare against .env.example

**"No module named slack_bolt"**
- Virtual environment not activated or dependencies not installed
- Run: `cd _agent\slack_adapter && .venv\Scripts\activate && pip install -r requirements.txt`

**Claude Code path error / "The system cannot find the file specified"**
- CLAUDE_PATH in .env points to an old extension version
- Find current version: `ls "$env:USERPROFILE\.vscode\extensions\" | Where-Object { $_ -like "anthropic.claude-code*" }`
- Update CLAUDE_PATH in .env

---

## Obsidian Sync conflict

Obsidian shows a conflict banner on a file. This happens if the same file was edited on two devices before syncing.

1. Open the conflicted file in Obsidian
2. Obsidian creates a second copy with "conflict" in the name
3. Compare the two versions — in a single-writer setup (only the agent writes, you don't edit wiki files directly), the agent's version is almost always correct
4. Delete the conflict copy
5. If the conflict is on a daily file, verify frontmatter (`status`, `reviewed`) is correct

---

## Git merge conflict

Shouldn't happen in a single-user setup. If it does (e.g., manual edits on two machines):

```
cd "C:\Data\Code\Market Research"
git status          # see conflicted files
git diff            # review changes
# Edit the file to keep the correct version, remove conflict markers <<<< ==== >>>>
git add <file>
git commit -m "fix: resolve merge conflict in <file>"
```

---

## Claude Code takes too long / times out

- Default timeout: 10 minutes for #agent messages, 15 minutes for briefings
- On heavy days (many inbox files + long web search), briefings can run close to the limit
- To increase: edit `_BRIEFING_TIMEOUT` in `_agent\slack_adapter\briefing.py` (value is in seconds)
- Commit after editing

---

## "Something broke, check logs" in Slack

The adapter caught an unhandled exception. Open `_agent\logs\adapter.log`, find the ERROR line with the traceback, and diagnose from there. Common causes are covered above. If the error is novel, post the traceback in #agent and ask the agent to help diagnose.

---

## Temporarily disabling the scheduled briefing

Task Scheduler → "Market Research Morning Briefing" → right-click → **Disable**

To re-enable when you're back: right-click → **Enable**

The adapter can keep running — disabling the scheduled task only stops the 6 AM auto-run. Manual "run the brief" in #briefings still works.

---

## Drive mirror isn't syncing

1. Check Google Drive Desktop is running (system tray icon)
2. Check `_agent\logs\mirror.log` for robocopy errors
3. Run the mirror manually: `"C:\Data\Code\Market Research\_agent\scripts\drive_mirror.bat"`
4. If Drive Desktop is stuck: right-click system tray icon → Quit, reopen Google Drive
