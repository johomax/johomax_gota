# usage: uv run python tmp/killers.py EPISODE_ID HERO_ID [WINDOW] — per WINDOW-tick bucket: enemy heroes' attackTarget commands aimed at HERO_ID (who hunts it), plus the hero's own top targets
import sys, pathlib, urllib.request, collections
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
eid, hid = sys.argv[1], int(sys.argv[2]); win = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
fp = pathlib.Path("tmp/replays") / f"{eid}.replay"
if not fp.exists():
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        url = dump(c.get_episode_request(eid)).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
rep = load_replay(str(fp)); T = rep["ticks"]; nb = T // win + 1
team = (hid - 100) // 5
hunt = [collections.Counter() for _ in range(nb)]
for a in rep["actions"]:
    if a["kind"] == "attackTarget" and a.get("targetId") == hid and (a["heroId"] - 100) // 5 != team:
        hunt[a["tick"] // win][a["heroId"]] += 1
names = {}
for p in rep.get("setup", {}).get("players", []) if isinstance(rep.get("setup"), dict) else []:
    pass
for b in range(nb):
    if hunt[b]: print(f"{b*win:6d}-{(b+1)*win:6d}: " + ", ".join(f"hero{h}x{n}" for h, n in hunt[b].most_common()))
