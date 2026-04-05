"""
Handles file uploads from Slack channels.
Routes to the correct inbox based on channel type:
  - #research → research/_raw/inbox/to-tag/
  - #training → training/inbox/to-tag/
  - Other channels → rejected with helpful error

Never overwrites existing files. Sanitizes filenames.
"""

import logging
import re
from datetime import datetime
from pathlib import Path

import requests

import config

logger = logging.getLogger(__name__)

_INBOX_PATHS = {
    "research": Path(config.VAULT_PATH) / "research" / "_raw" / "inbox" / "to-tag",
    "training": Path(config.VAULT_PATH) / "training" / "inbox" / "to-tag",
}

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


def handle_file_upload(file_info: dict, inbox_type: str) -> tuple[str, Path]:
    """
    Download a file from Slack and save to the appropriate inbox.

    Args:
        file_info: Slack file info dict from files.info API
        inbox_type: "research" or "training"

    Returns:
        Tuple of (confirmation message, saved file path)

    Raises on download or write failure.
    """
    inbox_dir = _INBOX_PATHS.get(inbox_type)
    if inbox_dir is None:
        raise ValueError(f"Unknown inbox_type: {inbox_type}")

    inbox_dir.mkdir(parents=True, exist_ok=True)

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
    dest = _unique_path(inbox_dir, filename)

    logger.info("inbox_handler: downloading %s → %s (%s)", url, dest.name, inbox_type)

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
    logger.info("inbox_handler: saved %s (%d KB) to %s", dest.name, size_kb, inbox_type)

    msg = (
        f"Filed `{dest.name}` to `{inbox_type}` inbox ({size_kb} KB). "
        f"Running inference-review..."
    )
    return msg, dest
