@echo off
REM =======================================
REM JARVIS AI - START EVERYTHING
REM =======================================

echo.
echo ================================================
echo  🚀 JARVIS AI - COMPLETE STARTUP
echo ================================================
echo.

REM Kill any existing process on port 5000
echo [1/3] Stopping previous backend instances...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    taskkill /PID %%a /F 2>nul
)

timeout /t 1 /nobreak

REM Navigate to project
cd /d "D:\e drive\Only_Project\jarvis1.0"

REM Activate virtual environment
echo [2/3] Activating virtual environment...
call .\.venv\Scripts\activate.bat

REM Start backend in new window
echo [3/3] Starting backend server...
start "Jarvis Backend" cmd /k "cd Backend && python app.py"

timeout /t 3 /nobreak

REM Start frontend
echo.
echo Starting frontend in 3 seconds...
echo.
timeout /t 3 /nobreak

npm run dev

pause
