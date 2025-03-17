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
            $_.FullName -notlike "*\__pycache__\*" -and
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

Write-Host "`nCreating recommended directory structure..."
$directories = @(
    "backend/src/controllers",
    "backend/src/models",
    "backend/src/routes",
    "backend/src/tests",
    "backend/src/utils",
    "frontend/src/components/ParcelForm",
    "frontend/src/components/RouteDisplay",
    "frontend/src/config",
    "frontend/src/error",
    "frontend/src/services",
    "frontend/src/styles",
    "frontend/public",
    "csv"
)

foreach ($dir in $directories) {
    $path = Join-Path $projectPath $dir
    if (!(Test-Path -Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created directory: $dir"
    }
}

# Clean up structure
Write-Host "`nCleaning up project structure..."

# Define file move operations with nested paths
$fileMoves = @{
    "src\components\*"     = "frontend\src\components"
    "src\modules\config\*" = "frontend\src\config"
    "src\modules\error\*"  = "frontend\src\error"
    "src\services\*"       = "frontend\src\services"
    "src\styles\*"         = "frontend\src\styles"
}

# Move files with directory structure preservation
foreach ($source in $fileMoves.Keys) {
    $sourcePath = Join-Path -Path $projectPath -ChildPath $source
    $targetPath = Join-Path -Path $projectPath -ChildPath $fileMoves[$source]
    $sourceDir = Split-Path -Parent $sourcePath
    
    if (Test-Path -Path $sourcePath) {
        # Create target directory
        if (!(Test-Path -Path $targetPath)) {
            New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
        }
        
        # Move files
        Get-ChildItem -Path $sourcePath -Recurse | ForEach-Object {
            $targetFile = $_.FullName.Replace($sourceDir, $targetPath)
            $targetDir = Split-Path -Parent $targetFile
            
            if (!(Test-Path -Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            
            Move-Item -Path $_.FullName -Destination $targetFile -Force -ErrorAction SilentlyContinue
        }
        Write-Host "Moved $source to $($fileMoves[$source])"
    }
}

# Clean up empty directories
$dirsToCheck = @(
    "src\components",
    "src\modules\config",
    "src\modules\error",
    "src\modules",
    "src\services",
    "src\styles",
    "src",
    "public"
)

foreach ($dir in $dirsToCheck) {
    $dirPath = Join-Path -Path $projectPath -ChildPath $dir
    if (Test-Path -Path $dirPath) {
        $items = Get-ChildItem -Path $dirPath -Force -Recurse
        if ($null -eq $items) {
            Remove-Item -Path $dirPath -Force -Recurse -ErrorAction SilentlyContinue
            Write-Host "Removed empty directory: $dir"
        }
    }
}

Write-Host "Project structure cleanup completed!"