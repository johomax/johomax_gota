#!/usr/bin/env python3
"""Hosted XP helper.

create: tools/xp.py create <candidate_ref> <opp_ref> [<opp_ref> ...] [-n 4] [--tag t]
   -> creates paired requests (candidate Red vs opp Blue, opp Red vs candidate Blue), saves xp/<tag>.json
report: tools/xp.py report xp/<tag>.json   -> per-opponent, per-side win rates and ticks
"""
import argparse, json, subprocess, sys, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAGUE = "league_3c60897b-25cf-4b37-9d1a-8554c1198f28"

def cw(*args):
    r = subprocess.run(["uv", "run", "coworld", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:], file=sys.stderr)
    return r.stdout

def create(cand, opps, n, tag):
    out = {"candidate": cand, "n": n, "requests": []}
    for opp in opps:
        for cand_side in ("red", "blue"):
            roster = []
            for s in range(10):
                mine = (s < 5) == (cand_side == "red")
                roster.append({"player": {"policy_ref": cand if mine else opp}, "slot": s})
            body = {"target": {"league_id": LEAGUE}, "roster": roster, "num_episodes": n,
                    "notes": f"[{tag}] {cand} ({cand_side}) vs {opp}"}
            res = cw("xp-request", "create", "-", "--json") if False else None
            p = subprocess.run(["uv", "run", "coworld", "xp-request", "create", "-", "--json"], cwd=ROOT,
                               input=json.dumps(body), capture_output=True, text=True)
            try:
                d = json.loads(p.stdout)
                xid = d["id"]
            except Exception:
                print("create failed:", p.stdout[-500:], p.stderr[-800:], file=sys.stderr); continue
            print(f"created {xid} {cand} ({cand_side}) vs {opp}")
            out["requests"].append({"id": xid, "opp": opp, "cand_side": cand_side})
    path = ROOT / "xp" / f"{tag}.json"
    json.dump(out, open(path, "w"), indent=1)
    print("saved", path)

def report(path):
    d = json.load(open(path))
    tot_w = tot_g = 0
    by_opp = {}
    for r in d["requests"]:
        det = json.loads(cw("xp-request", "get", r["id"], "--json") or "{}")
        status = det.get("status")
        w = g = 0; ticks = []; pend = 0
        for ep in det.get("episodes", []):
            if ep.get("status") != "completed":
                pend += 1; continue
            res = json.loads(cw("episode-results", ep["id"]) or "{}")
            if "outcome" not in res: pend += 1; continue
            g += 1
            win = (res["outcome"] == "RedTeam") == (r["cand_side"] == "red")
            w += win; ticks.append(res["ticks"])
        by_opp.setdefault(r["opp"], []).append((r["cand_side"], w, g, ticks, status, pend))
        tot_w += w; tot_g += g
    for opp, rows in by_opp.items():
        for side, w, g, ticks, status, pend in rows:
            mt = sum(ticks)/len(ticks) if ticks else 0
            print(f"{opp:40s} cand={side:4s} {w}/{g} win  mean_ticks={mt:6.0f}  status={status} pending={pend}")
    print(f"TOTAL {d['candidate']}: {tot_w}/{tot_g} = {tot_w/tot_g if tot_g else 0:.2f}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("create"); c.add_argument("cand"); c.add_argument("opps", nargs="+"); c.add_argument("-n", type=int, default=4); c.add_argument("--tag", required=True)
    r = sub.add_parser("report"); r.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "create": create(a.cand, a.opps, a.n, a.tag)
    else: report(a.path)
