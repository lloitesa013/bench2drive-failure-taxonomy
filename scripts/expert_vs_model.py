#!/usr/bin/env python3
"""
Expert-calibrated failure taxonomy: join LEAD model (brick #1) vs PDM-Lite expert (brick #2)
per-route Driving Scores on Bench2Drive-220 and classify each route into calibration buckets.

Buckets (only routes where the MODEL did not get a clean DS=100 are taxonomy entries):
  (b) fixable-model-gap        : model DS < 100  AND expert DS == 100
  (c) structural-ceiling-cand. : model DS < 100  AND expert DS < 100  (both struggle; not just-crash)
  (a) integration/env          : model crashed (Simulation crashed / not evaluable)
                                  -> sub-split by whether the expert also crashed (shared infra)
Usage:
  python expert_vs_model.py --model-dir <brick1 per_route> --expert-csv <b2d220_progress.csv> [--out <md>]
The expert CSV columns: route_id,town,status,score_composed,score_route,wall_s,attempt,ts
"""
import argparse, json, os, csv, glob

CRASH_MARKERS = ("crashed", "simulation crashed")

def model_records(model_dir):
    out = {}
    for ep in glob.glob(os.path.join(model_dir, "*", "checkpoint_endpoint.json")):
        rid = os.path.basename(os.path.dirname(ep))
        try:
            d = json.load(open(ep, encoding="utf-8"))
        except Exception:
            continue
        recs = d.get("_checkpoint", {}).get("records", [])
        entry = d.get("entry_status", "")
        if recs:
            r = recs[0]; s = r.get("scores", {})
            out[rid] = {
                "status": r.get("status", "?"),
                "ds": s.get("score_composed"),
                "route": s.get("score_route"),
                "entry": entry,
                "infr": {k: (len(v) if isinstance(v, list) else v) for k, v in r.get("infractions", {}).items() if v},
            }
        else:
            out[rid] = {"status": "NOREC/"+entry, "ds": None, "route": None, "entry": entry, "infr": {}}
    return out

def expert_records(expert_csv):
    out = {}
    if not expert_csv or not os.path.exists(expert_csv):
        return out
    with open(expert_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rid = (row.get("route_id") or "").strip()
            if not rid:
                continue
            ds = row.get("score_composed", "")
            try:
                ds = float(ds) if ds not in ("", None) else None
            except ValueError:
                ds = None
            out[rid] = {"status": row.get("status", ""), "ds": ds,
                        "route": row.get("score_route", ""), "town": row.get("town", "")}
    return out

def is_crash(status):
    s = (status or "").lower()
    return any(m in s for m in CRASH_MARKERS)

def is_clean(ds):
    return ds is not None and float(ds) >= 100.0

def classify(m, e):
    """Return (bucket, note). m,e are model/expert record dicts or None."""
    if m is None:
        return ("?", "no model record")
    if is_crash(m["status"]) or m["ds"] is None:
        if e is None:
            return ("a", "model infra/crash; expert pending")
        if e["ds"] is None or is_crash(e["status"]):
            return ("a", "model+expert both crash -> shared infra/benchmark")
        return ("a*", "model crashed but expert ran (DS %s) -> harness/model-specific, not benchmark" % e["ds"])
    if is_clean(m["ds"]):
        return ("clean", "model clean")
    # model failed (DS<100, not crash)
    if e is None:
        return ("b/c?", "model failed DS %s; expert pending" % m["ds"])
    if e["ds"] is None or is_crash(e["status"]):
        return ("c", "model failed; expert also crashed/none")
    if is_clean(e["ds"]):
        return ("b", "model failed DS %s; expert clean -> fixable model gap" % m["ds"])
    return ("c", "model DS %s & expert DS %s both <100 -> structural ceiling candidate" % (m["ds"], e["ds"]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--expert-csv", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    M = model_records(a.model_dir)
    E = expert_records(a.expert_csv)
    ids = sorted(M.keys(), key=lambda x: int(x) if x.isdigit() else 1<<30)

    rows, counts = [], {}
    model_ds_vals = [M[i]["ds"] for i in ids if M[i]["ds"] is not None and not is_crash(M[i]["status"])]
    for i in ids:
        m = M.get(i); e = E.get(i)
        bucket, note = classify(m, e)
        counts[bucket] = counts.get(bucket, 0) + 1
        rows.append((i, m["status"], m["ds"], (e["ds"] if e else "-"), bucket, note))

    lines = []
    lines.append("# Expert-calibrated taxonomy (LEAD model vs PDM-Lite expert) — Bench2Drive-220\n")
    n_model = len(model_ds_vals)
    lines.append("Model clean-route mean DS: **%.2f** over %d cleanly-evaluated routes.  Expert routes scored so far: **%d/220**.\n"
                 % ((sum(model_ds_vals)/n_model if n_model else 0), n_model, len(E)))
    lines.append("## Bucket counts\n")
    for b in sorted(counts):
        lines.append("- `%s`: %d" % (b, counts[b]))
    lines.append("\n## Calibration targets (model failed, DS<100) — the heart of the paper\n")
    lines.append("| route | town | model DS | expert DS | bucket | note |")
    lines.append("|---|---|---|---|---|---|")
    for i, mstat, mds, eds, bucket, note in rows:
        if bucket in ("b", "c", "b/c?", "a", "a*"):
            town = (E.get(i, {}) or {}).get("town", "")
            lines.append("| %s | %s | %s | %s | %s | %s |" % (i, town, mds, eds, bucket, note))
    out = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
        print("wrote", a.out)
    print(out)

if __name__ == "__main__":
    main()
