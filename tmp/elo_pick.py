# usage: uv run python tmp/elo_pick.py v212 v267 ... — Elo-weighted expected gain per round over tmp/league_mix.json using cached matrix cells
import json, glob, sys, re, collections
ROOT = "."
RATING = {"relh-gods": 1928, "richard-gods": 1777, "aaron-gota-ir-formation-profile-pruned-0920-coach": 1701, "aaron-gota-ir-formation-profile-pruned-0920:": 1659,
          "arena-codex": 1636, "macromackie": 1591, "red-kite": 1562, "nancy": 1543, "black-kite": 1520, "gota-g002": 1528, "gota-g003": 1500}
OURS = 1620
def rating(label):
    for k, v in RATING.items():
        if label.startswith(k): return v
    return 1550
cache = json.load(open("tmp/matrix_cache.json"))
res = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
for f in sorted(glob.glob("xp/mx*.json")):
    d = json.load(open(f)); ver = d["candidate"].split(":")[-1]
    for r in d["requests"]:
        if r["id"] in cache:
            w, n = cache[r["id"]]; t = res[ver][(r["opp"], r["side"])]; t[0] += w; t[1] += n
mix = collections.Counter()
for e in json.load(open("tmp/league_mix.json")):
    opp = [l for l in e["seat_policies"] if l and l != "?" and not l.startswith("Jordan")]
    if opp: mix[opp[0]] += 1
total = sum(mix.values()); print(f"mix ({total} games):", ", ".join(f"{l[:28]}:{n}" for l, n in mix.most_common()))
vers = sys.argv[1:] or sorted(res)
print(f"{'ver':6s} {'winrate':>8s} {'elo/game':>9s} {'cells':>6s}  per-label p(win) Red/Blue")
for ver in vers:
    if ver not in res: print(ver, "no cells"); continue
    exp = 0.0; gain = 0.0; cov = 0; parts = []
    for label, n in mix.most_common():
        e = 1 / (1 + 10 ** ((rating(label) - OURS) / 400))
        ps = []
        for side in (0, 1):
            w, g = res[ver].get((label, side), [0, 0]); ps.append(w / g if g else None); cov += g > 0
        p = sum(x if x is not None else e for x in ps) / 2
        exp += n * p; gain += n * (p - e)
        parts.append(f"{label[:10]}:{'-' if ps[0] is None else f'{ps[0]:.2f}'}/{'-' if ps[1] is None else f'{ps[1]:.2f}'}")
    print(f"{ver:6s} {exp/total:8.3f} {8*gain/total:9.2f} {cov:3d}/{2*len(mix)}  " + " ".join(parts))
