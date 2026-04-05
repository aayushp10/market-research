"""
Ledger system — promotion, resolution, revisit-date watching, monthly review.

All ledger operations go through the inference-review pattern.
No direct writes to ledger/open/ or ledger/resolved/.
"""

import logging
from datetime import date, datetime, timezone
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)

_LEDGER_DIR = Path(config.VAULT_PATH) / "ledger"


def detect_and_propose_promotion(source_path: str, source_content: str) -> str | None:
    """
    Scan content for falsifiable predictions. If found, return a
    promotion proposal for posting to #ledger. Returns None if
    no prediction detected.
    """
    prompt = (
        f"Scan this content for falsifiable predictions.\n\n"
        f"Source: {source_path}\n\n"
        f"Content:\n{source_content[:3000]}\n\n"
        f"A prediction is falsifiable if it has ALL THREE:\n"
        f"(a) A specific claim about a market, name, or sector\n"
        f"(b) An expected direction or target\n"
        f"(c) A timeframe\n\n"
        f"If you find a falsifiable prediction, format a promotion proposal:\n"
        f"```\n"
        f"Detected falsifiable prediction in {source_path}:\n"
        f"- prediction: <statement>\n"
        f"- revisit_date: <inferred from timeframe>\n"
        f"- confidence: <inferred or [needs input]>\n"
        f"- domain_path: <inferred from source domain>\n"
        f"- source: [[{source_path}]]\n"
        f"Promote to ledger/open/?\n"
        f"```\n\n"
        f"If NO falsifiable prediction is found, reply with exactly: NO_PREDICTION\n"
        f"Most content does NOT contain predictions — that's fine."
    )

    result = claude_runner.send(
        prompt=prompt,
        session_key=f"ledger-detect-{Path(source_path).stem}",
        timeout=60,
    )

    if "NO_PREDICTION" in result:
        return None
    return result


def finalize_promotion(entry_slug: str) -> str:
    """Write a confirmed promotion to ledger/open/ and commit."""
    prompt = (
        f"Finalize the ledger promotion for: {entry_slug}\n\n"
        f"Write the entry to ledger/open/{date.today().isoformat()}-{entry_slug}.md "
        f"with the confirmed frontmatter.\n"
        f"Commit: 'v2-ledger: promote {entry_slug} from <source>'\n"
        f"Return brief confirmation."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=f"ledger-promote-{entry_slug}",
        timeout=60,
    )


def check_revisit_dates() -> list[dict]:
    """
    Scan ledger/open/ for entries past their revisit_date.
    Returns list of overdue entries.
    """
    open_dir = _LEDGER_DIR / "open"
    if not open_dir.exists():
        return []

    today = date.today()
    overdue = []

    for f in open_dir.glob("*.md"):
        if f.name == ".gitkeep":
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if line.strip().startswith("revisit_date:"):
                revisit_str = line.split(":", 1)[1].strip().strip('"').strip("'")
                try:
                    revisit = date.fromisoformat(revisit_str)
                    if revisit <= today:
                        overdue.append({
                            "path": str(f),
                            "name": f.stem,
                            "revisit_date": revisit_str,
                        })
                except ValueError:
                    pass
                break

    return overdue


def propose_resolution(entry_path: str) -> str:
    """
    Draft a resolution proposal for an overdue entry.
    Returns the proposal for posting to #ledger.
    """
    prompt = (
        f"Resolve the ledger entry at: {entry_path}\n\n"
        f"Read the entry. Pull current market data relevant to the prediction "
        f"(use web search if needed).\n\n"
        f"Draft a resolution with:\n"
        f"- outcome: played_out | partial | wrong | expired | canceled  [inferred]\n"
        f"- delta: <what actually happened vs prediction>  [inferred]\n"
        f"- lessons: [needs input]  — ALWAYS needs input, only Aayush knows\n\n"
        f"Format as a confirmation request for Aayush."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=f"ledger-resolve-{Path(entry_path).stem}",
        timeout=120,
    )


def finalize_resolution(entry_path: str) -> str:
    """Apply confirmed resolution, move to resolved/."""
    prompt = (
        f"Finalize the resolution for: {entry_path}\n\n"
        f"Steps:\n"
        f"1. Add resolved_date, outcome, delta, and lessons to frontmatter.\n"
        f"2. Read domain_path from the entry's frontmatter.\n"
        f"3. Move the file from ledger/open/ to ledger/resolved/<domain_path>/.\n"
        f"4. Commit: 'v2-ledger: resolve <entry-name> — <outcome>'\n"
        f"5. Return brief confirmation."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=f"ledger-resolve-{Path(entry_path).stem}",
        timeout=60,
    )


def list_open(filter_str: str = "") -> str:
    """List open predictions, optionally filtered."""
    prompt = (
        f"List all entries in ledger/open/, sorted by revisit_date (earliest first).\n"
        f"Filter: {filter_str or 'none'}\n"
        f"For each: show prediction, revisit_date, confidence, tickers.\n"
        f"If none, say 'No open predictions.'"
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="ledger-query",
        timeout=60,
    )


def list_resolved(filter_str: str = "") -> str:
    """List resolved predictions, optionally filtered."""
    prompt = (
        f"List entries in ledger/resolved/, optionally filtered.\n"
        f"Filter: {filter_str or 'none'}\n"
        f"For each: show prediction, outcome, resolved_date, tickers.\n"
        f"If none, say 'No resolved entries matching filter.'"
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="ledger-query",
        timeout=60,
    )


def run_monthly_review() -> str:
    """Execute the monthly review ritual."""
    prompt = (
        f"Run the monthly ledger review per ledger/CLAUDE.md.\n\n"
        f"Steps:\n"
        f"1. Read ledger/resolved/ since the last review (check ledger/reviews/ for the latest).\n"
        f"   If no prior review, read all of ledger/resolved/.\n"
        f"2. Compute aggregate stats: total resolved, outcome breakdown, "
        f"win rate by domain, win rate by confidence.\n"
        f"3. Identify patterns: repeated misses, systematic over/underconfidence, "
        f"themes that played out well.\n"
        f"4. Draft the review at ledger/reviews/{datetime.now().strftime('%Y-%m')}-review.md\n"
        f"5. Propose specific post-mortem promotions (only for methodological insights, "
        f"not just situational learning).\n"
        f"6. Return the draft for Aayush's review. Include stats, patterns, "
        f"and proposed promotions."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="ledger-review",
        timeout=300,
    )
