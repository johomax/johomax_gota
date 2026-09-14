#!/usr/bin/env python3
"""Per-policy team-win rates from hosted random-roster experience requests.

usage: uv run python tools/roster_stats.py xp/a.json [xp/b.json ...] [--cache tmp/roster_cache.json]
Accepts xp.py and xp_mixed.py request files. For every completed episode it reads the ownership-scoped episode
stats (policy per seat, reward per seat) and prints: Red/Blue base rate, win rate per policy when present, and
per-seat win rate for the candidate policy of each file.
"""
import argparse, json, pathlib, sys
from collections import defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLASSES = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("paths", nargs="+"); ap.add_argument("--cache", default="tmp/roster_cache.json")
    a = ap.parse_args()
    cp = ROOT / a.cache; cp.parent.mkdir(exist_ok=True)
    cache = json.load(open(cp)) if cp.exists() else {}
    episodes = []  # (file, seats[10] policy labels, rewards[10])
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in a.paths:
            d = json.load(open(path))
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    if ep["id"] not in cache:
                        try:
                            st = dump(c.get_episode_request_episode_stats(ep["id"]))
                        except Exception as ex:
                            continue
                        seats = {ps["position"]: (f'{ps.get("policy_name")}:v{ps.get("policy_version")}', ps.get("avg_reward") or 0) for ps in st.get("policy_stats", [])}
                        if len(seats) < 10: continue
                        cache[ep["id"]] = [[seats[i][0] for i in range(10)], [seats[i][1] for i in range(10)]]
                    episodes.append((path, d.get("candidate"), *cache[ep["id"]]))
    json.dump(cache, open(cp, "w"))
    short = lambda n: n.split("-ply_")[0].replace("-gods-of-the-arena", "").replace("aaron-gota-ir-waveguard-r4", "aaron")[:28]
    red = sum(1 for e in episodes if e[3][0]); n = len(episodes)
    print(f"episodes {n}: Red wins {red} ({red/n:.2f}), Blue {n-red}")
    per = defaultdict(lambda: [0, 0]); per_side = defaultdict(lambda: [0, 0, 0, 0])
    for _, cand, pol, rw in episodes:
        for i in range(10):
            k = short(pol[i]); per[k][0] += rw[i]; per[k][1] += 1
            side = 0 if i < 5 else 2; per_side[k][side] += rw[i]; per_side[k][side + 1] += 1
    print("policy                        win   n    red        blue")
    for k, (w, g) in sorted(per.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][1])):
        s = per_side[k]
        print(f"{k:28s} {w/g:.3f} {g:4d}   {s[0]}/{s[1]:<6d} {s[2]}/{s[3]}")
    # candidate per seat
    for path in a.paths:
        d = json.load(open(path)); cand = d.get("candidate")
        by = defaultdict(lambda: [0, 0])
        for p, _, pol, rw in episodes:
            if p != path: continue
            for i in range(10):
                if pol[i] == cand: by[i][0] += rw[i]; by[i][1] += 1
        print(f"{path} {short(cand)}: " + " ".join(f"s{i}={by[i][0]}/{by[i][1]}" for i in sorted(by)))

if __name__ == "__main__":
    main()
