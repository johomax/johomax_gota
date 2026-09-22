# usage: uv run python tmp/score_report.py xp/a.json [...] — new ladder score (mean XP - 200/min) per opponent/side: ours vs theirs, steps
import json, sys, statistics, collections
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        d = json.load(open(path)); allo = []; allt = []
        print(f"== {path}")
        for r in d["requests"]:
            det = dump(c.get_experience_request(r["id"])); ours = []; theirs = []; steps = []
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed": continue
                try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                except Exception: continue
                sc = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                ours.append(sc.get(r["seat"], 0)); theirs.append(sc.get(5 - r["seat"], 0)); steps.append(st.get("steps") or 0)
            if not ours: continue
            allo += ours; allt += theirs
            print(f"  {r['opp'][:34]:34s} {'Red ' if r['side'] == 0 else 'Blue'} n{len(ours)} ours {statistics.mean(ours):6.0f} theirs {statistics.mean(theirs):6.0f} steps {statistics.median(steps):6.0f}")
        if allo: print(f"  TOTAL n{len(allo)} ours {statistics.mean(allo):.0f} theirs {statistics.mean(allt):.0f}")
