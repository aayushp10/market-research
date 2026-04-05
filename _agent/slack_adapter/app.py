"""
Slack Bolt app — Socket Mode.
Listens to events in #briefings, #inbox, and #agent and routes them
to Claude Code via claude_runner.
"""

import logging
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import briefing
import claude_runner
import config
import inbox_handler
from logging_setup import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = App(token=config.SLACK_BOT_TOKEN)

_START_TIME = datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _post_error(client, channel: str, thread_ts: str | None, err: Exception) -> None:
    msg = f"Something broke — check `_agent/logs/adapter.log` for details.\nError: `{type(err).__name__}: {err}`"
    try:
        client.chat_postMessage(channel=channel, text=msg, thread_ts=thread_ts)
    except Exception:
        logger.exception("Failed to post error message to Slack")


def _is_briefings(channel: str) -> bool:
    return channel == config.SLACK_BRIEFINGS_CHANNEL_ID


def _is_inbox(channel: str) -> bool:
    return channel == config.SLACK_INBOX_CHANNEL_ID


def _is_agent(channel: str) -> bool:
    return channel == config.SLACK_AGENT_CHANNEL_ID


def _trigger_briefing(client, channel: str, thread_ts: str | None) -> None:
    client.chat_postMessage(
        channel=channel,
        text="Running briefing... this takes 5–10 minutes.",
        thread_ts=thread_ts,
    )
    try:
        summary = briefing.run_morning_briefing()
        client.chat_postMessage(
            channel=channel,
            text=summary,
            thread_ts=thread_ts,
        )
    except Exception as e:
        logger.exception("Briefing failed")
        _post_error(client, channel, thread_ts, e)


def _health_status(client, channel: str, thread_ts: str | None) -> None:
    uptime = datetime.now(timezone.utc) - _START_TIME
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes = rem // 60

    # Last git commit
    try:
        git_log = subprocess.run(
            ["git", "log", "-1", "--format=%h %s (%ar)"],
            cwd=config.VAULT_PATH,
            capture_output=True, text=True, timeout=10,
        )
        last_commit = git_log.stdout.strip() or "unknown"
    except Exception:
        last_commit = "unavailable"

    # Disk space on vault drive
    try:
        import shutil
        usage = shutil.disk_usage(config.VAULT_PATH)
        free_gb = usage.free / (1024 ** 3)
        disk = f"{free_gb:.1f} GB free"
    except Exception:
        disk = "unavailable"

    # Unreviewed drafts
    daily_dir = Path(config.VAULT_PATH) / "shared" / "macro" / "daily"
    unreviewed = 0
    if daily_dir.exists():
        for f in daily_dir.glob("*.md"):
            text = f.read_text(encoding="utf-8", errors="ignore")
            if "reviewed: false" in text and "status: draft" in text:
                unreviewed += 1

    # Active setups count
    setups_file = Path(config.VAULT_PATH) / "shared" / "macro" / "setups.md"
    active_setups = 0
    if setups_file.exists():
        for line in setups_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "status: active" in line.lower():
                active_setups += 1

    # Last briefing session
    sessions = claude_runner._load_sessions()
    has_briefing_session = "briefing-daily" in sessions

    msg = (
        f"*Market Research Agent — Health*\n"
        f"• Uptime: {hours}h {minutes}m\n"
        f"• Last commit: {last_commit}\n"
        f"• Disk: {disk}\n"
        f"• Unreviewed drafts: {unreviewed}\n"
        f"• Active setups: {active_setups}\n"
        f"• Briefing session cached: {'yes' if has_briefing_session else 'no'}"
    )
    client.chat_postMessage(channel=channel, text=msg, thread_ts=thread_ts)


# ---------------------------------------------------------------------------
# Catch-all: log every raw event for debugging
# ---------------------------------------------------------------------------

@app.event({"type": "message"})
def handle_all_messages(body, event, client, logger):
    logger.info("RAW MESSAGE EVENT: channel=%s subtype=%s text=%r",
                event.get("channel"), event.get("subtype"), (event.get("text") or "")[:80])
    _dispatch_message(event, client, logger)


# ---------------------------------------------------------------------------
# #inbox — file uploads
# ---------------------------------------------------------------------------

