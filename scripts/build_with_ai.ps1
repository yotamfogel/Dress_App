# PowerShell script to build Flutter app with AI backend
param(
    [string]$Platform = "debug",
    [switch]$StartAI = $true,
    [switch]$StopAI = $false
)

Write-Host "🚀 DressApp Build Script with AI Backend" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Function to check if AI backend is running
function Test-AIBackend {
    try {
        $response = Invoke-WebRequest -Uri "http://192.168.1.172:8080/health" -TimeoutSec 2 -UseBasicParsing
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

# Function to start AI backend
function Start-AIBackend {
    Write-Host "🤖 Starting AI Backend..." -ForegroundColor Yellow
    
    # Check if Python is available
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
        exit 1
    }
    
    # Navigate to AI backend directory
    $aiBackendPath = Join-Path $PSScriptRoot "..\ai_backend"
    if (-not (Test-Path $aiBackendPath)) {
        Write-Host "❌ AI backend directory not found: $aiBackendPath" -ForegroundColor Red
        exit 1
    }
    
    Set-Location $aiBackendPath
    
    # Create virtual environment if it doesn't exist
    $venvPath = Join-Path $aiBackendPath "venv"
    if (-not (Test-Path $venvPath)) {
        Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
    }
    
    # Activate virtual environment and install dependencies
    $pythonPath = Join-Path $venvPath "Scripts\python.exe"
    $pipPath = Join-Path $venvPath "Scripts\pip.exe"
    
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    & $pipPath install -r requirements.txt
    
    # Start the server in background
    Write-Host "🌐 Starting Flask server..." -ForegroundColor Yellow
    $serverProcess = Start-Process -FilePath $pythonPath -ArgumentList "start_server.py" -PassThru -WindowStyle Hidden
    
    # Wait for server to start
    Write-Host "⏳ Waiting for server to start..." -ForegroundColor Yellow
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        if (Test-AIBackend) {
            Write-Host "✅ AI Backend started successfully!" -ForegroundColor Green
            return $serverProcess
        }
        Start-Sleep -Seconds 1
        $attempt++
    }
    
    Write-Host "❌ Failed to start AI backend" -ForegroundColor Red
    if ($serverProcess) {
        Stop-Process -Id $serverProcess.Id -Force
    }
    exit 1
}

# Function to stop AI backend
function Stop-AIBackend {
    Write-Host "🛑 Stopping AI Backend..." -ForegroundColor Yellow
    
    # Find and stop Python processes running the AI server
    $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -like "*start_server.py*" -or $_.ProcessName -eq "python"
    }
    
    foreach ($process in $processes) {
        try {
            Stop-Process -Id $process.Id -Force
            Write-Host "✅ Stopped process: $($process.Id)" -ForegroundColor Green
        }
        catch {
            Write-Host "⚠️ Could not stop process: $($process.Id)" -ForegroundColor Yellow
        }
    }
}

# Main execution
try {
    # Stop AI backend if requested
    if ($StopAI) {
        Stop-AIBackend
        exit 0
    }
    
    # Check if AI backend is already running
    if (Test-AIBackend) {
        Write-Host "✅ AI Backend is already running" -ForegroundColor Green
    }
    elseif ($StartAI) {
        $serverProcess = Start-AIBackend
    }
    else {
        Write-Host "⚠️ AI Backend not running. Use -StartAI to start it." -ForegroundColor Yellow
    }
    
    # Navigate back to project root
    Set-Location (Join-Path $PSScriptRoot "..")
    
    # Run Flutter commands
    Write-Host "📱 Building Flutter app..." -ForegroundColor Yellow
    
    switch ($Platform.ToLower()) {
        "debug" {
            Write-Host "🔧 Building debug APK..." -ForegroundColor Cyan
            flutter build apk --debug
        }
        "release" {
            Write-Host "🚀 Building release APK..." -ForegroundColor Cyan
            flutter build apk --release
        }
        "profile" {
            Write-Host "📊 Building profile APK..." -ForegroundColor Cyan
            flutter build apk --profile
        }
        default {
            Write-Host "❌ Unknown platform: $Platform" -ForegroundColor Red
            Write-Host "Available platforms: debug, release, profile" -ForegroundColor Yellow
            exit 1
        }
    }
    
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    
    # Keep AI backend running if it was started by this script
    if ($StartAI -and $serverProcess) {
        Write-Host "🤖 AI Backend is still running. Press Ctrl+C to stop." -ForegroundColor Yellow
        try {
            $serverProcess.WaitForExit()
        }
        catch {
            Stop-AIBackend
        }
    }
}
catch {
    Write-Host "❌ Build failed: $($_.Exception.Message)" -ForegroundColor Red
    Stop-AIBackend
    exit 1
} 