#!/usr/bin/env python3
"""Build a failure-taxonomy skeleton from CARLA leaderboard / Bench2Drive result JSONs.

Phase 2 tool (see AV_EXPERT_KEY_ROADMAP.md). Local-only, stdlib-only, deterministic.

Accepts, per input file, any of:
  - leaderboard checkpoint format: {"_checkpoint": {"records": [...]}}
  - {"records": [...]}
  - a bare list of route records

Each non-clean route becomes a taxonomy entry with empty `classification`
((a) integration/env, (b) fixable logic, (c) structural ceiling) and `hypothesis`
fields to be filled during analysis.

Example:
  python3 ops/build_pdmlite_failure_taxonomy.py \
    --input results.json --output reports/pdmlite_taxonomy/taxonomy.md --pretty
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def _records(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("_checkpoint"), dict) and isinstance(payload["_checkpoint"].get("records"), list):
            return payload["_checkpoint"]["records"]
        if isinstance(payload.get("records"), list):
            return payload["records"]
    raise ValueError("unrecognized result JSON shape")


def _route_id(rec):
    for key in ("route_id", "id", "name"):
        value = rec.get(key)
        if value is not None:
            return str(value)
    return "unknown"


def _infractions(rec):
    raw = rec.get("infractions") or {}
    out = {}
    if isinstance(raw, dict):
        for kind, items in sorted(raw.items()):
            if isinstance(items, list) and items:
                out[kind] = len(items)
            elif isinstance(items, (int, float)) and items:
                out[kind] = int(items)
    return out


def _scores(rec):
    raw = rec.get("scores") or {}
    keys = ("score_composed", "score_route", "score_penalty")
    return {k: raw.get(k) for k in keys if k in raw}


def analyze(payloads):
    entries = []
    total = 0
    for payload in payloads:
        for rec in _records(payload):
            total += 1
            status = str(rec.get("status", "unknown"))
            infractions = _infractions(rec)
            scores = _scores(rec)
            composed = scores.get("score_composed")
            # DS-benchmark semantics: a route is a "failure" worth taxonomy-ing iff its
            # driving score was actually reduced (composed < 100). Routes that scored 100
            # are passes even if they carry non-penalizing flags (e.g. min-speed).
            clean = (
                (composed is not None and float(composed) >= 100.0)
                or (status.lower().startswith("completed") and not infractions and composed is None)
            )
            if clean:
                continue
            entries.append({
                "route_id": _route_id(rec),
                "status": status,
                "infractions": infractions,
                "scores": scores,
                "town": rec.get("town") or rec.get("town_name"),
                "classification": "",
                "hypothesis": "",
                "fix_difficulty": "",
            })
    entries.sort(key=lambda e: (e["route_id"], e["status"]))
    return {"total_routes": total, "non_clean_count": len(entries), "entries": entries}


def render_markdown(result):
    lines = [
        "# Expert Failure Taxonomy (skeleton)",
        "",
        f"total routes: {result['total_routes']}  |  non-clean: {result['non_clean_count']}",
        "",
        "classification: (a) integration/env  (b) fixable logic  (c) structural ceiling",
        "",
        "| route | status | composed | infractions | class | hypothesis |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for e in result["entries"]:
        inf = ", ".join(f"{k}:{v}" for k, v in e["infractions"].items()) or "-"
        composed = e["scores"].get("score_composed", "-")
        lines.append(f"| {e['route_id']} | {e['status']} | {composed} | {inf} |  |  |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, nargs="+", help="result JSON file(s)")
    p.add_argument("--output", help="markdown output path")
    p.add_argument("--json-output", help="JSON output path")
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args(argv)

    payloads = []
    for path in args.input:
        with open(path, "r", encoding="utf-8") as f:
            payloads.append(json.load(f))

    result = analyze(payloads)

    for path, content in ((args.output, render_markdown(result)),
                          (args.json_output, json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))):
        if path:
            out_dir = os.path.dirname(path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content + "\n")

    print(json.dumps({"total_routes": result["total_routes"],
                      "non_clean_count": result["non_clean_count"]},
                     indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
