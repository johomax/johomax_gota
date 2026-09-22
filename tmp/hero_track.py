# usage: uv run python tmp/hero_track.py EPISODE_ID SLOT BUCKET — one hero's per-bucket top attack class @ mean walk target, plus item buys and buybacks
import sys, pathlib, urllib.request, collections
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
eid, slot, bucket = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); hid = 100 + slot
fp = pathlib.Path("tmp/replays") / f"{eid}.replay"
if not fp.exists():
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        url = dump(c.get_episode_request(eid)).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
rep = load_replay(str(fp)); acts = [a for a in rep["actions"] if a["heroId"] == hid]; T = rep["ticks"]; nb = T // bucket + 1
per = [collections.Counter() for _ in range(nb)]; pos = [[] for _ in range(nb)]; kinds = collections.Counter(a["kind"] for a in acts)
for a in acts:
    b = a["tick"] // bucket
    if a["kind"] == "attackTarget": per[b][cls(a["first"])] += 1
    elif a["kind"] == "walkTo" or a["kind"] == "attackMove": pos[b].append((a["x"], a["y"]))
print("episode", eid, "hero", hid, "ticks", T, "actions", len(acts), dict(kinds))
print("draft", [a["first"] for a in acts if a["kind"] == "draft"], "buys", [(a["tick"], a.get("itemId", a["first"])) for a in acts if a["kind"] == "buyItem"][:12], "buybacks", [a["tick"] for a in acts if a["kind"] == "buyback"][:8])
line = []
for b in range(nb):
    cc = per[b]; p = pos[b]; top = cc.most_common(1)[0] if cc else ("mv", len(p))
    mp = f"{sum(x for x,_ in p)/len(p):.0f},{sum(y for _,y in p)/len(p):.0f}" if p else "-"
    line.append(f"{b*bucket}:{top[0]}{top[1]}@{mp}")
print(" | ".join(line))
