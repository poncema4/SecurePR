$ErrorActionPreference = "Stop"

if (Test-Path .\.venv\Scripts\python.exe) {
    $python = (Resolve-Path .\.venv\Scripts\python.exe).Path
} else {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) {
        throw "Python 3 is required but was not found on PATH."
    }
    $python = $pythonCommand.Source
}

& $python -m pytest -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $python -m compileall -q app tests
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "SecurePR verification passed."
