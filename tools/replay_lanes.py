#!/usr/bin/env python3
"""Which lane decided each hosted game, and did our hero take part?

usage: uv run python tools/replay_lanes.py xp/a.json [...] [--limit N]
Downloads each completed episode's replay (cached in tmp/replays), parses hero actions with tools/replay_parse.py logic, and reports:
winner's breakthrough lane (lane of the enemy gate tower the winning team's heroes attacked most; 'creeps' if none), whether our hero
attacked the enemy fort / gate tower, and the number of our hero's tower/hero attack commands.
"""
import argparse, json, pathlib, subprocess, sys, urllib.request
from collections import Counter, defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp  # noqa: E402

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

def tower_info(tid):
    off = tid - 10; lane = off // 6; team = (off % 6) // 3; tier = off % 3
    return lane, team, tier

def analyze(path):
    data = rp.load_replay(path) if hasattr(rp, "load_replay") else None
    return data

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("paths", nargs="+"); ap.add_argument("--limit", type=int, default=100000)
    a = ap.parse_args()
    rdir = ROOT / "tmp/replays"; rdir.mkdir(parents=True, exist_ok=True)
    cache_p = ROOT / "tmp/lane_cache.json"; cache = json.load(open(cache_p)) if cache_p.exists() else {}
    rows = []
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in a.paths:
            d = json.load(open(path)); cand = d["candidate"]
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    if len(rows) >= a.limit: break
                    eid = ep["id"]
                    if eid in cache:
                        rows.append((path, cache[eid])); continue
                    url = ep.get("replay_url")
                    if not url:
                        try: url = dump(c.get_episode_request(eid)).get("replay_url")
                        except Exception: url = None
                    if not url: continue
                    try:
                        st = dump(c.get_episode_request_episode_stats(eid))
                        seats = {ps["position"]: (f'{ps.get("policy_name")}:v{ps.get("policy_version")}', ps.get("avg_reward") or 0) for ps in st.get("policy_stats", [])}
                        mine = [i for i in range(10) if seats[i][0] == cand]
                        if not mine: continue
                        seat = mine[0]; win = int(bool(seats[seat][1]))
                        red_won = any(seats[i][1] for i in range(5))
                    except Exception as ex:
                        continue
                    f = rdir / (eid + ".replay")
                    if not f.exists():
                        try: urllib.request.urlretrieve(url, f)
                        except Exception as ex: print("dl fail", eid, ex, file=sys.stderr); continue
                    try:
                        out = subprocess.run([sys.executable, str(ROOT / "tools/replay_parse.py"), str(f), "--json"], capture_output=True, text=True, timeout=300)
                        rep = json.loads(out.stdout)
                    except Exception as ex:
                        print("parse fail", eid, repr(ex)[:100], file=sys.stderr); continue
                    acts = rep["actions"]; ticks = rep.get("ticks")
                    winner = 0 if red_won else 1
                    my_id = 100 + seat
                    gate_hits = Counter(); fort_by_team = {0: None, 1: None}; my = Counter(); team_tower_hits = Counter()
                    first_gate_tick = {}
                    for act in acts:
                        if act.get("kind") != "attackTarget": continue
                        hid = act["heroId"]; team = 0 if hid < 105 else 1; tid = act["targetId"]
                        if 10 <= tid <= 27:
                            lane, tteam, tier = tower_info(tid)
                            if tteam == team: continue
                            team_tower_hits[(team, lane, tier)] += 1
                            if tier == 2:
                                gate_hits[(team, lane)] += 1
                                first_gate_tick.setdefault((team, lane), act["tick"])
                            if hid == my_id: my[f"tower{tier}"] += 1
                        elif tid in (1, 2):
                            if fort_by_team[team] is None: fort_by_team[team] = act["tick"]
                            if hid == my_id: my["fort"] += 1
                        elif 100 <= tid <= 109:
                            if hid == my_id: my["hero"] += 1
                        elif hid == my_id: my["foot"] += 1
                    wl = [(l, n) for (t, l), n in gate_hits.items() if t == winner]
                    wl.sort(key=lambda x: -x[1])
                    lane = wl[0][0] if wl else -1
                    my_lane_hits = {l: sum(n for (t, ll, tier), n in team_tower_hits.items() if t == (0 if seat < 5 else 1) and ll == l) for l in range(3)}
                    rec = {"seat": seat, "win": win, "ticks": ticks, "winner": winner, "win_lane": lane, "fort_tick": fort_by_team[winner],
                           "hero_fort": fort_by_team[winner] is not None, "my": dict(my), "my_team_lane_hits": my_lane_hits,
                           "n_gate_attackers_winner": len({act["heroId"] for act in acts if act.get("kind") == "attackTarget" and 10 <= act["targetId"] <= 27 and tower_info(act["targetId"])[2] == 2 and tower_info(act["targetId"])[1] != (0 if act["heroId"] < 105 else 1) and ((0 if act["heroId"] < 105 else 1) == winner)})}
                    cache[eid] = rec; rows.append((path, rec))
            json.dump(cache, open(cache_p, "w"))
    json.dump(cache, open(cache_p, "w"))
    CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]
    print(f"games {len(rows)}")
    c = Counter((r["win_lane"]) for _, r in rows); print("winner breakthrough lane (Red lane k mirrors Blue lane 2-k; -1 = creeps only):", dict(c))
    c = Counter(("W" if r["win"] else "L", r["hero_fort"]) for _, r in rows); print("hero attacked fort by our result:", dict(c))
    c = Counter(("W" if r["win"] else "L", min(r["n_gate_attackers_winner"], 4)) for _, r in rows); print("winner gate attackers (heroes) by our result:", dict(sorted(c.items())))
    # our hero involvement
    for res in ("W", "L"):
        sub = [r for _, r in rows if ("W" if r["win"] else "L") == res]
        if not sub: continue
        avg = lambda k: sum(r["my"].get(k, 0) for r in sub) / len(sub)
        print(f"{res}: n={len(sub)} mean ticks {sum(r['ticks'] or 0 for r in sub)/len(sub):.0f} my cmds: tower0 {avg('tower0'):.0f} tower1 {avg('tower1'):.0f} tower2 {avg('tower2'):.0f} fort {avg('fort'):.0f} hero {avg('hero'):.0f} foot {avg('foot'):.0f}")
    # in wins: was the breakthrough lane our push lane? our push lane = 2 for Red(seat<5), 0 for Blue in v19
    wins = [r for _, r in rows if r["win"]]
    mine_lane = sum(1 for r in wins if r["win_lane"] == (2 if r["seat"] < 5 else 0)); print(f"wins where breakthrough lane == our fixed push lane: {mine_lane}/{len(wins)}")
    c = Counter((CL[(r['seat'] % 5) + (5 if r['seat'] < 5 else 0)], r["win_lane"]) for _, r in rows if r["win"]); print("per class win-lane:", dict(sorted(c.items())))
    c = Counter(r["win_lane"] for _, r in rows if not r["win"]); print("enemy breakthrough lane when we lose:", dict(c))

if __name__ == "__main__":
    main()
