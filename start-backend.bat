@echo off
echo Starting FileMyRTI Backend Server...
cd /d "%~dp0\backend"
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
