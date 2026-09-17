#!/usr/bin/env python3
"""Per-matchup race analysis for tools/xp_league.py homo runs (five copies vs five copies).

usage: uv run python tools/homo_stats.py xp/homo-v209.json [...]
Per (opponent, our side): games, wins, median length, each team's first tower/gate/guard/fort attack, heroes on the guards,
physical-lane shares of each team's tower attacks, and dead time per hero (command gaps >= 40 ticks).
"""
import json, pathlib, statistics, sys, urllib.request
from collections import defaultdict, Counter
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def short(l): return l.split(":")[0].replace("-gods-of-the-arena", "").replace("aaron-gota-ir-", "aaron:")[:26]

def game(rep):
    T = rep["ticks"]; first = {}; who = defaultdict(set); lanes = {0: Counter(), 1: Counter()}; last = {}; gaps = {0: 0, 1: 0}
    for a in rep["actions"]:
        hid = a["heroId"]; team = 0 if hid < 105 else 1; t = a["tick"]
        if t - last.get(hid, 0) >= 40: gaps[team] += t - last.get(hid, 0)
        last[hid] = t
        if a.get("kind") != "attackTarget": continue
        tid = a["targetId"]
        if 10 <= tid <= 27:
            lane, tteam, tier = (tid - 10) // 6, ((tid - 10) % 6) // 3, (tid - 10) % 3
            if tteam == team: continue
            lanes[team][lane] += 1; kind = "gate" if tier == 2 else "tower"
        elif 28 <= tid <= 31: kind = "guard"; who[team].add(hid)
        elif tid in (1, 2): kind = "fort"
        else: continue
        first.setdefault((team, kind), t)
    return T, first, who, lanes, gaps

def main():
    rdir = ROOT / "tmp/replays"; rdir.mkdir(parents=True, exist_ok=True)
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in sys.argv[1:]:
            d = json.load(open(path)); print(f"== {path}")
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"])); rows = []
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    eid = ep["id"]; f = rdir / (eid + ".replay")
                    if not f.exists():
                        url = ep.get("replay_url")
                        if not url:
                            try: url = dump(c.get_episode_request(eid)).get("replay_url")
                            except Exception: url = None
                        if not url: continue
                        try: urllib.request.urlretrieve(url, f)
                        except Exception: continue
                    try: rep = rp.load_replay(f)
                    except Exception: continue
                    try:
                        st = dump(c.get_episode_request_episode_stats(eid)); rw = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                        win = 1 if rw.get(r["seat"]) else 0
                    except Exception: win = -1
                    rows.append((win, game(rep)))
                if not rows: print(f"  {short(r['opp']):26s} ours {'Red ' if r['side'] == 0 else 'Blue'}: no games"); continue
                us = r["side"]; them = 1 - us
                def med(k, team): v = [g[1].get((team, k), -1) for _, g in rows]; v = [x for x in v if x >= 0]; return f"{int(statistics.median(v)) if v else -1:5d}({len(v)}/{len(rows)})"
                def lanes(team):
                    tot = Counter()
                    for _, g in rows: tot.update(g[3][team])
                    s = sum(tot.values()) or 1; return f"{tot[0]/s:.2f}/{tot[1]/s:.2f}/{tot[2]/s:.2f}"
                wins = sum(1 for w, _ in rows if w == 1)
                print(f"  {short(r['opp']):26s} ours {'Red ' if us == 0 else 'Blue'}: {wins}/{len(rows)} win, ticks {int(statistics.median([g[0] for _, g in rows]))}")
                print(f"      ours : tower {med('tower', us)} gate {med('gate', us)} guard {med('guard', us)} (heroes {statistics.mean([len(g[2][us]) for _, g in rows]):.1f}) fort {med('fort', us)} lanes {lanes(us)} dead/hero {statistics.mean([g[4][us] for _, g in rows])/5:.0f}")
                print(f"      theirs: tower {med('tower', them)} gate {med('gate', them)} guard {med('guard', them)} (heroes {statistics.mean([len(g[2][them]) for _, g in rows]):.1f}) fort {med('fort', them)} lanes {lanes(them)} dead/hero {statistics.mean([g[4][them] for _, g in rows])/5:.0f}")

if __name__ == "__main__":
    main()
