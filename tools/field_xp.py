#!/usr/bin/env python3
"""What does each policy's hero do in hosted random-roster batches, by side? (replay command patterns)

usage: uv run python tools/field_xp.py xp/a.json [...] [--min-games N]
Per policy x side: games, win rate, commands per game (tower by lane/tier, guard ids 28-31, fort, hero, foot, walk),
median first tower / guard / fort attack tick, and command share per 2000-tick window.
"""
import argparse, json, pathlib, statistics, sys, urllib.request
from collections import Counter, defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp

def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def tower_info(tid):
    off = tid - 10; return off // 6, (off % 6) // 3, off % 3

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("paths", nargs="+"); ap.add_argument("--min-games", type=int, default=30)
    ap.add_argument("--only", default=None, help="substring filter on policy label")
    a = ap.parse_args()
    rdir = ROOT / "tmp/replays"; rdir.mkdir(parents=True, exist_ok=True)
    rc_p = ROOT / "tmp/roster_cache.json"; rc = json.load(open(rc_p)) if rc_p.exists() else {}
    per = defaultdict(lambda: {"g": 0, "w": 0, "tower": Counter(), "guard": 0, "fort": 0, "hero": 0, "foot": 0, "walk": 0, "wx": 0.0, "wy": 0.0,
                               "ft": [], "fg": [], "ff": [], "win": defaultdict(Counter), "guard_games": 0, "fort_games": 0})
    n = 0
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in a.paths:
            d = json.load(open(path))
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    eid = ep["id"]
                    if eid not in rc:
                        try:
                            st = dump(c.get_episode_request_episode_stats(eid))
                            seats = {ps["position"]: (f'{ps.get("policy_name")}:v{ps.get("policy_version")}', ps.get("avg_reward") or 0) for ps in st.get("policy_stats", [])}
                            if len(seats) < 10: continue
                            rc[eid] = [[seats[i][0] for i in range(10)], [seats[i][1] for i in range(10)]]
                        except Exception: continue
                    labels, rewards = rc[eid]
                    f = rdir / (eid + ".replay")
                    if not f.exists():
                        url = ep.get("replay_url")
                        if not url:
                            try: url = dump(c.get_episode_request(eid)).get("replay_url")
                            except Exception: url = None
                        if not url: continue
                        try: urllib.request.urlretrieve(url, f)
                        except Exception as ex: print("dl fail", eid, ex, file=sys.stderr); continue
                    try: rep = rp.load_replay(f)
                    except Exception as ex: print("parse fail", eid, repr(ex)[:80], file=sys.stderr); continue
                    n += 1
                    heroes = {h["id"]: h for h in rep["header"]["setup"]["heroes"]}
                    st = {hid: {"tower": Counter(), "guard": 0, "fort": 0, "hero": 0, "foot": 0, "walk": 0, "wx": 0.0, "wy": 0.0, "ft": None, "fg": None, "ff": None, "win": defaultdict(Counter)} for hid in heroes}
                    for act in rep["actions"]:
                        hid = act["heroId"]; s = st.get(hid)
                        if s is None: continue
                        team = 0 if hid < 105 else 1; w = act["tick"] // 2000
                        if act.get("kind") == "attackTarget":
                            tid = act["targetId"]
                            if 10 <= tid <= 27:
                                lane, tteam, tier = tower_info(tid)
                                if tteam == team: continue
                                s["tower"][(lane if team == 0 else 2 - lane, tier)] += 1; s["win"][w]["tower"] += 1
                                if s["ft"] is None: s["ft"] = act["tick"]
                            elif 28 <= tid <= 31:
                                s["guard"] += 1; s["win"][w]["guard"] += 1
                                if s["fg"] is None: s["fg"] = act["tick"]
                            elif tid in (1, 2):
                                s["fort"] += 1; s["win"][w]["fort"] += 1
                                if s["ff"] is None: s["ff"] = act["tick"]
                            elif 100 <= tid <= 109: s["hero"] += 1; s["win"][w]["hero"] += 1
                            else: s["foot"] += 1; s["win"][w]["foot"] += 1
                        elif act.get("kind") == "walkTo":
                            x, y = act.get("x"), act.get("y")
                            if x is None: continue
                            if team == 1: x, y = 115 - x, 115 - y
                            s["walk"] += 1; s["wx"] += x; s["wy"] += y; s["win"][w]["walk"] += 1
                    for hid, h in heroes.items():
                        seat = h["slot"] + (5 if h["team"] == 1 else 0)
                        lab = labels[seat]
                        if a.only and a.only not in lab: continue
                        key = (lab, "Red" if h["team"] == 0 else "Blue"); p = per[key]; s = st[hid]
                        p["g"] += 1; p["w"] += int(bool(rewards[seat]))
                        p["tower"].update(s["tower"]); p["guard"] += s["guard"]; p["fort"] += s["fort"]; p["hero"] += s["hero"]; p["foot"] += s["foot"]
                        p["walk"] += s["walk"]; p["wx"] += s["wx"]; p["wy"] += s["wy"]
                        p["guard_games"] += int(s["guard"] > 0); p["fort_games"] += int(s["fort"] > 0)
                        for k in ("ft", "fg", "ff"):
                            if s[k] is not None: p[k].append(s[k])
                        for w, cnt in s["win"].items(): p["win"][w].update(cnt)
    json.dump(rc, open(rc_p, "w"))
    print(f"episodes {n}")
    med = lambda xs: int(statistics.median(xs)) if xs else -1
    for (lab, side), p in sorted(per.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        g = p["g"]
        if g < a.min_games: continue
        lanes = Counter(); tiers = Counter()
        for (lane, tier), v in p["tower"].items(): lanes[lane] += v; tiers[tier] += v
        tt = sum(lanes.values()) or 1
        print(f"\n{lab[:40]:40s} {side:4s} g={g:3d} win={p['w']/g:.3f}  cmds/g: tower {tt/g:5.0f} (lanes {lanes[0]/tt:.2f}/{lanes[1]/tt:.2f}/{lanes[2]/tt:.2f}; tiers {tiers[0]/tt:.2f}/{tiers[1]/tt:.2f}/{tiers[2]/tt:.2f}) guard {p['guard']/g:4.0f} fort {p['fort']/g:4.0f} hero {p['hero']/g:5.0f} foot {p['foot']/g:5.0f} walk {p['walk']/g:5.0f} meanWalk {p['wx']/max(1,p['walk']):.0f},{p['wy']/max(1,p['walk']):.0f}")
        print(f"    first tower {med(p['ft'])} ({len(p['ft'])}/{g})  first guard {med(p['fg'])} ({p['guard_games']}/{g})  first fort {med(p['ff'])} ({p['fort_games']}/{g})")
        line = "    per 2k window (tower/guard/fort/hero/foot/walk per game): "
        for w in range(6):
            c = p["win"].get(w, Counter()); line += f" {w*2}k[{c['tower']/g:.0f}/{c['guard']/g:.0f}/{c['fort']/g:.0f}/{c['hero']/g:.0f}/{c['foot']/g:.0f}/{c['walk']/g:.0f}]"
        print(line)

if __name__ == "__main__":
    main()
