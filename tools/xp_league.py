#!/usr/bin/env python3
"""Hosted tests with an explicit league-like roster (no `random champion` seats).

usage: uv run python tools/xp_league.py create <policy_ref> --seat S -n N --tag t [--pool tmp/league_pool.txt]
The candidate sits at seat S; the other nine seats are filled from the pool file (one policy_ref per line, first nine
after shuffling with the request index as seed). Report with tools/xp_mixed.py report xp/t.json.
"""
import argparse, json, pathlib, random, sys, time
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAGUE = "league_3c60897b-25cf-4b37-9d1a-8554c1198f28"

def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    cr = sub.add_parser("create"); cr.add_argument("ref"); cr.add_argument("--seat", type=int, default=0); cr.add_argument("-n", type=int, default=12)
    cr.add_argument("--tag", required=True); cr.add_argument("--pool", default="tmp/league_pool.txt"); cr.add_argument("--reps", type=int, default=1, help="requests with different shuffles")
    du = sub.add_parser("duel", help="cand at seat S and ctrl at S+5, then swapped; eight pool seats"); du.add_argument("cand"); du.add_argument("ctrl")
    du.add_argument("--seat", type=int, default=0); du.add_argument("-n", type=int, default=24); du.add_argument("--tag", required=True); du.add_argument("--pool", default="tmp/league_pool.txt"); du.add_argument("--reps", type=int, default=1)
    a = ap.parse_args()
    pool = [l.strip() for l in open(ROOT / a.pool) if l.strip() and not l.startswith("#")]
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        orders = [None] if a.cmd == "create" else [0, 1]
        for rep in range(a.reps):
            for order in orders:
                rnd = random.Random((sum(map(ord, a.tag)) * 31 + rep) & 0xffff); others = pool[:]; rnd.shuffle(others)
                fixed = {a.seat: a.ref} if a.cmd == "create" else ({a.seat: a.cand, a.seat + 5: a.ctrl} if order == 0 else {a.seat: a.ctrl, a.seat + 5: a.cand})
                cand_seat = a.seat if a.cmd == "create" or order == 0 else a.seat + 5
                k = 0; roster = []
                for s in range(10):
                    if s in fixed: roster.append({"player": {"policy_ref": fixed[s]}, "slot": s})
                    else: roster.append({"player": {"policy_ref": others[k]}, "slot": s}); k += 1
                cand = a.ref if a.cmd == "create" else a.cand
                body = {"target": {"league_id": LEAGUE}, "roster": roster, "num_episodes": a.n, "notes": f"[{a.tag}] {cand} cand seat {cand_seat} league-like roster"}
                d = None
                for attempt in range(40):
                    try:
                        d = dump(c.create_experience_request(body)); break
                    except Exception as ex:
                        msg = repr(ex)
                        if "429" in msg: time.sleep(30)
                        else: print("create failed:", msg[:300]); time.sleep(5)
                if d is None: sys.exit(1)
                print("created", d["id"], "cand seat", cand_seat, "others", [o.split(":")[0][:14] for o in others[:k]])
                path = ROOT / "xp" / f"{a.tag}.json"
                cur = json.load(open(path)) if path.exists() else {"candidate": cand, "n": a.n, "requests": []}
                cur["requests"].append({"id": d["id"], "seat": cand_seat, "roster": others[:k]}); json.dump(cur, open(path, "w"), indent=1)
                time.sleep(1)
    print("saved", path)

if __name__ == "__main__":
    main()
