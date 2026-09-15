# Gods of the Arena — policy project

**Objective:** build a BASIC hero policy that tops the Gods of the Arena Competition ladder.

- League: `league_3c60897b-25cf-4b37-9d1a-8554c1198f28` (Gods of the Arena), division `div_a4534073-c5d2-4193-a94a-93d9c5e2e443` (Competition).
  Page: https://softmax.com/observatory/v2?detail=league:league_3c60897b-25cf-4b37-9d1a-8554c1198f28
- Coworld: `cow_0752b441-af96-421d-8a1e-f8365a95e022` version 2026.9.14.2 (downloaded to `coworld/`).
- Game README: see `docs/game_readme.md`; docs https://github.com/Metta-AI/polyworld/blob/main/examples/gods_of_the_arena/docs/index.html
- Runtime: **game-hosted** — a single `.bas` file runs as five independent hero VMs (one team of five seats).
- Softmax player: Jordan (`ply_bcb80069-fb0c-4ba5-a45c-06b647870aeb`).

## Layout
- `policy/` — policy versions (`base.bas` = bundled baseline, `v1.bas` ...). The file uploaded is noted per version below.
- `tools/probe.bas` — map/object dumper; `tools/eval.py` — local A/B harness (both sides, N seeds).
- `docs/ARENA_NOTES.md` — verified mechanics, map coordinates, host API, limits (read first).
- `docs/map_kinds.txt` — decoded 128x128 terrain with structures.
- `runs/` — local episode artifacts (gitignored). `source/polyworld` — engine source at the pinned commit (gitignored).

## Commands
```bash
uv run softmax status
export DOCKER_DEFAULT_PLATFORM=linux/amd64
P=policy/v1.bas; uv run coworld run-episode ./coworld/cow_0752b441-af96-421d-8a1e-f8365a95e022/coworld_manifest.json $P $P $P $P $P policy/base.bas policy/base.bas policy/base.bas policy/base.bas policy/base.bas -o runs/x
python3 tools/eval.py policy/v1.bas policy/base.bas -n 3
uv run coworld upload-policy --file policy/v1.bas
uv run coworld xp-request create xp/candidate.json
uv run coworld submit <name>:vN -l league_3c60897b-25cf-4b37-9d1a-8554c1198f28
```

## Current status (2026-09-15 18:20 UTC) — game version 33
- **Engine change:** the league coworld is `cow_252fb6a6` (2026.9.15.1, game version 33): towers 1200/2400/4800 HP and 28/56/112 damage
  (ranges unchanged), hero/tower collision. 61% of league games time out (0 for everyone). Details in docs/ARENA_NOTES.md (top).
- **Champion:** v49a = `Jordan:v44` (promoted 18:13 UTC): tower-safe siege (out of range, footman cover, 2 allies, low tower, or late game),
  long-range kiting (Crossbowman out-ranges every tower), damage-first shop, lane commitment (no lane switch or rejoin), all-in from tick 12000.
  Local: a lone v49a Crossbowman beat nine base.bas heroes at tick 9665. Duel vs v30 (same games): 28 wins vs 20, 59 timeouts of 107.
- v30 (previous champion) won 9/41 league games on the new coworld; ladder rank 6, 1498 MMR after 42 rounds.
- Field on the new coworld (tools/field_behavior.py --coworld cow_252fb6a6): six entrants camp mid all game; red-kite, black-kite and daveey
  push side lanes and are the only ones who attack forts. Decisive games: first gate attack ~tick 10,000, 2-5 heroes at the fort.
- Next: Codex S14 (farm when idle) and S15 (join an allied side-lane pusher) on v49a, duels vs v49a.

## Strategy log (hosted = league coworld cow_975af671, 116x116 map)
- v1 blitz (mid, 5-stack): lost 0/4 to baseline (dove towers without waves, retreated home at 25% HP; no HP regen in this game).
- v2 waveguard (follow the friendly footman front): 1/4 vs baseline; side-lane footmen decide games.
- v3 edge blitz (5-stack pushes one side lane, hardcoded coordinates): 4/4 vs baseline in ~2500 ticks; hosted Red 12/12 but Blue broken
  (waypoint inside trees + the league map turned out to be a different coworld version).
- v4 mid blitz: faster in a pure race but 0/4 vs baseline (mid campers). Rejected.
- v5 map-generic edge blitz (route from own tower ids + point symmetry, stuck recovery, boots first) = Jordan:v3, submitted.
  Hosted: 64/66 vs the whole field; ~75% vs Aaron (the #1 policy), whose defenders wipe a level-1 stack under their outer tower.
- v6 fort-first/tower-first priorities; v7 + cohesion ignores crippled allies, hold timeout, tower-suicide reset for hopeless heroes
  (fixes a hosted deadlock) = Jordan:v5, promoted champion. Still ~75% vs Aaron.
- v8 (Codex W4) resistance-driven lane switching + rejoin: beats the turtle sparring partner in ~4000 ticks (v5: ~11000) but loses
  clashes vs a pushing stack (switching away from a pusher loses the race). v9 = v8 + v7 fixes.
- v10 = v9 + no footman farming (engaged or kill shots only), switch only at the enemy outer tower vs 3+ defenders, stable rejoin.
- v11/v12: lane switch at any defended structure (3+ defenders) + rejoin via lane road: beats the turtle in ~4500 ticks but only 9/12
  vs Aaron (switching away from Aaron's 3-hero lane group loses the race). v13 = v12 with swapped lanes (Red lane 2, Blue lane 0): 11/12 vs Aaron.
- Hosted A/B vs Aaron (n=12 each, both sides): v10 11/12 (2630/2724 ticks), v12 9/12, v13 11/12 (2318/3366), v13b (v10+swap) 10/12,
  v14 (v10+fight micro) 8/12, v15 (v14+swap) 10/12. Fight micro rejected; lane swap neutral. v10 stays champion pending larger samples.
- v16 = v13 + rejoin armed only by respawn (v12's rejoin re-triggered every tick and stranded respawned heroes).
- Larger hosted samples vs Aaron (36 or 24 episodes, both sides): v10 27/36 (75%), v13 31/36 (86%), v16 34/36 (94%), v17 (v10, lane 2 both sides) 22/24 (92%).
- **v16 = Jordan:v14 promoted champion** (36/36 vs the rest of the field).
- v18 (v16 + regroup rule, no solo pushes): 21/24 vs Aaron with slower games. Rejected; v16 stays champion.
- v19 (v16 + respawned heroes guard their own gate until two allies are near, max 30 s): 45/48 vs Aaron (Red 24/24), 36/36 vs the field.
  **v19 = Jordan:v17 promoted champion.** v20 = v19 with lane 2 for Blue too (hosted test pending).
- League coworld moved to 2026.9.14.4 (cow_0752b441, same map, game version 29) during the evening; tooling updated.
- Local benchmarks: RACE (mirror lanes, speed), CLASH (--clash: both teams lane 2, fights), BASE, TURTLE (policy/spar_turtle.bas).
