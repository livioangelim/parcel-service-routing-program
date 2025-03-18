# Get the current directory
$currentDir = $PSScriptRoot

# Set Python path to include backend directory
$env:PYTHONPATH = "$currentDir\backend"

# Set Flask environment variables
$env:FLASK_APP = "src/main.py"
$env:FLASK_ENV = "development"

Write-Host "Environment setup complete!"
Write-Host "PYTHONPATH set to: $env:PYTHONPATH"
Write-Host "FLASK_APP set to: $env:FLASK_APP"
Write-Host "FLASK_ENV set to: $env:FLASK_ENV"
