#!/usr/bin/env python3
"""Print the league division ladder: rank, entrant, MMR, rounds, win rate, current policy label.
usage: uv run python tools/ladder.py [--top 12]"""
import argparse, json
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
LEAGUE = "league_3c60897b-25cf-4b37-9d1a-8554c1198f28"; DIV = "div_a4534073-c5d2-4193-a94a-93d9c5e2e443"
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--top", type=int, default=12); ap.add_argument("--raw", action="store_true"); a = ap.parse_args()
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        rows = [dump(r) for r in (c.get_division_leaderboard(DIV) or [])]
    if a.raw: print(json.dumps(rows[:2], default=str)[:3000]); return
    for r in rows[: a.top]:
        print(f"{r.get('rank', 0):2d} {str(r.get('player_name'))[:16]:16s} {r.get('score') or 0:5.0f} rounds {r.get('rounds_played') or 0:4d} wr {r.get('win_rate') or 0:.3f} {r.get('policy_label')}")
if __name__ == "__main__":
    main()
