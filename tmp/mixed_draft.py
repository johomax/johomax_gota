# usage: uv run python tmp/mixed_draft.py xp/mx-vNNN.json — per hosted mixed game: seat, drafted class, deaths, level, score, steps (from our policy log)
import json, sys, statistics, collections
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]
ME = "Jordan-ply_bcb80069"; d = json.load(open(sys.argv[1])); rows = []
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in d["requests"]:
        det = dump(c.get_experience_request(r["id"]))
        for ep in det.get("episodes", []):
            if ep.get("status") != "completed": continue
            try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
            except Exception: continue
            me = [ps for ps in st["policy_stats"] if ME in ps["policy_name"]][0]
            try:
                log = c.get_episode_request_policy_log(ep["id"], me["policy_version_id"], me["position"])
                text = log if isinstance(log, str) else (dump(log).get("content") or dump(log).get("log") or str(log))
            except Exception as ex: text = ""
            cls = -1; deaths = -1; lvl = -1; floats = 0
            for l in text.split("\n"):
                if l.startswith("DRAFT ") and " ok 1" in l: cls = int(l.split()[1])
                if l.startswith("F "):
                    p = l.split(); 
                    try:
                        if "cls" in p: cls = int(p[p.index("cls") + 1])
                        lvl = int(p[p.index("at") - 1].lstrip("L")) if False else lvl
                        deaths = int(p[-1]); lvl = int([x for x in p if x.startswith("L")][-1][1:]) if any(x.startswith("L") and x[1:].isdigit() for x in p) else lvl
                    except Exception: pass
                if l.startswith("FLOAT"): floats += 1
            rows.append((r["seat"], cls, deaths, lvl, floats, me.get("avg_reward") or 0, st.get("steps") or 0))
for seat, cls, deaths, lvl, fl, sc, steps in sorted(rows): print(f"seat {seat} {CL[cls] if 0 <= cls < 10 else '?':8s} deaths {deaths:2d} L{lvl:2d} floats {fl} score {sc:6.0f} steps {steps:6d}")
by = collections.defaultdict(list)
for _, cls, _, _, _, sc, _ in rows: by[CL[cls] if 0 <= cls < 10 else "?"].append(sc)
print("by class:", {k: (len(v), round(statistics.mean(v))) for k, v in sorted(by.items(), key=lambda kv: -statistics.mean(kv[1]))})
