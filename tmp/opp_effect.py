# usage: uv run python tmp/opp_effect.py xp/a.json [...] — our hero's mean score split by each other policy's presence on the enemy team vs our team vs absent (which opponents hurt us)
import json, sys, statistics, collections
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"
cache_p = "tmp/mixed_files_cache.json"
try: cache = json.load(open(cache_p))
except Exception: cache = {}
names_p = "tmp/opp_names_cache.json"
try: names = json.load(open(names_p))
except Exception: names = {}
rows = []  # (our score, our team, {name: team})
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        d = json.load(open(path))
        for r in d["requests"]:
            key = r["id"]
            if key not in names:
                det = dump(c.get_experience_request(key)); eps = []
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                    except Exception: continue
                    eps.append([(ps["position"], ps["policy_name"], ps.get("policy_version"), ps.get("avg_reward") or 0) for ps in st.get("policy_stats", [])])
                names[key] = eps
            for ep in names[key]:
                for pos, nm, ver, sc in ep:
                    if ME in nm:
                        rows.append((sc, pos // 5, {f"{n[:26]}:v{v}": p // 5 for p, n, v, s in ep if ME not in n}))
json.dump(names, open(names_p, "w"))
stat = collections.defaultdict(lambda: {"foe": [], "mate": [], "absent": []})
allnames = {k for _, _, m in rows for k in m}
for sc, team, m in rows:
    for k in allnames:
        if k not in m: stat[k]["absent"].append(sc)
        elif m[k] == team: stat[k]["mate"].append(sc)
        else: stat[k]["foe"].append(sc)
print(f"our hero games {len(rows)} mean {statistics.mean(r[0] for r in rows):.0f}")
def f(v): return f"{statistics.mean(v):5.0f}(n{len(v):3d})" if v else "     -     "
for k, s in sorted(stat.items(), key=lambda kv: statistics.mean(kv[1]['foe']) if kv[1]['foe'] else 9e9):
    print(f"{k:32s} foe {f(s['foe'])} mate {f(s['mate'])} absent {f(s['absent'])}")
