@echo off
REM Anime Picker System - Install Requirements (Batch version)

echo ============================================================
echo   ANIME PICKER SYSTEM - INSTALLING DEPENDENCIES
echo ============================================================
echo.

REM Check if venv exists
if not exist "..\venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Creating virtual environment...
    cd ..
    python -m venv venv
    cd Backend
    
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    
    echo Virtual environment created
)

echo Virtual environment found
echo.

REM Upgrade pip
echo Upgrading pip...
..\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
echo.

REM Install requirements
echo Installing requirements from requirements.txt...
echo This may take a few minutes...
echo.

..\venv\Scripts\pip.exe install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   INSTALLATION COMPLETE!
echo ============================================================
echo.
echo You can now run the application with:
echo   run.bat
echo.
pause
