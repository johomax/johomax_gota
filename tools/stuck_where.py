#!/usr/bin/env python3
"""Where do our heroes get stuck? Histogram of STUCK targets/positions per class from cached hosted logs.

usage: uv run python tools/stuck_where.py xp/a.json [...]   (run tools/log_stats.py on the same files first to fill the cache)
"""
import json, pathlib, re, sys
from collections import Counter, defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLS = {0: "DK", 1: "Xbow", 2: "Lich", 3: "Warlock", 4: "Berserk", 5: "VK", 6: "Ranger", 7: "Arcanist", 8: "Druid", 9: "DH"}
RX = re.compile(r"STUCK (\d+) at (\d+) (\d+) -> (\d+) (\d+) hits (\d+)")

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

cache = json.load(open(ROOT / "tmp/log_cache.json"))
eps = defaultdict(int); stuck = defaultdict(list)
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        for r in json.load(open(path))["requests"]:
            for ep in dump(c.get_experience_request(r["id"])).get("episodes", []):
                e = cache.get(ep["id"])
                if not e: continue
                cl = CLS[e["seat"]]; eps[cl] += 1
                for line in e["txt"].splitlines():
                    m = RX.match(line)
                    if m: stuck[cl].append(tuple(map(int, m.groups())) + (e["win"],))
for cl in CLS.values():
    if not eps[cl]: continue
    s = stuck[cl]; n = eps[cl]
    print(f"== {cl}: {n} games, {len(s)} STUCK ({len(s)/n:.1f}/game), median tick {sorted(x[0] for x in s)[len(s)//2] if s else '-'}")
    print("   targets  ", Counter((x[3], x[4]) for x in s).most_common(8))
    print("   positions", Counter((x[1] // 2 * 2, x[2] // 2 * 2) for x in s).most_common(8))
    print("   hits>=3  ", sum(1 for x in s if x[5] >= 3), " in wins", sum(1 for x in s if x[6]), " in losses", sum(1 for x in s if not x[6]))
