# Changelog

All notable changes to this artifact. Versions are reproduction milestones, not software releases.

## v1.1 — structural-cluster forensics + multi-seed variance (pending push)

Adds two analyses that harden the v1.0 verdicts; **no numbers change**, the calibration is refined.

- **`results/expert/structural_cluster_forensics.md`** — for every interactive-traffic class flagged
  as a structural ceiling, lists each route where *either* agent fails (DS < 100) with both agents'
  status + infraction signature. Finding: the privileged expert's failures here are **collisions**
  (layout on InterurbanActorFlow / InvadingTurn geometry, DS 14–18; vehicle during junction
  right-of-way negotiation, DS 30–65), and within a class the two agents fail *different instances*
  — so the **class**, not a single route, is the ceiling.
- **`results/expert/multiseed_variance.md`** — re-ran 18 structural-cluster routes for the expert
  across up to 3 traffic-manager seeds. Mean per-route DS std **3.97**; **3 of 18** routes flip
  pass↔fail across seeds (e.g. EnterActorFlow 2201 = 100/100/60); 9 stable-clean. Refines the (c)
  label: route-level pass/fail is **seed-sensitive**, but the **class-level** structural pattern
  (collisions during junction / actor-flow negotiation, across instances and seeds) is the robust claim.

Why it matters: directly quantifies the single-repetition limitation disclosed in v1.0 `CLAIMS.md`,
and moves the structural-ceiling claim from route-level to the (defensible) class-level.

## v1.0 — expert-calibrated taxonomy (`b1ded96`)

Ran the privileged **PDM-Lite** expert (carla_garage) on the identical Bench2Drive-220 routes
(expert mean DS **95.71**, 188/208 clean) and calibrated every model failure against it:
**28** fixable model gaps (b) / **4** structural-ceiling candidates (c) / **12** shared sim-infra (a) /
**6** model-or-harness-specific crashes (a\*). Per-route + per-scenario reports, route-scatter and
per-scenario pass-rate figures, raw expert per-route JSON, and `scripts/expert_vs_model.py`.

## v0.1 — stable-vs-flaky (`8095851`)

Folded re-run results to begin separating stable failures from flaky (infrastructure) ones.

## v0 — reproducible baseline + model taxonomy (`0776e62`)

Single-checkpoint LEAD `tfv6_resnet34` reproduced on Bench2Drive-220 (mean DS **93.36** over 202
cleanly-evaluated routes), with the per-route model failure taxonomy (a / b / c buckets), the exact
single-GPU native-Windows harness, and a claim-safe `CLAIMS.md` / `MANIFEST.md`.
