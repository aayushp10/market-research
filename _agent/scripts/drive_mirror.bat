@echo off
set SOURCE=C:\Data\Code\Market Research
set DEST=G:\My Drive\Market Research Mirror
robocopy "%SOURCE%" "%DEST%" /MIR /XD ".git" "_agent\logs" "_agent\slack_adapter\.venv" /XF ".env" "*.tmp" "workspace.json" "workspace-mobile.json" "workspaces.json" /R:2 /W:5 /NFL /NDL /NP /LOG+:"C:\Data\Code\Market Research\_agent\logs\mirror.log"
exit /b 0
