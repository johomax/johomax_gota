# usage: uv run python tmp/mixed_pool.py 317 320 324 ... — pooled league-format score over every xp/mx*-vNNN.json batch: n, mean, zero share, mean of others
import json, sys, glob, statistics
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"
cache_p = "tmp/mixed_pool_cache.json"
try: cache = json.load(open(cache_p))
except Exception: cache = {}
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for v in sys.argv[1:]:
        ours = []; theirs = []; files = sorted(glob.glob(f"xp/mx*-v{v}.json"))
        for path in files:
            d = json.load(open(path))
            for r in d["requests"]:
                key = r["id"]
                if key not in cache or cache[key]["n"] < 2:
                    det = dump(c.get_experience_request(r["id"])); o = []; t = []
                    for ep in det.get("episodes", []):
                        if ep.get("status") != "completed": continue
                        try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                        except Exception: continue
                        for ps in st.get("policy_stats", []):
                            (o if ME in ps["policy_name"] else t).append(ps.get("avg_reward") or 0)
                    cache[key] = {"n": len(o), "o": o, "t": statistics.mean(t) if t else 0}
                ours += cache[key]["o"]; theirs.append(cache[key]["t"])
        if ours: print(f"v{v}: n{len(ours):3d} mean {statistics.mean(ours):5.0f} median {statistics.median(ours):5.0f} zeros {sum(1 for x in ours if x == 0)/len(ours):.0%} others {statistics.mean(theirs):4.0f} files {len(files)}")
json.dump(cache, open(cache_p, "w"))
