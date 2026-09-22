# usage: uv run python tmp/early_compare.py xp/mx-v338.json [...] — first 3000 ticks: per policy family, attacks on heroes/creeps/towers per hero, grouping (allies within 8 tiles at walk commands), buybacks (deaths) in the whole game
import json, sys, pathlib, collections, statistics
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
FAM = [("Jordan", "ours"), ("richard", "richard"), ("relh", "relh"), ("khors", "khors")]
def cls(t):
    if 10 <= t <= 31: return "twr"
    if 100 <= t <= 109: return "hero"
    if t >= 1000: return "crp"
    return "oth"
agg = collections.defaultdict(lambda: collections.defaultdict(list))
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for path in sys.argv[1:]:
        for r in json.load(open(path))["requests"]:
            det = dump(c.get_experience_request(r["id"]))
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed": continue
                fp = pathlib.Path("tmp/replays") / f"{ep['id']}.replay"
                if not fp.exists(): continue
                try: st = dump(c.get_episode_request_episode_stats(ep["id"])); rep = load_replay(str(fp))
                except Exception: continue
                fam_of = {}
                for ps in st["policy_stats"]:
                    f = next((f for k, f in FAM if k in ps["policy_name"]), "other"); fam_of[100 + ps["position"]] = (f, ps.get("avg_reward") or 0)
                acts = rep["actions"]
                # last known position per hero from walk commands (coarse)
                pos = {}; early = collections.defaultdict(collections.Counter); near = collections.defaultdict(list); bb = collections.Counter(); firstbb = {}
                for a in acts:
                    h = a["heroId"]
                    if a["kind"] in ("walkTo", "attackMove"):
                        pos[h] = (a["x"], a["y"])
                        if a["tick"] < 3000:
                            allies = sum(1 for o, p in pos.items() if o != h and (o < 105) == (h < 105) and (p[0]-a["x"])**2 + (p[1]-a["y"])**2 <= 64)
                            near[h].append(allies)
                    if a["kind"] == "attackTarget" and a["tick"] < 3000: early[h][cls(a["first"])] += 1
                    if a["kind"] == "buyback":
                        bb[h] += 1
                        if h not in firstbb: firstbb[h] = a["tick"]
                for h, (f, sc) in fam_of.items():
                    agg[f]["hero"].append(early[h]["hero"]); agg[f]["crp"].append(early[h]["crp"]); agg[f]["twr"].append(early[h]["twr"])
                    agg[f]["near"].append(statistics.mean(near[h]) if near[h] else 0); agg[f]["bb"].append(bb[h]); agg[f]["firstbb"].append(firstbb.get(h, 99999)); agg[f]["score"].append(sc)
for f in ("ours", "relh", "richard", "khors", "other"):
    d = agg[f]
    if not d["score"]: continue
    print(f"{f:8s} n{len(d['score']):3d} score {statistics.mean(d['score']):5.0f} | first 3000 ticks: hero-attacks {statistics.mean(d['hero']):5.0f} creep {statistics.mean(d['crp']):5.0f} tower {statistics.mean(d['twr']):4.0f} allies-near {statistics.mean(d['near']):.2f} | buybacks/game {statistics.mean(d['bb']):.1f} first buyback median {statistics.median(d['firstbb']):.0f}")
