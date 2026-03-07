# Helper script to run backend from PowerShell
# Usage: .\run_backend.ps1  (optionally pass port as first param)
param(
    [string]$port = "8000"
)

# Ensure script runs inside backend folder
Set-Location -Path $PSScriptRoot
Write-Host "Starting backend from: $(Get-Location)"

# If you use a virtual environment, activate it before running this script.
# Example (PowerShell venv activation):
# .\.venv\Scripts\Activate.ps1

# Start Django using our convenience entrypoint
python main.py runserver 0.0.0.0:$port
