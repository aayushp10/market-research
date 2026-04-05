"""
Slack Bolt app — Socket Mode.
Routes events across six channels to appropriate handlers.

Channels: #research, #training, #journal, #ledger, #briefings, #agent-ops
Routing: file uploads by channel → inbox, command prefixes → dispatchers,
         free-form messages → intent router, thread replies → session continuity.
"""

import logging
import re
import subprocess
import shlex
from datetime import datetime, timezone
from pathlib import Path

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import briefing
import claude_runner
import config
import inbox_handler
import ingestion
import intent_router
import thread_state
from config import ChannelType, channel_type
from logging_setup import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = App(token=config.SLACK_BOT_TOKEN)

_START_TIME = datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _post_error(client, channel: str, thread_ts: str | None, err: Exception) -> None:
    msg = (
        f"Something broke — check `_agent/logs/adapter.log` for details.\n"
        f"Error: `{type(err).__name__}: {err}`"
    )
    try:
        client.chat_postMessage(channel=channel, text=msg, thread_ts=thread_ts)
    except Exception:
        logger.exception("Failed to post error message to Slack")


def _post_ops_error(client, err: Exception, context: str) -> None:
    """Post transient errors to #agent-ops instead of the source channel."""
    msg = (
        f"*Transient error* in `{context}`\n"
        f"`{type(err).__name__}: {err}`\n"
        f"Check `_agent/logs/adapter.log` for full traceback."
    )
    try:
        client.chat_postMessage(
            channel=config.SLACK_AGENT_OPS_CHANNEL_ID,
            text=msg,
        )
    except Exception:
        logger.exception("Failed to post error to #agent-ops")


def _parse_command(text: str) -> tuple[str | None, str]:
    """
    Parse a command prefix from text.
    Returns (command, remaining_args) or (None, original_text).
    """
    text = text.strip()
    if not text.startswith("/"):
        return None, text
    parts = text.split(None, 1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return cmd, args


# ---------------------------------------------------------------------------
# Command dispatchers per channel
# ---------------------------------------------------------------------------

def _dispatch_research_command(cmd: str, args: str, client, channel: str, thread_ts: str, ts: str) -> bool:
    """Handle command prefixes in #research. Returns True if handled."""
    if cmd == "/dive":
        if not args:
            client.chat_postMessage(channel=channel, text="Missing argument. Usage: `/dive <ticker|topic>`", thread_ts=thread_ts or ts)
            return True
        _start_deep_dive(client, channel, ts, args)
        return True
    if cmd == "/sources":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"List all raw sources in research/_raw/ related to: {args}. "
                        f"Show file path, source_type, as_of_date for each. Be concise.")
        return True
    if cmd == "/situations":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"List active situations in research/credit/special-situations/ "
                        f"and research/credit/themes/. Filter: {args or 'all'}. Show title, date, tickers.")
        return True
    if cmd == "/themes":
        _run_agent_task(client, channel, thread_ts or ts,
                        "List current themes in research/credit/themes/. Show title, date, key tickers.")
        return True
    if cmd == "/issuer":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"Show the issuer page for {args} from research/credit/issuers/. "
                        f"If it doesn't exist, say so and offer to create it.")
        return True
    if cmd == "/sector":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"Show the sector page for {args} from research/credit/sectors/. "
                        f"If it doesn't exist, say so and offer to create it.")
        return True
    if cmd == "/status":
        _research_status(client, channel, thread_ts or ts)
        return True
    if cmd == "/help":
        client.chat_postMessage(
            channel=channel, thread_ts=thread_ts or ts,
            text="*#research commands:* `/dive <ticker>`, `/sources <ticker>`, "
                 "`/situations [filter]`, `/themes`, `/issuer <ticker>`, "
                 "`/sector <name>`, `/status`, `/help`",
        )
        return True
    return False


