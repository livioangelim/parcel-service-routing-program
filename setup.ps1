# Store original directory and set project root
$projectRoot = $PSScriptRoot
$backendDir = Join-Path $projectRoot "backend"

# Clean up all virtual environments
Write-Host "Cleaning up virtual environments..." -ForegroundColor Yellow
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue `
    $projectRoot\.venv, `
    $projectRoot\venv, `
    $backendDir\venv

# Verify Python version
$pythonVersion = python --version
if ($pythonVersion -notmatch "Python 3.[8-9]|3.1[0-9]") {
    Write-Host "Error: Python 3.8 or higher is required" -ForegroundColor Red
    Write-Host "Current version: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Create virtual environment in backend directory
Write-Host "Creating new virtual environment..." -ForegroundColor Green
cd $backendDir
python -m venv venv --prompt parcel-routing
./venv/Scripts/Activate.ps1

# Add PYTHONPATH to include the backend directory
$env:PYTHONPATH = "$PWD\backend"
Write-Host "PYTHONPATH set to: $env:PYTHONPATH" -ForegroundColor Green

# Clean previous installations
Write-Host "Cleaning previous installations..." -ForegroundColor Yellow
pip uninstall -y Flask Werkzeug
pip cache purge

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
python -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# Verify Flask and python-dotenv installation
Write-Host "Verifying installations..." -ForegroundColor Green
pip show Flask python-dotenv

# Setup frontend
Write-Host "Setting up frontend..." -ForegroundColor Green
cd ../frontend
npm install

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host "1. cd $backendDir" -ForegroundColor Yellow
Write-Host "2. .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "3. python -m flask run" -ForegroundColor Yellow
