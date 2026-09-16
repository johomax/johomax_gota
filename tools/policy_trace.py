#!/usr/bin/env python3
"""What does each policy's hero do over a game? Aggregates over cached hosted replays (tmp/replays/<episode>.replay)
using tmp/roster_cache.json (episode -> seat policies, rewards) so filler policies can be compared with ours.

usage: uv run python tools/policy_trace.py [--match black-kite richard khors Jordan] [--limit N]
Per policy: games, team win rate, per-1000-tick window mean walkTo target (Red frame), commands per game by kind,
lane share of tower commands (Red frame: physical lane P2 = Red lane 2 = Blue lane 0), first tower attack tick.
"""
import argparse, json, pathlib, sys, statistics as st
from collections import Counter, defaultdict
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp

def tower_info(tid):
    off = tid - 10; return off // 6, (off % 6) // 3, off % 3

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--match", nargs="+", default=["black-kite", "richard", "khors", "red-kite", "Jordan"])
    ap.add_argument("--limit", type=int, default=100000); ap.add_argument("--window", type=int, default=1000)
    ap.add_argument("--ids", default=None, help="json list of episode ids to restrict to"); ap.add_argument("--exact", action="store_true", help="match keys as full labels"); a = ap.parse_args()
    only = set(json.load(open(a.ids))) if a.ids else None
    cache = json.load(open(ROOT / "tmp/roster_cache.json"))
    per = defaultdict(lambda: {"games": 0, "wins": 0, "win": defaultdict(Counter), "cmds": Counter(), "lane": Counter(), "first_tower": [], "fort_first": [], "walkwin": defaultdict(lambda: [0, 0, 0])})
    n = 0
    for eid, (pols, rws) in cache.items():
        if only is not None and eid not in only: continue
        f = ROOT / "tmp/replays" / (eid + ".replay")
        if not f.exists(): continue
        try: rep = rp.load_replay(f)
        except Exception: continue
        n += 1
        if n > a.limit: break
        acts_by_hero = defaultdict(list)
        for act in rep["actions"]: acts_by_hero[act["heroId"]].append(act)
        for seat in range(10):
            label = pols[seat]; key = None
            for m in a.match:
                if (label == m) if a.exact else (m in label): key = m if m != "Jordan" else label.split(":")[-1]; break
            if key is None: continue
            p = per[key]; team = 0 if seat < 5 else 1; hid = 100 + seat
            p["games"] += 1; p["wins"] += 1 if rws[seat] else 0
            ft = None; ff = None
            for act in acts_by_hero[hid]:
                w = min(act["tick"] // a.window, 11); k = act.get("kind")
                if k == "walkTo":
                    x, y = act.get("x", act.get("first")), act.get("y", act.get("second"))
                    if x is None: continue
                    if team == 1: x, y = 115 - x, 115 - y
                    ww = p["walkwin"][w]; ww[0] += 1; ww[1] += x; ww[2] += y
                    p["cmds"]["walk"] += 1
                elif k == "attackTarget":
                    tid = act["targetId"]
                    if 10 <= tid <= 27:
                        lane, tt, tier = tower_info(tid)
                        if tt == team: p["cmds"]["ownTower"] += 1; continue
                        p["cmds"][f"tower{tier}"] += 1; p["lane"][lane if team == 0 else 2 - lane] += 1
                        if ft is None: ft = act["tick"]
                    elif tid in (1, 2):
                        p["cmds"]["fort"] += 1
                        if ff is None: ff = act["tick"]
                    elif 100 <= tid <= 109: p["cmds"]["hero"] += 1
                    else: p["cmds"]["foot"] += 1
                else: p["cmds"][k] += 1
            if ft is not None: p["first_tower"].append(ft)
            if ff is not None: p["fort_first"].append(ff)
    print(f"replays {n}")
    for key, p in sorted(per.items(), key=lambda kv: -kv[1]["games"]):
        g = p["games"]; tot = sum(p["lane"].values()) or 1
        print(f"\n== {key}: games {g} team-win {p['wins']/g:.3f}  lanes P0 {p['lane'][0]/tot:.2f} P1 {p['lane'][1]/tot:.2f} P2 {p['lane'][2]/tot:.2f}"
              f"  first tower attack median {st.median(p['first_tower']) if p['first_tower'] else 0:.0f} ({len(p['first_tower'])}/{g})"
              f"  fort attacked in {len(p['fort_first'])}/{g} games, median first {st.median(p['fort_first']) if p['fort_first'] else 0:.0f}")
        print("   cmds/g: " + " ".join(f"{k} {v/g:.0f}" for k, v in sorted(p["cmds"].items(), key=lambda kv: -kv[1])))
        print("   walk by window: " + " ".join(f"{w*a.window//1000}k({v[1]//v[0]},{v[2]//v[0]})" for w, v in sorted(p["walkwin"].items()) if v[0]))

if __name__ == "__main__":
    main()
