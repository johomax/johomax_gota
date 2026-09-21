# usage: uv run python tmp/replay_timeline.py XP.json OPPFRAG SIDE BUCKET [EPINDEX] — per bucket, per team: attack targets by class + mean walkTo target
import json, sys, pathlib, urllib.request, collections
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def cls(t):
    if t in (1, 2): return "fort"
    if 10 <= t <= 27: return "gate" if (t - 10) % 3 == 2 else "twr"
    if 28 <= t <= 31: return "guard"
    if 101 <= t <= 110: return "hero"
    if t >= 1000: return "creep"
    return "other"
path, oppf, side, bucket = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); epi = int(sys.argv[5]) if len(sys.argv) > 5 else 0
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
        print("episode", eid, "opp", r["opp"], "ours", "Red" if side == 0 else "Blue", "ticks", rep["ticks"])
        T = rep["ticks"]; nb = T // bucket + 1
        cnt = [[collections.Counter() for _ in range(nb)] for _ in range(2)]
        pos = [[[] for _ in range(nb)] for _ in range(2)]
        active = [[set() for _ in range(nb)] for _ in range(2)]
        for a in acts:
            team = 0 if a["heroId"] <= 104 else 1; b = a["tick"] // bucket
            active[team][b].add(a["heroId"])
            if a["kind"] == "attackTarget": cnt[team][b][cls(a["first"])] += 1
            elif a["kind"] == "castTarget": cnt[team][b]["cast"] += 1
            elif a["kind"] == "walkTo": pos[team][b].append((a["x"], a["y"]))
        for b in range(nb):
            line = f"{b*bucket:5d}"
            for team in range(2):
                cc = cnt[team][b]; p = pos[team][b]
                mp = f"({sum(x for x,_ in p)/len(p):3.0f},{sum(y for _,y in p)/len(p):3.0f})" if p else "(  -,  -)"
                line += f" | {'R' if team==0 else 'B'} n{len(active[team][b])} {mp} twr{cc['twr']:4d} gate{cc['gate']:4d} grd{cc['guard']:4d} fort{cc['fort']:4d} hero{cc['hero']:4d} crp{cc['creep']:4d}"
            print(line)
        break
