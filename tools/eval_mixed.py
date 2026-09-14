#!/usr/bin/env python3
"""Mixed-team local harness: candidate in ONE seat, filler policy in the other 9 seats.
usage: tools/eval_mixed.py CAND.bas [-n N] [--filler policy/base.bas] [--tag t]
Runs N seeds with the candidate in seat 0 (Red, class DeathKnight) and N seeds in seat 5 (Blue, VanguardKnight),
plus N seeds of pure filler for the baseline team win rate. Prints the candidate's team win rate per side vs baseline.
"""
import argparse, json, os, subprocess, sys, time, pathlib, fcntl
ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "coworld/cow_0752b441-af96-421d-8a1e-f8365a95e022/coworld_manifest.json"
def run(seats, n, out):
    cmd = ["uv","run","coworld","run-episode",str(MANIFEST)] + seats + ["-o",str(out),"-n",str(n),"--timeout-seconds","900","--variant","competition"]
    env = dict(os.environ, DOCKER_DEFAULT_PLATFORM="linux/amd64")
    p = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if p.returncode: print(p.stderr.decode()[-800:], file=sys.stderr)
    res = []
    for pth in (sorted(out.glob("episode-*/results.json")) if n > 1 else [out/"results.json"]):
        try: res.append(json.load(open(pth)))
        except Exception: res.append(None)
    return res
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cand"); ap.add_argument("-n", type=int, default=3)
    ap.add_argument("--filler", default="policy/base.bas"); ap.add_argument("--tag", default=None); ap.add_argument("--seat", type=int, default=None)
    a = ap.parse_args(); tag = a.tag or f"mixed-{int(time.time())}"; base = ROOT/"runs"/tag; base.mkdir(parents=True, exist_ok=True)
    lock = open(ROOT/"runs"/".eval.lock","w"); fcntl.flock(lock, fcntl.LOCK_EX)
    f = a.filler; t0 = time.time()
    seats_list = [(0,"red"),(5,"blue")] if a.seat is None else [(a.seat, "red" if a.seat < 5 else "blue")]
    summary = {}
    for seat, side in seats_list:
        seats = [f]*10; seats[seat] = a.cand
        res = run(seats, a.n, base/f"seat{seat}")
        wins = sum(1 for r in res if r and r["outcome"] == ("RedTeam" if side=="red" else "BlueTeam")); games = sum(1 for r in res if r)
        ticks = [r["ticks"] for r in res if r]; xp = [r["total_xp"][seat] for r in res if r]
        summary[side] = (wins, games)
        print(f"seat {seat} ({side}): team wins {wins}/{games}, mean ticks {sum(ticks)/max(1,len(ticks)):.0f}, my hero xp {xp}")
    res = run([f]*10, a.n, base/"filler")
    rw = sum(1 for r in res if r and r["outcome"]=="RedTeam"); g = sum(1 for r in res if r)
    print(f"filler-only baseline: Red wins {rw}/{g} (Blue {g-rw}/{g}), wall {time.time()-t0:.0f}s, dir runs/{tag}")
if __name__ == "__main__": main()