def _dispatch_training_command(cmd: str, args: str, client, channel: str, thread_ts: str, ts: str) -> bool:
    if cmd == "/compile":
        sub = args.strip().lower()
        if sub == "status":
            _run_agent_task(client, channel, thread_ts or ts,
                            "Report compile status: how many new training files since last compile, "
                            "last compile date and version, recommendation on whether to recompile.")
        elif sub == "history":
            _run_agent_task(client, channel, thread_ts or ts,
                            "List recent compile versions in training/_compiled/credit-trading/ "
                            "with dates and statuses.")
        elif sub in ("approve", "reject"):
            _run_agent_task(client, channel, thread_ts or ts,
                            f"Process compile {sub} command. "
                            f"{'Repoint current to the new version and publish.' if sub == 'approve' else 'Mark as rejected, do not publish.'}")
        else:
            client.chat_postMessage(channel=channel, text="Starting compile pipeline...", thread_ts=thread_ts or ts)
            _run_agent_task(client, channel, thread_ts or ts,
                            "Run the compile pipeline per training/CLAUDE.md and root CLAUDE.md. "
                            "Read training corpus, two-pass extraction, generate diff and canary results, "
                            "post results here for review.")
        return True
    if cmd == "/inbox":
        _run_agent_task(client, channel, thread_ts or ts,
                        "List contents of training/inbox/to-tag/ and training/inbox/to-file/. "
                        "Show filename, size, and how long each has been waiting.")
        return True
    if cmd in ("/rule", "/rules"):
        if args.lower().startswith("propose"):
            proposal_text = args[len("propose"):].strip()
            _handle_rule_proposal(client, channel, thread_ts or ts, proposal_text)
        else:
            _run_agent_task(client, channel, thread_ts or ts,
                            "Show the rule change log from _agent/rule_changes.md.")
        return True
    if cmd == "/sources":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"Search the training corpus for sources matching: {args}. "
                        f"Check by author, topic, source_type. Show matches with key frontmatter.")
        return True
    if cmd == "/status":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Training status: pending ingestions in inbox, compile backlog count, "
                        "last compile date and version.")
        return True
    if cmd == "/help":
        client.chat_postMessage(
            channel=channel, thread_ts=thread_ts or ts,
            text="*#training commands:* `/compile [status|history|approve|reject]`, "
                 "`/inbox`, `/rule propose <text>`, `/sources <query>`, `/status`, `/help`",
        )
        return True
    return False


def _dispatch_journal_command(cmd: str, args: str, client, channel: str, thread_ts: str, ts: str) -> bool:
    if cmd == "/find":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"Search journal entries for: {args}. Check text, tickers, sectors, entry_type. "
                        f"Show matching entries with date, type, and first line.")
        return True
    if cmd == "/today":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Show all journal entries from today. List date, entry_type, tickers, first line.")
        return True
    if cmd == "/week":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Show all journal entries from this week. List date, entry_type, tickers, first line.")
        return True
    if cmd == "/status":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Journal status: entries today, entries this week, any pending inference-reviews.")
        return True
    if cmd == "/help":
        client.chat_postMessage(
            channel=channel, thread_ts=thread_ts or ts,
            text="*#journal commands:* `/find <query>`, `/today`, `/week`, `/status`, `/help`",
        )
        return True
    return False


def _dispatch_ledger_command(cmd: str, args: str, client, channel: str, thread_ts: str, ts: str) -> bool:
    if cmd == "/open":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"List all open predictions in ledger/open/, sorted by revisit_date. "
                        f"Filter: {args or 'none'}. Show prediction, revisit_date, confidence, tickers.")
        return True
    if cmd == "/resolved":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"List resolved entries in ledger/resolved/. "
                        f"Filter: {args or 'none'}. Show prediction, outcome, resolved_date.")
        return True
    if cmd == "/review":
        client.chat_postMessage(channel=channel, text="Starting monthly review...", thread_ts=thread_ts or ts)
        _run_agent_task(client, channel, thread_ts or ts,
                        "Run the monthly review ritual per ledger/CLAUDE.md. "
                        "Read resolved entries since last review, compute stats, identify patterns, "
                        "draft review document, propose post-mortem promotions.")
        return True
    if cmd == "/ledger":
        _run_agent_task(client, channel, thread_ts or ts,
                        f"Show details for ledger entry: {args}")
        return True
    if cmd == "/stats":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Compute aggregate ledger stats: total predictions, outcome breakdown, "
                        "win rate by domain, confidence calibration.")
        return True
    if cmd == "/status":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Ledger status: open predictions count, overdue revisit dates, "
                        "last review date, pending promotions.")
        return True
    if cmd == "/help":
        client.chat_postMessage(
            channel=channel, thread_ts=thread_ts or ts,
            text="*#ledger commands:* `/open [filter]`, `/resolved [filter]`, "
                 "`/review`, `/ledger <entry>`, `/stats`, `/status`, `/help`",
        )
        return True
    return False


