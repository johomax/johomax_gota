#!/usr/bin/env python3
"""Per-opponent, per-side results of tools/xp_league.py homo runs.
usage: uv run python tools/homo_report.py xp/homo-v209.json [xp/homo-v186.json ...]
"""
import json, pathlib, sys
from collections import defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def short(l): return l.split(":")[0].replace("-gods-of-the-arena", "").replace("aaron-gota-ir-", "aaron:")[:28]
def main():
    res = {}
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in sys.argv[1:]:
            d = json.load(open(path)); tab = defaultdict(lambda: [0, 0])
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                    except Exception: continue
                    rw = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                    t = tab[(short(r["opp"]), "Red" if r["side"] == 0 else "Blue")]; t[0] += 1; t[1] += 1 if rw.get(r["seat"]) else 0
            res[path] = tab
    opps = sorted({k for tab in res.values() for k in tab})
    print(f"{'opponent':30s} side " + " ".join(f"{pathlib.Path(p).stem[-9:]:>10s}" for p in res))
    for k in opps:
        print(f"{k[0]:30s} {k[1]:4s} " + " ".join(f"{res[p].get(k, [0, 0])[1]:4d}/{res[p].get(k, [0, 0])[0]:<5d}" for p in res))
    for p, tab in res.items():
        g = sum(v[0] for v in tab.values()); w = sum(v[1] for v in tab.values())
        rg = sum(v[0] for k, v in tab.items() if k[1] == "Red"); rw_ = sum(v[1] for k, v in tab.items() if k[1] == "Red")
        print(f"{pathlib.Path(p).stem:14s} total {w}/{g} = {w/max(1,g):.3f}  Red {rw_}/{rg}  Blue {w-rw_}/{g-rg}")
if __name__ == "__main__":
    main()
