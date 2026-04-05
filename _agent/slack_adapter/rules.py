"""
Rule evolution flow — proposes, tracks, and applies CLAUDE.md changes.

All changes require explicit Slack approval. Never silently edit rules.
Protected rules cannot be weakened (only extended or excepted).
"""

import logging
from datetime import date
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)

_RULE_LOG = Path(config.VAULT_PATH) / "_agent" / "rule_changes.md"

_PROTECTED_RULES = [
    "inference-review pattern",
    "journal append-only discipline",
    "ledger promotion-only discipline",
    "facts/views firewall",
    "provenance requirements",
    "raw source immutability",
    "concept stub lazy-creation rule",
    "copyright quote limits",
]


def draft_proposal(user_text: str) -> str:
    """
    Take a freeform rule change request and draft a formal proposal.
    Returns the formatted proposal for posting to #agent-ops.
    """
    protected_list = "\n".join(f"  - {r}" for r in _PROTECTED_RULES)

    prompt = (
        f"Aayush proposed a rule change:\n\n"
        f'"{user_text}"\n\n'
        f"Draft a formal rule-change proposal per root CLAUDE.md rule evolution flow.\n\n"
        f"Steps:\n"
        f"1. Identify the most likely CLAUDE.md file affected.\n"
        f"2. Find the current rule text (quote it).\n"
        f"3. Draft the proposed change.\n"
        f"4. Check against protected rules. If the proposal would weaken any of these, "
        f"refuse and explain why:\n{protected_list}\n\n"
        f"Format:\n"
        f"```\n"
        f"Rule-change proposal\n"
        f"- File: <path to CLAUDE.md>\n"
        f"- Current rule: <quoted text>\n"
        f"- Proposed change: <new text>\n"
        f"- Reason: <from Aayush's request>\n"
        f"- Triggered by: direct proposal from Aayush\n"
        f"```\n\n"
        f"End with: 'Approve, modify, or reject?'"
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="rule-proposal",
        timeout=60,
    )


def apply_approved_change(file_path: str, change_description: str) -> str:
    """Apply an approved rule change and log it."""
    prompt = (
        f"Apply the approved rule change.\n\n"
        f"File: {file_path}\n"
        f"Change: {change_description}\n\n"
        f"Steps:\n"
        f"1. Read the file.\n"
        f"2. Apply the change.\n"
        f"3. Write the updated file.\n"
        f"4. Commit: 'v2-rules: {file_path} — {change_description[:60]}'\n"
        f"5. Return confirmation."
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key="rule-proposal",
        timeout=60,
    )

    # Log the change
    _log_change(file_path, change_description)

    return result


def _log_change(file_path: str, description: str) -> None:
    """Append to _agent/rule_changes.md."""
    today = date.today().isoformat()
    entry = f"\n## [{today}] {file_path}\n\n{description}\n"

    if _RULE_LOG.exists():
        current = _RULE_LOG.read_text(encoding="utf-8")
    else:
        current = "# Rule Changes Log\n\nChronological record of approved CLAUDE.md changes.\n"

    _RULE_LOG.write_text(current + entry, encoding="utf-8")
    logger.info("rules: logged change to %s", file_path)


def get_change_log() -> str:
    """Return the contents of the rule changes log."""
    if _RULE_LOG.exists():
        return _RULE_LOG.read_text(encoding="utf-8")
    return "No rule changes recorded yet."


def is_protected_weakening(proposal_text: str) -> bool:
    """
    Quick check if a proposal might weaken a protected rule.
    Returns True if it looks like a weakening attempt.
    """
    text_lower = proposal_text.lower()
    weakening_signals = ["remove", "relax", "weaken", "skip", "bypass", "optional"]
    for rule in _PROTECTED_RULES:
        rule_lower = rule.lower()
        if rule_lower in text_lower:
            for signal in weakening_signals:
                if signal in text_lower:
                    return True
    return False
