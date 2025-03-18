$projectPath = $PSScriptRoot
$outputFile = Join-Path $projectPath "all-files.txt"

Write-Host "Listing all files in: $projectPath"
Write-Host "----------------------------------------"

try {
    # Ensure directory exists
    $outputDir = Split-Path -Parent $outputFile
    if (!(Test-Path -Path $outputDir)) {
        try {
            New-Item -ItemType Directory -Path $outputDir -Force -ErrorAction Stop | Out-Null
        }
        catch {
            throw "Failed to create output directory: $_"
        }
    }

    # Clear or create the output file
    try {
        Set-Content -Path $outputFile -Value "Files in $projectPath" -ErrorAction Stop
        Add-Content -Path $outputFile -Value "----------------------------------------" -ErrorAction Stop
    }
    catch {
        throw "Failed to initialize output file: $_"
    }

    # Get file list excluding unnecessary files
    try {
        $files = Get-ChildItem -Path $projectPath -Recurse -File -ErrorAction Stop | 
        Where-Object { 
            $_.FullName -notlike "*\node_modules\*" -and 
            $_.FullName -notlike "*\venv\*" -and
            $_.FullName -notlike "*\.venv\*" -and
            $_.Name -notlike "*.pyc"
        }

        foreach ($file in $files) {
            $relativePath = $file.FullName.Replace($projectPath, "").TrimStart("\")
            Write-Host $relativePath
            Add-Content -Path $outputFile -Value $relativePath -ErrorAction Stop
        }
    }
    catch {
        throw "Failed to process files: $_"
    }

    Write-Host "`nFile list has been saved to: $outputFile"
}
catch {
    Write-Error "An error occurred: $_"
    exit 1
}

Write-Host "Project structure cleanup completed!"