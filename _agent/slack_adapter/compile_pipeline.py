"""
Skill compile pipeline — reads the training corpus, extracts playbooks,
synthesizes declarative content, writes versioned artifacts with provenance,
surfaces diffs for human review, publishes on approval.

Trigger: /compile in #training.
"""

import json
import logging
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import claude_runner
import config

logger = logging.getLogger(__name__)

_COMPILE_TIMEOUT = 1200  # 20 minutes — compiles are long
_COMPILED_DIR = Path(config.VAULT_PATH) / "training" / "_compiled" / "credit-trading"
_PROVENANCE_DIR = Path(config.VAULT_PATH) / "training" / "_provenance" / "credit-trading"


def _parse_version(v: str) -> tuple[int, int]:
    """Parse 'v1.2' -> (1, 2). Returns (0, 0) for invalid."""
    try:
        major, minor = v[1:].split(".")
        return (int(major), int(minor))
    except (ValueError, IndexError):
        return (0, 0)


def get_current_version() -> str:
    versions = [
        d.name for d in _COMPILED_DIR.iterdir()
        if d.is_dir() and d.name.startswith("v") and d.name != "current"
    ]
    if not versions:
        return "v1.0"
    return max(versions, key=_parse_version)


def get_next_version() -> str:
    major, minor = _parse_version(get_current_version())
    return f"v{major}.{minor + 1}"


# ---------------------------------------------------------------------------
# Canary testing
# ---------------------------------------------------------------------------

_CANARY_FILE = _COMPILED_DIR / "canary_questions.md"
_CANARY_RESULTS = _COMPILED_DIR / "canary_results.json"


def _parse_canaries() -> list[dict]:
    """Parse canary_questions.md into [{q, required: [...]}]."""
    if not _CANARY_FILE.exists():
        return []
    text = _CANARY_FILE.read_text(encoding="utf-8")
    blocks = re.split(r"\n## ", text)
    canaries = []
    for block in blocks[1:]:  # skip header
        q_match = re.search(r"Q:\s*(.+)", block)
        r_match = re.search(r"Required:\s*(.+)", block)
        if q_match and r_match:
            required = [
                s.strip().strip('"').lower()
                for s in r_match.group(1).split(",")
            ]
            canaries.append({"q": q_match.group(1).strip(), "required": required})
    return canaries


def run_canaries(version: str) -> dict:
    """
    Run every canary against the specified compiled version.
    Each canary is asked in its own Claude session, pinned to the version
    directory, to prevent cross-contamination between questions.
    Returns {pass: bool, results: [...], version, timestamp}.
    """
    canaries = _parse_canaries()
    if not canaries:
        return {"pass": True, "results": [], "note": "no canary file — gate skipped"}

    ver_dir = _COMPILED_DIR / version
    if not ver_dir.exists():
        return {"pass": False, "results": [], "note": f"version dir {version} not found"}

    results = []

    for i, c in enumerate(canaries):
        prompt = (
            f"Answer this question using ONLY the credit-trading skill at "
            f"{ver_dir.as_posix()}/SKILL.md and its references/ folder. "
            f"Do not consult any other sources, prior knowledge from outside "
            f"this skill, or the internet. Keep the answer under 150 words.\n\n"
            f"Question: {c['q']}"
        )
        try:
            answer = claude_runner.send(
                prompt=prompt,
                session_key=f"canary-{version}-{i}",
                timeout=180,
            )
        except Exception as e:
            answer = f"[canary execution failed: {e}]"

        lower = answer.lower()
        missing = [r for r in c["required"] if r not in lower]
        results.append({
            "q": c["q"],
            "required": c["required"],
            "answer": answer,
            "missing": missing,
            "pass": len(missing) == 0,
        })

    overall = all(r["pass"] for r in results)
    payload = {
        "version": version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pass": overall,
        "results": results,
    }
    _CANARY_RESULTS.write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    return payload


