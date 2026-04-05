"""
Load and validate environment configuration from the vault root .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Vault root is two levels up from this file (_agent/slack_adapter/config.py)
_VAULT_ROOT = Path(__file__).resolve().parents[2]
_ENV_PATH = _VAULT_ROOT / ".env"

load_dotenv(dotenv_path=_ENV_PATH)

_REQUIRED = [
    "SLACK_BOT_TOKEN",
    "SLACK_APP_TOKEN",
    "SLACK_BRIEFINGS_CHANNEL_ID",
    "SLACK_INBOX_CHANNEL_ID",
    "SLACK_AGENT_CHANNEL_ID",
    "VAULT_PATH",
    "CLAUDE_PATH",
]

_missing = [k for k in _REQUIRED if not os.getenv(k)]
if _missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(_missing)}\n"
        f"Check {_ENV_PATH}"
    )

SLACK_BOT_TOKEN: str = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN: str = os.environ["SLACK_APP_TOKEN"]
SLACK_BRIEFINGS_CHANNEL_ID: str = os.environ["SLACK_BRIEFINGS_CHANNEL_ID"]
SLACK_INBOX_CHANNEL_ID: str = os.environ["SLACK_INBOX_CHANNEL_ID"]
SLACK_AGENT_CHANNEL_ID: str = os.environ["SLACK_AGENT_CHANNEL_ID"]
VAULT_PATH: str = os.environ["VAULT_PATH"]
CLAUDE_PATH: str = os.environ["CLAUDE_PATH"]
