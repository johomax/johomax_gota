# usage: uv run python tmp/duel_read.py xp/duel-vNNN.json CAND CTRL — paired per-episode scores of our CAND and CTRL versions (same game, seats s and s+5): n, means, delta, SE, per-seat lines
import json, sys, statistics, math, collections
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"
path, cand, ctrl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
cache_p = "tmp/mixed_files_cache.json"
try: cache = json.load(open(cache_p))
except Exception: cache = {}
d = json.load(open(path)); pairs = []; byseat = collections.defaultdict(list); others = []
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
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
            cs = [x for x in ep if x[3] and x[1] == cand]; ks = [x for x in ep if x[3] and x[1] == ctrl]
            oth = [x[2] for x in ep if not x[3]]
            if cs and ks:
                pairs.append((cs[0][2], ks[0][2])); byseat[cs[0][0]].append(cs[0][2] - ks[0][2])
                if oth: others.append(statistics.mean(oth))
json.dump(cache, open(cache_p, "w"))
if not pairs: print("no paired episodes yet"); sys.exit(0)
diffs = [a - b for a, b in pairs]; n = len(diffs); se = statistics.pstdev(diffs) / math.sqrt(n) if n > 1 else 0
print(f"{path}: v{cand} vs v{ctrl} paired n{n} cand {statistics.mean(a for a,_ in pairs):5.0f} ctrl {statistics.mean(b for _,b in pairs):5.0f} delta {statistics.mean(diffs):+5.0f} se {se:4.0f} cand>ctrl {sum(1 for x in diffs if x > 0)}/{n} zeros cand {sum(1 for a,_ in pairs if a==0)} ctrl {sum(1 for _,b in pairs if b==0)} others {statistics.mean(others) if others else 0:4.0f}")
print("  by cand seat: " + "  ".join(f"s{s}:{statistics.mean(v):+5.0f}(n{len(v)})" for s, v in sorted(byseat.items())))
