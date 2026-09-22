# usage: uv run python tmp/lvl_at.py xp/duel-vNNN.json CAND CTRL — paired level of our CAND vs CTRL hero at ticks 4800/9600/14400/19200 (from levelAbility replay actions), mean diff and SE; a lower-noise progress metric than the floored score
import json, sys, pathlib, urllib.request, statistics, math
sys.path.insert(0, "tools")
from replay_parse import load_replay
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
ME = "Jordan-ply_bcb80069"; TICKS = [4800, 9600, 14400, 19200]
path, cand, ctrl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = json.load(open(path)); rows = []
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
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
            pos = {ps.get("policy_version"): (ps["position"], ps.get("avg_reward") or 0) for ps in st["policy_stats"] if ME in ps["policy_name"]}
            if cand not in pos or ctrl not in pos: continue
            ups = {}
            for a in rep["actions"]:
                if a["kind"] == "levelAbility": ups.setdefault(a["heroId"], []).append(a["tick"])
            def lvl_at(hid, t): return 1 + sum(1 for x in ups.get(hid, []) if x <= t)
            T = rep["ticks"]
            rows.append({"T": T, "cand": [lvl_at(100 + pos[cand][0], t) for t in TICKS], "ctrl": [lvl_at(100 + pos[ctrl][0], t) for t in TICKS], "sc": (pos[cand][1], pos[ctrl][1])})
print(f"{path}: v{cand} vs v{ctrl} games {len(rows)}")
for i, t in enumerate(TICKS):
    use = [r for r in rows if r["T"] >= t]
    if len(use) < 5: continue
    diffs = [r["cand"][i] - r["ctrl"][i] for r in use]
    print(f"  level@{t:5d}: cand {statistics.mean(r['cand'][i] for r in use):5.2f} ctrl {statistics.mean(r['ctrl'][i] for r in use):5.2f} diff {statistics.mean(diffs):+5.2f} se {statistics.pstdev(diffs)/math.sqrt(len(diffs)):4.2f} (n{len(use)})")
