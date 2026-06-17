#!/usr/bin/env python3
"""
Per-scenario model-vs-expert calibration for Bench2Drive-220 (44 scenario types x 5 routes).
For each scenario class: model pass-rate / mean DS vs expert pass-rate / mean DS, and a
calibration verdict. This is the paper's headline per-scenario table.

Usage:
  python per_scenario.py --model-dir <brick1 per_route> --expert-csv <progress.csv> \
      --scenario-map ops/route_scenario.json [--out ops/per_scenario_report.md]
"""
import argparse, json, os, csv, glob, collections

CRASH = ("crashed", "simulation crashed")
def is_crash(s): s=(s or "").lower(); return any(m in s for m in CRASH)
def clean(ds): return ds is not None and float(ds) >= 100.0

def model_recs(d):
    out={}
    for ep in glob.glob(os.path.join(d,"*","checkpoint_endpoint.json")):
        rid=os.path.basename(os.path.dirname(ep))
        try: j=json.load(open(ep,encoding="utf-8"))
        except: continue
        recs=j.get("_checkpoint",{}).get("records",[])
        if recs:
            r=recs[0]
            out[rid]={"ds":r["scores"].get("score_composed"),"status":r.get("status","?")}
        else:
            out[rid]={"ds":None,"status":"NOREC/"+j.get("entry_status","")}
    return out

def expert_recs(p):
    out={}
    if p and os.path.exists(p):
        for row in csv.DictReader(open(p,encoding="utf-8")):
            rid=(row.get("route_id") or "").strip()
            if not rid: continue
            ds=row.get("score_composed","")
            try: ds=float(ds) if ds not in("",None) else None
            except: ds=None
            out[rid]={"ds":ds,"status":row.get("status","")}
    return out

def passrate(recs):
    """returns (n_eval, n_pass, mean_ds_over_eval, n_crash)"""
    ev=[r for r in recs if r is not None]
    crash=[r for r in ev if is_crash(r["status"]) or r["ds"] is None]
    scored=[r for r in ev if r["ds"] is not None and not is_crash(r["status"])]
    npass=sum(1 for r in scored if clean(r["ds"]))
    mean=sum(r["ds"] for r in scored)/len(scored) if scored else None
    return len(ev), npass, mean, len(crash), len(scored)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",required=True)
    ap.add_argument("--expert-csv",required=True)
    ap.add_argument("--scenario-map",required=True)
    ap.add_argument("--out",default=None)
    a=ap.parse_args()
    M=model_recs(a.model_dir); E=expert_recs(a.expert_csv)
    r2s=json.load(open(a.scenario_map,encoding="utf-8"))
    by=collections.defaultdict(list)
    for rid,sc in r2s.items(): by[sc].append(rid)

    rows=[]
    for sc in sorted(by):
        ids=by[sc]
        mrec=[M.get(i) for i in ids]
        erec=[E.get(i) for i in ids]
        mn,mp,mds,mc,ms = passrate(mrec)
        en,ep,eds,ec,es = passrate(erec)
        # calibration verdict (only meaningful where expert coverage exists)
        verdict=""
        if es>0 or ec>0:
            model_struggles = (mp < ms) or mc>0          # model fails/crashes some
            if not model_struggles:
                verdict="model-clean"
            elif ep==es and ec==0 and es>0:
                verdict="(b) fixable: expert solves all it ran"
            elif ec>0 and mc>0:
                verdict="(a) shared infra (both crash some)"
            elif ep<es:
                verdict="(c) structural: expert ALSO fails some"
            else:
                verdict="mixed"
        rows.append((sc,mn,mp,mds,mc, en,ep,eds,ec, verdict))

    # sort: scenarios where model struggles most first
    def modelfail(r):
        _,mn,mp,mds,mc,_,_,_,_,_=r; return (mc+ (mn-mp))  # crashes + fails
    rows.sort(key=lambda r:-modelfail(r))

    L=["# Per-scenario model-vs-expert calibration — Bench2Drive-220 (44 classes x 5)\n"]
    L.append("Expert coverage so far: %d/220 routes scored.\n"%sum(1 for v in E.values()))
    L.append("| scenario | model pass | model meanDS | model crash | expert pass | expert meanDS | expert crash | verdict |")
    L.append("|---|---|---|---|---|---|---|---|")
    for sc,mn,mp,mds,mc, en,ep,eds,ec, verdict in rows:
        mdsS="%.0f"%mds if mds is not None else "-"
        edsS="%.0f"%eds if eds is not None else "-"
        L.append("| %s | %d/%d | %s | %d | %d/%d | %s | %d | %s |"%(
            sc, mp,mn-mc, mdsS, mc, ep,en-ec, edsS, ec, verdict))
    out="\n".join(L)+"\n"
    if a.out: open(a.out,"w",encoding="utf-8").write(out); print("wrote",a.out)
    print(out)

if __name__=="__main__":
    main()
