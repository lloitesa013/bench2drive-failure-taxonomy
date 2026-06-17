#!/usr/bin/env python3
"""Generate the paper's two key figures from model + expert results.
  fig1: per-route model DS vs expert DS scatter, colored by calibration bucket.
  fig2: per-scenario model vs expert pass-rate (scenarios with >=1 model failure).
Usage: python figs.py --model-dir <..> --expert-csv <..> --scenario-map <..> --outdir paper/figs
"""
import argparse, json, os, csv, glob, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CRASH=("crashed","simulation crashed")
def is_crash(s): s=(s or "").lower(); return any(m in s for m in CRASH)
def clean(d): return d is not None and float(d)>=100.0

def model_recs(d):
    o={}
    for ep in glob.glob(os.path.join(d,"*","checkpoint_endpoint.json")):
        rid=os.path.basename(os.path.dirname(ep))
        try: j=json.load(open(ep,encoding="utf-8"))
        except: continue
        recs=j.get("_checkpoint",{}).get("records",[])
        if recs: o[rid]={"ds":recs[0]["scores"].get("score_composed"),"status":recs[0].get("status","?")}
        else: o[rid]={"ds":None,"status":"NOREC"}
    return o
def expert_recs(p):
    o={}
    if p and os.path.exists(p):
        for row in csv.DictReader(open(p,encoding="utf-8")):
            rid=(row.get("route_id") or "").strip()
            if not rid: continue
            ds=row.get("score_composed","")
            try: ds=float(ds) if ds not in("",None) else None
            except: ds=None
            o[rid]={"ds":ds,"status":row.get("status","")}
    return o

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-dir",required=True); ap.add_argument("--expert-csv",required=True)
    ap.add_argument("--scenario-map",required=True); ap.add_argument("--outdir",default="paper/figs")
    a=ap.parse_args(); os.makedirs(a.outdir,exist_ok=True)
    M=model_recs(a.model_dir); E=expert_recs(a.expert_csv); r2s=json.load(open(a.scenario_map,encoding="utf-8"))

    # fig1: scatter (only routes scored by both, where model not clean)
    bx={"b":([],[]),"c":([],[]),"a":([],[]),"other":([],[])}
    for rid in r2s:
        m=M.get(rid); e=E.get(rid)
        if not m or not e or e["ds"] is None: continue
        md = 0.0 if (is_crash(m["status"]) or m["ds"] is None) else m["ds"]
        ed = e["ds"]
        if clean(m["ds"] if m["ds"] is not None else -1): continue  # model clean -> skip
        if is_crash(m["status"]) or m["ds"] is None: k="a"
        elif clean(ed): k="b"
        else: k="c"
        bx[k][0].append(md); bx[k][1].append(ed)
    plt.figure(figsize=(5,5))
    colors={"b":"#2ca02c","c":"#d62728","a":"#7f7f7f"}
    labels={"b":"(b) fixable: expert solves","c":"(c) structural: expert also fails","a":"(a) model crash"}
    for k in ("b","c","a"):
        if bx[k][0]: plt.scatter(bx[k][0],bx[k][1],c=colors[k],label=labels[k],alpha=0.75,edgecolors="k",linewidths=0.3)
    plt.plot([0,100],[0,100],"--",c="gray",lw=0.8)
    plt.xlabel("model Driving Score"); plt.ylabel("expert (PDM-Lite) Driving Score")
    plt.title("Per-route calibration (model non-clean routes)"); plt.legend(fontsize=8,loc="lower left")
    plt.xlim(-3,103); plt.ylim(-3,103); plt.tight_layout()
    f1=os.path.join(a.outdir,"fig1_route_scatter.png"); plt.savefig(f1,dpi=160); plt.close()

    # fig2: per-scenario pass-rate, scenarios with >=1 model failure (model pass<5 among evaluated)
    by=collections.defaultdict(list)
    for rid,sc in r2s.items(): by[sc].append(rid)
    rows=[]
    for sc,ids in by.items():
        mev=[M.get(i) for i in ids if M.get(i)]
        msc=[r for r in mev if r["ds"] is not None and not is_crash(r["status"])]
        mp=sum(1 for r in msc if clean(r["ds"]))
        eev=[E.get(i) for i in ids if E.get(i) and E.get(i)["ds"] is not None]
        ep=sum(1 for r in eev if clean(r["ds"]))
        if msc and mp<len(msc):  # model failed at least one evaluated route
            rows.append((sc, mp/len(msc) if msc else 0, (ep/len(eev) if eev else None), len(eev)))
    rows=[r for r in rows if r[2] is not None]
    rows.sort(key=lambda r:(r[1]-(r[2] or 0)))  # biggest model<expert gap first
    if rows:
        scs=[r[0] for r in rows]; mr=[r[1]*100 for r in rows]; er=[r[2]*100 for r in rows]
        import numpy as np; y=np.arange(len(scs))
        plt.figure(figsize=(7,max(3,0.42*len(scs))))
        plt.barh(y-0.2,mr,height=0.4,label="model pass%",color="#1f77b4")
        plt.barh(y+0.2,er,height=0.4,label="expert pass%",color="#2ca02c")
        plt.yticks(y,scs,fontsize=7); plt.xlabel("pass-rate (DS=100) %")
        plt.title("Per-scenario calibration (scenarios with model failures)")
        plt.legend(fontsize=8); plt.gca().invert_yaxis(); plt.tight_layout()
        f2=os.path.join(a.outdir,"fig2_scenario_passrate.png"); plt.savefig(f2,dpi=160); plt.close()
    else: f2="(no scenarios yet)"
    print("wrote", f1, "and", f2)

if __name__=="__main__": main()
