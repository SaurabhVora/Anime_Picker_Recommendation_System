# Quick start script for Anime Picker with Docker

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Anime Picker - Docker Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "[OK] Docker is running" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if docker-compose is available
try {
    docker-compose --version | Out-Null
    Write-Host "[OK] docker-compose is available" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] docker-compose not found!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop which includes docker-compose." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting Anime Picker..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run." -ForegroundColor Yellow
Write-Host ""
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend API will be available at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the services" -ForegroundColor Gray
Write-Host ""

# Start services
docker-compose up

# Cleanup on exit
Write-Host ""
Write-Host "Stopping services..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Services stopped" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
