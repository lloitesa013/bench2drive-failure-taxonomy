#!/usr/bin/env python3
"""Classify LEAD tfv6 Bench2Drive failures into the (a)/(b)/(c) taxonomy and write an
annotated Failure Taxonomy v0 markdown.

Buckets (model-baseline framing):
  (a) integration/env  -- our setup failed (CARLA sim crash, runtime error). Re-run candidate.
  (b) fixable logic     -- the MODEL'S policy made a beatable error (collision, ran light,
                           failed to yield, deviated, got blocked). A stronger model/expert
                           would plausibly handle it.
  (c) structural ceiling-- scenario at/near the benchmark difficulty ceiling (even the expert
                           fails). NOT asserted from model data alone -> marked as a candidate
                           pending an expert (PDM-Lite/LEAD-expert) comparison.

stdlib only (py3.7+). Reads the pulled per-route checkpoint_endpoint.json files.
"""
import argparse, glob, json, os, statistics
from collections import defaultdict


def rid_of(rec, path):
    rid = str(rec.get("route_id", ""))
    rid = rid.replace("RouteScenario_", "").replace("_rep0", "")
    return rid or os.path.basename(os.path.dirname(path))


def infr_counts(rec):
    out = {}
    for k, v in (rec.get("infractions") or {}).items():
        if isinstance(v, list) and v:
            out[k] = len(v)
        elif isinstance(v, (int, float)) and v:
            out[k] = int(v)
    return out


