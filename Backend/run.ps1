# Anime Picker System - Run Script
# This script automatically activates the venv and runs the application

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  ANIME PICKER SYSTEM - STARTING SERVER" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-Not (Test-Path "..\venv\Scripts\python.exe")) {
    Write-Host "❌ ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Expected location: ..\venv\Scripts\python.exe" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "   python -m venv venv" -ForegroundColor White
    exit 1
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green

# Check if requirements are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow

$checkResult = & ..\venv\Scripts\python.exe check_requirements.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Some dependencies are missing!" -ForegroundColor Red
    Write-Host "   Run: .\install_requirements.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting Flask server..." -ForegroundColor Green
Write-Host "   Server will be available at: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "   Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the application
& ..\venv\Scripts\python.exe app.py
