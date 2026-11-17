# NIAT Parent Decision Lens - Quick Launcher
$pythonPath = "C:\Users\KALASH JAIN\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting NIAT Parent Decision Lens (Growth System) ...  " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# Set environment
$env:PYTHONPATH = $scriptDir

# Start server
Write-Host "Running server at http://localhost:8080 ..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"
& $pythonPath "$scriptDir\backend\server.py"
