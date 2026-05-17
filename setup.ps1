Param(
    [string]$Python = "python"
)

$ErrorActionPreference = 'Stop'

Set-Location -Path $PSScriptRoot

$venvPath = Join-Path $PSScriptRoot ".venv"

function Step($current, $total, $message) {
    $percent = ($current / $total) * 100

    Write-Progress `
        -Activity "Project Setup" `
        -Status $message `
        -PercentComplete $percent

    Write-Host "[$current/$total] $message"
}

Write-Host "Using repo root: $PSScriptRoot"

# STEP 1
Step 1 4 "Checking virtual environment"

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..."
    & $Python -m venv $venvPath
}

$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    throw "Virtualenv python not found."
}

# STEP 2
Step 2 4 "Upgrading pip"

& $venvPython -m pip install --upgrade pip

# STEP 3
Step 3 4 "Installing dependencies"

& $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")

# STEP 4
Step 4 4 "Setup complete"

Write-Progress `
    -Activity "Project Setup" `
    -Completed

Write-Host ""
Write-Host "Setup complete!"
Write-Host "Activate with:"
Write-Host ".\.venv\Scripts\Activate.ps1"