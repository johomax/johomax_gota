# HANDOFF — Gods of the Arena policy project (updated 2026-09-15, 00:40 UTC)

## Where things stand (solo-hero regime)
- **Champion:** v30 = `Jordan:v28` (submitted 23:50 UTC, placed, auto-champion always). v30 = v19 minus the post-respawn home guard and
  the ally hold. Ten-seat hosted result 146/240 (61%) vs v19 132/240 (55%). Ladder: rank 5, 1543 MMR after 7 rounds.
- **Measurement:** `uv run python tools/xp_mixed.py create <label> --seats 0-9 -n 24 --tag t` then `report xp/t.json` (random champions in
  the other nine seats = the league's distinct-teammates seating). Platform cap: 300 undispatched episodes per user (the tool waits on 429).
  A 240-game batch has SE ~3.2%; differences under ~7 points are noise. Random champion base rate: Red 41%, Blue 59%.
- **Analysis tools:** `tools/league_data.py` (our league episodes per seat), `tools/log_stats.py` (our telemetry incl. death contexts "DC"),
  `tools/replay_lanes.py` (which lane/heroes decided each game), `tools/roster_stats.py` (per-policy win rates in random rosters).
- **Key evidence:** winners' heroes always attack the fort; usually 4 heroes hit the final gate together; mid decides 42% of games; only 20% of
  our wins came through the side lane we push alone; after a death the rejoin logic sends us to mid and those games were won more.
  Cautious/passive variants lose (v23 solo mode 45%, v25 ranged safety 51%, v32 fight-on-our-half 55%). Aggression + no waiting wins.
- **League coworld changed again ~00:00 UTC:** now `cow_9d9d7070-2210-4899-81de-f39401b32162` (2026.9.14.5, game version 30, map hash 48422D57).
  Towers/forts/spawns keep the same coordinates; terrain differs. Tools and the replay parser are updated; v30/v35/v43 smoke-tested on it.
- **Ten-seat results are confounded by field drift** (other players uploaded new versions overnight). Decide with duels only:
  `uv run python tools/xp_mixed.py duel <cand> <ctrl> --seats 0-4 -n 24 --tag duel-x` -> candidate/control in mirrored seats of the same games.
  Duel so far: v35 mid lane vs v30 43/100 (mid loses). Queued duels vs v30: v38 fort-anywhere, v40 farm-then-push (+damage-first shop),
  v41 defend threatened towers, v43 swapped side lanes. Labels: v31=:v29, v32=:v30, ..., v40=:v38, v41=:v39, v42=:v40, v43=:v41.
- Codex workers: `docs/WORKER_BRIEF2.md` + `docs/tasks/s*.md`; launch with `node "$CC" task --background --fresh --write --model gpt-6-astra --effort xhigh`.

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
