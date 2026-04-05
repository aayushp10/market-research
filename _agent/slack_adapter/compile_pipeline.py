"""
Skill compile pipeline — reads the training corpus, extracts playbooks,
synthesizes declarative content, writes versioned artifacts with provenance,
surfaces diffs for human review, publishes on approval.

Trigger: /compile in #training.
"""

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)

_COMPILE_TIMEOUT = 1200  # 20 minutes — compiles are long
_COMPILED_DIR = Path(config.VAULT_PATH) / "training" / "_compiled" / "credit-trading"
_PROVENANCE_DIR = Path(config.VAULT_PATH) / "training" / "_provenance" / "credit-trading"


def get_current_version() -> str:
    """Read the current version from the latest directory in _compiled/."""
    versions = sorted(
        [d.name for d in _COMPILED_DIR.iterdir()
         if d.is_dir() and d.name.startswith("v") and d.name != "current"],
        key=lambda v: float(v[1:]) if v[1:].replace(".", "").isdigit() else 0,
    )
    return versions[-1] if versions else "v1.0"


def get_next_version() -> str:
    """Compute the next version number."""
    current = get_current_version()
    major, minor = current[1:].split(".")
    return f"v{major}.{int(minor) + 1}"


def check_status() -> str:
    """Report compile status: new files since last compile, recommendation."""
    training_root = Path(config.VAULT_PATH) / "training"
    content_dirs = ["primers", "frameworks", "conversations", "post-mortems"]

    total_files = 0
    for d in content_dirs:
        dir_path = training_root / d
        if dir_path.exists():
            total_files += len([f for f in dir_path.glob("*.md") if f.name != ".gitkeep"])

    current = get_current_version()

    # Check provenance for last compile date
    prov_file = _PROVENANCE_DIR / f"{current}.md"
    last_compile = "unknown"
    if prov_file.exists():
        text = prov_file.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if line.startswith("created:"):
                last_compile = line.split(":", 1)[1].strip()
                break

    recommend = ""
    if total_files >= 5:
        recommend = "Recommended: 5+ new training files since last compile."
    elif total_files > 0:
        recommend = f"{total_files} training file(s) — compile possible but corpus is thin."
    else:
        recommend = "No training files yet. Compile would be a no-op."

    return (
        f"*Compile Status*\n"
        f"• Current version: {current}\n"
        f"• Last compile: {last_compile}\n"
        f"• Training files in corpus: {total_files}\n"
        f"  - primers/: {len(list((training_root / 'primers').glob('*.md'))) - (1 if (training_root / 'primers' / '.gitkeep').exists() else 0)}\n"
        f"  - frameworks/: {len(list((training_root / 'frameworks').glob('*.md'))) - (1 if (training_root / 'frameworks' / '.gitkeep').exists() else 0)}\n"
        f"  - conversations/: {len(list((training_root / 'conversations').glob('*.md'))) - (1 if (training_root / 'conversations' / '.gitkeep').exists() else 0)}\n"
        f"  - post-mortems/: {len(list((training_root / 'post-mortems').glob('*.md'))) - (1 if (training_root / 'post-mortems' / '.gitkeep').exists() else 0)}\n"
        f"• {recommend}"
    )


def run_compile() -> str:
    """
    Execute the full compile pipeline. Returns the summary for Slack.
    The summary includes diff and canary results for review.
    """
    current = get_current_version()
    next_ver = get_next_version()

    prompt = (
        f"Run the skill compile pipeline per training/CLAUDE.md and root CLAUDE.md.\n\n"
        f"Current version: {current}\n"
        f"Target version: {next_ver}\n\n"
        f"Steps:\n"
        f"1. Read the full training corpus: training/primers/, training/frameworks/, "
        f"training/conversations/, training/post-mortems/. Parse frontmatter.\n"
        f"2. Extract playbooks: find files with contains_playbooks in frontmatter. "
        f"Preserve playbook content structurally — do NOT paraphrase procedures.\n"
        f"3. Apply playbook amendments: scan post-mortems with amends_playbook field, "
        f"apply in date order.\n"
        f"4. Extract declarative content: non-playbook content from all sources.\n"
        f"5. Synthesize the compiled skill with sections: Philosophy/judgment, "
        f"Market mechanics, Concepts reference, Playbooks, Anti-patterns.\n"
        f"6. Write to training/_compiled/credit-trading/{next_ver}/SKILL.md\n"
        f"7. Generate provenance graph at training/_provenance/credit-trading/{next_ver}.md\n"
        f"8. Generate a changelog comparing {next_ver} to {current}.\n"
        f"9. If training/_compiled/credit-trading/canary_questions.md exists, run canary tests.\n"
        f"10. Return a structured summary for Slack:\n"
        f"    - Version and timestamp\n"
        f"    - Summary of changes (new training files, playbook count, anti-pattern count)\n"
        f"    - Diff summary (sections added/removed/modified)\n"
        f"    - Canary test results (if applicable)\n"
        f"    - Instructions: '/compile approve' or '/compile reject'"
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="compile-pipeline",
        timeout=_COMPILE_TIMEOUT,
    )


def approve(version: str | None = None) -> str:
    """Approve and publish a compiled version."""
    ver = version or get_next_version()
    ver_dir = _COMPILED_DIR / ver

    if not ver_dir.exists():
        return f"Version {ver} not found in _compiled/. Nothing to approve."

    prompt = (
        f"Approve and publish credit-trading {ver}.\n\n"
        f"Steps:\n"
        f"1. Copy contents of training/_compiled/credit-trading/{ver}/ "
        f"to training/_compiled/credit-trading/current/ (overwrite).\n"
        f"2. Create a .skill ZIP archive at training/_compiled/credit-trading/current.skill "
        f"containing the current/ folder contents (SKILL.md + references/) — this is the "
        f"portable format for sharing or external loading.\n"
        f"3. If SKILLS_PUBLISH_PATH is set in .env, copy current.skill there.\n"
        f"4. Log the publish to training/_compiled/credit-trading/publish_log.md.\n"
        f"5. Commit: 'v2-compile: credit-trading {ver} published'\n"
        f"6. Return confirmation with version, timestamp, and publish path."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="compile-pipeline",
        timeout=120,
    )


def reject(version: str | None = None, reason: str = "") -> str:
    """Reject a compiled version. Keeps it in history but doesn't publish."""
    ver = version or get_next_version()
    ver_dir = _COMPILED_DIR / ver

    if not ver_dir.exists():
        return f"Version {ver} not found. Nothing to reject."

    prompt = (
        f"Reject credit-trading {ver}.\n\n"
        f"Steps:\n"
        f"1. Write rejection reason to training/_compiled/credit-trading/{ver}/rejected.md\n"
        f"   Reason: {reason or '[no reason provided]'}\n"
        f"2. Do NOT repoint current. Do NOT publish.\n"
        f"3. Commit: 'v2-compile: credit-trading {ver} rejected'\n"
        f"4. Return confirmation."
    )

    return claude_runner.send(
        prompt=prompt,
        session_key="compile-pipeline",
        timeout=60,
    )


def should_nudge() -> bool:
    """Check whether to nudge Aayush about compiling."""
    training_root = Path(config.VAULT_PATH) / "training"
    content_dirs = ["primers", "frameworks", "conversations", "post-mortems"]

    total = 0
    for d in content_dirs:
        dir_path = training_root / d
        if dir_path.exists():
            total += len([f for f in dir_path.glob("*.md") if f.name != ".gitkeep"])

    return total >= 5
