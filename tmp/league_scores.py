# usage: uv run python tmp/league_scores.py [ROUNDS] — our league games: opponent, side, our team mean score vs theirs, steps
import sys, statistics
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
DIV="div_a4534073-c5d2-4193-a94a-93d9c5e2e443"; ME = "Jordan"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    ours_all = []; theirs_all = []
    for r in c.list_rounds(division_id=DIV, status="completed", limit=n).entries:
        rd = dump(r); eps = dump(c.list_round_episode_requests(r.id, limit=100))["entries"]; rows = []
        for e in eps:
            try: st = dump(c.get_episode_request_episode_stats(e["id"]))
            except Exception: continue
            seats = {ps["position"]: ps for ps in st.get("policy_stats", [])}
            if 0 not in seats or 5 not in seats: continue
            mine = 0 if ME in seats[0]["policy_name"] else (5 if ME in seats[5]["policy_name"] else None)
            if mine is None: continue
            opp = seats[5 - mine]; me = seats[mine]
            rows.append((mine, opp["policy_name"][:30] + ":v" + str(opp["policy_version"]), me["avg_reward"] or 0, opp["avg_reward"] or 0, st.get("steps") or 0, me["policy_version"]))
        for mine, opp, a, b, steps, ver in rows:
            ours_all.append(a); theirs_all.append(b)
            print(f"r{rd['round_number']} v{ver} {'Red ' if mine == 0 else 'Blue'} ours {a:6.0f} theirs {b:6.0f} steps {steps:6d} | {opp}")
    if ours_all: print(f"TOTAL n{len(ours_all)} ours {statistics.mean(ours_all):.0f} theirs {statistics.mean(theirs_all):.0f}")