def _dispatch_briefings_command(cmd: str, args: str, client, channel: str, thread_ts: str, ts: str) -> bool:
    if cmd == "/brief":
        topic = args.strip() or None
        _trigger_briefing(client, channel, ts, topic=topic)
        return True
    if cmd == "/briefing":
        sub = args.strip().lower()
        if sub == "scope":
            _run_agent_task(client, channel, thread_ts or ts,
                            "Show the current contents of research/briefing-scope.md.")
        elif sub.startswith("scope propose"):
            proposal = args[len("scope propose"):].strip()
            _handle_rule_proposal(client, channel, thread_ts or ts, proposal)
        else:
            client.chat_postMessage(
                channel=channel, thread_ts=thread_ts or ts,
                text="Usage: `/briefing scope` or `/briefing scope propose <text>`",
            )
        return True
    if cmd == "/status":
        _run_agent_task(client, channel, thread_ts or ts,
                        "Briefings status: last run time, any unreviewed drafts, "
                        "next scheduled run.")
        return True
    if cmd == "/help":
        client.chat_postMessage(
            channel=channel, thread_ts=thread_ts or ts,
            text="*#briefings commands:* `/brief [topic]`, `/briefing scope`, "
                 "`/briefing scope propose <text>`, `/status`, `/help`",
        )
        return True
    return False


def _dispatch_ops_command(cmd: str, args: str, client, channel: str, thread_ts: str, ts: str) -> bool:
    if cmd == "/ping":
        uptime = datetime.now(timezone.utc) - _START_TIME
        hours, rem = divmod(int(uptime.total_seconds()), 3600)
        minutes = rem // 60
        client.chat_postMessage(
            channel=channel, text=f"pong — up {hours}h {minutes}m",
            thread_ts=thread_ts or ts,
        )
        return True
    if cmd in ("/health", "/status"):
        _health_status(client, channel, thread_ts or ts)
        return True
    if cmd in ("/rule", "/rules"):
        if args.lower().startswith("propose"):
            proposal_text = args[len("propose"):].strip()
            _handle_rule_proposal(client, channel, thread_ts or ts, proposal_text)
        else:
            _run_agent_task(client, channel, thread_ts or ts,
                            "Show the rule change log from _agent/rule_changes.md.")
        return True
    if cmd == "/help":
        client.chat_postMessage(
            channel=channel, thread_ts=thread_ts or ts,
            text="*#agent-ops commands:* `/ping`, `/health`, `/status`, "
                 "`/rules`, `/rule propose <text>`, `/help`",
        )
        return True
    return False


_COMMAND_DISPATCHERS = {
    ChannelType.RESEARCH: _dispatch_research_command,
    ChannelType.TRAINING: _dispatch_training_command,
    ChannelType.JOURNAL: _dispatch_journal_command,
    ChannelType.LEDGER: _dispatch_ledger_command,
    ChannelType.BRIEFINGS: _dispatch_briefings_command,
    ChannelType.AGENT_OPS: _dispatch_ops_command,
}


# ---------------------------------------------------------------------------
# Task helpers
# ---------------------------------------------------------------------------

def _run_agent_task(client, channel: str, reply_ts: str, prompt: str) -> None:
    """Send a prompt to Claude Code and post the result in a thread."""
    ch_type = channel_type(channel)
    session_key = f"{ch_type.value}-{reply_ts}"
    try:
        result = claude_runner.send(
            prompt=prompt,
            session_key=session_key,
            timeout=600,
        )
        client.chat_postMessage(channel=channel, text=result, thread_ts=reply_ts)
    except Exception as e:
        logger.exception("agent task failed: %s", prompt[:80])
        _post_error(client, channel, reply_ts, e)


