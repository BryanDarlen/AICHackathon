param(
    [int]$Port = 8000,
    [switch]$StopExisting
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Get-ListeningPids {
    param([int]$TargetPort)

    $lines = netstat -ano | Select-String "LISTENING" | Select-String ":$TargetPort\s"
    $ids = foreach ($line in $lines) {
        if ($line.Line -match "\sLISTENING\s+(\d+)\s*$") {
            [int]$Matches[1]
        }
    }
    $ids | Sort-Object -Unique
}

function Stop-BackendListeners {
    param([int]$TargetPort)

    $pids = @(Get-ListeningPids -TargetPort $TargetPort)
    foreach ($pidValue in $pids) {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId = $pidValue"
        if (-not $process -or $process.CommandLine -notmatch "uvicorn|app\.main:app") {
            throw "Port $TargetPort is used by PID $pidValue. Refusing to stop an unknown process."
        }

        Write-Host "Stopping stale backend server on port $TargetPort (PID $pidValue)."
        Stop-Process -Id $pidValue -Force
    }
}

if ($StopExisting) {
    Stop-BackendListeners -TargetPort $Port
    Start-Sleep -Seconds 1
}

$busyPids = @(Get-ListeningPids -TargetPort $Port)
if ($busyPids.Count -gt 0) {
    Write-Host "Port $Port is already in use by PID(s): $($busyPids -join ', ')."
    Write-Host "To stop a stale backend server safely, run:"
    Write-Host ".\scripts\run_backend.ps1 -Port $Port -StopExisting"
    exit 1
}

Set-Location $root
Write-Host "Starting ReconPilot backend on http://127.0.0.1:$Port"
Write-Host "Agent status: http://127.0.0.1:$Port/api/agent/status"
Write-Host "Keep this terminal open. Press Ctrl+C here to stop the backend."
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port $Port
