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
    a = ap.parse_args()
    pool = [l.strip() for l in open(ROOT / a.pool) if l.strip() and not l.startswith("#")]
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for rep in range(a.reps):
            rnd = random.Random(hash((a.tag, rep)) & 0xffff); others = pool[:]; rnd.shuffle(others)
            others = others[:9]; k = 0; roster = []
            for s in range(10):
                if s == a.seat: roster.append({"player": {"policy_ref": a.ref}, "slot": s})
                else: roster.append({"player": {"policy_ref": others[k]}, "slot": s}); k += 1
            body = {"target": {"league_id": LEAGUE}, "roster": roster, "num_episodes": a.n, "notes": f"[{a.tag}] {a.ref} seat {a.seat} league-like roster"}
            try:
                d = dump(c.create_experience_request(body))
            except Exception as ex:
                print("create failed:", repr(ex)[:400]); sys.exit(1)
            print("created", d["id"], "seat", a.seat, "others", [o.split(":")[0][:14] for o in others])
            path = ROOT / "xp" / f"{a.tag}.json"
            cur = json.load(open(path)) if path.exists() else {"candidate": a.ref, "n": a.n, "requests": []}
            cur["requests"].append({"id": d["id"], "seat": a.seat, "roster": others}); json.dump(cur, open(path, "w"), indent=1)
            time.sleep(1)
    print("saved", path)

if __name__ == "__main__":
    main()
