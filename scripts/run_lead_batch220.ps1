param(
  [int]$TimeoutSec = 1800,
  [string]$RouteList = ""
)
$ErrorActionPreference = "Continue"
$Lead     = "C:\lead"
$RouteDir = Join-Path $Lead "data\benchmark_routes\bench2drive"
$OutBase  = Join-Path $Lead "outputs\local_evaluation_win"
$Csv      = Join-Path $Lead "outputs\batch_progress.csv"
$RunLog   = Join-Path $Lead "outputs\batch_run.log"
$RunnerLogDir = Join-Path $Lead "outputs\runner_logs"
$Runner   = "C:\Users\tulpa\run_lead_route.ps1"
New-Item -ItemType Directory -Force -Path $OutBase | Out-Null
New-Item -ItemType Directory -Force -Path $RunnerLogDir | Out-Null

function Log($m) { $s = "$(Get-Date -Format s) $m"; Add-Content -LiteralPath $RunLog -Value $s }

if ($RouteList -ne "") {
  $ordered = $RouteList.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
} else {
  $priority = @("1825","2509","2513","2606")
  $all = Get-ChildItem -LiteralPath $RouteDir -Filter *.xml | ForEach-Object { $_.BaseName } | Sort-Object { [int]$_ }
  $ordered = @()
  foreach ($p in $priority) { if ($all -contains $p) { $ordered += $p } }
  foreach ($r in $all) { if ($priority -notcontains $r) { $ordered += $r } }
}

if (!(Test-Path -LiteralPath $Csv)) {
  Set-Content -LiteralPath $Csv -Encoding UTF8 -Value "route_id,status,score_composed,score_route,score_penalty,num_infractions,wall_seconds,result,timestamp"
}

function Is-Done($rid) {
  $cp = Join-Path (Join-Path $OutBase $rid) "checkpoint_endpoint.json"
  if (Test-Path -LiteralPath $cp) {
    try { $j = Get-Content -Raw -LiteralPath $cp | ConvertFrom-Json; return ($j.entry_status -eq "Finished") } catch { return $false }
  }
  return $false
}

Log "BATCH_START count=$($ordered.Count) timeout=$TimeoutSec"
$idx = 0
foreach ($rid in $ordered) {
  $idx++
  if (Is-Done $rid) { Log "[$idx/$($ordered.Count)] [$rid] already done, skip"; continue }
  $t0 = Get-Date
  Log "[$idx/$($ordered.Count)] [$rid] START"
  $rlog = Join-Path $RunnerLogDir "$rid.runner.log"
  try {
    & powershell -ExecutionPolicy Bypass -NoProfile -File $Runner -RouteId $rid -TimeoutSec $TimeoutSec *> $rlog
  } catch { Log "[$rid] runner exception: $_" }
  $wall = [int]((Get-Date) - $t0).TotalSeconds
  $status=""; $sc=""; $sr=""; $sp=""; $ni=""; $res="FAILED"
  $cp = Join-Path (Join-Path $OutBase $rid) "checkpoint_endpoint.json"
  if (Test-Path -LiteralPath $cp) {
    try {
      $j = Get-Content -Raw -LiteralPath $cp | ConvertFrom-Json
      $rec = $j._checkpoint.records[0]
      $status = $rec.status; $sc = $rec.scores.score_composed; $sr = $rec.scores.score_route; $sp = $rec.scores.score_penalty; $ni = $rec.num_infractions
      if ($j.entry_status -eq "Finished") { $res = "DONE" }
    } catch {}
  }
  $line = '"{0}","{1}",{2},{3},{4},{5},{6},{7},{8}' -f $rid,$status,$sc,$sr,$sp,$ni,$wall,$res,(Get-Date -Format s)
  Add-Content -LiteralPath $Csv -Value $line
  Log "[$idx/$($ordered.Count)] [$rid] $res composed=$sc wall=${wall}s"
}
Log "BATCH_COMPLETE"
