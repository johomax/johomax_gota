#!/usr/bin/env python3
"""Team-level race timelines for hosted league-like requests (tools/xp_league.py files).

usage: uv run python tools/lg_stats.py xp/lg-a.json [...]
Per episode (replay cached in tmp/replays): game length, winner, our seat/win, per team first gate/guard/fort attack tick and
heroes on the guards, our hero's first tower/guard attack and dead time (command gaps >= 40 ticks). Aggregates wins vs losses.
"""
import argparse, json, pathlib, statistics, sys, urllib.request
from collections import defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp

def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o

def analyze(rep, seat):
    T = rep["ticks"]; first = {}; who = defaultdict(set); my = 100 + seat; my_first = {}; last_t = 0; gaps = 0; gaptime = 0
    for a in rep["actions"]:
        hid = a["heroId"]; team = 0 if hid < 105 else 1
        if hid == my:
            if a["tick"] - last_t >= 40: gaps += 1; gaptime += a["tick"] - last_t
            last_t = a["tick"]
        if a.get("kind") != "attackTarget": continue
        tid = a["targetId"]
        if 10 <= tid <= 27:
            if ((tid - 10) % 6) // 3 == team: continue
            kind = "gate" if (tid - 10) % 3 == 2 else "tower"
        elif 28 <= tid <= 31: kind = "guard"
        elif tid in (1, 2): kind = "fort"
        elif 40 <= tid <= 51: kind = "barracks"
        else: continue
        first.setdefault((team, kind), a["tick"])
        if kind == "guard": who[team].add(hid)
        if hid == my: my_first.setdefault(kind, a["tick"])
    fk = [k for k in first if k[1] == "fort"]
    winner = max(fk, key=lambda k: first[k])[0] if fk else -1
    mt = seat // 5; et = 1 - mt
    return dict(T=T, winner=winner, my_team=mt, our_gate=first.get((mt, "gate"), -1), enemy_gate=first.get((et, "gate"), -1),
                our_guard=first.get((mt, "guard"), -1), enemy_guard=first.get((et, "guard"), -1), our_guard_heroes=len(who[mt]), enemy_guard_heroes=len(who[et]),
                our_fort=first.get((mt, "fort"), -1), enemy_fort=first.get((et, "fort"), -1), my_tower=my_first.get("tower", -1), my_gate=my_first.get("gate", -1),
                my_guard=my_first.get("guard", -1), my_barracks=my_first.get("barracks", -1), gaps=gaps, gaptime=gaptime)

