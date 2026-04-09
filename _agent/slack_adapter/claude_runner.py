"""
Wraps Claude Code subprocess invocation with session continuity.

Session IDs are persisted to _agent/sessions.json so conversations
survive adapter restarts. Session keys:
  briefing-daily       — morning briefing conversation
  inbox-ingest         — file ingestion
  agent-{thread_ts}    — ad-hoc threads in #agent, one per Slack thread
"""

import json
import logging
import subprocess
from pathlib import Path

import config

logger = logging.getLogger(__name__)

_SESSIONS_FILE = Path(__file__).resolve().parents[1] / "sessions.json"
_DEFAULT_TIMEOUT = 600   # 10 minutes
_BRIEFING_TIMEOUT = 900  # 15 minutes


def _load_sessions() -> dict:
    if _SESSIONS_FILE.exists():
        try:
            return json.loads(_SESSIONS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_sessions(sessions: dict) -> None:
    _SESSIONS_FILE.write_text(
        json.dumps(sessions, indent=2), encoding="utf-8"
    )


def send(prompt: str, session_key: str, timeout: int = _DEFAULT_TIMEOUT) -> str:
    """
    Send a prompt to Claude Code running in the vault directory.
    Returns the text output on success; raises RuntimeError on failure.
    """
    sessions = _load_sessions()
    session_id = sessions.get(session_key)

    cmd = [config.CLAUDE_PATH, "--dangerously-skip-permissions",
           "--output-format", "json"]

    if session_id:
        cmd += ["--resume", session_id]

    cmd += ["--print", prompt]

    logger.info("claude_runner: key=%s resume=%s", session_key, session_id or "new")

    try:
        result = subprocess.run(
            cmd,
            cwd=config.VAULT_PATH,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"Claude Code timed out after {timeout}s for session '{session_key}'"
        )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(
            f"Claude Code exited {result.returncode} for session '{session_key}': {stderr}"
        )

    output = result.stdout.strip()

    # Parse JSON response to extract result text and session ID
    try:
        data = json.loads(output)
        clean_output = data.get("result", "")
        new_session_id = data.get("session_id")
        is_error = data.get("is_error", False)
    except json.JSONDecodeError:
        logger.warning("claude_runner: failed to parse JSON, using raw output")
        clean_output = output
        new_session_id = None
        is_error = False

    if is_error:
        raise RuntimeError(
            f"Claude Code error for session '{session_key}': {clean_output}"
        )

    if new_session_id and new_session_id != session_id:
        sessions[session_key] = new_session_id
        _save_sessions(sessions)
        logger.info("claude_runner: saved session_id=%s for key=%s", new_session_id, session_key)

    return clean_output


def clear_session(session_key: str) -> None:
    """Remove a stored session ID, forcing a fresh conversation next time."""
    sessions = _load_sessions()
    if session_key in sessions:
        del sessions[session_key]
        _save_sessions(sessions)
        logger.info("claude_runner: cleared session for key=%s", session_key)
