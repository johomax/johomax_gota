#!/usr/bin/env python3
"""Our hero's telemetry from REAL league games (docs/league_episodes.json + private policy logs).
usage: uv run python tools/league_logs.py [--min-version 87] [--cache tmp/league_log_cache.json]
Fetches our policy log per league episode (cached), parses it with tools/log_stats.parse_log and prints: per class deaths/kills/level/win,
and our win rate + deaths split by which strong entrants sit on the enemy team.
"""
import argparse, json, pathlib, sys
from collections import defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from log_stats import parse_log  # noqa: E402
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--min-version", type=int, default=87); ap.add_argument("--cache", default="tmp/league_log_cache.json")
    ap.add_argument("--only-version", type=int, default=None); a = ap.parse_args()
    cp = ROOT / a.cache; cache = json.load(open(cp)) if cp.exists() else {}
    eps = [e for e in json.load(open(ROOT / "docs/league_episodes.json")) if e.get("win") is not None and (e.get("my_version") or 0) >= a.min_version]
    if a.only_version: eps = [e for e in eps if e.get("my_version") == a.only_version]
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for e in eps:
            if e["ereq"] in cache: continue
            try:
                log = c.get_episode_request_policy_log(e["ereq"], e["my_pv"], e["seat"])
                cache[e["ereq"]] = log if isinstance(log, str) else (log.decode() if isinstance(log, (bytes, bytearray)) else str(log))
            except Exception as ex:
                print("log fail", e["ereq"], repr(ex)[:80], file=sys.stderr)
        json.dump(cache, open(cp, "w"))
    rows = []
    for e in eps:
        if e["ereq"] not in cache: continue
        d = parse_log(cache[e["ereq"]]); d.pop("acts", None); d.pop("dc", None)
        enemy = [p.split(":")[0] for s, p in enumerate(e["seat_policies"]) if (0 if s < 5 else 1) != e["team"]]
        rows.append(dict(e=e, log=d, enemy=enemy))
    print(f"league games with logs: {len(rows)} (versions {sorted({r['e']['my_version'] for r in rows})})")
    def table(groups, label):
        print(f"-- {label:28s} {'n':>4s} {'win':>5s} {'deaths':>7s} {'hkills':>7s} {'tkills':>7s} {'level':>6s} {'stuck':>6s}")
        for g, rs in groups:
            if not rs: continue
            n = len(rs); f = lambda k: sum(r["log"][k] for r in rs) / n
            print(f"   {str(g):28s} {n:4d} {sum(r['e']['win'] for r in rs)/n:5.2f} {f('deaths'):7.2f} {f('hero_kills'):7.2f} {f('tower_kills'):7.2f} {f('level'):6.2f} {f('stuck'):6.1f}")
    bycls = defaultdict(list)
    for r in rows: bycls[r["e"]["cls"]].append(r)
    table(sorted(bycls.items(), key=lambda kv: -len(kv[1])), "by class")
    table([("Red", [r for r in rows if r["e"]["team"] == 0]), ("Blue", [r for r in rows if r["e"]["team"] == 1])], "by side")
    strong = ["richard-gods-of-the-arena", "black-kite", "games-bond-gota", "gota-codex-secondary-current-map-lanes-20260915", "khors", "nancy-goa", "red-kite", "relh-gods-of-the-arena"]
    table([(f"vs {s[:20]}", [r for r in rows if s in r["enemy"]]) for s in strong] + [("vs none of those top-4", [r for r in rows if not any(s in r["enemy"] for s in strong[:4])])], "by enemy entrant")
    table([("won", [r for r in rows if r["e"]["win"]]), ("lost", [r for r in rows if not r["e"]["win"]])], "by result")
main()
