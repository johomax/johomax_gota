#!/usr/bin/env python3
"""Hosted random-roster tests that model the league's distinct-teammates seating.

create: uv run python tools/xp_mixed.py create <policy_ref> [--seats 0-9] [-n 12] --tag t
        one experience request per seat: the policy in that seat, nine `random champion` seats.
report: uv run python tools/xp_mixed.py report xp/t.json [xp/u.json ...]   -> wins by seat/side/total
"""
import argparse, json, pathlib, sys, time
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAGUE = "league_3c60897b-25cf-4b37-9d1a-8554c1198f28"
CLASSES = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

def parse_seats(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out

def create(c, ref, seats, n, tag):
    for seat in seats:
        roster = [{"player": ({"policy_ref": ref} if s == seat else {"random": True}), "slot": s} for s in range(10)]
        body = {"target": {"league_id": LEAGUE}, "roster": roster, "num_episodes": n,
                "notes": f"[{tag}] {ref} seat {seat} + random roster"}
        d = None
        for attempt in range(60):
            try:
                d = dump(c.create_experience_request(body)); break
            except Exception as ex:
                msg = repr(ex)
                if "429" in msg:
                    if attempt % 6 == 0: print("queue full, waiting (seat", seat, ")", file=sys.stderr)
                    time.sleep(30)
                else:
                    print("create failed seat", seat, "attempt", attempt, msg[:200], file=sys.stderr); time.sleep(3 + 3 * attempt)
        if d is None:
            continue
        time.sleep(1)
        print("created", d["id"], "seat", seat)
        path = ROOT / "xp" / f"{tag}.json"
        cur = json.load(open(path)) if path.exists() else {"candidate": ref, "n": n, "requests": []}
        cur["requests"].append({"id": d["id"], "seat": seat})
        json.dump(cur, open(path, "w"), indent=1)
    print("saved", ROOT / "xp" / f"{tag}.json")

def report(c, paths):
    tot = {}
    for path in paths:
        d = json.load(open(path))
        by_seat = {}
        pending = 0
        for r in d["requests"]:
            seat = r["seat"]
            det = dump(c.get_experience_request(r["id"]))
            for ep in det.get("episodes", []):
                if ep.get("status") != "completed":
                    pending += 1; continue
                try:
                    st = dump(c.get_episode_request_episode_stats(ep["id"]))
                except Exception:
                    pending += 1; continue
                rw = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                if not rw:
                    pending += 1; continue
                w = 1 if rw.get(seat) else 0
                s = by_seat.setdefault(seat, [0, 0]); s[0] += w; s[1] += 1
        tw = sum(v[0] for v in by_seat.values()); tg = sum(v[1] for v in by_seat.values())
        rw_ = sum(v[0] for k, v in by_seat.items() if k < 5); rg = sum(v[1] for k, v in by_seat.items() if k < 5)
        print(f"== {path} {d['candidate']}")
        print("   " + "  ".join(f"s{k}({CLASSES[(k % 5) + (5 if k < 5 else 0)]}) {v[0]}/{v[1]}" for k, v in sorted(by_seat.items())))
        print(f"   Red {rw_}/{rg}  Blue {tw - rw_}/{tg - rg}  TOTAL {tw}/{tg} = {tw / tg if tg else 0:.3f}  pending={pending}")
        tot[path] = (tw, tg)
    return tot

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    cr = sub.add_parser("create"); cr.add_argument("ref"); cr.add_argument("--seats", default="0-9"); cr.add_argument("-n", type=int, default=12); cr.add_argument("--tag", required=True)
    rp = sub.add_parser("report"); rp.add_argument("paths", nargs="+")
    a = ap.parse_args()
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        if a.cmd == "create": create(c, a.ref, parse_seats(a.seats), a.n, a.tag)
        else: report(c, a.paths)
