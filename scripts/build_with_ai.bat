@echo off
setlocal enabledelayedexpansion

echo 🚀 DressApp Build Script with AI Backend
echo ==========================================

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

:: Set paths
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "AI_BACKEND=%PROJECT_ROOT%\ai_backend"

:: Check if AI backend directory exists
if not exist "%AI_BACKEND%" (
    echo ❌ AI backend directory not found: %AI_BACKEND%
    pause
    exit /b 1
)

:: Navigate to AI backend
cd /d "%AI_BACKEND%"

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment and install dependencies
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

:: Start the server in background
echo 🌐 Starting Flask server...
start /B python start_server.py

:: Wait for server to start
echo ⏳ Waiting for server to start...
set /a attempts=0
:wait_loop
curl -s http://192.168.1.172:8080/health >nul 2>&1
if errorlevel 1 (
    set /a attempts+=1
    if !attempts! lss 30 (
        timeout /t 1 /nobreak >nul
        goto wait_loop
    ) else (
        echo ❌ Failed to start AI backend
        pause
        exit /b 1
    )
) else (
    echo ✅ AI Backend started successfully!
)

:: Navigate back to project root
cd /d "%PROJECT_ROOT%"

:: Build Flutter app
echo 📱 Building Flutter app...
flutter build apk --debug

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo ✅ Build completed successfully!
echo 🤖 AI Backend is still running. Close this window to stop it.
pause 