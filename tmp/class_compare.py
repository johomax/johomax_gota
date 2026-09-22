# usage: uv run python tmp/class_compare.py xp/mx-v317.json [...] — per policy family and drafted class: games, mean score (from replays' draft actions + episode stats)
import json, sys, pathlib, urllib.request, collections, statistics
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]
FAM = [("Jordan", "ours"), ("richard", "richard"), ("relh", "relh"), ("khors", "khors")]
agg = collections.defaultdict(list)
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        for r in json.load(open(path))["requests"]:
            det = dump(c.get_experience_request(r["id"]))
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed": continue
                try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                except Exception: continue
                fp = pathlib.Path("tmp/replays") / f"{ep['id']}.replay"
                try:
                    if not fp.exists():
                        url = dump(c.get_episode_request(ep["id"])).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
                    rep = load_replay(str(fp))
                except Exception: continue
                cls = {}
                for a in rep["actions"]:
                    if a["kind"] == "draft" and a["heroId"] not in cls: cls[a["heroId"]] = a["first"]
                for ps in st["policy_stats"]:
                    fam = next((f for k, f in FAM if k in ps["policy_name"]), None)
                    if not fam: continue
                    k = cls.get(100 + ps["position"], -1)
                    agg[(fam, CL[k] if 0 <= k < 10 else "?")].append(ps.get("avg_reward") or 0)
fams = ["ours", "richard", "relh", "khors"]
print(f"{'class':8s}" + "".join(f"{f:>18s}" for f in fams))
for cl in CL + ["?"]:
    row = f"{cl:8s}"
    for f in fams:
        v = agg.get((f, cl), []); row += f"{(str(len(v)) + ' x ' + str(round(statistics.mean(v)))) if v else '-':>18s}"
    print(row)
for f in fams:
    v = [x for (ff, _), vals in agg.items() if ff == f for x in vals]
    if v: print(f"{f}: n{len(v)} mean {statistics.mean(v):.0f}")
