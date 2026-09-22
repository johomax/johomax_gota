# usage: uv run python tmp/duel_class.py xp/duel-vNNN.json CAND CTRL — unpaired per-class means of our CAND vs CTRL heroes in the duel games (class from the replay draft action); melee = VK/Druid/DH/DK/Berserker
import json, sys, pathlib, urllib.request, statistics, collections
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"; CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]; MELEE = {0, 3, 4, 5, 9}
cand, ctrl = int(sys.argv[2]), int(sys.argv[3]); by = {cand: collections.defaultdict(list), ctrl: collections.defaultdict(list)}
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1].split(","):
        d = json.load(open(path))
        for r in d["requests"]:
            det = dump(c.get_experience_request(r["id"]))
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed": continue
                eid = ep["id"]; fp = pathlib.Path("tmp/replays") / f"{eid}.replay"
                try:
                    if not fp.exists():
                        url = dump(c.get_episode_request(eid)).get("replay_url"); fp.write_bytes(urllib.request.urlopen(url).read())
                    rep = load_replay(str(fp)); st = dump(c.get_episode_request_episode_stats(eid))
                except Exception as ex: print("skip", eid, ex); continue
                cls = {a["heroId"]: a["first"] for a in rep["actions"] if a["kind"] == "draft"}
                for ps in st["policy_stats"]:
                    if ME in ps["policy_name"] and ps.get("policy_version") in by:
                        k = cls.get(100 + ps["position"], -1)
                        by[ps["policy_version"]][k].append(ps.get("avg_reward") or 0)
def row(v, keys):
    xs = [x for k in keys for x in by[v].get(k, [])]
    return f"{statistics.mean(xs):5.0f} n{len(xs):3d} z{sum(1 for x in xs if x==0)/max(1,len(xs)):4.0%}" if xs else "    -        "
print(f"{'class':8s} v{cand:<3d}               v{ctrl:<3d}")
for k in range(10):
    if by[cand].get(k) or by[ctrl].get(k): print(f"{CL[k]:8s} {row(cand,[k])}   {row(ctrl,[k])}")
print(f"{'MELEE':8s} {row(cand, MELEE)}   {row(ctrl, MELEE)}")
print(f"{'RANGED':8s} {row(cand, set(range(10)) - MELEE)}   {row(ctrl, set(range(10)) - MELEE)}")
print(f"{'ALL':8s} {row(cand, range(10))}   {row(ctrl, range(10))}")
