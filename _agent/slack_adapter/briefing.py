"""
Morning briefing runner.
Called by the scheduler or by a manual "/brief" command in #briefings.

Three-phase workflow:
  1. scan_headlines()       — load skill, read scope, web search in 3 tiers
  2. write_briefing()       — draft the daily file from scanned + staged sources
  3. propose_scope_update() — suggest amendments to briefing-scope.md
"""

import logging
from datetime import date

import claude_runner

logger = logging.getLogger(__name__)

_SCAN_TIMEOUT = 600   # 10 minutes — web searches
_WRITE_TIMEOUT = 900  # 15 minutes — writing the briefing
_SCOPE_TIMEOUT = 120  # 2 minutes — scope analysis


def scan_headlines(topic: str | None = None) -> str:
    """
    Phase 1: Load skill, read scope, scan the web for overnight developments.
    Saves fetched sources to research/_raw/inbox/briefing-stage/.
    Returns a summary of what was found.
    """
    today = date.today().isoformat()
    scope_line = f"Scoped briefing on: {topic}. " if topic else ""

    prompt = (
        f"Morning briefing scan phase. Today: {today}. {scope_line}"
        f"Steps:\n"
        f"1. Load the credit-trading skill (auto-load based on topic relevance).\n"
        f"2. Read research/briefing-scope.md — active names, themes, macro factors, "
        f"sector sensitivities.\n"
        f"3. Read the last 3 briefings in research/briefings/ to know what's already covered.\n"
        f"4. Run 8-12 web searches in three tiers:\n\n"
        f"   **Tier 1 — Overnight headline scan (3-4 searches):**\n"
        f"   What actually moved in credit/macro overnight? Search for:\n"
        f"   - Credit/bond market news, IG and HY spreads moves\n"
        f"   - Breaking macro: rates, oil, geopolitics developments since yesterday\n"
        f"   - Any surprise events (downgrades, defaults, M&A, geopolitical shocks)\n\n"
        f"   **Tier 2 — Active name/theme catalyst checks (3-4 searches):**\n"
        f"   One search per active name or theme that has a near-term catalyst.\n"
        f"   Check earnings dates, rating reviews, deal closings, etc.\n\n"
        f"   **Tier 3 — Scope-driven sector/macro scans (2-4 searches):**\n"
        f"   Sector sensitivities from scope: energy sub-industries, bank earnings,\n"
        f"   new issue calendar, ETF flows, CPI/rates data.\n\n"
        f"5. Save useful results to research/_raw/inbox/briefing-stage/ with frontmatter.\n"
        f"   Use descriptive kebab-case filenames, no dates.\n"
        f"   Include source_type, source_name, date_added, as_of_date, tags, tickers, sectors.\n"
        f"6. Return a summary: what's genuinely new today, what's stale/unchanged, "
        f"any gaps you couldn't fill.\n"
        f"Do NOT write the briefing yet — just scan and stage sources."
    )

    logger.info("briefing: scan phase starting for %s", today)
    return claude_runner.send(
        prompt=prompt,
        session_key="briefing-daily",
        timeout=_SCAN_TIMEOUT,
    )


def write_briefing(topic: str | None = None) -> str:
    """
    Phase 2: Write the briefing from scanned + staged sources.
    Returns the summary text for posting to Slack.
    """
    today = date.today().isoformat()
    scope_line = f"Scoped briefing on: {topic}. " if topic else ""

    prompt = (
        f"Write the morning briefing. Today: {today}. {scope_line}"
        f"Steps:\n"
        f"1. Read sources in research/_raw/inbox/briefing-stage/ (freshly fetched).\n"
        f"2. Read any tagged files in research/_raw/inbox/to-file/ (user-dropped material).\n"
        f"3. Read current macro state in research/macro/*.\n"
        f"4. Draft the daily file at research/briefings/briefing-{today}.md with "
        f"status: draft, reviewed: false.\n"
        f"5. Update relevant research/macro/* subfolders with descriptive-prefix snapshots. "
        f"Use the subfolder name as prefix: rates-{today}.md, ig-spreads-{today}.md, "
        f"narrative-{today}.md, oil-{today}.md, etc. Never use bare date-only filenames.\n"
        f"6. Move briefing-stage/ sources to their final research/_raw/ subfolders "
        f"(credit/issuers/, macro/rates/, etc. based on content).\n"
        f"7. STOP — do not update any issuer/sector pages or promote to ledger. "
        f"Wait for review.\n"
        f"8. Commit the draft: 'v2-briefings: {today} draft — {{one-line summary}}'.\n"
        f"9. Return a concise Slack summary: top-of-mind tension, key themes covered, "
        f"any ledger promotion candidates spotted (not committed), and any gaps flagged. "
        f"Keep it under 400 words."
    )

    logger.info("briefing: write phase starting for %s", today)
    return claude_runner.send(
        prompt=prompt,
        session_key="briefing-daily",
        timeout=_WRITE_TIMEOUT,
    )


def propose_scope_update() -> str:
    """
    Phase 3: Propose amendments to briefing-scope.md based on today's scan.
    Runs on the same session so it has full context from phases 1-2.
    Returns the proposal text for Slack.
    """
    prompt = (
        "Review what you found in today's scan and briefing against the current "
        "research/briefing-scope.md. Propose amendments if warranted.\n\n"
        "Consider:\n"
        "- New names that surfaced with material credit events (add to active coverage?)\n"
        "- Themes that have resolved or gone stale (downgrade priority or remove?)\n"
        "- New multi-week themes emerging from Tier 1 headlines (add with priority?)\n"
        "- Macro factors that shifted regime (update description?)\n"
        "- Sector sensitivities that need updating based on new data\n"
        "- Corrections log entry for today's changes\n\n"
        "Format each proposed change as:\n"
        "- **Add**: <section> — <what> — <why>\n"
        "- **Update**: <section> — <what changed> — <why>\n"
        "- **Remove**: <section> — <what> — <why (resolved/stale)>\n"
        "- **Re-prioritize**: <theme #> — <old priority> → <new priority> — <why>\n\n"
        "If nothing warrants a change, say 'No scope changes warranted today.'\n"
        "Do NOT edit briefing-scope.md — just propose. Keep under 200 words."
    )

    logger.info("briefing: scope update proposal phase")
    return claude_runner.send(
        prompt=prompt,
        session_key="briefing-daily",
        timeout=_SCOPE_TIMEOUT,
    )


def run_morning_briefing(topic: str | None = None) -> str:
    """
    Full briefing: scan → write → propose scope updates.
    Returns the write-phase summary (scope proposal posted separately).

    Note: when called from _trigger_briefing() in app.py, the phases
    are called individually with Slack progress updates between them.
    This function is a convenience wrapper for programmatic use.
    """
    today = date.today().isoformat()
    logger.info("briefing: starting full briefing for %s", today)
    scan_headlines(topic)
    result = write_briefing(topic)
    propose_scope_update()
    logger.info("briefing: completed for %s", today)
    return result
