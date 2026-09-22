# usage: uv run python tmp/league_scores.py [ROUNDS] — our league games in any seat: seat, score, steps, teammates' and enemies' means
import sys, statistics, collections
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
DIV="div_a4534073-c5d2-4193-a94a-93d9c5e2e443"; ME = "Jordan-ply_bcb80069"
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
rows = []
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for r in c.list_rounds(division_id=DIV, status="completed", limit=n).entries:
        rd = dump(r); eps = dump(c.list_round_episode_requests(r.id, limit=100))["entries"]
        for e in eps:
            try: st = dump(c.get_episode_request_episode_stats(e["id"]))
            except Exception: continue
            mine = [ps for ps in st.get("policy_stats", []) if ME in ps["policy_name"]]
            if not mine: continue
            me = mine[0]; steps = st.get("steps") or 0; sc = me.get("avg_reward") or 0
            mates = [ps.get("avg_reward") or 0 for ps in st["policy_stats"] if ps is not me and (ps["position"] < 5) == (me["position"] < 5)]
            foes = [ps.get("avg_reward") or 0 for ps in st["policy_stats"] if (ps["position"] < 5) != (me["position"] < 5)]
            rows.append((rd["round_number"], me["position"], me["policy_version"], sc, steps, statistics.mean(mates) if mates else 0, statistics.mean(foes) if foes else 0))
for rn, seat, ver, sc, steps, m, f in rows: print(f"r{rn} v{ver} seat {seat} ours {sc:6.0f} steps {steps:6d} mates {m:5.0f} foes {f:5.0f}")
by = collections.defaultdict(list)
for _, seat, _, sc, *_ in rows: by["farmer" if seat % 5 <= 2 else "guard"].append(sc)
for k, v in by.items(): print(f"{k}: n{len(v)} mean {statistics.mean(v):.0f} zeros {sum(1 for x in v if x == 0)}")
if rows: print(f"ALL n{len(rows)} mean {statistics.mean(r[3] for r in rows):.0f}")
