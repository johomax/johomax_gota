# usage: uv run python tmp/ep_log.py EPISODE_ID POSITION [EVERY] — one hosted hero's policy log: non-F lines plus every EVERY-th F line
import sys
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
eid, pos = sys.argv[1], int(sys.argv[2]); every = int(sys.argv[3]) if len(sys.argv) > 3 else 2
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    st = dump(c.get_episode_request_episode_stats(eid))
    ps = [p for p in st["policy_stats"] if p["position"] == pos][0]
    print("###", eid, "pos", pos, ps["policy_name"][:30], "v", ps.get("policy_version"), "score", ps.get("avg_reward"), "steps", st.get("steps"))
    log = c.get_episode_request_policy_log(eid, ps["policy_version_id"], pos)
    text = log if isinstance(log, str) else (dump(log).get("content") or dump(log).get("log") or str(log))
    i = 0
    for l in text.split("\n"):
        if l.startswith("F "):
            i += 1
            if i % every == 0:
                p = l.split(); print(p[1], "lane", p[3], "at", p[7], p[8], p[9], "goal", p[11], p[12], "tanks", p[14], "hp", p[18], "d", p[20])
        elif l.strip(): print(l)
