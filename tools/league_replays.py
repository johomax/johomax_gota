#!/usr/bin/env python3
"""How league games on a coworld are decided (from docs/league_episodes.json replays).
usage: uv run python tools/league_replays.py [--coworld cow_252fb6a6] [--limit N]
"""
import argparse, json, pathlib, sys, urllib.request
from collections import Counter, defaultdict
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import replay_parse as rp
CL = ["VK", "Ranger", "Arcanist", "Druid", "DH", "DK", "Xbow", "Lich", "Warlock", "Berserk"]

def tower_info(tid):
    off = tid - 10; return off // 6, (off % 6) // 3, off % 3

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--coworld", default="cow_252fb6a6"); ap.add_argument("--limit", type=int, default=1000); a = ap.parse_args()
    eps = [e for e in json.load(open(ROOT / "docs/league_episodes.json")) if str(e.get("coworld_id", "")).startswith(a.coworld)][: a.limit]
    rdir = ROOT / "tmp/replays"; rdir.mkdir(parents=True, exist_ok=True)
    n = 0; outcomes = Counter(); lane_c = Counter(); fort_heroes = Counter(); gate_classes = Counter(); fort_classes = Counter()
    tower_cmds_by_class = defaultdict(int); games_by_class = Counter(); first_gate = []; ends = []; xbow_on_winner = Counter()
    for e in eps:
        url = e.get("replay_url")
        if not url: continue
        f = rdir / (e["ereq"] + ".replay")
        if not f.exists():
            try: urllib.request.urlretrieve(url, f)
            except Exception as ex: print("dl fail", ex, file=sys.stderr); continue
        try: rep = rp.load_replay(f)
        except Exception as ex: print("parse fail", repr(ex)[:80], file=sys.stderr); continue
        n += 1
        heroes = {h["id"]: h for h in rep["header"]["setup"]["heroes"]}
        outcome = e.get("outcome"); outcomes[outcome] += 1
        winner = 0 if outcome == "RedTeam" else 1 if outcome == "BlueTeam" else -1
        ends.append(rep["ticks"])
        gate_hits = Counter(); fort_att = defaultdict(set); first_gate_tick = {}; tcmds = Counter()
        for act in rep["actions"]:
            if act.get("kind") != "attackTarget": continue
            hid = act["heroId"]; team = 0 if hid < 105 else 1; tid = act["targetId"]
            if 10 <= tid <= 27:
                lane, tteam, tier = tower_info(tid)
                if tteam == team: continue
                tcmds[hid] += 1
                if tier == 2:
                    gate_hits[(team, lane)] += 1; first_gate_tick.setdefault((team, lane), act["tick"])
            elif tid in (1, 2):
                fort_att[team].add(hid)
        for hid, h in heroes.items():
            cls = CL[h["class"]]; tower_cmds_by_class[cls] += tcmds[hid]; games_by_class[cls] += 1
        if winner >= 0:
            wl = sorted(((l, c) for (t, l), c in gate_hits.items() if t == winner), key=lambda x: -x[1])
            lane = wl[0][0] if wl else -1; lane_c[lane] += 1
            fort_heroes[len(fort_att[winner])] += 1
            for hid in fort_att[winner]: fort_classes[CL[heroes[hid]["class"]]] += 1
            if wl: first_gate.append(first_gate_tick[(winner, lane)])
            xb = any(heroes[hid]["class"] in (6, 1, 7) for hid in fort_att[winner]); xbow_on_winner[xb] += 1
    import statistics as st
    print(f"games {n} outcomes {dict(outcomes)}; game end median {st.median(ends) if ends else 0:.0f}")
    print("winner breakthrough lane:", dict(lane_c), "| winner first gate attack median", st.median(first_gate) if first_gate else None)
    print("winner heroes attacking fort:", dict(sorted(fort_heroes.items())))
    print("classes among winner fort attackers:", dict(fort_classes.most_common()))
    print("winner fort attackers include a long-range class (Xbow/Ranger/Lich):", dict(xbow_on_winner))
    print("tower attack commands per game by class:", {c: round(tower_cmds_by_class[c] / games_by_class[c]) for c in CL if games_by_class[c]})

if __name__ == "__main__":
    main()
