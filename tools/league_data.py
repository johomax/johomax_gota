#!/usr/bin/env python3
"""Pull our league episodes (distinct-teammates regime) and summarize per seat/class.

usage: uv run python tools/league_data.py [--rounds 20] [--out docs/league_episodes.json]
Prints, for every episode we sat in: round, seat, class, teammates, opponents, outcome, ticks.
"""
import argparse, json, sys, pathlib
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIV = "div_a4534073-c5d2-4193-a94a-93d9c5e2e443"
ME = "ply_bcb80069-fb0c-4ba5-a45c-06b647870aeb"
CLASSES = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=20)
    ap.add_argument("--out", default="docs/league_episodes.json")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args()
    names = {}
    try:
        for r in json.load(open(ROOT / "docs/standings.json")):
            names[r["player_id"]] = r["player_name"]
    except Exception:
        pass
    out = []
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        try:
            lb = dump(c.get_division_leaderboard(DIV))
            for r in lb:
                r = dump(r)
                if r.get("player_id"):
                    names[r["player_id"]] = r.get("player_name")
        except Exception as ex:
            print("leaderboard:", repr(ex)[:200], file=sys.stderr)
        rounds = c.list_rounds(division_id=DIV, status="completed", limit=a.rounds).entries
        for r in rounds:
            rd = dump(r)
            attr = {str(x["policy_version_id"]): str(x["subject_id"]) for x in rd["round_config"]["entrant_attributions"]}
            eps = dump(c.list_round_episode_requests(r.id, limit=100))["entries"]
            for e in eps:
                pvs = [str(p) for p in e["policy_version_ids"]]
                players = [attr.get(p, "?") for p in pvs]
                if ME not in players:
                    continue
                seat = players.index(ME)
                rec = {"round": rd["round_number"], "round_at": str(rd["created_at"]), "ereq": e["id"], "status": e["status"],
                       "seat": seat, "team": 0 if seat < 5 else 1, "cls": CLASSES[seat if seat >= 5 else seat + 5] if False else CLASSES[(seat % 5) + (5 if seat < 5 else 0)],
                       "my_pv": pvs[seat], "players": [names.get(p, p[:12]) for p in players], "replay_url": e.get("replay_url")}
                try:
                    st = dump(c.get_episode_request_episode_stats(e["id"]))
                except Exception as ex:
                    if a.debug: print("stats ERR", repr(ex)[:200], file=sys.stderr)
                    st = None
                if st:
                    seats = {}
                    for ps in st.get("policy_stats", []):
                        seats[ps["position"]] = (ps.get("policy_name"), ps.get("policy_version"), ps.get("avg_reward"))
                    rec["seat_policies"] = [f"{seats[i][0]}:v{seats[i][1]}" if i in seats else "?" for i in range(10)]
                    rec["rewards"] = [seats[i][2] if i in seats else None for i in range(10)]
                    rec["my_version"] = seats.get(seat, (None, None, None))[1]
                    red = sum(1 for i in range(5) if seats.get(i, (0, 0, 0))[2]); blue = sum(1 for i in range(5, 10) if seats.get(i, (0, 0, 0))[2])
                    rec["outcome"] = "RedTeam" if red else ("BlueTeam" if blue else "Timeout")
                    rec["win"] = int(bool(seats.get(seat, (0, 0, 0))[2]))
                out.append(rec)
    json.dump(out, open(ROOT / a.out, "w"), indent=1, default=str)
    # summary
    by = {}
    for r in out:
        if "win" not in r: continue
        k = (r["seat"], r["cls"]); w, g = by.get(k, (0, 0)); by[k] = (w + r["win"], g + 1)
    tw = sum(w for w, g in by.values()); tg = sum(g for w, g in by.values())
    for k in sorted(by): print(f"seat {k[0]} {k[1]:8s} {by[k][0]}/{by[k][1]}")
    short = lambda n: n.split("-ply_")[0][:14]
    for r in out:
        if "win" not in r: continue
        sp = r.get("seat_policies", ["?"] * 10)
        print(f"r{r['round']} s{r['seat']} {r['cls']:7s} v{r.get('my_version')} {'W' if r['win'] else 'L'} {r['outcome']:8s} | " + " ".join(short(x) for x in sp[:5]) + " || " + " ".join(short(x) for x in sp[5:]))
    print(f"TOTAL {tw}/{tg} = {tw/tg if tg else 0:.2f}  (episodes with result {tg} of {len(out)}); saved {a.out}")

if __name__ == "__main__":
    main()
