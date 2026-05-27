param(
    [int]$Port = 3002,
    [switch]$StopExisting,
    [switch]$CleanCache,
    [string]$Drive = "R:"
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$frontend = Join-Path $root "frontend"

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

function Stop-NodeListeners {
    param([int]$TargetPort)

    $pids = @(Get-ListeningPids -TargetPort $TargetPort)
    foreach ($pidValue in $pids) {
        $process = Get-Process -Id $pidValue -ErrorAction Stop
        if ($process.ProcessName -ne "node") {
            throw "Port $TargetPort is used by PID $pidValue ($($process.ProcessName)). Refusing to stop a non-Node process."
        }

        Write-Host "Stopping stale frontend dev server on port $TargetPort (PID $pidValue)."
        Stop-Process -Id $pidValue -Force
    }
}

if ($StopExisting) {
    Stop-NodeListeners -TargetPort $Port
    Start-Sleep -Seconds 1
}

$busyPids = @(Get-ListeningPids -TargetPort $Port)
if ($busyPids.Count -gt 0) {
    Write-Host "Port $Port is already in use by PID(s): $($busyPids -join ', ')."
    Write-Host "To stop a stale Next.js server safely, run:"
    Write-Host ".\scripts\run_frontend.ps1 -Port $Port -StopExisting -CleanCache"
    exit 1
}

if ($CleanCache) {
    $cache = Join-Path $frontend ".next"
    if (Test-Path -LiteralPath $cache) {
        $resolvedCache = (Resolve-Path -LiteralPath $cache).Path
        if (-not $resolvedCache.StartsWith($root)) {
            throw "Refusing to delete outside project: $resolvedCache"
        }
        Write-Host "Removing generated Next.js cache: $resolvedCache"
        Remove-Item -LiteralPath $resolvedCache -Recurse -Force
    }
}

$needsMappedDrive = $root -like "*!*"
$driveName = $Drive.TrimEnd(":")
$drivePath = "$driveName`:"

if ($needsMappedDrive) {
    Write-Host "Project path contains '!'. Mapping $drivePath to avoid Next.js/Webpack path validation issues."
    $existing = subst | Select-String "^$([regex]::Escape($drivePath))\\:"
    if ($existing) {
        subst $drivePath /D
    }
    subst $drivePath $root
    $frontend = "$drivePath\frontend"
}

try {
    Set-Location $frontend
    Write-Host "Starting ReconPilot frontend on http://localhost:$Port"
    Write-Host "Keep this terminal open. Press Ctrl+C here to stop the server and release the port."
    npm.cmd run dev -- -p $Port
}
finally {
    Set-Location $root
    if ($needsMappedDrive) {
        subst $drivePath /D
    }
}
