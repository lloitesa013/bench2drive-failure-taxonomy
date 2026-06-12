# Environment Manifest

Pinned components used to produce the artifacts in `results/`. Reproduce against these.

## Hardware / OS
- GPU: **NVIDIA GeForce RTX 5090** (32 GB), driver **595.97**, CUDA **12.8**
- OS: **Windows 11** (native; CARLA server + LEAD client on Windows)
- Python env: conda `lead-win`, **Python 3.10.20**

## Key Python packages
- **torch 2.7.0+cu128** (`torch.cuda.is_available() == True`); torchvision matched cu128
  - (Blackwell/RTX 5090 requires the cu128 wheels; LEAD's default `torch==2.5+cu124` does not
    run on this GPU.)
- LEAD runtime + dependencies per upstream `pyproject.toml` (carla, opencv, timm, ...)
- `carla` Python client **0.9.15**

## Simulator
- **CARLA 0.9.15** (`WindowsNoEditor`) + **AdditionalMaps 0.9.15** (Town11–15; Bench2Drive
  routes live on Town12/Town13). Launched headless: `-RenderOffScreen -quality-level=Low
  -carla-rpc-port=2000 -carla-streaming-port=2001`.

## Agent / model
- **LEAD** — `github.com/kesai-labs/lead`, commit `156afed` (tag/branch as cloned).
- Agent: `lead/inference/sensor_agent.py` (SENSORS track).
- Checkpoint: **`tfv6_resnet34` / `model_0030_0`** (single seed; NOT the 3-seed ensemble),
  from `huggingface.co/ln2697/tfv6`.
- Eval entrypoint: `python -m lead --checkpoint <ckpt> --routes <id>.xml --bench2drive
  --port 2000 --timeout 900 --output-dir <out>`.

## Benchmark
- **Bench2Drive** 220-route set: `data/benchmark_routes/bench2drive/<route_id>.xml`
  (shipped with LEAD). Metric: official `score_composed` (Driving Score) from each route's
  leaderboard `checkpoint_endpoint.json`.

## Upstream licenses (not covered by this repo's MIT)
- CARLA — MIT (simulator) / CC-BY (assets). LEAD — see its repository. Bench2Drive — see its
  repository. TransFuser-V6 checkpoints — see `huggingface.co/ln2697/tfv6`.

## Known deviations from the published TFv6 setup
- **Single checkpoint**, no 3-seed ensemble → mean DS 93.36 vs published 95.28.
- Native-Windows single-GPU setup; a subset of routes did not complete (sim crash/hang) and are
  reported in `results/` rather than scored 0 and folded silently into the mean.