def _start_deep_dive(client, channel: str, ts: str, target: str) -> None:
    """Kick off a deep dive in a new thread."""
    resp = client.chat_postMessage(
        channel=channel,
        text=f"*Deep dive: {target}* — scoping...",
    )
    thread_ts = resp["ts"]
    thread_state.create(
        thread_ts=thread_ts,
        channel="research",
        task_type="deep_dive",
        target=target,
    )
    _run_agent_task(
        client, channel, thread_ts,
        f"Start a deep dive on: {target}\n\n"
        f"Per research/CLAUDE.md deep dive discipline:\n"
        f"1. Propose scope: target artifact path, sources found in research/_raw/, "
        f"whether web search is needed, concepts expected.\n"
        f"2. Wait for Aayush's confirmation before executing.\n"
        f"Post the scope proposal now.",
    )


def _trigger_briefing(client, channel: str, ts: str, topic: str | None = None) -> None:
    resp = client.chat_postMessage(
        channel=channel,
        text=f"Running {'scoped' if topic else 'morning'} briefing... this takes 5–10 minutes.",
    )
    thread_ts = resp["ts"]
    thread_state.create(
        thread_ts=thread_ts,
        channel="briefings",
        task_type="briefing",
        target=topic or "daily",
    )
    try:
        summary = briefing.run_morning_briefing(topic=topic)
        client.chat_postMessage(channel=channel, text=summary, thread_ts=thread_ts)
        thread_state.update(thread_ts, status="pending_user")
    except Exception as e:
        logger.exception("Briefing failed")
        _post_error(client, channel, thread_ts, e)
        thread_state.update(thread_ts, status="error")


def _handle_rule_proposal(client, channel: str, reply_ts: str, proposal_text: str) -> None:
    """Route a rule proposal to #agent-ops via Claude Code."""
    _run_agent_task(
        client, config.SLACK_AGENT_OPS_CHANNEL_ID, reply_ts,
        f"Aayush proposed a rule change:\n\n{proposal_text}\n\n"
        f"Draft a formal rule-change proposal per root CLAUDE.md rule evolution flow. "
        f"Identify the most likely CLAUDE.md file affected, quote the current rule, "
        f"propose the change, and post the formatted proposal.",
    )


def _handle_journal_entry(client, channel: str, ts: str, text: str) -> None:
    """Process a journal entry through inference-review."""
    resp = client.chat_postMessage(
        channel=channel,
        text="Processing journal entry...",
        thread_ts=ts,
    )
    thread_ts = resp.get("ts", ts)
    thread_state.create(
        thread_ts=ts,
        channel="journal",
        task_type="ingestion",
        target="journal-entry",
    )
    _run_agent_task(
        client, channel, ts,
        f"A new journal entry was posted:\n\n{text}\n\n"
        f"Per journal/CLAUDE.md:\n"
        f"1. Infer entry_type, tickers, sectors, tags from the message.\n"
        f"2. Mark each field with [inferred], [guess], or [needs input].\n"
        f"3. Present the proposed entry with frontmatter for confirmation.\n"
        f"4. Wait for Aayush to confirm or correct.",
    )


