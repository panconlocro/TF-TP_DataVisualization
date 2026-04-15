Param(
    [string]$Python = "python"
)

$ErrorActionPreference = 'Stop'

# Run from repo root (folder containing this script)
Set-Location -Path $PSScriptRoot

$venvPath = Join-Path $PSScriptRoot ".venv"

Write-Host "Using repo root: $PSScriptRoot"

# Create venv if missing
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at .venv ..."
    & $Python -m venv $venvPath
}

$venvPython = Join-Path $venvPath "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Virtualenv python not found at $venvPython. Make sure venv creation succeeded."
}

Write-Host "Upgrading pip ..."
& $venvPython -m pip install --upgrade pip

Write-Host "Installing requirements.txt ..."
& $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")

Write-Host "Done. In VS Code: select the Python interpreter from .venv, then open the notebook." 
