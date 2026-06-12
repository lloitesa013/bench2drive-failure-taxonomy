param(
  [Parameter(Mandatory=$true)][string]$RouteId,
  [int]$TimeoutSec = 1800,
  [int]$MaxAttempts = 2
)
$ErrorActionPreference = "Continue"
$Python = "$env:USERPROFILE\miniconda3\envs\lead-win\python.exe"
$EnvDir = "$env:USERPROFILE\miniconda3\envs\lead-win"
$Lead   = "C:\lead"
$env:CARLA_ROOT = "C:\CARLA_0.9.15\WindowsNoEditor"
$env:LEAD_PROJECT_ROOT = $Lead
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$env:PATH = "$EnvDir;$EnvDir\Scripts;$EnvDir\Library\bin;$EnvDir\Library\usr\bin;$env:PATH"

$RouteXml = Join-Path $Lead "data\benchmark_routes\bench2drive\$RouteId.xml"
if (!(Test-Path -LiteralPath $RouteXml)) { Write-Output "ROUTE_XML_MISSING $RouteId"; exit 3 }
$OutDir = Join-Path $Lead "outputs\local_evaluation_win\$RouteId"
$LogDir = Join-Path $Lead "outputs\route_logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$StdLog = Join-Path $LogDir "$RouteId.out.log"
$ErrLog = Join-Path $LogDir "$RouteId.err.log"

function Stop-Carla {
  Get-Process CarlaUE4* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
}
function Start-Carla {
  schtasks /run /tn CarlaServerNewLog | Out-Null
  for ($i=1; $i -le 90; $i++) {
    $c = Test-NetConnection -ComputerName 127.0.0.1 -Port 2000 -WarningAction SilentlyContinue
    if ($c.TcpTestSucceeded) { Start-Sleep -Seconds 6; return $true }
    Start-Sleep -Seconds 1
  }
  return $false
}

$success = $false
for ($attempt=1; $attempt -le $MaxAttempts -and -not $success; $attempt++) {
  Write-Output "[$RouteId] attempt $attempt : restart CARLA"
  Stop-Carla
  if (-not (Start-Carla)) { Write-Output "[$RouteId] CARLA port 2000 did not open"; continue }
  Remove-Item -Recurse -Force -LiteralPath $OutDir -ErrorAction SilentlyContinue
  New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
  $leadArgs = @("-m","lead","--checkpoint","outputs/checkpoints/tfv6_resnet34","--routes","data/benchmark_routes/bench2drive/$RouteId.xml","--bench2drive","--port","2000","--timeout","900","--output-dir",$OutDir)
  Set-Location -LiteralPath $Lead
  $p = Start-Process -FilePath $Python -ArgumentList $leadArgs -NoNewWindow -PassThru -RedirectStandardOutput $StdLog -RedirectStandardError $ErrLog
  $deadline = (Get-Date).AddSeconds($TimeoutSec)
  while (-not $p.HasExited -and (Get-Date) -lt $deadline) { Start-Sleep -Seconds 5 }
  if (-not $p.HasExited) {
    Write-Output "[$RouteId] WATCHDOG TIMEOUT ${TimeoutSec}s - killing tree"
    cmd /c "taskkill /F /T /PID $($p.Id)" 2>$null | Out-Null
    Start-Sleep -Seconds 2
    Stop-Carla
    continue
  }
  $cp = Join-Path $OutDir "checkpoint_endpoint.json"
  if (Test-Path -LiteralPath $cp) {
    try { $j = Get-Content -Raw -LiteralPath $cp | ConvertFrom-Json; if ($j.entry_status -eq "Finished") { $success = $true } } catch {}
  }
  Write-Output "[$RouteId] attempt $attempt exit=$($p.ExitCode) finished=$success"
}
if ($success) { Write-Output "ROUTE_DONE $RouteId"; exit 0 } else { Write-Output "ROUTE_FAILED $RouteId"; exit 1 }
