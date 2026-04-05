@echo off
cd /d "C:\Data\Code\Market Research\_agent\slack_adapter"
call .venv\Scripts\activate
python -c "from briefing import run_morning_briefing; from slack_sdk import WebClient; import config; client = WebClient(token=config.SLACK_BOT_TOKEN); result = run_morning_briefing(); client.chat_postMessage(channel=config.SLACK_BRIEFINGS_CHANNEL_ID, text=result)"