def format_canary_summary(payload: dict) -> str:
    """Format canary results for a Slack message."""
    if payload.get("note"):
        return f"Canaries: {payload['note']}"
    results = payload.get("results", [])
    passed = sum(1 for r in results if r["pass"])
    total = len(results)
    lines = [f"*Canary results: {passed}/{total} passed*"]
    for r in results:
        q_short = r["q"][:80] + ("..." if len(r["q"]) > 80 else "")
        if r["pass"]:
            lines.append(f"PASS: {q_short}")
        else:
            missing_str = ", ".join(f"`{m}`" for m in r["missing"])
            lines.append(f"FAIL: {q_short}")
            lines.append(f"     missing: {missing_str}")
    return "\n".join(lines)


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

    # Canary state for current version
    canary_state = "not run"
    if _CANARY_RESULTS.exists():
        try:
            payload = json.loads(_CANARY_RESULTS.read_text(encoding="utf-8"))
            if payload.get("version") == current:
                passed = sum(1 for r in payload["results"] if r["pass"])
                total = len(payload["results"])
                canary_state = f"{passed}/{total} passing" if payload["pass"] else f"FAILING ({passed}/{total})"
            else:
                canary_state = f"stale (last run on {payload.get('version', 'unknown')})"
        except Exception:
            canary_state = "unreadable"

    return (
        f"*Compile Status*\n"
        f"• Current version: {current}\n"
        f"• Last compile: {last_compile}\n"
        f"• Canaries: {canary_state}\n"
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
    """Approve and publish a compiled version. Deterministic — no LLM for file ops."""
    import os
    ver = version or get_next_version()
    ver_dir = _COMPILED_DIR / ver

    if not ver_dir.exists():
        return f"Version {ver} not found in _compiled/. Nothing to approve."

    # Canary gate — added in Part 3, will be a no-op until then
    try:
        canary_payload = run_canaries(ver)
        if not canary_payload["pass"] and not canary_payload.get("note"):
            return (
                f"Canaries failed for {ver} — NOT publishing.\n\n"
                f"{format_canary_summary(canary_payload)}\n\n"
                f"Review `training/_compiled/credit-trading/canary_results.json`, "
                f"then either fix the compile or `/compile reject {ver}` with a reason."
            )
    except NameError:
        # run_canaries not yet defined (pre-Part 3)
        pass

    current_dir = _COMPILED_DIR / "current"

    # 1. Wipe current/
    if current_dir.exists():
        shutil.rmtree(current_dir)
    # 2. Copy v<N>/ into current/
    shutil.copytree(ver_dir, current_dir)

    # 3. Publish to the external skill directory if configured
    publish_path = os.environ.get("SKILLS_PUBLISH_PATH")
    published_to = None
    if publish_path:
        publish_dir = Path(publish_path)
        if publish_dir.exists():
            shutil.rmtree(publish_dir)
        shutil.copytree(current_dir, publish_dir)
        published_to = str(publish_dir)

    # 4. Log the publish
    log_file = _COMPILED_DIR / "publish_log.md"
    ts = datetime.now(timezone.utc).isoformat()
    files = sorted(
        p.relative_to(current_dir).as_posix()
        for p in current_dir.rglob("*") if p.is_file()
    )
    entry = (
        f"\n## {ver} — {ts}\n"
        f"- Published to: {published_to or '(not published — SKILLS_PUBLISH_PATH not set)'}\n"
        f"- Files: {len(files)}\n"
        + "\n".join(f"  - {f}" for f in files)
        + "\n"
    )
    existing = log_file.read_text(encoding="utf-8") if log_file.exists() else "# Publish log\n"
    log_file.write_text(existing + entry, encoding="utf-8")

    # 5. Commit through a thin Claude call
    prompt = (
        f"Git add and commit the publish of credit-trading {ver}. "
        f"Commit message: 'v2-compile: credit-trading {ver} published'. "
        f"Return a one-line confirmation."
    )
    commit_confirm = claude_runner.send(
        prompt=prompt, session_key="compile-pipeline", timeout=60,
    )

    return (
        f"credit-trading {ver} published\n"
        f"- current/: {len(files)} files\n"
        f"- Published to: {published_to or '(local only — SKILLS_PUBLISH_PATH not set)'}\n"
        f"- {commit_confirm}"
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
