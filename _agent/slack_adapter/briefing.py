"""
Morning briefing runner.
Called by the scheduler or by a manual "run the brief" command in #briefings.
"""

import logging
from datetime import date

import claude_runner

logger = logging.getLogger(__name__)

_BRIEFING_TIMEOUT = 900  # 15 minutes


def run_morning_briefing() -> str:
    """
    Kick off the morning briefing workflow via Claude Code.
    Returns the summary text for posting to Slack #briefings.
    """
    today = date.today().isoformat()
    prompt = (
        f"Run the morning briefing workflow per CLAUDE.md. "
        f"Today's date: {today}. "
        f"Steps: "
        f"1. Read shared/macro/briefing-scope.md and shared/macro/setups.md and the last 3 daily files. "
        f"2. Process any files in _raw/inbox/ (read each one). "
        f"3. Run 5-10 targeted web searches based on briefing scope, active setups, and inbox material. "
        f"4. Draft the daily file at shared/macro/daily/{today}.md with status: draft, reviewed: false. "
        f"5. Move inbox files to their permanent _raw/ homes. "
        f"6. STOP — do not update setups.md or any issuer/sector pages. "
        f"7. Commit the draft: 'daily: {today} draft — {{one-line summary}}'. "
        f"8. Return a concise Slack summary: top-of-mind tension, key themes covered, "
        f"any proposed setups (not committed), and any gaps flagged. Keep it under 400 words."
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
