#!/usr/bin/env python3
"""Paired comparison of candidates run with tools/xp_league.py --realistic (identical rosters per rep).

usage: uv run python tools/lg_pair.py xp/lgr-v186.json xp/lgr-v197.json [...]
Prints wins per rep for each file (Red/Blue by rep parity), totals per side, and pairwise rep-level sign counts vs the first file.
"""
import json, pathlib, sys
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o

def main():
    paths = sys.argv[1:]; per = {}
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in paths:
            d = json.load(open(path)); reps = {}
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"])); w = 0; n = 0
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                    except Exception: continue
                    rw = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                    n += 1; w += 1 if rw.get(r["seat"]) else 0
                reps[r["rep"]] = (w, n, r["seat"])
            per[path] = reps
    base = per[paths[0]]
    allreps = sorted(set().union(*[set(v) for v in per.values()]))
    print("rep side " + " ".join(f"{pathlib.Path(p).stem[-9:]:>10s}" for p in paths))
    for rep in allreps:
        side = "Red " if rep % 2 == 0 else "Blue"
        print(f"{rep:3d} {side} " + " ".join(f"{per[p].get(rep, (0, 0, 0))[0]:5d}/{per[p].get(rep, (0, 0, 0))[1]:<4d}" for p in paths))
    for p in paths:
        reps = per[p]; tw = sum(v[0] for v in reps.values()); tn = sum(v[1] for v in reps.values())
        rw = sum(v[0] for k, v in reps.items() if k % 2 == 0); rn = sum(v[1] for k, v in reps.items() if k % 2 == 0)
        print(f"{pathlib.Path(p).stem:14s} total {tw}/{tn} = {tw/max(1,tn):.3f}  Red {rw}/{rn}  Blue {tw-rw}/{tn-rn}")
        if p != paths[0]:
            better = sum(1 for k in reps if k in base and reps[k][0] > base[k][0]); worse = sum(1 for k in reps if k in base and reps[k][0] < base[k][0])
            print(f"    vs {pathlib.Path(paths[0]).stem}: reps better {better}, worse {worse}, equal {len([k for k in reps if k in base]) - better - worse}")

if __name__ == "__main__":
    main()
