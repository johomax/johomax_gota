# usage: uv run python tmp/replay_runs.py XP.json OPPFRAG SIDE LO HI [EPINDEX] — per-hero action runs (heroId 101-110) for one completed episode
import json, sys, pathlib, urllib.request
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
path, oppf, side = sys.argv[1], sys.argv[2], int(sys.argv[3]); lo, hi = int(sys.argv[4]), int(sys.argv[5]); epi = int(sys.argv[6]) if len(sys.argv) > 6 else 0
d = json.load(open(path))
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in d["requests"]:
        if oppf not in r["opp"] or r["side"] != side: continue
        det = dump(c.get_experience_request(r["id"]))
        eps = [ep for ep in det.get("episodes", []) if ep.get("status") == "completed"]
        eid = eps[epi]["id"]; fp = pathlib.Path("tmp/replays") / f"{eid}.replay"
        if not fp.exists():
            url = dump(c.get_episode_request(eid)).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
        rep = load_replay(str(fp)); acts = rep["actions"]
        print("episode", eid, "opp", r["opp"], "ours", "Red" if side == 0 else "Blue", "ticks", rep["ticks"], "actions", len(acts))
        for h in range(100, 110):
            idx = h - 100
            buys = [(a["tick"], a.get("first")) for a in acts if a["heroId"] == h and a["kind"] == "buyItem"]
            uses = [(a["tick"], a.get("first")) for a in acts if a["heroId"] == h and a["kind"] == "useItem"]
            runs = []
            for a in acts:
                if a["heroId"] != h or not (lo <= a["tick"] <= hi): continue
                key = (a["kind"], a.get("first") if a["kind"] != "walkTo" else "walk")
                if runs and runs[-1][1] == key: runs[-1][2] = a["tick"]; runs[-1][3] += 1
                else: runs.append([a["tick"], key, a["tick"], 1])
            who = "ours" if (idx < 5) == (side == 0) else "THEM"
            print(f"hero {idx} {who} buys {buys[:8]} uses {len(uses)} first {uses[:3]}")
            print("   " + " | ".join(f"{t0}-{t1} {k[0][:3]}:{k[1]} x{n}" for t0, k, t1, n in runs if n >= 3 or k[0] != 'walkTo')[:1100])
        break
