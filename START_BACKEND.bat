@echo off
REM =======================================
REM JARVIS AI - START BACKEND
REM =======================================

echo.
echo ========================================
echo  🤖 JARVIS AI BACKEND STARTUP
echo ========================================
echo.

REM Kill any existing process on port 5000
echo Stopping previous instances...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    taskkill /PID %%a /F 2>nul
)

REM Navigate to project
cd /d "D:\e drive\Only_Project\jarvis1.0"

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

REM Navigate to backend
cd Backend

REM Start the server
echo.
echo Starting Flask server on http://127.0.0.1:5000...
echo.
python app.py

pause
