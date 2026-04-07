@echo off
REM PaperLens Backend Startup Script for Windows

REM Load environment variables from .env file if it exists
if exist .env (
    for /f "tokens=*" %%i in (type .env ^| findstr /v "^#") do set %%i
)

REM Install dependencies if needed
REM pip install -r requirements.txt

REM Start the FastAPI server
echo Starting PaperLens backend server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
