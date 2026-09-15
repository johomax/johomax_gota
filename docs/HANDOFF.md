# HANDOFF — Gods of the Arena policy project (paused 2026-09-15, 00:45 UTC at the user's request)

## Current state (2026-09-15 18:35 UTC) — GAME VERSION 33
- League coworld `cow_252fb6a6` (2026.9.15.1, game version 33): towers 1200/2400/4800 HP, 28/56/112 dmg; 55-61% of games time out.
  Details: docs/ARENA_NOTES.md top section; new engine source in tmp/engine_new (source/polyworld origin/main).
- **Champion: v49a = `Jordan:v44`** (promoted 18:13 UTC): tower-safe siege, long-range kiting, damage-first shop, lane commitment, all-in from
  tick 12000. Duel vs v30: 30 wins / 20 control wins / 70 timeouts (120 games). Crossbowman seat wins 50% (the carry); other classes ~20%.
- Local truth on the new coworld: a lone v49a Crossbowman beats nine base.bas heroes (tick 9665); five committed clones win at tick 27402;
  mid-lane variants (v48b/v49b) time out; solo melee vs base loses. Local games take 5-10 min each; do not run two run-episode at once.
- Duels vs v49a (120 shared games; candidate wins / control wins / timeouts): v50 farm idle 23/24/73 (wash), v51 join allied pusher 29/21/70,
  v53 all-in from tick 4000 23/16/81, v52 long-range shop dropped (slower local Crossbowman game; seat batches 19/72 vs 17/72).
  v54 tower bait 24/25/71 (wash), v51 replication 32/27/61 (v51 total 61-48 over 240), v55 = v51+v53 27/26/67 (wash), v56 = v55 with
  all-in from tick 600 29/25/66. Nothing beats v49a by more than noise; champion stays v49a until a candidate shows >= +8 over 240 games.
  v57 (:v52) = v55 + spell posts: casts DO work and damage towers (~0.4 HP/tick, runs/v57dbg2), but the caster-seat duel was 15/28/53
  (Lich 0/24, Ranger 1/24) — posting instead of fighting loses; dropped. v53 replication 23/18 (total 46-34 over 240, modest).
  v58 (:v53, Codex S19) = v49a + buddy the ally deepest in enemy territory; duel vs v49a running, plus a third v51 batch (early 18/9).
- Ideas not done: Lich Ice Spear (6.33 tiles) snipes gate towers from outside their 6.0 range via castTarget (towers are valid spell targets);
  all-in timing; STUCK counts are high (tower collision footprints).

## Read first
1. `docs/ARENA_NOTES.md` — verified mechanics, map coordinates, host API, BASIC dialect gotchas, opponent habits, engineering lessons.
2. `README.md` — strategy log with every version and its measured result.
3. `policy/v19.bas` (champion) and `policy/v23.bas` (best solo-mode candidate). Both derive from v5 -> v8 (Codex lane switching) -> v9/v10 -> v12 -> v13 -> v16 -> v19.

## Measured results (hosted, both sides)
Five-clone rosters vs the #1 policy Aaron (`aaron-gota-ir-waveguard-r4:v2`): v10 27/36, v13 31/36, v16 34/36, v17 22/24, v19 45/48, v18 21/24, v20 21/24.
All strong versions beat every other ladder policy 36/36 in five-clone rosters.
Random rosters (my policy in seat 0 or 5, nine `{"random": true}` seats; models the new seating, very noisy, SE ~5-7%):
v19 61/96 (64%), v21 56/96 (58%), v22 25/48 (52%), v23 30/48 (62%; Blue 20/24, Red 10/24). Champion stays v19.
Caveat: those batches always used seats 0 and 5 (Death Knight / Vanguard Knight). Rotate seats 0-9 in future batches to cover all classes.

## Tooling
- `python3 tools/eval.py A.bas B.bas -n N --tag t [--clash]` — local five-clone A/B (RACE mirror lanes / CLASH both lane 2 / vs `policy/base.bas` / vs `policy/spar_turtle.bas`). File-locked, one at a time.
- `python3 tools/eval_mixed.py CAND.bas -n N` — local mixed-team proxy (candidate in seat 0 and 5, base.bas fillers). Weak proxy; base fillers just camp mid.
- `python3 tools/xp.py create <cand_ref> <opp_ref>... -n N --tag t` / `report xp/t.json` — hosted five-clone A/B. For random rosters see the inline snippets in git history (xp/*-mixed*.json were created with roster `{"random": true}` in nine seats; `report` works on them).
- `python3 tools/replay_parse.py FILE --summary | --timeline HERO_ID --every N` — parse hosted/local replays (game version 29 supported). Opponent lane habits came from this.
- `tools/probe.bas` dumps map/objects; `tools/mapcheck.py` validates waypoints on the decoded map (`docs/map_kinds.txt`).
- Codex workers: `docs/WORKER_BRIEF.md` + `docs/tasks/*.md`; launch with `node "$CC" task --background --fresh --write --model gpt-6-astra --effort xhigh`. They cannot run Docker, so the orchestrator runs all evals.
- Upload: `uv run coworld upload-policy --file policy/vNN.bas --tag version=vNN` (next label is `:v22`). Promote: `uv run coworld submit "<name>:vNN" -l <league> --auto-champion always --no-open-browser`.

## Policy design summary (v19 / v23)
- Map-generic: at tick 1 read own towers (ids 10+lane*6+team*3+tier) and fort; enemy positions = (mapWidth-1-x, mapHeight-1-y). Route = own gate->inner->outer, enemy outer->inner->gate, fort.
- Stack mode (allies >= 3 nearby at tick 360): Red pushes lane 2, Blue lane 0; focus fire lowest-HP enemy hero in range; footmen only when engaged or kill shots; fort-first when exposed; siege towers; lane switch when 3+ defenders hold a structure (cooldown 1500 ticks); boots first, then damage/HP items; kite ranged vs melee; potions at 55%; stuck recovery; hold-timeout; crippled-hero tower reset; home guard after respawn (v19).
- Solo mode (v21+, allies < 3 at tick 360): lane by seat parity; follow the friendly footman front; farm footmen; siege only with the wave or low towers; retreat when outnumbered (v22 hysteresis); v23 skips home guard and keeps the solo lane after respawn.

## Open ideas (not done)
1. Rotate seats in random-roster batches; compare v19 vs v23 at n >= 96 each per side before promoting anything.
2. Solo mode: choose the lane where the team already has allied heroes (help the group) vs. the empty lane; measure.
3. Defensive behaviour when the own fort is exposed; timeouts become possible in long mixed games.
4. buyItem is called every tick once thresholds are met (harmless but wasteful, ~800 calls/game).
5. STUCK recovery fires 7-26 times per game; better waypoints or smarter re-pathing could save time.
6. The forum/wiki have no entry from us yet; the coworld-version and seating changes are worth a forum note.
