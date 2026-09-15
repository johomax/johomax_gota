#!/usr/bin/env python3
"""What does each league entrant's hero do? Aggregates per player name over local replays (tmp/replays/*.replay).

Per hero: lane of tower attacks (by count), fort attacks, hero attacks, mean walkTo target. Aggregates per player:
share of tower commands per lane, mean tower/hero/fort commands per game, mean walkTo target position (Red-normalized:
Blue positions are mirrored to Red's frame so lanes align: Red lane k == Blue lane 2-k).
usage: uv run python tools/field_behavior.py [--limit N]
"""
import argparse, json, pathlib, sys
from collections import defaultdict, Counter
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp

def tower_info(tid):
    off = tid - 10; return off // 6, (off % 6) // 3, off % 3

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=100000); a = ap.parse_args()
    files = sorted((ROOT / "tmp/replays").glob("*.replay"))[: a.limit]
    per = defaultdict(lambda: {"games": 0, "lane": Counter(), "tower": 0, "hero": 0, "fort": 0, "foot": 0, "walk": 0, "wx": 0, "wy": 0, "gate": 0, "camp": 0})
    for f in files:
        try:
            rep = rp.load_replay(f)
        except Exception as ex:
            continue
        players = [p["name"] for p in rep["config"]["players"]]
        heroes = {h["id"]: h for h in rep["header"]["setup"]["heroes"]}
        stats = {hid: {"lane": Counter(), "tower": 0, "hero": 0, "fort": 0, "foot": 0, "walk": 0, "wx": 0, "wy": 0, "gate": 0} for hid in heroes}
        for act in rep["actions"]:
            hid = act["heroId"]; s = stats.get(hid)
            if s is None: continue
            team = 0 if hid < 105 else 1
            if act.get("kind") == "attackTarget":
                tid = act["targetId"]
                if 10 <= tid <= 27:
                    lane, tteam, tier = tower_info(tid)
                    if tteam == team: continue
                    s["tower"] += 1; s["lane"][lane if team == 0 else 2 - lane] += 1
                    if tier == 2: s["gate"] += 1
                elif tid in (1, 2): s["fort"] += 1
                elif 100 <= tid <= 109: s["hero"] += 1
                else: s["foot"] += 1
            elif act.get("kind") == "walkTo":
                x, y = act.get("x", act.get("first")), act.get("y", act.get("second"))
                if x is None or y is None: continue
                if team == 1: x, y = 115 - x, 115 - y
                s["walk"] += 1; s["wx"] += x; s["wy"] += y
        for hid, h in heroes.items():
            seat = h["slot"] + (5 if h["team"] == 1 else 0)
            name = players[seat] if seat < len(players) else "?"
            p = per[name]; s = stats[hid]
            p["games"] += 1; p["lane"].update(s["lane"]); p["tower"] += s["tower"]; p["hero"] += s["hero"]; p["fort"] += s["fort"]; p["foot"] += s["foot"]; p["gate"] += s["gate"]
            if s["walk"]:
                mx, my = s["wx"] / s["walk"], s["wy"] / s["walk"]; p["walk"] += 1; p["wx"] += mx; p["wy"] += my
                if (mx - 57.5) ** 2 + (my - 57.5) ** 2 <= 400: p["camp"] += 1
    print(f"replays {len(files)}")
    print(f"{'player':20s} {'games':>5s} {'tower/g':>7s} {'gate/g':>6s} {'fort/g':>6s} {'hero/g':>6s} {'foot/g':>6s} {'lane0':>5s} {'lane1':>5s} {'lane2':>5s} {'meanWalk(RedFrame)':>19s} {'midcamp':>7s}")
    for name, p in sorted(per.items(), key=lambda kv: -kv[1]["games"]):
        g = p["games"]; tot = sum(p["lane"].values()) or 1
        print(f"{name[:20]:20s} {g:5d} {p['tower']/g:7.0f} {p['gate']/g:6.0f} {p['fort']/g:6.0f} {p['hero']/g:6.0f} {p['foot']/g:6.0f} {p['lane'][0]/tot:5.2f} {p['lane'][1]/tot:5.2f} {p['lane'][2]/tot:5.2f} {p['wx']/max(1,p['walk']):8.0f},{p['wy']/max(1,p['walk']):<8.0f} {p['camp']/max(1,p['walk']):7.2f}")

if __name__ == "__main__":
    main()
