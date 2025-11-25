@echo off
REM Quick start script for Anime Picker with Docker

echo ========================================
echo   Anime Picker - Docker Quick Start
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] docker-compose not found!
    echo Please install Docker Desktop which includes docker-compose.
    echo.
    pause
    exit /b 1
)

echo [OK] docker-compose is available
echo.

echo Starting Anime Picker...
echo This may take a few minutes on first run.
echo.

REM Start services
docker-compose up

REM If user stops with Ctrl+C, clean up
echo.
echo Stopping services...
docker-compose down

echo.
echo ========================================
echo   Services stopped
echo ========================================
pause
