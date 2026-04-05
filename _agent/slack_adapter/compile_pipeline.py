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
        f"IMPORTANT: The skill is a MULTI-FILE system, not a single document.\n"
        f"Read the current baseline first:\n"
        f"  - training/_compiled/credit-trading/{current}/SKILL.md (entry point)\n"
        f"  - training/_compiled/credit-trading/{current}/references/ (all files)\n\n"
        f"The current reference files are:\n"
        f"  - references/masters_frameworks.md — mental models from Marks, Klarman, Fridson, etc.\n"
        f"  - references/workflows.md — analytical playbooks (RV, new issue, event-driven, etc.)\n"
        f"  - references/individual_credit_eval.md — three-lens credit evaluation methodology\n"
        f"  - references/ig_sector_map.md — 276 IG issuers across 15 mega-sectors\n\n"
        f"Steps:\n"
        f"1. Read the current skill baseline (SKILL.md + all references/).\n"
        f"2. Read the full training corpus: training/primers/, training/frameworks/, "
        f"training/conversations/, training/post-mortems/. Parse frontmatter.\n"
        f"3. Extract playbooks: find files with contains_playbooks in frontmatter. "
        f"Preserve playbook content structurally — do NOT paraphrase procedures.\n"
        f"4. Apply playbook amendments: scan post-mortems with amends_playbook field, "
        f"apply in date order.\n"
        f"5. Extract declarative content: non-playbook content from all sources.\n"
        f"6. Determine which files need updating based on the new training content:\n"
        f"   - New framework sources → may update masters_frameworks.md\n"
        f"   - New workflow/playbook content → may update workflows.md\n"
        f"   - Credit evaluation methodology changes → may update individual_credit_eval.md\n"
        f"   - Sector coverage changes → may update ig_sector_map.md\n"
        f"   - Persona/reasoning changes → may update SKILL.md\n"
        f"   - Entirely new knowledge domain → may create a NEW reference file\n"
        f"7. Write ALL updated files to training/_compiled/credit-trading/{next_ver}/\n"
        f"   Copy unchanged files from {current}/ so the new version is complete.\n"
        f"   Structure: {next_ver}/SKILL.md + {next_ver}/references/*.md\n"
        f"8. Generate provenance graph at training/_provenance/credit-trading/{next_ver}.md\n"
        f"   Map which training sources influenced which output files.\n"
        f"9. Generate a changelog comparing {next_ver} to {current} — per file.\n"
        f"10. If training/_compiled/credit-trading/canary_questions.md exists, run canary tests.\n"
        f"11. Return a structured summary for Slack:\n"
        f"    - Version and timestamp\n"
        f"    - Summary of changes (new training files, files updated, playbook count)\n"
        f"    - Per-file diff summary (which files changed and how)\n"
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
        f"1. Delete the contents of training/_compiled/credit-trading/current/ entirely.\n"
        f"2. Copy the FULL contents of training/_compiled/credit-trading/{ver}/ "
        f"to training/_compiled/credit-trading/current/ ��� this includes SKILL.md AND "
        f"the entire references/ subdirectory. The current/ directory must be an exact "
        f"mirror of {ver}/.\n"
        f"3. Create a .skill ZIP archive at training/_compiled/credit-trading/current.skill "
        f"containing the current/ folder contents (SKILL.md + references/) — this is the "
        f"portable format for sharing or external loading.\n"
        f"4. If SKILLS_PUBLISH_PATH is set in .env, copy current.skill there.\n"
        f"5. Log the publish to training/_compiled/credit-trading/publish_log.md "
        f"including: version, timestamp, files updated, files unchanged.\n"
        f"6. Commit: 'v2-compile: credit-trading {ver} published'\n"
        f"7. Return confirmation with version, timestamp, list of files in current/, "
        f"and publish path."
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