@app.event("file_shared")
def handle_file_shared(event, client, logger):
    file_id = event.get("file_id")
    channel_id = event.get("channel_id")

    if not _is_inbox(channel_id):
        return

    try:
        info = client.files_info(file=file_id)
        file_info = info["file"]
        msg = inbox_handler.handle_file_upload(file_info)
        client.chat_postMessage(channel=channel_id, text=msg)
    except Exception as e:
        logger.exception("inbox file handling failed")
        _post_error(client, channel_id, None, e)


# ---------------------------------------------------------------------------
# Message dispatch (called from handle_all_messages)
# ---------------------------------------------------------------------------

def _dispatch_message(event, client, logger):
    subtype = event.get("subtype")
    if subtype in ("bot_message", "message_changed", "message_deleted", "file_share"):
        return

    channel = event.get("channel", "")
    text = (event.get("text") or "").strip()
    thread_ts = event.get("thread_ts")
    ts = event.get("ts")

    # ------------------------------------------------------------------
    # #inbox — text messages (no file)
    # ------------------------------------------------------------------
    if _is_inbox(channel):
        # Files are handled by file_shared; plain text just gets an ack
        try:
            client.reactions_add(channel=channel, name="thumbsup", timestamp=ts)
        except Exception:
            pass
        return

    # ------------------------------------------------------------------
    # #briefings
    # ------------------------------------------------------------------
    if _is_briefings(channel):
        text_lower = text.lower()

        # Thread reply = correction/review feedback
        if thread_ts and thread_ts != ts:
            try:
                prompt = (
                    f"Review feedback from Aayush on today's briefing:\n\n{text}\n\n"
                    f"Apply all corrections to the daily file. If he approves or rejects proposed setups, "
                    f"update setups.md accordingly (approved setups only). "
                    f"Mark status: final, reviewed: true, add reviewed_at timestamp. "
                    f"Update issuer/sector pages if material. Append to log.md. "
                    f"Commit with format: 'daily: YYYY-MM-DD reviewed — {{one-line summary}}'. "
                    f"Return a short finalization summary for Slack (under 200 words)."
                )
                client.chat_postMessage(
                    channel=channel, text="Applying corrections...", thread_ts=thread_ts
                )
                result = claude_runner.send(
                    prompt=prompt,
                    session_key="briefing-daily",
                    timeout=600,
                )
                client.chat_postMessage(channel=channel, text=result, thread_ts=thread_ts)
            except Exception as e:
                logger.exception("briefings correction failed")
                _post_error(client, channel, thread_ts, e)
            return

        # Top-level: manual briefing trigger
        if any(kw in text_lower for kw in ("run the brief", "run brief", "brief")):
            _trigger_briefing(client, channel, thread_ts=None)
        return

    # ------------------------------------------------------------------
    # #agent — ad-hoc research
    # ------------------------------------------------------------------
    if _is_agent(channel):
        text_lower = text.lower().strip()

        if text_lower == "ping":
            client.chat_postMessage(channel=channel, text="pong", thread_ts=thread_ts or ts)
            return

        if text_lower in ("status", "health", "health check"):
            _health_status(client, channel, thread_ts or ts)
            return

        session_key = f"agent-{thread_ts or ts}"
        reply_ts = thread_ts or ts

        try:
            result = claude_runner.send(
                prompt=text,
                session_key=session_key,
                timeout=600,
            )
            client.chat_postMessage(channel=channel, text=result, thread_ts=reply_ts)
        except Exception as e:
            logger.exception("agent message handling failed")
            _post_error(client, channel, reply_ts, e)
        return


# ---------------------------------------------------------------------------
# App mention — any channel
# ---------------------------------------------------------------------------

@app.event("app_mention")
def handle_mention(event, client, logger):
    channel = event.get("channel", "")
    text = event.get("text", "")
    thread_ts = event.get("thread_ts")
    ts = event.get("ts")

    # Strip the bot mention token
    import re
    clean_text = re.sub(r"<@[A-Z0-9]+>", "", text).strip()
    if not clean_text:
        return

    session_key = f"agent-{thread_ts or ts}"
    reply_ts = thread_ts or ts

    try:
        result = claude_runner.send(
            prompt=clean_text,
            session_key=session_key,
            timeout=600,
        )
        client.chat_postMessage(channel=channel, text=result, thread_ts=reply_ts)
    except Exception as e:
        logger.exception("mention handling failed")
        _post_error(client, channel, reply_ts, e)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Market Research Agent (Socket Mode)")
    handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)
    handler.start()
