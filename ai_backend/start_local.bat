@echo off
echo 🤖 Starting Local AI Backend Server...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Start the server
echo 🚀 Starting AI Backend Server...
python start_local_server.py

pause