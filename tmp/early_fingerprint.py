# usage: uv run python tmp/early_fingerprint.py XP.json SIDE BUCKET HI — for every opponent in the file (our side SIDE), the ENEMY heroes' top action @ mean walk target per bucket up to HI
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
    if 100 <= t <= 109: return "hero"
    if t >= 1000: return "crp"
    return "oth"
path, side, bucket, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
d = json.load(open(path)); nb = hi // bucket
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in d["requests"]:
        if r["side"] != side: continue
        det = dump(c.get_experience_request(r["id"]))
        eps = [ep for ep in det.get("episodes", []) if ep.get("status") == "completed"]
        if not eps: continue
        eid = eps[0]["id"]; fp = pathlib.Path("tmp/replays") / f"{eid}.replay"
        if not fp.exists():
            url = dump(c.get_episode_request(eid)).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
        rep = load_replay(str(fp)); acts = rep["actions"]
        per = collections.defaultdict(lambda: [collections.Counter() for _ in range(nb)]); pos = collections.defaultdict(lambda: [[] for _ in range(nb)])
        for a in acts:
            if a["tick"] >= hi: continue
            h = a["heroId"]; enemy = (h >= 105) if side == 0 else (h <= 104)
            if not enemy: continue
            b = a["tick"] // bucket
            if a["kind"] == "attackTarget": per[h][b][cls(a["first"])] += 1
            elif a["kind"] == "walkTo": pos[h][b].append((a["x"], a["y"]))
        print(f"== {r['opp'][:44]} (enemy is {'Blue' if side == 0 else 'Red'}) ticks {rep['ticks']}")
        for h in sorted(set(per) | set(pos)):
            cells = []
            for b in range(nb):
                cc = per[h][b]; p = pos[h][b]
                top = cc.most_common(1)[0] if cc else ("wlk", len(p))
                mp = f"{sum(x for x,_ in p)/len(p):.0f},{sum(y for _,y in p)/len(p):.0f}" if p else "-"
                cells.append(f"{top[0]}{top[1]}@{mp}".rjust(15))
            print(f"  h{h-100} " + "".join(cells))