def _health_status(client, channel: str, thread_ts: str) -> None:
    uptime = datetime.now(timezone.utc) - _START_TIME
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes = rem // 60

    try:
        git_log = subprocess.run(
            ["git", "log", "-1", "--format=%h %s (%ar)"],
            cwd=config.VAULT_PATH,
            capture_output=True, text=True, timeout=10,
        )
        last_commit = git_log.stdout.strip() or "unknown"
    except Exception:
        last_commit = "unavailable"

    try:
        import shutil
        usage = shutil.disk_usage(config.VAULT_PATH)
        free_gb = usage.free / (1024 ** 3)
        disk = f"{free_gb:.1f} GB free"
    except Exception:
        disk = "unavailable"

    # Unreviewed drafts
    briefings_dir = Path(config.VAULT_PATH) / "research" / "briefings"
    unreviewed = 0
    if briefings_dir.exists():
        for f in briefings_dir.glob("*.md"):
            if f.name.startswith("_"):
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            if "reviewed: false" in text and "status: draft" in text:
                unreviewed += 1

    # Open ledger entries
    ledger_open = Path(config.VAULT_PATH) / "ledger" / "open"
    open_predictions = len(list(ledger_open.glob("*.md"))) if ledger_open.exists() else 0

    # Active threads
    active_threads = thread_state.list_active()

    # Pending ingestions
    research_inbox = Path(config.VAULT_PATH) / "research" / "_raw" / "inbox" / "to-tag"
    training_inbox = Path(config.VAULT_PATH) / "training" / "inbox" / "to-tag"
    pending_research = len(list(research_inbox.glob("*"))) if research_inbox.exists() else 0
    pending_training = len(list(training_inbox.glob("*"))) if training_inbox.exists() else 0

    msg = (
        f"*Market Research Agent — Health*\n"
        f"• Uptime: {hours}h {minutes}m\n"
        f"• Last commit: {last_commit}\n"
        f"• Disk: {disk}\n"
        f"• Unreviewed briefing drafts: {unreviewed}\n"
        f"• Open ledger predictions: {open_predictions}\n"
        f"• Active task threads: {len(active_threads)}\n"
        f"• Pending ingestion: research={pending_research}, training={pending_training}"
    )
    client.chat_postMessage(channel=channel, text=msg, thread_ts=thread_ts)


# ---------------------------------------------------------------------------
# File upload handler
# ---------------------------------------------------------------------------

@app.event("file_shared")
def handle_file_shared(event, client, logger):
    file_id = event.get("file_id")
    channel_id = event.get("channel_id")
    ch_type = channel_type(channel_id)

    # Only accept files in #research and #training
    if ch_type == ChannelType.RESEARCH:
        inbox_type = "research"
    elif ch_type == ChannelType.TRAINING:
        inbox_type = "training"
    elif ch_type == ChannelType.JOURNAL:
        client.chat_postMessage(
            channel=channel_id,
            text="Journal entries are text-only. Drop files in #research or #training instead.",
        )
        return
    else:
        client.chat_postMessage(
            channel=channel_id,
            text="File uploads go in #research (for raw sources) or #training (for training material).",
        )
        return

    try:
        info = client.files_info(file=file_id)
        file_info = info["file"]
        msg, saved_path = inbox_handler.handle_file_upload(file_info, inbox_type)
        resp = client.chat_postMessage(channel=channel_id, text=msg)
        thread_ts = resp["ts"]

        # Track the ingestion thread
        thread_state.create(
            thread_ts=thread_ts,
            channel=ch_type.value,
            task_type="ingestion",
            target=str(saved_path),
        )

        # Run inference-review proposal
        try:
            proposal = ingestion.propose_frontmatter(str(saved_path), inbox_type)
            client.chat_postMessage(channel=channel_id, text=proposal, thread_ts=thread_ts)
            thread_state.update(thread_ts, status="pending_user")
        except Exception as e:
            logger.exception("Inference-review proposal failed")
            _post_ops_error(client, e, f"ingestion proposal for {saved_path}")
    except Exception as e:
        logger.exception("File handling failed")
        _post_error(client, channel_id, None, e)


# ---------------------------------------------------------------------------
# Message dispatch
# ---------------------------------------------------------------------------

@app.event({"type": "message"})
def handle_all_messages(body, event, client, logger):
    logger.info(
        "MESSAGE: channel=%s subtype=%s thread=%s text=%r",
        event.get("channel"), event.get("subtype"),
        event.get("thread_ts"), (event.get("text") or "")[:80],
    )
    _dispatch_message(event, client, logger)


