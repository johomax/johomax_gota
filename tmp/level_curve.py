# usage: uv run python tmp/level_curve.py xp/a.json [...] — per policy family: median tick at which heroes reached levels 4/6/8/10/12 (from levelAbility replay actions), share reaching each, final level; ours split by version
import json, sys, pathlib, urllib.request, collections, statistics
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"
FAM = [("Jordan", "ours"), ("relh", "relh"), ("richard", "richard"), ("khors", "khors"), ("aaron-gota-micro0922", "aaron-micro"), ("arena-codex", "arena-codex")]
LV = [4, 6, 8, 10, 12]
reach = collections.defaultdict(lambda: collections.defaultdict(list)); final = collections.defaultdict(list); games = collections.Counter()
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        d = json.load(open(path))
        for r in d["requests"]:
            det = dump(c.get_experience_request(r["id"]))
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed": continue
                eid = ep["id"]; fp = pathlib.Path("tmp/replays") / f"{eid}.replay"
                try:
                    if not fp.exists():
                        url = dump(c.get_episode_request(eid)).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
                    rep = load_replay(str(fp)); st = dump(c.get_episode_request_episode_stats(eid))
                except Exception as ex: print("skip", eid, ex); continue
                names = {ps["position"]: (ps["policy_name"], ps.get("policy_version")) for ps in st["policy_stats"]}
                ups = collections.defaultdict(list)
                for a in rep["actions"]:
                    if a["kind"] == "levelAbility": ups[a["heroId"]].append(a["tick"])
                for pos, (nm, ver) in names.items():
                    fam = next((f for k, f in FAM if k in nm), None)
                    if fam is None: continue
                    if fam == "ours": fam = f"ours v{ver}"
                    ticks = sorted(ups.get(100 + pos, [])); lvl = 1 + len(ticks); games[fam] += 1; final[fam].append(lvl)
                    for L in LV:
                        if lvl >= L: reach[fam][L].append(ticks[L - 2])
                        else: reach[fam][L].append(None)
print(f"{'family':14s} n   " + "  ".join(f"L{L:<2d} med-tick reach" for L in LV) + "   final lvl mean")
for fam in sorted(games, key=lambda f: -games[f]):
    cells = []
    for L in LV:
        v = [t for t in reach[fam][L] if t is not None]
        cells.append(f"{statistics.median(v):6.0f} {len(v)/len(reach[fam][L]):4.0%}   " if v else f"{'-':>6s} {0:4.0%}   ")
    print(f"{fam:14s} {games[fam]:3d} " + " ".join(cells) + f" {statistics.mean(final[fam]):5.1f}")
