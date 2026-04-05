"""
Per-thread task state tracking, persisted to _agent/thread_state.json.

Each Slack thread used for a task gets an entry here so the adapter
can route thread replies to the correct handler with session continuity.
State survives adapter restarts. Entries auto-expire after 7 days of
inactivity.
"""

import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

_STATE_FILE = Path(__file__).resolve().parents[1] / "thread_state.json"
_EXPIRY_DAYS = 7


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load() -> dict:
    if _STATE_FILE.exists():
        try:
            return json.loads(_STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("thread_state: corrupt state file, resetting")
            return {}
    return {}


def _save(state: dict) -> None:
    _STATE_FILE.write_text(
        json.dumps(state, indent=2), encoding="utf-8"
    )


def _prune_expired(state: dict) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=_EXPIRY_DAYS)
    pruned = {}
    for ts, entry in state.items():
        last = entry.get("last_activity", entry.get("created_at", ""))
        try:
            if datetime.fromisoformat(last) > cutoff:
                pruned[ts] = entry
        except (ValueError, TypeError):
            pruned[ts] = entry
    return pruned


def get(thread_ts: str) -> dict | None:
    """Get the state entry for a thread, or None if not tracked."""
    state = _load()
    return state.get(thread_ts)


def create(
    thread_ts: str,
    channel: str,
    task_type: str,
    target: str = "",
    session_key: str | None = None,
    metadata: dict | None = None,
) -> dict:
    """Create a new thread state entry."""
    state = _load()
    entry = {
        "channel": channel,
        "task_type": task_type,
        "target": target,
        "status": "in_progress",
        "session_key": session_key or f"{channel}-{thread_ts}",
        "created_at": _now_iso(),
        "last_activity": _now_iso(),
        "metadata": metadata or {},
    }
    state[thread_ts] = entry
    state = _prune_expired(state)
    _save(state)
    return entry


def update(thread_ts: str, **fields) -> dict | None:
    """Update fields on an existing thread state entry."""
    state = _load()
    entry = state.get(thread_ts)
    if entry is None:
        return None
    entry.update(fields)
    entry["last_activity"] = _now_iso()
    state[thread_ts] = entry
    _save(state)
    return entry


def complete(thread_ts: str) -> None:
    """Mark a thread as complete."""
    update(thread_ts, status="complete")


def abandon(thread_ts: str) -> None:
    """Mark a thread as abandoned."""
    update(thread_ts, status="abandoned")


def list_active(channel: str | None = None) -> list[dict]:
    """List active (non-complete, non-abandoned) thread entries."""
    state = _load()
    active = []
    for ts, entry in state.items():
        if entry.get("status") in ("in_progress", "pending_user"):
            if channel is None or entry.get("channel") == channel:
                active.append({"thread_ts": ts, **entry})
    return active
