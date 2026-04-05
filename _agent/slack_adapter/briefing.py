"""
Morning briefing runner.
Called by the scheduler or by a manual "/brief" command in #briefings.
"""

import logging
from datetime import date

import claude_runner

logger = logging.getLogger(__name__)

_BRIEFING_TIMEOUT = 900  # 15 minutes


def run_morning_briefing(topic: str | None = None) -> str:
    """
    Kick off the morning briefing workflow via Claude Code.
    If topic is provided, runs a scoped briefing on that topic.
    Returns the summary text for posting to Slack #briefings.
    """
    today = date.today().isoformat()

    if topic:
        scope_line = f"Scoped briefing on: {topic}. "
    else:
        scope_line = ""

    prompt = (
        f"Run the morning briefing workflow per CLAUDE.md. "
        f"Today's date: {today}. {scope_line}"
        f"Steps: "
        f"1. Read the credit-trading skill for methodology: "
        f"training/_compiled/credit-trading/current/SKILL.md (read its references/ as needed). "
        f"2. Read research/briefing-scope.md and the last 3 files in research/briefings/. "
        f"3. Read current macro state in research/macro/*. "
        f"4. Process any tagged files in research/_raw/inbox/to-file/ (tagged but not yet filed). "
        f"5. Run 5-10 targeted web searches based on briefing scope and material from inbox. "
        f"6. Draft the daily file at research/briefings/{today}.md with status: draft, reviewed: false. "
        f"7. Update relevant research/macro/* subfolders with dated snapshots of what you covered. "
        f"8. STOP — do not update any issuer/sector pages or promote to ledger. Wait for review. "
        f"9. Commit the draft: 'v2-briefings: {today} draft — {{one-line summary}}'. "
        f"10. Return a concise Slack summary: top-of-mind tension, key themes covered, "
        f"any ledger promotion candidates spotted (not committed), and any gaps flagged. "
        f"Keep it under 400 words."
    )

    logger.info("briefing: starting morning briefing for %s", today)
    try:
        result = claude_runner.send(
            prompt=prompt,
            session_key="briefing-daily",
            timeout=_BRIEFING_TIMEOUT,
        )
        logger.info("briefing: completed for %s", today)
        return result
    except Exception as e:
        logger.error("briefing: failed for %s: %s", today, e)
        raise
