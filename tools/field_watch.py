#!/usr/bin/env python3
"""Alarm for league field changes: the set of opponent policy labels seen in our last N league rounds vs the last run.
usage: uv run python tools/field_watch.py [--rounds 3] [--state tmp/field_labels.json]
Prints the current label set and 'FIELD CHANGED: +new -gone' when it differs from the stored one (then stores it).
"""
import argparse, json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rounds", type=int, default=3); ap.add_argument("--state", default="tmp/field_labels.json"); a = ap.parse_args()
    out = ROOT / "tmp/field_recent.json"
    subprocess.run([sys.executable.replace("python", "python"), str(ROOT / "tools/league_data.py"), "--rounds", str(a.rounds), "--out", str(out)], capture_output=True, text=True, cwd=ROOT)
    try: d = json.load(open(out))
    except Exception: print("no league data"); return
    labels = sorted({l for e in d for l in e["seat_policies"] if l and l != "?" and not l.startswith("Jordan")})
    sp = ROOT / a.state; prev = json.load(open(sp)) if sp.exists() else []
    new = sorted(set(labels) - set(prev)); gone = sorted(set(prev) - set(labels))
    print("labels:", ", ".join(l.split(":")[0][-22:] + ":" + l.split(":")[1] for l in labels))
    if prev and (new or gone): print("FIELD CHANGED: +" + ", ".join(new) + " -" + ", ".join(gone))
    json.dump(labels, open(sp, "w"))
if __name__ == "__main__":
    main()
