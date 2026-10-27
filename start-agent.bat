@echo off
cd /d "%~dp0"
set /p TARGET_URL=Enter the full service URL (e.g. https://your-service.onrender.com): 
if "%TARGET_URL%"=="" (
  echo No URL provided.
  pause
  exit /b 1
)
python wake_agent.py "%TARGET_URL%" --interval 300
pause
