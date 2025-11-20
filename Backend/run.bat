@echo off
REM Anime Picker System - Run Script (Batch version)
REM This script automatically uses the venv and runs the application

echo ============================================================
echo   ANIME PICKER SYSTEM - STARTING SERVER
echo ============================================================
echo.

REM Check if venv exists
if not exist "..\venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Expected location: ..\venv\Scripts\python.exe
    echo.
    echo Please create a virtual environment first:
    echo python -m venv venv
    pause
    exit /b 1
)

echo Virtual environment found
echo Starting Flask server...
echo Server will be available at: http://127.0.0.1:5000
echo Press CTRL+C to stop the server
echo.

REM Run the application
..\venv\Scripts\python.exe app.py
