# Bench2Drive-220 Failure Taxonomy + Reproducible Baseline (LEAD / TransFuser-V6)

A **reproducible Bench2Drive-220 closed-loop baseline** of the open-source LEAD
*TransFuser-V6* (`tfv6_resnet34`) agent, run end-to-end on a **single consumer GPU
(RTX 5090, native Windows + CARLA 0.9.15)**, together with — to our knowledge — the
**first public per-route failure taxonomy** of a state-of-the-art *open* driving model
on Bench2Drive: *where* it fails, *why*, and into which actionable bucket.

> This repo is infrastructure, not a new model. Its value is **reproducibility + an honest,
> per-route failure analysis** — the parts of the benchmark that are usually missing.

## TL;DR result

| | value |
| --- | --- |
| Mean Driving Score (DS) | **93.36** over 202 cleanly-evaluated routes |
| Published reference (TFv6, 3-seed ensemble) | 95.28 |
| Perfect routes (DS = 100) | 170 / 202 |
| Routes with a driving failure (DS < 100) | 28 |
| Routes not evaluable on this setup (sim crash/hang) | see [results/](results/) — reported honestly, not hidden |
| Checkpoint used | single `model_0030_0` (no ensemble) |

The ~2-point gap vs the published 95.28 is **expected and disclosed**: we run a *single*
checkpoint, the published number uses a 3-seed ensemble. See [CLAIMS.md](CLAIMS.md).

## What's here

- **[results/baseline_summary.md](results/)** — DS, completion, infraction totals, per-route table.
- **[results/taxonomy_v0.md](results/)** — failures classified into
  **(a) integration/env · (b) fixable model-policy · (c) structural-ceiling-candidate**,
  with per-route hypotheses, confidence, and scenario-type clusters.
- **[results/](results/)** — raw per-route `checkpoint_endpoint.json` (the evidence) + `batch_progress.csv`.
- **[scripts/](scripts/)** — the exact harness: per-route runner, batch orchestrator (resumable,
  watchdog), and the stdlib-only taxonomy/baseline tools.
- **[REPRODUCE.md](REPRODUCE.md)** + **[MANIFEST.md](MANIFEST.md)** — one-path reproduction and pinned environment.

## Headline failure findings (taxonomy v0)

- 🔴 **`YieldToEmergencyVehicle` fails on every instance** (4/4, DS 70) — a *systematic* missing
  behavior, not noise. The clearest, highest-confidence model weakness.
- 🔴 **Vehicle collisions while negotiating dynamic traffic** dominate (~14 routes, mostly DS 60):
  junction turns, actor-flows, lane changes, merges, bicycle crossings.
- ⚠️ **Pedestrian collisions** on 2 crossing scenarios (DS 50) — safety-critical.
- ⚠️ A handful of **route-deviation / lane-departure** failures on highway exits & interurban flows.

## v1.0 — Expert-calibrated (NEW)

We ran the **privileged PDM-Lite expert** (carla_garage) on the *identical* 220 routes and
calibrated every model failure against it. A route the expert solves but the model fails is a
**fixable model gap**; a route the expert *also* fails is a **structural-ceiling candidate**.
Expert mean DS **95.71** (188/208 clean). Of the model's **50 non-clean routes**:

| bucket | n | meaning |
| --- | --- | --- |
| **(b) fixable model gap** | **28** | model DS<100, expert DS=100 |
| **(c) structural-ceiling candidate** | **4** | model & expert both DS<100 (e.g. route 23910 InterurbanActorFlow → expert DS 17.7) |
| **(a) shared sim/infra** | **12** | both crash (heavy Town12/13) — real benchmark fragility |
| **(a\*) model/harness-specific** | **6** | model crashes, **expert runs clean** (Town05/02) — *not* benchmark |

Two findings that need the expert to see:
- **Most model failures are fixable** (28/32). `YieldToEmergencyVehicle` (model 0/4 → expert 4/4)
  is a clean missing-behavior gap, not a benchmark ceiling.
- **A coherent structural cluster** — `OppositeVehicleTakingPriority`, `InvadingTurn`,
  `MergerIntoSlowTrafficV2`, `InterurbanActorFlow`, `*JunctionLeftTurnEnterFlow` — where the
  **privileged expert is no better, or worse, than the sensorimotor model**: traffic-merging /
  right-of-way negotiation is structurally hard, not a perception gap.
- **Calibration reclassifies 6 of 18 model "crashes"** as model/harness-specific (the expert runs
  them) rather than simulator fragility — a distinction invisible from the model's score alone.

Artifacts: **[results/expert/calibration_report.md](results/expert/)** (per-route a/b/c/a\*),
**[results/expert/per_scenario_report.md](results/expert/)** (44 scenario classes),
**[figs/](figs/)** (route scatter + per-scenario pass-rates), raw expert per-route JSON under
`results/expert/per_route/`, and **[scripts/expert_vs_model.py](scripts/)** /
`per_scenario.py` / `figs.py`. (c) remains a *candidate* label: PDM-Lite is a strong reference,
not an oracle — see [CLAIMS.md](CLAIMS.md).

## Scope & honesty

See **[CLAIMS.md](CLAIMS.md)** for exactly what is and is not claimed. In short: this is a
faithful *single-checkpoint* reproduction + a *model* (not expert) failure taxonomy, on a
*single-GPU native-Windows* setup whose evaluable-route coverage is reported transparently.

## License

[MIT](LICENSE). The LEAD agent, CARLA, and Bench2Drive are the property of their respective
authors; see [MANIFEST.md](MANIFEST.md) for upstream sources and versions.