def classify(status, infr, composed):
    s = status.lower()
    has = lambda *ks: any(k in infr for k in ks)
    # (a) integration / env
    if "simulation crashed" in s or "tickruntime" in s or "watchdog" in s or "agent took too long" in s:
        return "a", "CARLA sim crash / runtime error (our infra) -- not a driving failure; re-run", "high"
    # (b) fixable model-policy errors, ordered by score-driving infraction
    if has("collisions_pedestrian"):
        return "b", "Model struck a crossing pedestrian -- perception/braking gap (safety-critical)", "high"
    if has("collisions_vehicle"):
        return "b", "Model collided with a vehicle while negotiating dynamic traffic -- gap-acceptance/timing", "med"
    if has("collisions_layout"):
        return "b", "Model hit static layout (curb/barrier) -- path/lateral control", "med"
    if has("yield_emergency_vehicle_infractions"):
        return "b", "Model fails to yield to emergency vehicle -- missing scenario behavior (systematic)", "high"
    if has("red_light"):
        return "b", "Model ran a red light -- traffic-light compliance gap", "high"
    if has("vehicle_blocked") or "got blocked" in s:
        return "b", "Model got blocked/stuck -- overly cautious or failed maneuver", "med"
    if has("route_dev", "outside_route_lanes") or "deviated from the route" in s:
        return "b", "Model deviated from route / left lane -- path-following/localization", "med"
    # leftover: low score from min-speed pressure only -> structural-metric candidate
    return "c", "Score reduced without a discrete fault (min-speed vs aggressive traffic) -- candidate metric/structural ceiling; confirm vs expert", "low"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    rows = []
    allscored = []
    for f in sorted(glob.glob(args.glob)):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        recs = d.get("_checkpoint", {}).get("records", [])
        if not recs:
            # crashed before a record -> infra
            rows.append({"rid": os.path.basename(os.path.dirname(f)), "status": d.get("entry_status", "no-record"),
                         "composed": None, "scenario": "?", "town": None, "infr": {},
                         "cls": "a", "hyp": "No record written (sim crashed at load) -- infra; re-run", "conf": "high"})
            continue
        rec = recs[0]
        es = d.get("entry_status")
        sc = rec.get("scores", {}).get("score_composed")
        if isinstance(sc, (int, float)):
            allscored.append(sc)
        # clean pass
        if es == "Finished" and isinstance(sc, (int, float)) and sc >= 100:
            continue
        infr = infr_counts(rec)
        cls, hyp, conf = classify(str(rec.get("status", "")), infr, sc)
        rows.append({"rid": rid_of(rec, f), "status": rec.get("status", ""), "composed": sc,
                     "scenario": rec.get("scenario_name", "?"), "town": rec.get("town_name"),
                     "infr": infr, "cls": cls, "hyp": hyp, "conf": conf})

    by = defaultdict(list)
    for r in rows:
        by[r["cls"]].append(r)
    # scenario clustering within (b)
    scen = defaultdict(list)
    for r in by["b"]:
        base = r["scenario"].rsplit("_", 1)[0] if r["scenario"] and r["scenario"][-1].isdigit() else r["scenario"]
        scen[base].append(r)

    out = []
    out.append("# LEAD tfv6 — Bench2Drive-220 Failure Taxonomy v0\n")
    if allscored:
        out.append("Baseline: mean Driving Score **%.2f** over %d scored routes "
                   "(single checkpoint `model_0030_0`; published 3-seed ensemble ref 95.28).\n"
                   % (statistics.mean(allscored), len(allscored)))
    out.append("Failures classified: **%d**  —  (a) integration/env: **%d**  ·  "
               "(b) fixable logic: **%d**  ·  (c) structural ceiling (candidate): **%d**\n"
               % (len(rows), len(by["a"]), len(by["b"]), len(by["c"])))
    out.append("> (c) is a *candidate* label only: it cannot be asserted from the learned model alone — "
               "it requires an expert (PDM-Lite / LEAD-expert) comparison to confirm a true benchmark ceiling.\n")

    out.append("\n## (a) Integration / env — %d (re-run candidates, NOT driving failures)\n" % len(by["a"]))
    out.append("| route | status | score |")
    out.append("| --- | --- | --- |")
    for r in sorted(by["a"], key=lambda r: r["rid"]):
        out.append("| %s | %s | %s |" % (r["rid"], r["status"], r["composed"]))

    out.append("\n## (b) Fixable model-policy errors — %d\n" % len(by["b"]))
    out.append("Grouped by scenario type (systematic clusters first):\n")
    for base in sorted(scen, key=lambda k: -len(scen[k])):
        grp = scen[base]
        out.append("- **%s** — %d route(s): %s"
                   % (base, len(grp), ", ".join("%s(DS %.0f)" % (g["rid"], g["composed"] or 0) for g in grp)))
    out.append("")
    out.append("| route | scenario | DS | infractions | hypothesis | conf |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for r in sorted(by["b"], key=lambda r: (r["composed"] if r["composed"] is not None else 999)):
        ik = ", ".join("%s:%d" % (k, v) for k, v in sorted(r["infr"].items()))
        out.append("| %s | %s | %s | %s | %s | %s |"
                   % (r["rid"], r["scenario"], ("%.1f" % r["composed"] if r["composed"] is not None else "-"), ik, r["hyp"], r["conf"]))

    if by["c"]:
        out.append("\n## (c) Structural-ceiling candidates — %d (confirm vs expert)\n" % len(by["c"]))
        out.append("| route | scenario | DS | infractions | note |")
        out.append("| --- | --- | --- | --- | --- |")
        for r in sorted(by["c"], key=lambda r: (r["composed"] if r["composed"] is not None else 999)):
            ik = ", ".join("%s:%d" % (k, v) for k, v in sorted(r["infr"].items()))
            out.append("| %s | %s | %s | %s | %s |"
                       % (r["rid"], r["scenario"], ("%.1f" % r["composed"] if r["composed"] is not None else "-"), ik, r["hyp"]))

    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    open(args.output, "w", encoding="utf-8").write(text)
    print("wrote", args.output)
    print("classified: a=%d b=%d c=%d total=%d" % (len(by["a"]), len(by["b"]), len(by["c"]), len(rows)))


if __name__ == "__main__":
    main()
