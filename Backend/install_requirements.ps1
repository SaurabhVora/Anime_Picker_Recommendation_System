# Anime Picker System - Install Requirements Script
# This script installs all required packages in the virtual environment

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host "  ANIME PICKER SYSTEM - INSTALLING DEPENDENCIES" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 59 -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-Not (Test-Path "..\venv\Scripts\python.exe")) {
    Write-Host "❌ ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Expected location: ..\venv\Scripts\python.exe" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Creating virtual environment..." -ForegroundColor Yellow
    
    Set-Location ..
    python -m venv venv
    Set-Location Backend
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "📦 Upgrading pip..." -ForegroundColor Yellow
& ..\venv\Scripts\python.exe -m pip install --upgrade pip --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ pip upgraded successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️  pip upgrade failed (continuing anyway)" -ForegroundColor Yellow
}

Write-Host ""

# Install requirements
Write-Host "📦 Installing requirements from requirements.txt..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Cyan
Write-Host ""

& ..\venv\Scripts\pip.exe install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ All requirements installed successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Verify installation
    Write-Host "🔍 Verifying installation..." -ForegroundColor Yellow
    & ..\venv\Scripts\python.exe check_requirements.py
    
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host "=" * 59 -ForegroundColor Green
    Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host "=" * 59 -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run the application with:" -ForegroundColor Cyan
    Write-Host "  .\run.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Installation failed!" -ForegroundColor Red
    Write-Host "   Please check the error messages above" -ForegroundColor Yellow
    exit 1
}
