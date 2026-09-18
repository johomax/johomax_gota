#!/usr/bin/env python3
"""Pick the live policy from the 5v5 matrix and the recent league opponent mix.

usage: uv run python tools/portfolio_pick.py [--rounds 10] [--files xp/mx*.json ...]
For each candidate version (from the matrix files' 'candidate' field) computes p(win | opponent label, side) from the completed
episodes, weights by the opponent frequency in our last N league rounds (labels from league_data), assumes 0.5 for unmeasured
labels, and prints the expected win rate per candidate. Matrix caches per-request results in tmp/matrix_cache.json.
"""
import argparse, glob, json, pathlib, subprocess, sys
from collections import Counter, defaultdict
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rounds", type=int, default=10); ap.add_argument("--files", nargs="*", default=None); a = ap.parse_args()
    files = a.files or sorted(glob.glob(str(ROOT / "xp/mx*.json")))
    cp = ROOT / "tmp/matrix_cache.json"; cache = json.load(open(cp)) if cp.exists() else {}
    res = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # version -> (label, side) -> [wins, games]
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for f in files:
            d = json.load(open(f)); ver = d["candidate"].split(":")[-1]
            for r in d["requests"]:
                key = r["id"]
                if key not in cache or cache[key][1] < d["n"]:
                    det = dump(c.get_experience_request(r["id"])); w = 0; n = 0
                    for ep in det.get("episodes", []):
                        if ep.get("status") != "completed": continue
                        try: st = dump(c.get_episode_request_episode_stats(ep["id"]))
                        except Exception: continue
                        rw = {ps["position"]: ps.get("avg_reward") or 0 for ps in st.get("policy_stats", [])}
                        n += 1; w += 1 if rw.get(r["seat"]) else 0
                    cache[key] = [w, n]
                w, n = cache[key]; t = res[ver][(r["opp"], "Red" if r["side"] == 0 else "Blue")]; t[0] += w; t[1] += n
    json.dump(cache, open(cp, "w"))
    out = ROOT / "tmp/league_mix.json"
    subprocess.run([sys.executable, str(ROOT / "tools/league_data.py"), "--rounds", str(a.rounds), "--out", str(out)], capture_output=True, text=True, cwd=ROOT)
    mix = Counter()
    for e in json.load(open(out)):
        opp = [l for l in e["seat_policies"] if l and l != "?" and not l.startswith("Jordan")]
        mix[opp[0] if opp else "?"] += 1
    total = sum(mix.values())
    print(f"opponent mix over the last {a.rounds} rounds ({total} games):", ", ".join(f"{l.split(':')[0][-18:]}:{l.split(':')[-1]} x{n}" for l, n in mix.most_common()))
    for ver in sorted(res, key=lambda v: int(v[1:])):
        exp = 0.0; covered = 0
        for label, n in mix.items():
            ps = []
            for side in ("Red", "Blue"):
                w, g = res[ver].get((label, side), [0, 0]); ps.append(w / g if g else 0.5)
                covered += g > 0
            exp += n * 0.5 * (ps[0] + ps[1])
        print(f"  {ver}: expected win rate {exp/total:.3f}  (measured cells {covered}/{2*len(mix)})")
if __name__ == "__main__":
    main()
