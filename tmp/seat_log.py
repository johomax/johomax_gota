# usage: uv run python tmp/seat_log.py XP.json SEAT CLASSNAME [EVERY] — full hosted policy log of our hero in that seat with that drafted class: F lines every EVERY-th, all non-F lines
import json, sys
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]
ME = "Jordan-ply_bcb80069"; d = json.load(open(sys.argv[1])); seat = int(sys.argv[2]); want = sys.argv[3]; every = int(sys.argv[4]) if len(sys.argv) > 4 else 4; zero = len(sys.argv) > 5 and sys.argv[5] == "zero"
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in d["requests"]:
        if r["seat"] != seat: continue
        det = dump(c.get_experience_request(r["id"]))
        for ep in det.get("episodes", []):
            if ep.get("status") != "completed": continue
            st = dump(c.get_episode_request_episode_stats(ep["id"]))
            me = [ps for ps in st["policy_stats"] if ME in ps["policy_name"]][0]
            log = c.get_episode_request_policy_log(ep["id"], me["policy_version_id"], me["position"])
            text = log if isinstance(log, str) else (dump(log).get("content") or dump(log).get("log") or str(log))
            cls = -1
            for l in text.split("\n"):
                if l.startswith("DRAFT ") and " ok 1" in l: cls = int(l.split()[1])
            if not (0 <= cls < 10) or (want != "any" and CL[cls] != want): continue
            if zero and ((me.get("avg_reward") or 0) > 0 or (st.get("steps") or 0) < 15000): continue
            print(f"### episode {ep['id']} seat {seat} {want} score {me.get('avg_reward')} steps {st.get('steps')}")
            print("roster:", [ (ps["position"], ps["policy_name"][:28]) for ps in st["policy_stats"]])
            i = 0
            for l in text.split("\n"):
                if l.startswith("F "):
                    i += 1
                    if i % every == 0: print(l)
                elif l.strip(): print(l)
            break
