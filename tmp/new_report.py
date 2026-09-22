# usage: uv run python tmp/new_report.py xp/a.json [...] — per opponent/side: wins, losses, no-result games (nobody scored), median steps
import json, sys, statistics, collections
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
cache_p = "tmp/new_report_cache.json"
try: cache = json.load(open(cache_p))
except Exception: cache = {}
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        d = json.load(open(path)); rows = collections.OrderedDict(); tot = [0, 0, 0]
        for r in d["requests"]:
            key = r["id"]; n_expected = d.get("n", 0)
            if key not in cache or len(cache[key]) < n_expected:
                det = dump(c.get_experience_request(r["id"])); eps = []
                for ep in det.get("episodes", []):
                    if ep.get("status") != "completed": continue
                    try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                    except Exception: continue
                    rw = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                    eps.append([1 if rw.get(r["seat"]) else 0, 1 if rw.get(5 - r["seat"]) else 0, st.get("steps") or 0])
                cache[key] = eps
            eps = cache[key]
            w = sum(e[0] for e in eps); l = sum(e[1] for e in eps); nr = sum(1 for e in eps if not e[0] and not e[1])
            steps = statistics.median([e[2] for e in eps]) if eps else 0
            k = (r["opp"].split(":")[0][-26:] + ":" + r["opp"].split(":")[-1], "Red " if r["side"] == 0 else "Blue")
            rows[k] = (w, l, nr, steps); tot[0] += w; tot[1] += l; tot[2] += nr
        print(f"== {path}  W {tot[0]} / L {tot[1]} / no-result {tot[2]}")
        for (opp, side), (w, l, nr, steps) in rows.items():
            print(f"  {opp:32s} {side}  W{w} L{l} N{nr}  steps {steps:6.0f}")
json.dump(cache, open(cache_p, "w"))
