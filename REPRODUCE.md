# Reproduce

This reproduces the Bench2Drive-220 baseline + per-route artifacts for the LEAD
`tfv6_resnet34` agent. Exact pinned versions are in [MANIFEST.md](MANIFEST.md).

## Prerequisites

- An NVIDIA GPU with the CUDA 12.8 driver (validated on **RTX 5090**).
- **CARLA 0.9.15** (with AdditionalMaps — Town11–15 are required for Bench2Drive).
- The **LEAD** repository (`kesai-labs/lead`) and its `tfv6_resnet34` checkpoint
  (`scripts/download_one_checkpoint.sh` in that repo downloads `model_0030_0`).
- A Python 3.10 env with the LEAD dependencies (`torch==2.7.0+cu128` for Blackwell GPUs).

This baseline was produced on **native Windows** (CARLA server + LEAD client both on Windows,
conda env `lead-win`). A Linux setup works equally well; the per-route eval command is identical.

## One route (smoke test)

With CARLA running on port 2000:

```
python -m lead --checkpoint outputs/checkpoints/tfv6_resnet34 \
  --routes data/benchmark_routes/bench2drive/1825.xml --bench2drive \
  --port 2000 --timeout 900 --output-dir outputs/eval/1825
```

Produces `outputs/eval/1825/checkpoint_endpoint.json` (the per-route record this repo analyzes).

## Full 220 (this baseline)

The harness in `scripts/` automates the 220-route sweep with **per-route fresh CARLA**
(avoids actor-leak accumulation), a **watchdog** (kills a hung route after N minutes and
retries once), and **resume** (skips routes already `Finished`, so a crashed run continues):

```
# Windows (as used here):
powershell -ExecutionPolicy Bypass -File scripts/run_lead_batch220.ps1 -TimeoutSec 1800
```

`run_lead_batch220.ps1` calls `run_lead_route.ps1` per route and appends a row to
`batch_progress.csv`. Each route's result lands in `outputs/local_evaluation_win/<id>/`.

> The two PowerShell scripts encode the *exact* working invocation (env vars, CARLA launch
> flags, ports). Port them to a shell loop for Linux — the inner `python -m lead ...` is identical.

## Aggregate → baseline + taxonomy (stdlib Python, any OS)

After the sweep, point the tools at the per-route `checkpoint_endpoint.json` files:

```
# baseline (mean DS, completion, infraction totals, per-route table)
python scripts/summarize_baseline.py \
  --glob "results/per_route/*/checkpoint_endpoint.json" --output results/baseline_summary.md

# failure taxonomy skeleton (route, status, score, infractions; failure = DS < 100)
python scripts/build_pdmlite_failure_taxonomy.py \
  --input results/per_route/*/checkpoint_endpoint.json \
  --output results/taxonomy.md --json-output results/taxonomy.json --pretty

# annotated a/b/c taxonomy with hypotheses, confidence, scenario clusters
python scripts/classify_taxonomy.py \
  --glob "results/per_route/*/checkpoint_endpoint.json" --output results/taxonomy_v0.md
```

All three tools are stdlib-only (no third-party deps) and run on Python 3.7+.

## Known gotchas (cost real time — documented so you don't rediscover them)

- **CARLA needs a real GPU session.** On Windows, launch it in the interactive console session
  (a GPU-less service/SSH session renders nothing and crashes on the first frame).
- **Per-route CARLA restart** matters for long sweeps; a single multi-hour CARLA process
  accumulates state and starts crashing late routes.
- **Watchdog the eval as a process you can kill**, not via `Process.WaitForExit(ms)` — that
  timed overload silently ignores its timeout, so a hung route stalls the whole sweep forever.
