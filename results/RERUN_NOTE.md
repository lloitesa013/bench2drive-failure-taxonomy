# Re-run note (stable-vs-flaky, v0.1)

The routes that did **not** complete on the first 220-sweep (CARLA sim crash / hang) were
sampled for a second run to separate *transient* infrastructure failures from *stable* ones.

- **202 routes** completed cleanly → **mean Driving Score 93.36** (the reported baseline).
- **18 routes** (IDs **24206–28048**, a contiguous cluster) did not complete. A re-run sample
  (24206, 24759, 24816) **failed again the same way** → these are **stable** failures of *this
  setup* (single-GPU native-Windows CARLA), not flaky noise. They are bucketed **(a)
  integration/env** and **excluded** from the DS mean (rather than scored 0 and hidden).
- One earlier "infra" route (2204) **completed on re-run** with DS ≈ 30 (a real
  `BlockedIntersection` driving failure) → reclassified to **(b) fixable model-policy**. This is
  exactly why the re-run matters: it moves a route from "tooling artifact" to "real finding".

**Honest takeaway:** ~8% of Bench2Drive-220 was not evaluable on this exact setup. This is a
*reproducibility limit of the harness/hardware*, reported transparently — not a property of the
agent. Reproducing on a Linux / multi-GPU / cluster setup would likely recover most of these.
A full 2x-rerun of *all* routes (not just the failures) for per-route variance is future work.
