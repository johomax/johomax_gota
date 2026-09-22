# usage: uv run python tmp/mixed_score.py xp/mx-vNNN.json [...] — league-format score: our hero's mean XP-score per seat, the other nine heroes' mean, median steps
import json, sys, statistics
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        d = json.load(open(path)); allo = []; allt = []; rows = []
        for r in d["requests"]:
            det = dump(c.get_experience_request(r["id"])); ours = []; theirs = []; steps = []
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed": continue
                try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                except Exception: continue
                for ps in st.get("policy_stats", []):
                    if ME in ps["policy_name"]: ours.append(ps.get("avg_reward") or 0)
                    else: theirs.append(ps.get("avg_reward") or 0)
                steps.append(st.get("steps") or 0)
            if not ours: continue
            allo += ours; allt += theirs
            rows.append((r.get("seat"), len(ours), statistics.mean(ours), statistics.mean(theirs) if theirs else 0, statistics.median(steps)))
        print(f"== {path}")
        for seat, n, a, b, s in sorted(rows, key=lambda x: (x[0] is None, x[0])): print(f"  seat {seat} n{n} ours {a:6.0f} others {b:6.0f} steps {s:6.0f}")
        if allo: print(f"  TOTAL n{len(allo)} ours {statistics.mean(allo):.0f} others {statistics.mean(allt):.0f} zero-games {sum(1 for v in allo if v == 0)}")
