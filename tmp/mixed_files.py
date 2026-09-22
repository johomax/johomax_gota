# usage: uv run python tmp/mixed_files.py [GLOB...] — per hosted batch file (time order): candidate version's n/mean/zeros, the live policy's hero in the same games (paired control), others' mean
import json, sys, glob, os, re, statistics
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"
cache_p = "tmp/mixed_files_cache.json"
try: cache = json.load(open(cache_p))
except Exception: cache = {}
pats = sys.argv[1:] or ["xp/mx*-v3[0-9][0-9]*.json"]
files = sorted({f for p in pats for f in glob.glob(p)}, key=os.path.getmtime)
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in files:
        m = re.search(r"-v(\d+)", path); ver = int(m.group(1)) if m else -1
        d = json.load(open(path)); cand = []; live = []; others = []; pairs = []
        for r in d["requests"]:
            key = r["id"]; e = cache.get(key)
            if e is None or e["done"] < e["total"]:
                det = dump(c.get_experience_request(key)); eps = []
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                    except Exception: continue
                    eps.append([(ps["position"], ps.get("policy_version"), ps.get("avg_reward") or 0, ME in ps["policy_name"]) for ps in st.get("policy_stats", [])])
                e = {"total": det.get("episode_count") or len(det.get("episodes", [])), "done": len(eps), "eps": eps}; cache[key] = e
            for ep in e["eps"]:
                mine = [x for x in ep if x[3]]; oth = [x[2] for x in ep if not x[3]]
                if oth: others.append(statistics.mean(oth))
                cs = [x[2] for x in mine if x[1] == ver]; ls = [x[2] for x in mine if x[1] != ver]
                cand += cs; live += ls
                if cs and ls: pairs.append((cs[0], ls[0]))
        if not cand: print(f"{os.path.basename(path):24s} v{ver} pending"); continue
        pr = f" paired n{len(pairs)} cand {statistics.mean(p[0] for p in pairs):5.0f} live {statistics.mean(p[1] for p in pairs):5.0f}" if pairs else ""
        print(f"{os.path.basename(path):24s} v{ver} n{len(cand):3d} mean {statistics.mean(cand):5.0f} zeros {sum(1 for x in cand if x == 0)/len(cand):.0%} others {statistics.mean(others) if others else 0:4.0f}{pr}")
json.dump(cache, open(cache_p, "w"))
