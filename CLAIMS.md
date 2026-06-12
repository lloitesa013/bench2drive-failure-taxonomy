# Claims & Non-Claims

This project follows a claim-safe discipline: state exactly what the evidence supports,
and explicitly disclaim what it does not.

## What this IS (claimed)

1. **A reproducible closed-loop baseline.** The LEAD `tfv6_resnet34` agent evaluated on the
   full Bench2Drive-220 route set in CARLA 0.9.15, on one RTX 5090 (native Windows), with the
   exact harness in `scripts/` and the pinned environment in `MANIFEST.md`. Re-running the
   harness reproduces the per-route `checkpoint_endpoint.json` artifacts in `results/`.
2. **Mean Driving Score 93.36** over the 202 routes that completed cleanly (entry_status
   `Finished`), computed as the mean of `score_composed` — the standard Bench2Drive metric.
3. **A per-route failure taxonomy** classifying each non-perfect route into
   (a) integration/env, (b) fixable model-policy, or (c) structural-ceiling-candidate, with a
   stated hypothesis and confidence, derived from each route's leaderboard status string and
   infraction record (the evidence ships in `results/`).
4. **Systematic findings**, e.g. `YieldToEmergencyVehicle` failing on 4/4 instances — a
   reproducible, scenario-type-level weakness, not a single flaky route.

## What this is NOT (explicit non-claims)

1. **Not a new model, method, or SOTA.** Bench2Drive is near-saturated; this is a reproduction
   + analysis, not a result that advances the leaderboard.
2. **Not the published 95.28.** That figure uses a **3-seed ensemble**; we run a **single**
   checkpoint (`model_0030_0`). The ~2-point gap is the expected cost of dropping the ensemble,
   not a discrepancy in the agent or benchmark.
3. **Not an expert taxonomy.** This analyzes a *learned sensorimotor model*, whose failures are
   largely *expected*. It does **not** establish where the privileged *expert* (PDM-Lite /
   LEAD-expert — the "answer key" that training data is distilled from) fails. The (c)
   "structural ceiling" label is therefore a **candidate only**; confirming it requires an
   expert run under the same protocol (the planned next artifact).
4. **Not full-coverage of all 220 routes.** A subset of routes did not complete on this setup
   (CARLA sim crash / hang under the long unattended run). These are reported transparently in
   `results/` and excluded from the DS mean (rather than scored 0 and hidden inside an inflated
   "we ran everything" claim). They are flagged as integration/env (bucket a).
5. **Not a multi-seed / variance-controlled benchmark.** Each route was evaluated once (with a
   single retry on infrastructure failure). Stable-vs-flaky separation is partial; a full
   2x-rerun variance pass is future work.

## Protocol notes

- Metric: official Bench2Drive `score_composed` (DS), via the agent's leaderboard
  `checkpoint_endpoint.json`. No custom scoring is mixed in.
- Determinism: fixed traffic-manager seed; CARLA restarted fresh per route to avoid actor-leak
  accumulation.
- Comparison hygiene: we compare only to the upstream-published TFv6 numbers under the same
  Bench2Drive protocol, and disclose the single-vs-ensemble difference rather than matching by
  selection.
