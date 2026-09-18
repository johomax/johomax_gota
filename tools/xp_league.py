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

# League seating as observed 2026-09-17: we sit at slot 0 of our team in ~90% of games (DK on Red, VK on Blue); slots follow
# rating order, so our teammates are the lower-rated entrants and the enemy team is the top of the ladder.
# Aaron's league label switched from win-bounded to perimeter-blue_repair in rounds 397-399 (2026-09-17 ~19:30 UTC); lgr-* used win-bounded, lgr2-* uses this pool
# black-kite v13 -> v16 (league since round 407, 2026-09-18 ~00:00 UTC); lgr2-* used v13, lgr3-* uses v16
TOP = ["aaron-gota-ir-coordinated-support-anchor-0916:v1", "aaron-gota-ir-perimeter-blue_repair-0916-aaron:v1", "relh-gods-of-the-arena:v154", "black-kite:v16", "red-kite:v34", "gota-g002:v1", "richard-gods-of-the-arena:v78"]  # rating order, 2026-09-18 07:40 UTC field
LOW = ["gota-g003:v2", "gota-vanguard-rally-hold:v1", "khors:v1", "nancy-goa:v1", "Polyworld GOTA base.bas:v1"]  # vanguard/nancy stand in for the hidden daveey policies

def realistic_roster(ref, rep, force_enemy=None, mate_top=None):
    """rep-th realistic roster: rosters depend only on rep, so two candidates run with the same --reps play identical rosters."""
    rnd = random.Random(1000 + rep)
    top = [p for p in TOP if p != mate_top]; low = [p for p in LOW if p != force_enemy]
    if force_enemy:
        pick_e = set(rnd.sample(top, 4)); enemy = [p for p in top if p in pick_e] + [force_enemy]   # forced enemy sits last (lowest rated)
        pick_m = set(rnd.sample(low, 4))
    else:
        pick_e = set(rnd.sample(top, 5)); enemy = [p for p in top if p in pick_e]   # rating order kept
        pick_m = set(rnd.sample(low, 4))
    mates = [p for p in low if p in pick_m]
    side = rep % 2  # 0 = we are Red (seats 0-4), 1 = we are Blue (seats 5-9)
    ours = [ref] + mates
    if mate_top:
        mates = mates[:3]; ours = [mate_top, ref] + mates
    red, blue = (ours, enemy) if side == 0 else (enemy, ours)
    return [{"player": {"policy_ref": (red + blue)[s]}, "slot": s} for s in range(10)], side * 5 + (1 if mate_top else 0), red + blue

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    cr = sub.add_parser("create"); cr.add_argument("ref"); cr.add_argument("--seat", type=int, default=0); cr.add_argument("-n", type=int, default=12)
    cr.add_argument("--tag", required=True); cr.add_argument("--pool", default="tmp/league_pool.txt"); cr.add_argument("--reps", type=int, default=1, help="requests with different shuffles")
    cr.add_argument("--realistic", action="store_true", help="rating-ordered league seating (TOP vs us+LOW), alternating sides per rep; same rosters for every candidate")
    cr.add_argument("--rep0", type=int, default=0, help="first rep index (realistic mode)")
    cr.add_argument("--aaron", choices=["perimeter", "winbounded"], default="perimeter", help="which aaron pair sits in TOP (winbounded = the lgr-* pool)")
    cr.add_argument("--force-enemy", default=None, help="policy_ref that must sit on the enemy team (removed from LOW if there; e.g. relh-gods-of-the-arena:v133)")
    cr.add_argument("--mate-top", default=None, help="policy_ref that leads OUR team at slot 0 (we sit at slot 1 as Xbow/Ranger); removed from TOP")
    ho = sub.add_parser("homo", help="competition format: five copies of REF vs five copies of each --opp, both sides"); ho.add_argument("ref")
    ho.add_argument("--opp", action="append", required=True, help="opponent policy_ref (repeatable)"); ho.add_argument("-n", type=int, default=12); ho.add_argument("--tag", required=True)
    du = sub.add_parser("duel", help="cand at seat S and ctrl at S+5, then swapped; eight pool seats"); du.add_argument("cand"); du.add_argument("ctrl")
    du.add_argument("--seat", type=int, default=0); du.add_argument("-n", type=int, default=24); du.add_argument("--tag", required=True); du.add_argument("--pool", default="tmp/league_pool.txt"); du.add_argument("--reps", type=int, default=1)
    a = ap.parse_args()
    if a.cmd == "homo":
        with CoworldApiClient.from_login(server_url=get_api_server()) as c:
            path = ROOT / "xp" / f"{a.tag}.json"
            cur = json.load(open(path)) if path.exists() else {"candidate": a.ref, "n": a.n, "requests": []}
            for opp in a.opp:
                for side in (0, 1):
                    red, blue = (a.ref, opp) if side == 0 else (opp, a.ref)
                    roster = [{"player": {"policy_ref": red if s < 5 else blue}, "slot": s} for s in range(10)]
                    body = {"target": {"league_id": LEAGUE}, "roster": roster, "num_episodes": a.n, "notes": f"[{a.tag}] 5x{a.ref} vs 5x{opp} ours {'Red' if side == 0 else 'Blue'}"}
                    d = None
                    for attempt in range(60):
                        try:
                            d = dump(c.create_experience_request(body)); break
                        except Exception as ex:
                            msg = repr(ex)
                            if "429" in msg: time.sleep(30)
                            else: print("create failed:", msg[:300]); time.sleep(5)
                    if d is None: sys.exit(1)
                    print("created", d["id"], "opp", opp.split(":")[0][:20], "ours", "Red" if side == 0 else "Blue")
                    cur["requests"].append({"id": d["id"], "seat": side * 5, "opp": opp, "side": side}); json.dump(cur, open(path, "w"), indent=1)
                    time.sleep(1)
        print("saved", path); return
    pool = [l.strip() for l in open(ROOT / a.pool) if l.strip() and not l.startswith("#")]
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        orders = [None] if a.cmd == "create" else [0, 1]
        if a.cmd == "create" and a.realistic:
            if a.aaron == "winbounded":
                TOP[0] = "aaron-gota-ir-win-bounded-0916:v1"; TOP[1] = "aaron-gota-ir-win-bounded-0916-aaron:v1"
            for rep in range(a.rep0, a.rep0 + a.reps):
                roster, cand_seat, labels = realistic_roster(a.ref, rep, a.force_enemy, a.mate_top)
                body = {"target": {"league_id": LEAGUE}, "roster": roster, "num_episodes": a.n, "notes": f"[{a.tag}] {a.ref} realistic rep {rep} seat {cand_seat}"}
                d = None
                for attempt in range(60):
                    try:
                        d = dump(c.create_experience_request(body)); break
                    except Exception as ex:
                        msg = repr(ex)
                        if "429" in msg: time.sleep(30)
                        else: print("create failed:", msg[:300]); time.sleep(5)
                if d is None: sys.exit(1)
                print("created", d["id"], "rep", rep, "seat", cand_seat, [l.split(":")[0][:10] for l in labels])
                path = ROOT / "xp" / f"{a.tag}.json"
                cur = json.load(open(path)) if path.exists() else {"candidate": a.ref, "n": a.n, "requests": []}
                cur["requests"].append({"id": d["id"], "seat": cand_seat, "rep": rep, "roster": [l for i, l in enumerate(labels) if i != cand_seat]}); json.dump(cur, open(path, "w"), indent=1)
                time.sleep(1)
            print("saved", path); return
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
