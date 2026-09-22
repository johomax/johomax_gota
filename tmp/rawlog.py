# usage: uv run python tmp/rawlog.py XP.json OPPFRAG SIDE [EVERY] — raw hosted policy log of our seat-0/5 hero: header, sampled F lines, notable lines
import json, sys
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
path, frag, side = sys.argv[1], sys.argv[2], int(sys.argv[3]); every = int(sys.argv[4]) if len(sys.argv) > 4 else 8
d = json.load(open(path)); cand = d["candidate"]
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    r = [r for r in d["requests"] if frag in r["opp"] and r["side"] == side][0]
    det = dump(c.get_experience_request(r["id"]))
    ep = [e for e in det["episodes"] if e.get("status") == "completed"][0]
    pv = [p for p in dump(c.get_episode_request_episode_stats(ep["id"]))["policy_stats"] if p["position"] == r["seat"]][0]["policy_version_id"]
    log = c.get_episode_request_policy_log(ep["id"], pv, r["seat"])
    text = log if isinstance(log, str) else (dump(log).get("content") or dump(log).get("log") or str(log))
    lines = text.split("\n"); print("lines", len(lines)); print("\n".join(lines[:4]))
    f = [l for l in lines if l.startswith("F ")]; print("F lines", len(f))
    for l in f[::every][:16]: print(" ", l[:120])
    for l in lines:
        if any(k in l for k in ("BUYBACK", "DRAFT", "error", "Error", "completed", "disabled")): print("!", l[:140])
