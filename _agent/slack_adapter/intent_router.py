"""
Classifies free-form Slack messages by intent and dispatches to the
appropriate handler.

Uses Claude Code for classification with a short prompt; falls back
to keyword matching on parse failure.
"""

import logging
import re

import claude_runner

logger = logging.getLogger(__name__)


class Intent:
    INGESTION = "ingestion"
    TASK = "task"
    QUESTION = "question"
    JOURNAL_ENTRY = "journal_entry"
    RULE_PROPOSAL = "rule_proposal"
    STATUS = "status"
    UNKNOWN = "unknown"


# Keyword patterns for fast fallback classification
_RULE_KEYWORDS = re.compile(
    r"\b(rule\s+propos|propose\s+rule|change\s+rule|amend\s+rule|add\s+rule)\b", re.I
)
_STATUS_KEYWORDS = re.compile(
    r"^(status|health|ping)\s*$", re.I
)
_QUESTION_MARKERS = re.compile(
    r"^(what|how|why|when|where|who|is\s|are\s|do\s|does\s|can\s|could\s|should\s)", re.I
)


def classify(channel_type: str, text: str) -> str:
    """
    Classify a free-form message into an intent.

    For #journal, every message is a journal entry unless it matches
    a command or status keyword. For other channels, uses keyword
    matching with Claude Code fallback for ambiguous cases.
    """
    text_stripped = text.strip()

    if not text_stripped:
        return Intent.UNKNOWN

    # Status keywords — any channel
    if _STATUS_KEYWORDS.match(text_stripped):
        return Intent.STATUS

    # Rule proposal keywords — any channel
    if _RULE_KEYWORDS.search(text_stripped):
        return Intent.RULE_PROPOSAL

    # Channel-specific defaults
    if channel_type == "journal":
        return Intent.JOURNAL_ENTRY

    if channel_type == "training":
        if _RULE_KEYWORDS.search(text_stripped):
            return Intent.RULE_PROPOSAL
        return Intent.QUESTION

    # Research and other channels: try to distinguish task vs question
    if _QUESTION_MARKERS.match(text_stripped):
        return Intent.QUESTION

    # For longer messages that look like they contain instructions
    if len(text_stripped) > 100:
        return Intent.TASK

    # Default: try Claude Code classification for ambiguous cases
    try:
        return _classify_with_claude(channel_type, text_stripped)
    except Exception:
        logger.warning("intent_router: Claude classification failed, defaulting to question")
        return Intent.QUESTION


def _classify_with_claude(channel_type: str, text: str) -> str:
    """Use Claude Code to classify an ambiguous message."""
    prompt = (
        f"Classify this Slack message from the #{channel_type} channel into "
        f"exactly one of: task, question, ingestion, rule_proposal, status.\n\n"
        f"Message: {text[:500]}\n\n"
        f"Reply with ONLY the classification word, nothing else."
    )
    result = claude_runner.send(
        prompt=prompt,
        session_key=f"intent-classify-{channel_type}",
        timeout=30,
    )
    result_lower = result.strip().lower()
    valid = {Intent.TASK, Intent.QUESTION, Intent.INGESTION, Intent.RULE_PROPOSAL, Intent.STATUS}
    if result_lower in valid:
        return result_lower
    return Intent.QUESTION
