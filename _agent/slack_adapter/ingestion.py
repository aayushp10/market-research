"""
Implements the inference-review pattern for file and message ingestion.

Three ingestion paths:
  - Training: files dropped in #training → training/inbox/to-tag/
  - Research: files dropped in #research → research/_raw/inbox/to-tag/
  - Journal: text messages in #journal → journal/entries/

Each path follows the inference-review pattern:
  propose → user confirms/corrects → diff → finalize → commit

Also handles rate limiting (>5 files in 2 minutes → batch offer)
and ambiguity (one follow-up, then flag).
"""

import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

_recent_uploads: list[float] = []
_RATE_WINDOW = 120  # seconds
_RATE_THRESHOLD = 5


def check_rate_limit() -> bool:
    """
    Returns True if rate limit is exceeded (>5 files in 2 minutes).
    Caller should offer batch processing to the user.
    """
    now = time.time()
    _recent_uploads.append(now)
    # Prune old entries
    while _recent_uploads and _recent_uploads[0] < now - _RATE_WINDOW:
        _recent_uploads.pop(0)
    return len(_recent_uploads) > _RATE_THRESHOLD


def format_batch_offer(count: int) -> str:
    return (
        f"{count} files received in the last 2 minutes. "
        f"Process individually or apply a shared template?\n"
        f"Reply `individual` or `batch <template notes>`."
    )


# ---------------------------------------------------------------------------
# Training ingestion
# ---------------------------------------------------------------------------

_TRAINING_FIELDS = """Required frontmatter fields:
- source_type [REQUIRED, closed vocab]: primer, framework, memo, paper, book, book_chapter, transcript, podcast_notes, call_notes, claude_conversation, post_mortem
- author [REQUIRED]: person or organization who wrote/spoke this
- date_added [REQUIRED]: today's date (when added to training corpus)
- origin [REQUIRED]: where Aayush got it (book, conversation, podcast, paper, etc.)
- tags [REQUIRED]: topical tags for filtering, e.g. [cycles, risk, distressed, bdc, valuation]

Optional frontmatter fields:
- date_published: when originally published
- trust_weight: high | medium | low (defaults: primers/frameworks/post-mortems=high, conversations=medium)
- supersedes: path to an older version this replaces
- contains_playbooks: [list of playbook names] — CRITICAL for procedural content
- amends_playbook: playbook name this post-mortem amends
- change_type: refine | reorder | add_step | remove_step (required if amends_playbook is set)
- new_step_order: [...] (required if change_type is reorder)
- rationale: why this amendment is needed (required on post-mortems that amend playbooks)"""


_RESEARCH_FIELDS = """Required frontmatter fields:
- source_type [REQUIRED, closed vocab]: filing, earnings_release, news_article, research_report, trace_data, market_data, press_release, court_doc, rating_action, transcript, web_page, other
- source_name [REQUIRED]: human-readable name (e.g. "Citi IG Weekly Snapshot")
- date_added [REQUIRED]: today's date
- as_of_date [REQUIRED]: when the data in the source was captured — CRITICAL for time-sensitive material
- tags [REQUIRED]: topical tags
- tickers [REQUIRED]: list of tickers mentioned, can be empty []
- sectors [REQUIRED]: list of sectors, can be empty []

Optional frontmatter fields:
- publisher: organization that published this
- author: person or desk
- supersedes: path to older version
- paywalled: true/false
- url: if web-fetched"""


_JOURNAL_FIELDS = """Required frontmatter fields:
- date [REQUIRED]: defaults to today
- entry_type [REQUIRED, closed vocab]: trade, conversation, reading, observation, daily, other
- tickers [REQUIRED]: list of tickers mentioned, can be empty []
- sectors [REQUIRED]: list of sectors, can be empty []
- tags [REQUIRED]: topical tags
- links [REQUIRED]: wikilinks to related entries or research artifacts, can be empty []"""


# ---------------------------------------------------------------------------
# Proposal generation
# ---------------------------------------------------------------------------

def propose_frontmatter(file_path: str, inbox_type: str) -> str:
    """
    Read a file and use Claude Code to infer frontmatter with confidence
    markers. Returns the formatted proposal text for posting to Slack.

    inbox_type: "research" or "training"
    """
    vault = config.VAULT_PATH
    rel_path = str(Path(file_path).relative_to(vault))

    field_spec = _TRAINING_FIELDS if inbox_type == "training" else _RESEARCH_FIELDS

    prompt = (
        f"You are running an ingestion inference-review for a {inbox_type} source.\n\n"
        f"File: {rel_path}\n\n"
        f"Read the file. Infer as many frontmatter fields as possible from its content.\n\n"
        f"{field_spec}\n\n"
        f"For EVERY field, mark your confidence:\n"
        f"  [inferred] — you're confident, with specific reasoning available on request\n"
        f"  [guess] — educated guess, could easily be wrong\n"
        f"  [needs input] — cannot determine from available material\n\n"
        f"Format your response as:\n"
        f"1. A 3-sentence summary of what this source is, for disambiguation.\n"
        f"2. A clean YAML block with inline confidence markers as comments.\n"
        f"3. End with: 'Confirm, correct, or extend?'\n\n"
        f"Be honest about confidence. If you can see the author's name on the document, "
        f"that's [inferred]. If you're guessing the source_type from format cues, say [guess]. "
        f"If origin is unknowable from the file alone, say [needs input]."
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{Path(file_path).stem}",
        timeout=120,
    )
    return result


