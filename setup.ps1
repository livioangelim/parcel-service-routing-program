# Verify Python version
$pythonVersion = python --version
if ($pythonVersion -notmatch "Python 3.[8-9]|3.1[0-9]") {
    Write-Host "Error: Python 3.8 or higher is required" -ForegroundColor Red
    Write-Host "Current version: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Setting up Python virtual environment..." -ForegroundColor Green
cd backend
python -m venv venv --prompt parcel-routing
./venv/Scripts/Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Setup frontend
Write-Host "Setting up frontend..." -ForegroundColor Green
cd ../frontend
npm install

Write-Host "Setup complete!" -ForegroundColor Green
