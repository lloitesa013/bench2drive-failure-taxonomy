#!/usr/bin/env python3
"""Summarize a directory of LEAD Bench2Drive per-route checkpoint_endpoint.json files
into a baseline report (mean Driving Score, completion, infraction breakdown).

Usage:
  python ops/summarize_baseline.py --glob "reports/lead_b2d_win/*/checkpoint_endpoint.json" \
      --output reports/lead_b2d_win/baseline_summary.md

stdlib only (py3.7+). Reads each file's _checkpoint.records[0] (one route per file).
"""
import argparse
import glob
import json
import os
import re
import statistics


def _route_id(rec, path):
    rid = str(rec.get("route_id", ""))
    m = re.search(r"(\d+)", rid)
    if m:
        return m.group(1)
    # fall back to parent dir name
    return os.path.basename(os.path.dirname(path))


def load_records(paths):
    rows = []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:  # noqa
            print("skip (unreadable):", p, e)
            continue
        recs = (d.get("_checkpoint") or {}).get("records") or []
        for rec in recs:
            scores = rec.get("scores") or {}
            infr = rec.get("infractions") or {}
            infr_counts = {}
            for k, v in infr.items():
                if isinstance(v, list):
                    infr_counts[k] = len(v)
                elif isinstance(v, (int, float)):
                    infr_counts[k] = int(v)
            rows.append({
                "route_id": _route_id(rec, p),
                "town": rec.get("town_name") or rec.get("town"),
                "scenario": rec.get("scenario_name"),
                "status": rec.get("status", ""),
                "score_composed": scores.get("score_composed"),
                "score_route": scores.get("score_route"),
                "score_penalty": scores.get("score_penalty"),
                "num_infractions": rec.get("num_infractions"),
                "infractions": infr_counts,
            })
    return rows


def fmt(x):
    return "-" if x is None else (("%.2f" % x) if isinstance(x, float) else str(x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True, help="glob for checkpoint_endpoint.json files")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    paths = sorted(glob.glob(args.glob))
    rows = load_records(paths)
    rows.sort(key=lambda r: (int(r["route_id"]) if r["route_id"].isdigit() else 1 << 30, r["route_id"]))

    composed = [r["score_composed"] for r in rows if isinstance(r["score_composed"], (int, float))]
    route = [r["score_route"] for r in rows if isinstance(r["score_route"], (int, float))]
    completed = [r for r in rows if str(r["status"]).lower().startswith("completed")]

    infr_totals = {}
    for r in rows:
        for k, v in r["infractions"].items():
            infr_totals[k] = infr_totals.get(k, 0) + v

    n = len(rows)
    out = []
    out.append("# LEAD tfv6 — Bench2Drive baseline summary\n")
    out.append("routes evaluated: **%d** / 220\n" % n)
    if composed:
        out.append("**Driving Score (mean score_composed): %.2f**  (published TFv6 ref: 95.28)\n" % statistics.mean(composed))
    if route:
        out.append("mean route completion: %.2f\n" % statistics.mean(route))
    out.append("completed (clean status): %d / %d\n" % (len(completed), n))
    out.append("")
    out.append("## Infraction totals (sum across routes)\n")
    if infr_totals:
        for k in sorted(infr_totals, key=lambda k: -infr_totals[k]):
            out.append("- %s: %d" % (k, infr_totals[k]))
    else:
        out.append("- none")
    out.append("")
    out.append("## Per-route\n")
    out.append("| route | town | status | composed | route | penalty | infractions |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        infr = ", ".join("%s:%d" % (k, v) for k, v in sorted(r["infractions"].items())) or "-"
        out.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            r["route_id"], r["town"] or "-", r["status"], fmt(r["score_composed"]),
            fmt(r["score_route"]), fmt(r["score_penalty"]), infr))
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", args.output, "| routes=%d" % n,
          "| meanDS=%.2f" % (statistics.mean(composed) if composed else 0.0))


if __name__ == "__main__":
    main()
