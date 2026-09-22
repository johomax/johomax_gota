# usage: uv run python tmp/zero_games.py xp/duel-vNNN.json VERSION [MAX] — our VERSION heroes that scored 0: class, ticks, level, buybacks, top enemy attackers (commands aimed at us), our attack mix per 4800 ticks
import json, sys, pathlib, collections
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"; CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]
def cls(t):
    if t in (1, 2): return "fort"
    if 10 <= t <= 27: return "twr"
    if 28 <= t <= 31: return "grd"
    if 100 <= t <= 109: return "hero"
    if t >= 1000: return "crp"
    return "oth"
path, ver = sys.argv[1], int(sys.argv[2]); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 20; shown = 0
d = json.load(open(path))
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in d["requests"]:
        det = dump(c.get_experience_request(r["id"]))
        for ep in det.get("episodes", []):
            if ep.get("status") != "completed": continue
            fp = pathlib.Path("tmp/replays") / f"{ep['id']}.replay"
            if not fp.exists(): continue
            st = dump(c.get_episode_request_episode_stats(ep["id"]))
            me = [ps for ps in st["policy_stats"] if ME in ps["policy_name"] and ps.get("policy_version") == ver]
            if not me or (me[0].get("avg_reward") or 0) > 0: continue
            rep = load_replay(str(fp)); pos = me[0]["position"]; hid = 100 + pos
            names = {ps["position"]: ps["policy_name"][:12] for ps in st["policy_stats"]}
            draft = {a["heroId"]: a["first"] for a in rep["actions"] if a["kind"] == "draft"}
            acts = [a for a in rep["actions"] if a["heroId"] == hid]
            lv = 1 + sum(1 for a in acts if a["kind"] == "levelAbility"); bb = sum(1 for a in acts if a["kind"] == "buyback")
            hunt = collections.Counter(a["heroId"] for a in rep["actions"] if a["kind"] == "attackTarget" and a.get("targetId") == hid and (a["heroId"] - 100) // 5 != pos // 5)
            per = collections.defaultdict(collections.Counter)
            for a in acts:
                if a["kind"] == "attackTarget": per[a["tick"] // 4800][cls(a["first"])] += 1
            mix = " ".join(f"{b*4800//1000}k:" + "/".join(f"{k}{v}" for k, v in per[b].most_common(2)) for b in sorted(per))
            top = ", ".join(f"{names.get(h-100,'?')}({CL[draft.get(h,-1)] if draft.get(h,-1)>=0 else '?'})x{n}" for h, n in hunt.most_common(3))
            print(f"{CL[draft.get(hid,-1)]:7s} seat {pos} ticks {rep['ticks']:5d} L{lv:<2d} bb {bb} | hunted by {top} | ours: {mix}")
            shown += 1
            if shown >= mx: raise SystemExit