def per_hero(rep):
    """first tower/gate/barracks/guard/fort attack tick and dead time per hero id"""
    out = {h["id"]: {"cls": h["class"], "team": h["team"], "slot": h["slot"], "gaps": 0, "gaptime": 0, "last": 0, "tower_cmds": 0} for h in rep["header"]["setup"]["heroes"]}
    for a in rep["actions"]:
        hid = a["heroId"]; o = out[hid]; t = a["tick"]
        if t - o["last"] >= 40: o["gaps"] += 1; o["gaptime"] += t - o["last"]
        o["last"] = t
        if a.get("kind") != "attackTarget": continue
        tid = a["targetId"]; team = o["team"]
        if 10 <= tid <= 27:
            if ((tid - 10) % 6) // 3 == team: continue
            kind = "gate" if (tid - 10) % 3 == 2 else "tower"; o["tower_cmds"] += 1
        elif 28 <= tid <= 31: kind = "guard"; o["tower_cmds"] += 1
        elif tid in (1, 2): kind = "fort"
        elif 40 <= tid <= 51: kind = "barracks"
        else: continue
        o.setdefault(kind, t)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("paths", nargs="+"); ap.add_argument("--dump", action="store_true"); a = ap.parse_args()
    rdir = ROOT / "tmp/replays"; rdir.mkdir(parents=True, exist_ok=True); rows = []
    rc_p = ROOT / "tmp/roster_cache.json"; rc = json.load(open(rc_p)) if rc_p.exists() else {}
    prog = defaultdict(lambda: defaultdict(list))
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in a.paths:
            d = json.load(open(path))
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"]))
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
                        except Exception as ex: print("dl fail", eid, ex, file=sys.stderr); continue
                    try: rep = rp.load_replay(f)
                    except Exception as ex: print("parse fail", eid, repr(ex)[:80], file=sys.stderr); continue
                    row = analyze(rep, r["seat"]); row["seat"] = r["seat"]; row["win"] = int(row["winner"] == row["my_team"]); row["eid"] = eid; rows.append(row)
                    if eid not in rc:
                        try:
                            st = dump(c.get_episode_request_episode_stats(eid))
                            seats = {ps["position"]: (f'{ps.get("policy_name")}:v{ps.get("policy_version")}', ps.get("avg_reward") or 0) for ps in st.get("policy_stats", [])}
                            if len(seats) == 10: rc[eid] = [[seats[i][0] for i in range(10)], [seats[i][1] for i in range(10)]]
                        except Exception: pass
                    if eid in rc:
                        labels, rewards = rc[eid]
                        row["win"] = int(bool(rewards[r["seat"]]))  # authoritative result (the fort-attack inference can be wrong)
                    if a.dump: print(json.dumps(row))
                    if eid in rc:
                        labels, rewards = rc[eid]
                        for hid, o in per_hero(rep).items():
                            seat = o["slot"] + (5 if o["team"] == 1 else 0); lab = labels[seat].split(":")[0][:22]
                            key = (lab, "Red" if o["team"] == 0 else "Blue"); p = prog[key]
                            p["g"].append(1); p["win"].append(int(bool(rewards[seat])))
                            for k in ("tower", "gate", "barracks", "guard", "fort"): p[k].append(o.get(k, -1))
                            p["gaps"].append(o["gaps"]); p["gaptime"].append(o["gaptime"]); p["tower_cmds"].append(o["tower_cmds"])
    json.dump(rc, open(rc_p, "w"))
    if not rows: print("no episodes"); return
    def med(xs): xs = [x for x in xs if x >= 0]; return int(statistics.median(xs)) if xs else -1
    print(f"episodes {len(rows)}  win {sum(r['win'] for r in rows)}/{len(rows)} = {sum(r['win'] for r in rows)/len(rows):.3f}  median ticks {med([r['T'] for r in rows])}")
    for side in (0, 1):
        rs = [r for r in rows if r["my_team"] == side]
        if rs: print(f"  {'Red' if side == 0 else 'Blue'}: {sum(r['win'] for r in rs)}/{len(rs)} = {sum(r['win'] for r in rs)/len(rs):.3f}")
    for label, rs in (("WON", [r for r in rows if r["win"]]), ("LOST", [r for r in rows if not r["win"]])):
        if not rs: continue
        print(f"-- {label} n={len(rs)}: ticks {med([r['T'] for r in rs])} | our team gate {med([r['our_gate'] for r in rs])} guard {med([r['our_guard'] for r in rs])} (heroes {statistics.mean([r['our_guard_heroes'] for r in rs]):.1f}) fort {med([r['our_fort'] for r in rs])} | enemy gate {med([r['enemy_gate'] for r in rs])} guard {med([r['enemy_guard'] for r in rs])} (heroes {statistics.mean([r['enemy_guard_heroes'] for r in rs]):.1f}) fort {med([r['enemy_fort'] for r in rs])}")
        print(f"       our hero: first tower {med([r['my_tower'] for r in rs])} gate {med([r['my_gate'] for r in rs])} ({sum(1 for r in rs if r['my_gate'] >= 0)}/{len(rs)}) barracks ({sum(1 for r in rs if r['my_barracks'] >= 0)}/{len(rs)}) guard {med([r['my_guard'] for r in rs])} ({sum(1 for r in rs if r['my_guard'] >= 0)}/{len(rs)}) | dead: gaps {statistics.mean([r['gaps'] for r in rs]):.1f} time {statistics.mean([r['gaptime'] for r in rs]):.0f}")

    print("-- per policy x side: games, win, median first tower/gate/barracks/guard/fort tick (share reaching), dead gaps/time, tower+guard cmds")
    def medshare(xs): v = [x for x in xs if x >= 0]; return f"{int(statistics.median(v)) if v else -1:5d}({len(v)/len(xs):.2f})"
    for key in sorted(prog, key=lambda k: (k[1], -sum(prog[k]["win"]) / max(1, len(prog[k]["g"])))):
        p = prog[key]; g = len(p["g"])
        print(f"   {key[0]:22s} {key[1]:4s} g={g:3d} win={sum(p['win'])/g:.3f} tower {medshare(p['tower'])} gate {medshare(p['gate'])} barracks {medshare(p['barracks'])} guard {medshare(p['guard'])} fort {medshare(p['fort'])} dead {statistics.mean(p['gaps']):.1f}/{statistics.mean(p['gaptime']):.0f} cmds {statistics.mean(p['tower_cmds']):.0f}")

if __name__ == "__main__":
    main()
