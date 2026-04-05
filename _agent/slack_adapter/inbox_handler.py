"""
Handles file uploads from Slack #inbox.
Downloads the file and saves it to VAULT_PATH/_raw/inbox/ with a
timestamp-prefixed, sanitized filename. Never overwrites existing files.
"""

import logging
import re
from datetime import datetime
from pathlib import Path

import requests

import config

logger = logging.getLogger(__name__)

_INBOX_DIR = Path(config.VAULT_PATH) / "_raw" / "inbox"
_UNSAFE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _sanitize(name: str) -> str:
    name = _UNSAFE.sub("-", name)
    name = re.sub(r"-{2,}", "-", name)
    return name.strip("-")[:200]


def _unique_path(dest_dir: Path, filename: str) -> Path:
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    candidate = dest_dir / filename
    counter = 2
    while candidate.exists():
        candidate = dest_dir / f"{stem}-{counter}{suffix}"
        counter += 1
    return candidate


def handle_file_upload(file_info: dict) -> str:
    """
    Download a file from Slack and save to _raw/inbox/.
    Returns a confirmation message string.
    Raises on download or write failure.
    """
    _INBOX_DIR.mkdir(parents=True, exist_ok=True)

    original_name = file_info.get("name", "upload")
    url = (
        file_info.get("url_private_download")
        or file_info.get("url_private")
    )
    if not url:
        raise ValueError(f"No download URL in file_info: {file_info.get('id')}")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = _sanitize(original_name)
    filename = f"{timestamp}-{safe_name}"
    dest = _unique_path(_INBOX_DIR, filename)

    logger.info("inbox_handler: downloading %s → %s", url, dest.name)

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {config.SLACK_BOT_TOKEN}"},
        timeout=120,
        stream=True,
    )
    response.raise_for_status()

    with open(dest, "wb") as fh:
        for chunk in response.iter_content(chunk_size=8192):
            fh.write(chunk)

    size_kb = dest.stat().st_size // 1024
    logger.info("inbox_handler: saved %s (%d KB)", dest.name, size_kb)
    return f"Filed `{dest.name}` to inbox ({size_kb} KB). Will be processed on the next briefing run or ingest command."