def _dispatch_message(event, client, logger):
    subtype = event.get("subtype")
    if subtype in ("bot_message", "message_changed", "message_deleted", "file_share"):
        return

    channel = event.get("channel", "")
    text = (event.get("text") or "").strip()
    thread_ts = event.get("thread_ts")
    ts = event.get("ts")
    ch_type = channel_type(channel)

    if ch_type == ChannelType.UNKNOWN:
        return

    # ------------------------------------------------------------------
    # Thread reply — route to existing task
    # ------------------------------------------------------------------
    if thread_ts and thread_ts != ts:
        _handle_thread_reply(client, channel, ch_type, thread_ts, ts, text)
        return

    # ------------------------------------------------------------------
    # Top-level message — try command prefix first, then free-form
    # ------------------------------------------------------------------
    cmd, args = _parse_command(text)

    if cmd is not None:
        dispatcher = _COMMAND_DISPATCHERS.get(ch_type)
        if dispatcher and dispatcher(cmd, args, client, channel, thread_ts, ts):
            return
        # Unknown command
        client.chat_postMessage(
            channel=channel, thread_ts=ts,
            text=f"Unknown command `{cmd}`. Try `/help` for available commands in this channel.",
        )
        return

    # Free-form message handling
    _handle_freeform(client, channel, ch_type, ts, text)


def _handle_thread_reply(client, channel: str, ch_type: ChannelType, thread_ts: str, ts: str, text: str) -> None:
    """Handle a reply in an existing thread."""
    state = thread_state.get(thread_ts)

    if state is not None:
        session_key = state.get("session_key", f"{ch_type.value}-{thread_ts}")
        task_type = state.get("task_type", "general")

        # For briefing threads, use the review flow
        if task_type == "briefing" and ch_type == ChannelType.BRIEFINGS:
            client.chat_postMessage(
                channel=channel, text="Applying review feedback...", thread_ts=thread_ts,
            )
            prompt = (
                f"Review feedback from Aayush on today's briefing:\n\n{text}\n\n"
                f"Apply all corrections to the daily file. "
                f"If he approves or rejects any ledger promotion candidates, note that. "
                f"Mark status: final, reviewed: true, add reviewed_at timestamp. "
                f"Update relevant research/macro/* subfolders if material. "
                f"Append to research/briefings/_log.md and log.md. "
                f"Commit with format: 'v2-briefings: YYYY-MM-DD reviewed — {{one-line summary}}'. "
                f"Return a short finalization summary for Slack (under 200 words)."
            )
        else:
            # Generic thread continuation
            prompt = text

        try:
            result = claude_runner.send(
                prompt=prompt,
                session_key=session_key,
                timeout=600,
            )
            client.chat_postMessage(channel=channel, text=result, thread_ts=thread_ts)
            thread_state.update(thread_ts)
        except Exception as e:
            logger.exception("Thread reply handling failed")
            _post_error(client, channel, thread_ts, e)
        return

    # No tracked state — treat as a generic agent task in thread
    session_key = f"{ch_type.value}-{thread_ts}"
    try:
        result = claude_runner.send(prompt=text, session_key=session_key, timeout=600)
        client.chat_postMessage(channel=channel, text=result, thread_ts=thread_ts)
    except Exception as e:
        logger.exception("Untracked thread reply failed")
        _post_error(client, channel, thread_ts, e)


def _handle_freeform(client, channel: str, ch_type: ChannelType, ts: str, text: str) -> None:
    """Handle a free-form (non-command) top-level message."""
    if not text:
        return

    # Journal: every message is a journal entry
    if ch_type == ChannelType.JOURNAL:
        _handle_journal_entry(client, channel, ts, text)
        return

    # Classify intent
    intent = intent_router.classify(ch_type.value, text)

    if intent == intent_router.Intent.STATUS:
        _health_status(client, channel, ts)
        return

    if intent == intent_router.Intent.RULE_PROPOSAL:
        _handle_rule_proposal(client, channel, ts, text)
        return

    # Default: run as an agent task in a thread
    _run_agent_task(client, channel, ts, text)


# ---------------------------------------------------------------------------
# App mention — any channel
# ---------------------------------------------------------------------------

@app.event("app_mention")
def handle_mention(event, client, logger):
    channel = event.get("channel", "")
    text = event.get("text", "")
    thread_ts = event.get("thread_ts")
    ts = event.get("ts")

    clean_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()
    if not clean_text:
        return

    reply_ts = thread_ts or ts
    _run_agent_task(client, channel, reply_ts, clean_text)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Market Research Agent v2 (Socket Mode)")
    handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)
    handler.start()
