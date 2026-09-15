# HANDOFF — Gods of the Arena policy project (paused 2026-09-15, 00:45 UTC at the user's request)

## Current state (2026-09-15 18:35 UTC) — GAME VERSION 33
- League coworld `cow_252fb6a6` (2026.9.15.1, game version 33): towers 1200/2400/4800 HP, 28/56/112 dmg; 55-61% of games time out.
  Details: docs/ARENA_NOTES.md top section; new engine source in tmp/engine_new (source/polyworld origin/main).
- **Labels now equal file numbers.** Platform versions auto-increment per policy name (a ':' in --name is rejected), so v66-v70 were
  re-uploaded in order to land as :v66-:v70; from now on upload every policy file exactly once, in numeric order, and the label matches.
- **Champion: v68 = `Jordan:v68`** (same bytes as the earlier :v63; promoted 20:29 UTC, re-pointed to :v68 at 20:36; v62 + Red non-Crossbowman heroes escort the allied Crossbowman while it pushes;
  102-85 vs v62 over 360 duel games, positive in both batches). v69 (:v64, escort only while the Crossbowman sieges/is threatened) is dueling v62.
  Previous: v62 = `Jordan:v57` (v51 + weakest-lane switch; 63-56 vs v51 over 240, 43-45 vs v49a over 240 — parity).
  Previous: v51 = `Jordan:v46` (promoted 19:00 UTC; v49a + join an allied side-lane push; 91-66 vs v49a over 360 duel games).
  Previous: v49a = `Jordan:v44` (promoted 18:13 UTC): tower-safe siege, long-range kiting, damage-first shop, lane commitment, all-in from
  tick 12000. Duel vs v30: 30 wins / 20 control wins / 70 timeouts (120 games). Crossbowman seat wins 50% (the carry); other classes ~20%.
- Local truth on the new coworld: a lone v49a Crossbowman beats nine base.bas heroes (tick 9665); five committed clones win at tick 27402;
  mid-lane variants (v48b/v49b) time out; solo melee vs base loses. Local games take 5-10 min each; do not run two run-episode at once.
- Duels vs v49a (120 shared games; candidate wins / control wins / timeouts): v50 farm idle 23/24/73 (wash), v51 join allied pusher 29/21/70,
  v53 all-in from tick 4000 23/16/81, v52 long-range shop dropped (slower local Crossbowman game; seat batches 19/72 vs 17/72).
  v54 tower bait 24/25/71 (wash), v51 replication 32/27/61 (v51 total 61-48 over 240), v55 = v51+v53 27/26/67 (wash), v56 = v55 with
  all-in from tick 600 29/25/66. Nothing beats v49a by more than noise; champion stays v49a until a candidate shows >= +8 over 240 games.
  v57 (:v52) = v55 + spell posts: casts DO work and damage towers (~0.4 HP/tick, runs/v57dbg2), but the caster-seat duel was 15/28/53
  (Lich 0/24, Ranger 1/24) — posting instead of fighting loses; dropped. v53 replication 23/18 (total 46-34 over 240, modest).
  v58 (:v53, Codex S19) buddy the deepest ally: 20/25 vs v49a (dropped). v51 third batch 30/18 -> promoted (91-66 over 360).
  v59 (:v54, Codex S20) Crossbowman survival: seat-1 batches 10/48 vs v49a 15/48 (dropped; caution loses every time).
  v60 (:v55) = v51 with the join rule covering mid too: 22/24 vs v51 (wash; its mid condition rarely fired because campers sit ~17 tiles
  from the mid towers). v61 (:v56) = v51 without Crossbowman kiting: seat-1 batches 20/48 vs v51 18/48 (no signal; kiting kept).
  v63 = v51 + join the mid brawl when 2+ allies are within 20 tiles of the map centre: duel vs v51 queued.
  v62 (:v57, Codex S21) = v51 + switch to the lane whose enemy towers have the least remaining HP (from tick 6000): duel vs v51 26/15 after
  120 games 33/21/66 -> promoted; replication 30/35/55, so v62 is only 63-56 over 240 (noise; kept as champion/base since it is not worse).
  v63 (:v58) join-the-mid-brawl 17/27/76 (dropped). v64 (:v59) opportunistic tower spells: caster seats 14/72 vs v51 11/72 (no signal; only
  ~4 casts per game). v65 (:v60) = v62 with the weakest-lane check from tick 3000 and a 20% margin: 39/26/55 vs v62 -> replication and a
  v65 replication vs v62 32/31 and v65 vs v51 35/36: the weakest-lane family is parity/noise (v62 kept as base only).
  v68 (:v63, Codex S23) = v62 + Red non-Crossbowman heroes escort the allied Crossbowman while it pushes: 38/28/54 vs v62 -> 240-game
  replication at 54/46 after 199 (combined 92-74 over 319, consistently positive). v69 (:v64, Codex S24) escorts only while the
  Crossbowman is within 8 tiles of an exposed tower or 10 tiles of an enemy hero: duel vs v62 queued. v62 ten-seat: 49/240 (Xbow 11/24; every other seat 1-8/24, i.e. base rate);
  v62 vs v49a 240 games 43/45 -> everything since v49a is within noise of each other. Also queued: v66 (:v61, weakest-lane
  check every 300 ticks from 1500, 10% margin) vs v62, and v67 (:v62, tunnel-vision all-in: attack the tower even with heroes adjacent,
  fight only kill shots) vs v62. Results: v66 23/33/64 (dropped), v67 25/39/56 (dropped: fighting adjacent heroes during dives matters).
  Round 308 (first with v62): 1501 MMR, rank 7. Rule: promote only >= +8 over >= 240 shared games.
  v64 (:v59, Codex S22) opportunistic tower spells: caster-seat batches (2,6,7) vs v51 queued.
  Local games are deterministic per seed (verified), so single local games are exact seed-specific A/Bs.
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
