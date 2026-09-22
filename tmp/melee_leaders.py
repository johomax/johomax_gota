# usage: uv run python tmp/melee_leaders.py xp/duel-vNNN.json [MAX] — for relh/richard/aaron-micro heroes that drafted a melee class: score, buybacks, levels, and per-2400-tick top target @ mean walk point for the first 14400 ticks; plus our melee heroes in the same games for contrast
import json, sys, pathlib, collections
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]; MELEE = {0, 3, 4, 5, 9}
def cls(t):
    if t in (1, 2): return "fort"
    if 10 <= t <= 27: return "twr"
    if 28 <= t <= 31: return "grd"
    if 100 <= t <= 109: return "hero"
    if t >= 1000: return "crp"
    return "oth"
d = json.load(open(sys.argv[1])); mx = int(sys.argv[2]) if len(sys.argv) > 2 else 8; shown = 0
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in d["requests"]:
        det = dump(c.get_experience_request(r["id"]))
        for ep in det.get("episodes", []):
            if ep.get("status") != "completed": continue
            fp = pathlib.Path("tmp/replays") / f"{ep['id']}.replay"
            if not fp.exists(): continue
            rep = load_replay(str(fp)); st = dump(c.get_episode_request_episode_stats(ep["id"]))
            names = {ps["position"]: (ps["policy_name"], ps.get("avg_reward") or 0) for ps in st["policy_stats"]}
            draft = {a["heroId"]: a["first"] for a in rep["actions"] if a["kind"] == "draft"}
            for pos, (nm, sc) in names.items():
                fam = "relh" if "relh" in nm else "richard" if "richard" in nm else "aaron-micro" if "aaron-gota-micro0922" == nm else "ours" if "Jordan" in nm else None
                hid = 100 + pos; k = draft.get(hid, -1)
                if fam is None or k not in MELEE: continue
                acts = [a for a in rep["actions"] if a["heroId"] == hid]
                bb = sum(1 for a in acts if a["kind"] == "buyback"); lv = 1 + sum(1 for a in acts if a["kind"] == "levelAbility")
                per = collections.defaultdict(collections.Counter); pos_ = collections.defaultdict(list)
                for a in acts:
                    b = a["tick"] // 2400
                    if b > 5: continue
                    if a["kind"] == "attackTarget": per[b][cls(a["first"])] += 1
                    elif a["kind"] in ("walkTo", "attackMove"): pos_[b].append((a["x"], a["y"]))
                line = []
                for b in range(6):
                    top = per[b].most_common(1)[0] if per[b] else ("mv", len(pos_[b]))
                    p = pos_[b]; mp = f"{sum(x for x,_ in p)/len(p):.0f},{sum(y for _,y in p)/len(p):.0f}" if p else "-"
                    line.append(f"{top[0]}{top[1]}@{mp}")
                team = "A" if pos < 5 else "B"
                print(f"{fam:11s} {CL[k]:7s} team {team} score {sc:5.0f} L{lv:<2d} bb {bb} ticks {rep['ticks']:5d} | " + " | ".join(line))
            shown += 1
            if shown >= mx: raise SystemExit
