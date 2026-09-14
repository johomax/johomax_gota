#!/usr/bin/env python3
"""Local A/B harness: run candidate vs opponent on both sides over N seeds.

usage: tools/eval.py A.bas B.bas [-n N] [--tag name]
Runs two run-episode batches in parallel (A red / B blue, and B red / A blue),
each with N seeds (2026, 2027, ...). Prints A's win rate and mean ticks.
"""
import argparse, json, os, subprocess, sys, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "coworld/cow_975af671-4f4d-4a04-8b95-d5c5a54b7f40/coworld_manifest.json"

def run(red, blue, n, out):
    cmd = ["uv", "run", "coworld", "run-episode", str(MANIFEST)] + [red] * 5 + [blue] * 5 + \
          ["-o", str(out), "-n", str(n), "--timeout-seconds", "900", "--variant", "competition"]
    env = dict(os.environ, DOCKER_DEFAULT_PLATFORM="linux/amd64")
    return subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def collect(out, n):
    res = []
    if n == 1:
        paths = [out / "results.json"]
    else:
        paths = sorted(out.glob("episode-*/results.json"))
    for p in paths:
        try:
            res.append(json.load(open(p)))
        except Exception as e:
            res.append(None)
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a"); ap.add_argument("b")
    ap.add_argument("-n", type=int, default=3)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--jobs", type=int, default=2, help="parallel run-episode batches (each batch is sequential)")
    ap.add_argument("--clash", action="store_true", help="set `clash = 1` in copies of both policies so both teams push lane 2 and meet head-on")
    args = ap.parse_args()
    tag = args.tag or f"eval-{int(time.time())}"
    base = ROOT / "runs" / tag
    base.mkdir(parents=True, exist_ok=True)
    if args.clash:
        for attr in ("a", "b"):
            src = pathlib.Path(getattr(args, attr)); txt = src.read_text()
            assert "clash = 0" in txt, f"{src} has no `clash = 0` flag"
            dst = base / (src.stem + "_clash.bas"); dst.write_text(txt.replace("clash = 0", "clash = 1"))
            setattr(args, attr, str(dst.relative_to(ROOT)))
    # split seeds across jobs: each job runs ceil(n/jobs) episodes? run-episode -n increments seed from the fixture seed,
    # so all batches would reuse the same seeds; keep it simple: 2 batches (sides), n episodes each.
    t0 = time.time()
    # one eval at a time machine-wide: concurrent run-episode calls can collide
    import fcntl
    lock = open(ROOT / "runs" / ".eval.lock", "w"); fcntl.flock(lock, fcntl.LOCK_EX)
    # batches run sequentially: parallel run-episode calls collide on staged player files
    for red, blue, name in ((args.a, args.b, "a_red"), (args.b, args.a, "b_red")):
        p = run(red, blue, args.n, base / name)
        _, err = p.communicate()
        if p.returncode != 0:
            print(f"[{name}] run-episode failed rc={p.returncode}\n{err.decode()[-2000:]}", file=sys.stderr)
    ra = collect(base / "a_red", args.n)
    rb = collect(base / "b_red", args.n)
    wins = 0; games = 0; ticks = []
    rows = []
    for i, r in enumerate(ra):
        if r is None: rows.append(("a_red", i, "FAIL")); continue
        w = r["outcome"] == "RedTeam"; wins += w; games += 1; ticks.append(r["ticks"])
        rows.append(("a_red", i, "A" if w else "B", r["ticks"], r["total_xp"]))
    for i, r in enumerate(rb):
        if r is None: rows.append(("b_red", i, "FAIL")); continue
        w = r["outcome"] == "BlueTeam"; wins += w; games += 1; ticks.append(r["ticks"])
        rows.append(("b_red", i, "A" if w else "B", r["ticks"], r["total_xp"]))
    for row in rows: print(row)
    print(f"A={args.a} vs B={args.b}: A wins {wins}/{games} ({(wins/games if games else 0):.2f}), mean ticks {sum(ticks)/len(ticks) if ticks else 0:.0f}, wall {time.time()-t0:.0f}s, dir runs/{tag}")
    json.dump({"a": args.a, "b": args.b, "wins": wins, "games": games, "rows": rows}, open(base / "summary.json", "w"))

if __name__ == "__main__":
    main()