def propose_journal_entry(message_text: str) -> str:
    """
    Infer journal entry frontmatter from a Slack message.
    Returns the formatted proposal for confirmation.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    prompt = (
        f"You are running an ingestion inference-review for a journal entry.\n\n"
        f"Aayush posted this message in #journal:\n\n"
        f'"""\n{message_text}\n"""\n\n'
        f"Today's date: {today}\n\n"
        f"{_JOURNAL_FIELDS}\n\n"
        f"Infer all fields from the message content. Mark confidence on each:\n"
        f"  [inferred] — confident from the text\n"
        f"  [guess] — educated guess\n"
        f"  [needs input] — can't determine\n\n"
        f"Format your response as:\n"
        f"1. The proposed YAML frontmatter block with confidence markers.\n"
        f"2. The original message preserved as the entry body.\n"
        f"3. A proposed filename: journal/entries/{today}-<short-slug>.md\n"
        f"4. End with: 'Confirm, correct, or extend?'\n\n"
        f"Common inference patterns:\n"
        f"- 'Put on a long' / 'bought' / 'sold' → entry_type: trade\n"
        f"- 'Talked to' / 'heard from' → entry_type: conversation\n"
        f"- 'Reading' / 'article says' → entry_type: reading\n"
        f"- 'Noticed' / 'watching' / 'seems like' → entry_type: observation\n"
        f"- Extract ticker symbols (uppercase 1-5 letter words that look like tickers)\n"
        f"- Extract sectors from context (bdc, ig, hy, energy, banks, etc.)"
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-journal-{today}",
        timeout=60,
    )
    return result


# ---------------------------------------------------------------------------
# Correction and finalization
# ---------------------------------------------------------------------------

def apply_correction(file_path_or_slug: str, inbox_type: str, user_reply: str) -> str:
    """
    Parse freeform user reply against the previous proposal, apply
    corrections, and return an updated proposal with a diff summary.

    The Claude Code session maintains context from the proposal step,
    so we just send the user's reply as a continuation.
    """
    stem = Path(file_path_or_slug).stem if "/" in file_path_or_slug else file_path_or_slug

    prompt = (
        f"Aayush replied to the ingestion proposal:\n\n{user_reply}\n\n"
        f"Apply all corrections to the proposed frontmatter.\n"
        f"Show a brief diff: 'Updated: X, Y. Unchanged: Z.'\n"
        f"Then show the final YAML frontmatter (no confidence markers — all confirmed).\n"
        f"End with: 'Confirm final version?'"
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{stem}",
        timeout=60,
    )
    return result


def finalize_and_file(file_path_or_slug: str, inbox_type: str) -> str:
    """
    Write confirmed frontmatter, move file to final location, commit.
    Returns a confirmation message for Slack.

    For training/research: moves from to-tag/ → final content folder.
    For journal: writes the entry file to journal/entries/.
    """
    stem = Path(file_path_or_slug).stem if "/" in file_path_or_slug else file_path_or_slug

    if inbox_type == "journal":
        prompt = (
            f"Finalize the journal entry.\n\n"
            f"Steps:\n"
            f"1. Write the confirmed entry (frontmatter + body) to the proposed "
            f"journal/entries/ path.\n"
            f"2. Git commit: 'v2-journal: <date> <entry_type> — <one-line summary>'\n"
            f"3. Return a brief confirmation: file path, entry_type, tickers. "
            f"Under 50 words.\n\n"
            f"After filing, also check: does this entry contain a falsifiable prediction? "
            f"A prediction needs: (a) specific claim about a market/name/sector, "
            f"(b) expected direction or target, (c) a timeframe. "
            f"If yes, note it — a ledger promotion proposal will follow separately."
        )
    else:
        vault = config.VAULT_PATH
        if inbox_type == "training":
            dest_desc = (
                "the correct training subfolder (primers/, frameworks/, "
                "conversations/, or post-mortems/) based on source_type"
            )
        else:
            dest_desc = (
                "the correct research/_raw/ subfolder based on source_type, "
                "tickers, and sectors"
            )

        prompt = (
            f"Finalize the ingestion.\n\n"
            f"Steps:\n"
            f"1. Write the confirmed frontmatter into the file (for markdown) or "
            f"create a sidecar .md file next to it (for PDFs/images/binary).\n"
            f"2. Move the file from its current inbox location to {dest_desc}.\n"
            f"3. Make sure to-tag/ is empty for this file after the move.\n"
            f"4. Git commit: 'v2-ingest: <source-name> <date> — {inbox_type} raw filed'\n"
            f"5. Return a brief confirmation: final path, key fields, commit hash. "
            f"Under 80 words."
        )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{stem}",
        timeout=120,
    )
    return result


def flag_ambiguous(file_path: str, inbox_type: str, issue: str) -> str:
    """
    Mark a file as needing manual attention when inference-review
    can't resolve after one follow-up.
    """
    vault = config.VAULT_PATH
    flag_path = Path(file_path).with_name(Path(file_path).stem + "_flagged.md")
    rel_flag = str(flag_path.relative_to(vault))

    prompt = (
        f"The ingestion for {Path(file_path).name} could not be resolved "
        f"after one clarifying follow-up.\n\n"
        f"Issue: {issue}\n\n"
        f"Create a flag file at {rel_flag} explaining the issue. "
        f"Leave the original file in to-tag/. "
        f"Return a brief message for Slack explaining the file needs manual attention."
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{Path(file_path).stem}",
        timeout=60,
    )
    return result
