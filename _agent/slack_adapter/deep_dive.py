"""
Deep dive agent — produces practitioner-grade research memos on demand.

Trigger: /dive <ticker|topic> in #research, or free-form intent.
Execution: scope → source check → optional web search → write → commit.
"""

import logging
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)

_FETCH_TIMEOUT = 600  # 10 minutes — web searches + save
_DIVE_TIMEOUT = 900   # 15 minutes — writing the deep dive


def scope_dive(target: str, session_key: str | None = None) -> str:
    """
    Propose the scope of a deep dive. Returns the proposal text
    for posting to a Slack thread for Aayush's confirmation.
    """
    prompt = (
        f"You are starting a deep dive on: {target}\n\n"
        f"Apply the credit-trading skill's methodology — it should auto-load based on "
        f"topic relevance. If the target is a BDC, the bdc-knowledge skill should also load.\n\n"
        f"Per research/CLAUDE.md deep dive discipline:\n\n"
        f"1. Determine the target artifact path:\n"
        f"   - If an issuer page exists at research/credit/issuers/, propose updating it\n"
        f"   - If not, propose creating it using the appropriate template from research/_templates/\n"
        f"   - For situations/themes, use research/credit/special-situations/ or research/credit/themes/\n\n"
        f"2. Search research/_raw/ for existing sources related to {target}. List what you find.\n\n"
        f"3. Assess whether web search is needed:\n"
        f"   - If fewer than 3 relevant sources, or all >30 days old, propose specific search queries\n"
        f"   - Otherwise note existing sources are sufficient\n\n"
        f"4. List concept stubs you expect to invoke (check concepts/ for existing ones).\n\n"
        f"5. Post the scope proposal. Format:\n"
        f"   - Target: <artifact path>\n"
        f"   - Existing sources: <list or 'none'>\n"
        f"   - Web search needed: <yes/no, with proposed queries if yes>\n"
        f"   - Concepts: <list of concepts to invoke, noting which stubs exist vs need creation>\n"
        f"   - Estimated sections: <what the dive will cover>\n\n"
        f"Wait for confirmation before proceeding."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=session_key or f"dive-{target.lower().replace(' ', '-')}",
        timeout=300,
    )


def fetch_sources(target: str, session_key: str | None = None) -> str:
    """
    Phase 1: Run the web searches proposed in the scope step.
    Saves fetched content to research/_raw/inbox/to-tag/.
    Returns a summary of what was fetched.
    """
    prompt = (
        f"Run the web searches you proposed in the scope for {target}.\n\n"
        f"For each search result:\n"
        f"1. Fetch the content\n"
        f"2. Save to research/_raw/inbox/to-tag/ with a descriptive kebab-case "
        f"filename (no dates, no timestamps)\n"
        f"3. Create frontmatter with origin: web-fetched-during-deep-dive, "
        f"plus source_type, source_name, date_added, as_of_date, tags, tickers, sectors\n\n"
        f"Do NOT write the deep dive yet. Only fetch and save sources.\n"
        f"Return a brief summary: how many sources fetched, their filenames, "
        f"and any searches that failed or returned no useful content."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=session_key or f"dive-{target.lower().replace(' ', '-')}",
        timeout=_FETCH_TIMEOUT,
    )


def execute_dive(target: str, session_key: str | None = None) -> str:
    """
    Phase 2: Write the deep dive from existing/fetched sources.
    Returns the completion summary for Slack.
    """
    prompt = (
        f"Now write the deep dive on: {target}\n\n"
        f"Sources have been fetched (or already existed). Write the artifact.\n\n"
        f"Rules (from research/CLAUDE.md and root CLAUDE.md):\n"
        f"1. Apply the credit-trading skill's methodology (auto-loaded). "
        f"If this is a BDC, the bdc-knowledge skill should also be active.\n"
        f"2. Read all relevant raw sources in research/_raw/.\n"
        f"3. Read related concept stubs in concepts/.\n"
        f"4. Read current macro state from research/macro/ if relevant.\n"
        f"5. Write the deep dive using the appropriate template.\n"
        f"6. EVERY claim must cite a specific raw source via wikilink. No claims without citations.\n"
        f"   For seeded content without raw sources, use: [from prior conversation — no raw source available]\n"
        f"7. Enforce the facts/views firewall: facts on issuer pages, views on situations/themes.\n"
        f"8. Create concept stubs inline for any invoked concept that lacks a stub.\n"
        f"   Post a brief notification for each new stub.\n"
        f"9. End with: ## Confidence and what would change my mind\n"
        f"10. Link bidirectionally: add issuer_page: \"[[research/credit/issuers/TICKER]]\" "
        f"to the deep dive's frontmatter. Then update the issuer page's ## Views section "
        f"with a wikilink to this deep dive. If the issuer page doesn't exist yet, "
        f"create it from research/_templates/issuer-credit.md first.\n"
        f"11. Commit: 'v2-research: deep dive on {target} — <summary>'\n"
        f"12. Return a summary: artifact path, key conclusions, concepts invoked, sources cited.\n"
        f"    Keep under 300 words."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=session_key or f"dive-{target.lower().replace(' ', '-')}",
        timeout=_DIVE_TIMEOUT,
    )


def propose_web_search(target: str, existing_sources: int, oldest_days: int,
                       session_key: str | None = None) -> str:
    """
    Generate a web search proposal when existing sources are insufficient.
    """
    prompt = (
        f"For the deep dive on {target}, existing raw sources are insufficient:\n"
        f"  - Found: {existing_sources} relevant sources\n"
        f"  - Oldest: {oldest_days} days old\n\n"
        f"Propose 3-8 targeted web search queries. Prefer primary sources:\n"
        f"SEC filings, company releases, rating agency notes, Bloomberg, Reuters, WSJ, FT.\n\n"
        f"Format:\n"
        f"I'd like to search for:\n"
        f"1. <query> — looking for <what>\n"
        f"2. <query> — looking for <what>\n"
        f"...\n"
        f"Proceed with these searches?"
    )

    return claude_runner.send(
        prompt=prompt,
        session_key=session_key or f"dive-{target.lower().replace(' ', '-')}",
        timeout=60,
    )
