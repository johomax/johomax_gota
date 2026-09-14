#!/usr/bin/env python3
"""Summarize our hero's telemetry across hosted episodes (xp.py / xp_mixed.py request files).

usage: uv run python tools/log_stats.py xp/a.json [...] [--cache tmp/log_cache.json] [--dump]
Per episode: seat, class, win, deaths, kill rewards, final level/gold, max objective index, STUCK count, last tick seen.
Then aggregates by win/loss and by class.
"""
import argparse, json, pathlib, re, sys
from collections import defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLASSES = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

def parse_log(txt):
    d = {"deaths": 0, "kills": 0, "kill_gold": 0, "stuck": 0, "max_oi": 0, "level": 1, "gold": 0, "last_t": 0, "hero_kills": 0, "tower_kills": 0, "acts": defaultdict(int), "mode": None, "lanes": 0}
    for line in txt.splitlines():
        p = line.split()
        if not p: continue
        if p[0] == "D": d["deaths"] += 1
        elif p[0] == "K":
            g = int(p[2]); d["kills"] += 1; d["kill_gold"] += g
            if g >= 100: d["hero_kills"] += 1
            elif g == 75: d["tower_kills"] += 1
        elif p[0] == "STUCK": d["stuck"] += 1
        elif p[0] == "LANE": d["lanes"] += 1
        elif p[0] == "MODE": d["mode"] = p[1]
        elif p[0] == "T":
            try:
                d["last_t"] = int(p[1]); d["level"] = int(p[7][1:]); d["gold"] = int(p[8][1:])
                oi = int(p[10]); d["max_oi"] = max(d["max_oi"], oi); d["acts"][p[12]] += 1
            except Exception:
                pass
    d["acts"] = dict(d["acts"])
    return d

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("paths", nargs="+"); ap.add_argument("--cache", default="tmp/log_cache.json"); ap.add_argument("--dump", action="store_true")
    a = ap.parse_args()
    cp = ROOT / a.cache; cp.parent.mkdir(exist_ok=True)
    cache = json.load(open(cp)) if cp.exists() else {}
    rows = []
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for path in a.paths:
            d = json.load(open(path)); cand = d["candidate"]
            for r in d["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    key = ep["id"]
                    if key not in cache:
                        try:
                            st = dump(c.get_episode_request_episode_stats(ep["id"]))
                            seats = {ps["position"]: (f'{ps.get("policy_name")}:v{ps.get("policy_version")}', ps.get("avg_reward") or 0, str(ps.get("policy_version_id"))) for ps in st.get("policy_stats", [])}
                            mine = [i for i in range(10) if seats.get(i, ("",))[0] == cand]
                            if not mine: continue
                            seat = mine[0]
                            log = c.get_episode_request_policy_log(ep["id"], seats[seat][2], seat)
                            txt = log if isinstance(log, str) else (log.decode() if isinstance(log, (bytes, bytearray)) else json.dumps(dump(log)))
                            cache[key] = {"seat": seat, "win": int(bool(seats[seat][1])), "txt": txt}
                        except Exception as ex:
                            print("skip", ep["id"], repr(ex)[:120], file=sys.stderr); continue
                    e = dict(cache[key]); e["log"] = parse_log(e.pop("txt")); rows.append((path, e))
    json.dump(cache, open(cp, "w"))
    agg = defaultdict(lambda: defaultdict(float)); cnt = defaultdict(int)
    for path, r in rows:
        seat = r["seat"]; cls = CLASSES[(seat % 5) + (5 if seat < 5 else 0)]
        for key in ((path, "W" if r["win"] else "L"), (path, "all"), ("cls", cls), ("cls", cls + ("W" if r["win"] else "L"))):
            cnt[key] += 1
            for k in ("deaths", "kills", "kill_gold", "stuck", "max_oi", "level", "gold", "last_t", "hero_kills", "tower_kills"):
                agg[key][k] += r["log"][k]
            agg[key]["wins"] += r["win"]
        if a.dump:
            print(path, seat, cls, "W" if r["win"] else "L", {k: r["log"][k] for k in ("deaths", "kills", "hero_kills", "tower_kills", "level", "gold", "max_oi", "stuck", "last_t")}, r["log"]["acts"])
    print(f"{'group':40s} {'n':>4s} {'win':>5s} {'deaths':>6s} {'kills':>6s} {'hk':>5s} {'tk':>5s} {'lvl':>5s} {'gold':>5s} {'maxoi':>5s} {'stuck':>5s} {'lastT':>6s}")
    for key in sorted(cnt, key=lambda k: (str(k[0]), str(k[1]))):
        n = cnt[key]; g = agg[key]
        print(f"{str(key)[:40]:40s} {n:4d} {g['wins']/n:5.2f} {g['deaths']/n:6.2f} {g['kills']/n:6.1f} {g['hero_kills']/n:5.2f} {g['tower_kills']/n:5.2f} {g['level']/n:5.2f} {g['gold']/n:5.0f} {g['max_oi']/n:5.2f} {g['stuck']/n:5.1f} {g['last_t']/n:6.0f}")

if __name__ == "__main__":
    main()
