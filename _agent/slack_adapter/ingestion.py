"""
Implements the inference-review pattern for file ingestion.

Handles training sources (via #training) and research sources (via #research).
Each ingestion goes through: propose → confirm/correct → diff → file → commit.
"""

import logging
import re
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)


def propose_frontmatter(file_path: str, inbox_type: str) -> str:
    """
    Read a file and use Claude Code to infer frontmatter with confidence
    markers. Returns the formatted proposal text for posting to Slack.

    inbox_type: "research" or "training"
    """
    vault = config.VAULT_PATH
    rel_path = str(Path(file_path).relative_to(vault))

    if inbox_type == "training":
        field_spec = (
            "Required: source_type (closed vocab: primer, framework, memo, paper, "
            "book, book_chapter, transcript, podcast_notes, call_notes, "
            "claude_conversation, post_mortem), author, date_added, origin, tags.\n"
            "Optional: date_published, trust_weight (high|medium|low, defaults: "
            "primers/frameworks/post-mortems=high, conversations=medium), "
            "supersedes, contains_playbooks, amends_playbook, change_type, "
            "new_step_order, rationale."
        )
    else:
        field_spec = (
            "Required: source_type (closed vocab: filing, earnings_release, "
            "news_article, research_report, trace_data, market_data, "
            "press_release, court_doc, rating_action, transcript, web_page, "
            "other), source_name, date_added, as_of_date, tags, tickers, sectors.\n"
            "Optional: publisher, author, supersedes, paywalled, url."
        )

    prompt = (
        f"You are running an ingestion inference-review for a {inbox_type} source.\n\n"
        f"File: {rel_path}\n\n"
        f"Read the file. Infer as many frontmatter fields as possible.\n"
        f"Fields spec:\n{field_spec}\n\n"
        f"For each field, mark confidence: [inferred], [guess], or [needs input].\n"
        f"Include a 3-sentence summary for disambiguation.\n"
        f"Format the output as a clean YAML block with inline confidence markers.\n"
        f"End with: 'Confirm, correct, or extend?'"
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{Path(file_path).stem}",
        timeout=120,
    )
    return result


def apply_correction(file_path: str, inbox_type: str, original_proposal: str, user_reply: str) -> str:
    """
    Parse freeform user reply against the original proposal, apply
    corrections, and return the updated proposal with a diff summary.
    """
    prompt = (
        f"You previously proposed this frontmatter for a {inbox_type} source:\n\n"
        f"{original_proposal}\n\n"
        f"Aayush replied with:\n{user_reply}\n\n"
        f"Apply all corrections. Show a brief diff: 'Updated: X, Y. Unchanged: Z.'\n"
        f"Then show the final YAML frontmatter block (no confidence markers — all confirmed).\n"
        f"End with: 'Confirm final version?'"
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{Path(file_path).stem}",
        timeout=60,
    )
    return result


def finalize_and_file(file_path: str, inbox_type: str) -> str:
    """
    Write confirmed frontmatter into the file (or create a sidecar for
    binary files), move from to-tag/ → to-file/ → final content folder,
    and commit with a descriptive message.

    Returns a confirmation message for Slack.
    """
    vault = config.VAULT_PATH
    rel_path = str(Path(file_path).relative_to(vault))

    prompt = (
        f"Finalize the ingestion for: {rel_path}\n\n"
        f"Steps:\n"
        f"1. Write the confirmed frontmatter into the file (for markdown) or "
        f"create a sidecar .md file next to it (for PDFs/images/binary files).\n"
        f"2. Move the file from its current inbox location to the correct "
        f"content folder based on the frontmatter tags and source type.\n"
        f"3. Git commit with message format: 'v2-ingest: <source-name> <date> — "
        f"{inbox_type} raw filed'\n"
        f"4. Return a brief confirmation: the final path, key frontmatter fields, "
        f"and the commit hash. Keep it under 100 words."
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ingest-{inbox_type}-{Path(file_path).stem}",
        timeout=120,
    )
    return result


def format_file_ack(filename: str, size_kb: int, inbox_type: str) -> str:
    """Format the initial acknowledgment message when a file is received."""
    inbox_path = (
        "training/inbox/to-tag/" if inbox_type == "training"
        else "research/_raw/inbox/to-tag/"
    )
    return (
        f"Received `{filename}` ({size_kb} KB) → `{inbox_path}`\n"
        f"Running inference-review..."
    )
