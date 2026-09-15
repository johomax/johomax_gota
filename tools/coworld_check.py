#!/usr/bin/env python3
"""Detect league coworld/engine changes. usage: uv run python tools/coworld_check.py [--expect cow_...]
Prints the league's current coworld id/version, the latest engine commit on origin/main, and warns if either differs from the last run
(state in tmp/coworld_check.json)."""
import argparse, json, pathlib, subprocess
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAGUE = "league_3c60897b-25cf-4b37-9d1a-8554c1198f28"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--expect", default=None); a = ap.parse_args()
    state_p = ROOT / "tmp/coworld_check.json"; state = json.load(open(state_p)) if state_p.exists() else {}
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        lg = c.get_league(LEAGUE).model_dump()
        cow = lg["game"]["coworld_id"]
    src = ROOT / "source/polyworld"
    subprocess.run(["git", "-C", str(src), "fetch", "--depth", "20", "origin", "main"], capture_output=True)
    head = subprocess.run(["git", "-C", str(src), "log", "--oneline", "origin/main", "-1"], capture_output=True, text=True).stdout.strip()
    changed = []
    if state.get("coworld") and state["coworld"] != cow: changed.append(f"COWORLD CHANGED {state['coworld']} -> {cow}")
    if state.get("head") and state["head"] != head: changed.append(f"ENGINE CHANGED {state['head']} -> {head}")
    if a.expect and a.expect != cow: changed.append(f"coworld differs from expected {a.expect}")
    print(f"league coworld: {cow}\nengine origin/main: {head}")
    for m in changed: print("WARNING:", m)
    json.dump({"coworld": cow, "head": head}, open(state_p, "w"))

if __name__ == "__main__":
    main()
