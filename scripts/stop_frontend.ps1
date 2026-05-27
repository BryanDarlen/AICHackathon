param(
    [int]$Port = 3002
)

$ErrorActionPreference = "Stop"

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

$pids = @(Get-ListeningPids -TargetPort $Port)
if ($pids.Count -eq 0) {
    Write-Host "No frontend server is listening on port $Port."
    exit 0
}

foreach ($pidValue in $pids) {
    $process = Get-Process -Id $pidValue -ErrorAction Stop
    if ($process.ProcessName -ne "node") {
        throw "Port $Port is used by PID $pidValue ($($process.ProcessName)). Refusing to stop a non-Node process."
    }

    Write-Host "Stopping frontend server on port $Port (PID $pidValue)."
    Stop-Process -Id $pidValue -Force
}

Write-Host "Port $Port is free."
