# usage: uv run python tmp/replay_heroes.py XP.json OPPFRAG SIDE BUCKET [EPINDEX] — per hero per bucket: top attack class:count @ mean walkTo target
import json, sys, pathlib, urllib.request, collections
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def cls(t):
    if t in (1, 2): return "fort"
    if 10 <= t <= 27: return "gate" if (t - 10) % 3 == 2 else "twr"
    if 28 <= t <= 31: return "grd"
    if 101 <= t <= 110: return "hero"
    if t >= 1000: return "crp"
    return "oth"
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
        rep = load_replay(str(fp)); acts = rep["actions"]; T = rep["ticks"]; nb = T // bucket + 1
        print("episode", eid, "opp", r["opp"], "ours", "Red" if side == 0 else "Blue", "ticks", T, "| cells: topclass count @ mean walk target; '.' = no actions")
        per = collections.defaultdict(lambda: [collections.Counter() for _ in range(nb)]); pos = collections.defaultdict(lambda: [[] for _ in range(nb)])
        for a in acts:
            h = a["heroId"]; b = a["tick"] // bucket
            if a["kind"] == "attackTarget": per[h][b][cls(a["first"])] += 1
            elif a["kind"] == "walkTo": pos[h][b].append((a["x"], a["y"]))
            else: per[h][b][a["kind"][:3]] += 0
        print("hero      " + "".join(f"{b*bucket:>14d}" for b in range(nb)))
        for h in sorted(per):
            idx = h - 100; who = "ours" if (idx < 5) == (side == 0) else "THEM"
            cells = []
            for b in range(nb):
                cc = per[h][b]; p = pos[h][b]
                if not cc and not p: cells.append(f"{'.':>14}"); continue
                top = cc.most_common(1)[0] if cc else ("wlk", len(p))
                mp = f"{sum(x for x,_ in p)/len(p):.0f},{sum(y for _,y in p)/len(p):.0f}" if p else "-"
                cells.append(f"{top[0]}{top[1]}@{mp}".rjust(14))
            print(f"h{idx} {who:4s} " + "".join(cells))
        break
