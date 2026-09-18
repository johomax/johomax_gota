# Gods of the Arena — policy project

**Objective:** build a BASIC hero policy that tops the Gods of the Arena Competition ladder.

- League: `league_3c60897b-25cf-4b37-9d1a-8554c1198f28` (Gods of the Arena), division `div_a4534073-c5d2-4193-a94a-93d9c5e2e443` (Competition).
  Page: https://softmax.com/observatory/v2?detail=league:league_3c60897b-25cf-4b37-9d1a-8554c1198f28
- Coworld: `cow_126f2fcb-80a0-4b6e-8166-eb6163576db5` (league build since 2026-09-16 ~22:30 UTC, "guarded gods" engine f2ab959: two 1950-HP guard towers per fort, ids 28-31; downloaded to `coworld/`).
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

## Current status (2026-09-16 00:50 UTC) — game version 36
- **Game version 36 (~23:20 UTC 2026-09-15, coworld `cow_fdd365d8`):** balance as version 34, creeps route around towers, new BASIC
  observations (objectTarget etc., docs/ARENA_NOTES.md top). Games run ~2x faster than version 34 (hosted median end 8400 ticks; winner's
  first gate attack ~5700, fort ~8000). Champion stays **v76 = `Jordan:v76`**: ten-seat baseline on v36 119/240; league 5/21 (rounds 315-316), rank 8.
- Duels vs v76 on v36 (candidate/control per shared games): v82 target-aware siege 59/61 + 117/123 (level), v83 58/62 (level), v84 group follow
  53/66 (negative), sanity v76 vs v68 117/121. Field strength over 840 hosted games (tools/roster_stats.py): black-kite 0.566, richard 0.563,
  khors 0.552, red-kite 0.519, base.bas 0.484; v76 0.496. Lane tests: v85 mid lane 50/70 (negative), v86 other side lane 62/58 (parity).
- **Champion since ~17:40 UTC 2026-09-16: v148 = `Jordan:v148`** — emergency fix for GAME VERSION 37 (league coworld cow_dd6ceed6,
  engine 5c701f9): dead towers/barracks are no longer listed to policies, so v113/v139 parked on dead tower coordinates until the
  timeout (local Ranger game: 318 stuck prints, 28800 ticks). v148 = v139 + walks stop 3 tiles short of buildings + an unseen
  building objective within 4 tiles counts as dead. Local: Ranger won 7727 / 0 stuck, DK won 14074 (both lost/timed out with v139).
  Hosted on the new coworld: v148 vs v139 174/240 (0.725); ten-seat random-roster baseline 156/240 = 0.650 (Red 0.67, Blue 0.63). Later baselines 0.575 and 0.608 (Blue seats 0.55-0.61). **Champion since 00:17 UTC 2026-09-17: v186 = v177 + guard focus (siege a fort guard through defenders when our wave is on it); 386/720 = 0.536 vs v175 over three batches, ~0.505 in ten-seat random rosters on the guarded-gods engine. v177 (guard objective) held 23:46-00:17, v175 (guarded-gods hotfix) 22:44-23:46.** (skip tower ids >= 28 in both route scans; v148 died at init on the new engine and idled through rounds 359-360). **League after round 395 (17:41 UTC 2026-09-17): rank 7 at 1541** (Aaron's Optimize 1621); rank 1 was held 21:32-00:15 UTC on 2026-09-16 before the guarded-gods engine change; after round 357: 1583 (relh 1577, daveey 1561, black-kite 1535); v148 league record ~42/73 over rounds 349-357. Random-roster level has slid to ~0.50 as the field adapts (black-kite:v13 0.59). Candidates v149-v163 (tower HP defaults, barracks endgame, melee farm radius, Blue lane choice, VIA waypoint, objective reset, Druid support, melee back-off, Blue farm-first, Blue wave-camper) all level or negative — see docs/HANDOFF.md. Version 37 also adds barracks buildings (kind 5, 950 HP, killable after the
- **19:35 UTC 2026-09-18: champion v267** = v254 with the group focus (siege through standing enemy heroes with two allies beside me) restricted to Red. Aaron fielded a counter named after v254 (j254-warning100) that camps our Blue lane and beat v254/v228/v218 0/12; v267's Blue fights the defenders first and beats it 6/6. Six-seed bed over thirteen labels 115/156 (Blue 78/78, Red 37/78 = v254's Red).
- **10:10 UTC 2026-09-18: champion v254** = v228 + Red-only spell-farming (castTarget slots 1-2 on the footman target when no enemy hero is within 10 tiles). Six-seed matrix over ten labels 93/120 = 0.775 (Blue 60/60, Red 33/60: black-kite 3/6 and red-kite 3/6 where every earlier version had 0, relh 2/6, perim-aaron 2/6); picker 0.762 vs v228 0.696. Root cause found on the way: fort guards are immune to spells and the engine never auto-casts on them; relh's guard-phase edge is two hero levels from area-spelling the creep waves, which v254 now copies on Red.
- **01:36 UTC 2026-09-18: champion v228** (six-seed matrix over fifteen labels 126/180 = 0.700; portfolio picker 0.707 vs v218 0.605 and v186 0.600 for the current round mix) = v218 with the group-focus rule limited to lane towers (fort guards excluded): keeps every v218 win and adds both kite matchups on Blue (12/12 over six seeds where v218 had 0/12). League with v228 through round 425: 30/42; v254 live from round 426: 33/47 through round 442 -> rank 4 at 1658 (19:15 UTC; Aaron 1697, relh 1687, Aaron's Co-play 1687); round 442 brought the first Blue loss, to Aaron's new j254-warning100 label built against v254. v267 live from round 443: 4/4 through round 444 -> rank 4 at 1671 (20:42 UTC; Aaron's Co-play 1699, Aaron 1684, relh 1674).
- **Portfolio (2026-09-18 00:50 UTC):** the field re-tunes against the live policy within hours; the matrix of our versions vs the current league labels (`xp_league.py homo`, `homo_report.py`) decides what is live. six-seed matrix over twelve labels: v218 93/132, v186 90/132 — exact complements (v186 beats every kite version and codex-side-aware, v218 beats aaron-on-Blue, relh, richard, g002, macromackie).
- **Two formats:** v228 is tuned for the league's 5v5 homogeneous rounds; for mixed-team (offline tournament) play use v212. Realistic mixed bed (us + four weak allies vs five top labels, 48 rosters x 3): v212 46/144 vs v228 31/144 on the black-kite v16 pool; v212 32/144 vs v228 19/144, v254 20/144 and v267 21/144 on the 2026-09-18 pool (relh v154, red-kite v34, aaron coordinated-support-anchor in TOP).
- **23:08 UTC 2026-09-17: champion v218** (six-seed 5v5 bed 51/72: Blue 35/36, Red 16/36; 24/24 vs the six weaker league opponents) = v215 with the camped-lane switch disabled (it fled the mid collision at first contact): 5v5 bed 18/24 — Blue 12/12, Red 6/12 (relh, richard, gota-g002).
- **22:57 UTC 2026-09-17: champion v215** = v209 with a conservative ally-majority rule and boots before the dagger (no Red hold): 5v5 bed Blue 12/12 across the six main opponents, Red 2/12.
- **22:52 UTC 2026-09-17: champion v214** = v209 with a conservative ally-majority rule, boots bought before the dagger, and (to be removed) a Red hold at the own mid tower. The competition is five copies vs five copies; games are deterministic per matchup; boots flip the Blue race (11/12 across the six main opponents). See docs/HANDOFF.md.
- **20:57 UTC 2026-09-17: champion v209** = adaptive lane (join the lane where most allies are, ticks 600-3000), leave a lane camped by two enemy heroes, and group focus (siege the tower in reach whenever two allies are within 8 tiles). Realistic paired rosters: 106/288 against Aaron's camping pair (v192 14/144), 79/144 against his previous pair (v192 ~0.48).
- **20:39 UTC 2026-09-17: interim champion v205** (= v192 + group focus: siege the tower in reach whenever two allies are within 8 tiles) — Aaron's pair switched to a mid-choke camping policy (perimeter-blue) that beats the plain mid rush 130-14 on realistic rosters; v205 reads 38/144 there vs v192's 14/144.
- **19:45 UTC 2026-09-17: champion v192** (= v186 with Red pushing mid). The league is a ~3000-tick race in which we are the Red DK / Blue VK at slot 0 with lower-rated teammates who push mid; measured on realistic paired rosters (`tools/xp_league.py --realistic`): v192 104/216 vs v186 80/216 (Red +20 over 108, Blue identical code).
  lane's towers, 3 creeps each per wave), towers 950/1300/1950 HP with bigger footprints, and buffs for Crossbowman/Berserker/Lich.
- **Champion 09:10-17:40 UTC 2026-09-16: v139 = `Jordan:v139`** = v113 + a melee-only package (Codex S41/S43): melee heroes last-hit
  before hitting a healthy tower, open on enemy heroes only when adjacent / nearly dead / with an ally near, and never run ahead of
  their own lane's front footman toward a standing enemy tower. Melee-seat duels vs v113: 133/240 then 122/240 (= 255/480, +30, both
  batches positive; melee deaths down 25-40%); ranged code unchanged. Promoted below the +36/360 bar on the consistency of three
  positive batches (v135 +12/120 was the same mechanism). Ten-seat random-roster baseline 150/240 = 0.625 (v113 0.575). League with
  v139: 56/90 = 0.62 over rounds 333-342 (Red 0.58, Blue 0.66); rank 2 at 1582 MMR at 14:00 UTC (richard 1621, black-kite 1547). Dropped today: v135-v138
  (wave-riding variants), v140 (Blue pushing physical lane 2: 0.633 vs 0.613 in a fair Blue-seat test), v141 (casters wave-bound,
  +10/240), v142 (no Crossbowman escort, +8/480 with the Red rows at 0.479), v143/v144 (race-aware gate defence: -20/240 — safety
  rules keep losing tempo on version 36). League findings: Red wins only 0.36 of league games, seating puts the higher-rated players
  on Blue (black-kite sits Blue 78% of the time), private policy logs are available for league episodes (tools/league_logs.py).
  League structure found today: Red wins only 0.36 of league games and Blue seats hold the higher-rated players in 73% of games.
- **Previous champion 03:36-09:10 UTC 2026-09-16: v113 = `Jordan:v113`** = v93 + stutter-step kiting for ranged classes (hit while the attack
  cooldown is within the windup, step away from melee threats during recovery, via the version-36 selfAttackCooldown observation):
  67-53 then 140-100 vs v93 (207-153 over 360). Ranged deaths per game fell from 2.4-3.0 to 0.6-1.2. Level vs v113 and dropped: v114
  (wider kite trigger) 58/62, v115 (melee anti-kite) 58/62, v116 (range-advantage kiting) 61/59. The remaining gap is on the Red-side
  classes (DK 0.38, Berserk 0.29, Lich/Warlock 0.46 vs Blue classes 0.71-0.88). Level vs v113 and dropped: v117 (escort only for ranged
  Red heroes) 62/58, v118 (no Red escort) 61/59, v119 (free inventory slot for elixirs) 59/61, v120 (melee flee at 40%) 59/61, v121 (melee
  farm radius 8 tiles) 63/57. v122 (walk the lane's route points when the objective is far) opened 67/53 vs v113 but replicated 86/114
  and v123 (v122 + audit fixes) lost 44/76: tower-centre route points snag on footprints (hosted stuck events doubled), so road-following
  is rejected. A Codex audit of v113 found several mis-gated rules (dead respawn rejoin, stale tower-HP defaults, kite target out of
  range, fallback siege beside an enemy, forward-pointing retreat point) but the fix bundle did not help: v124 (route-point switch at 6
  tiles) 55/65, v125 (audit fixes only) 53/66, v126 (fixes + walk home after six stuck hits) 57/63. Spell dodging via the version-36
  spell list (v127 all area strikes 58/62, v128 + heavy projectiles 55/65, v129 only 70+ damage strikes 67/53 then 121/119) saves deaths
  but not games; v130 (looser lane join) 57/63. v113 stays champion; v131 (prefer guaranteed last hits) is dueling. v113's ten-seat
  random-roster baseline is 138/240 = 0.575 (v76 0.496, v93 0.537), second in its batch behind nancy-goa:v1 0.596, ahead of black-kite 0.565.
  v131 (prefer guaranteed last hits) 57/63, dropped. The strong campers use items ~50x more often than we do, so v132 (keep an elixir
  stocked, drink at 70% HP, free slot) 59/60, dropped. v133 (short-range kite steps for Druid/Warlock) 65/55 with no change on the
  seats it touches, dropped. v134 (walk back to meet the creep wave instead of waiting outside a tower) opened 66/54 but its rule fires
  in 0.3% of samples, so that was noise too; its replication served as a second null calibration and read 108/132 (-24 over 240 for two
  identical policies). Promotion now needs >= +36 over 360 with both batches positive. v113 remains champion (league 30/47 in rounds 324-328; rank 4, 1536).
- Champion 00:56-03:36 UTC: v93 = `Jordan:v93` = v87 + keep farming footmen in basic range while travelling between lanes:
  64-56 then 136-104 vs v87 (200-160 over 360). Level or negative since: v95 focus fire 60/60, v96 two-ally dive 51/69 (vs v87); v97 61/59,
  v98 52/68 (vs v93). Running vs v93: v99 (no Red-only Crossbowman escort; first batch 66/54, replicating), v100 (never fight alone),
  v101 (level-aware fights) — all level or negative (v99 176-184 over 360, v100 55/65, v101 57/63). v93 ten-seat baseline 129/240
  (Red 60, Blue 69). League with v93: rounds 319-321 = 18/29, 1520 MMR, rank 8.
- Since 02:42 UTC: v102's hold rule turned out never to fire, which made its duel a null calibration: 69/48 then 112/127 vs an identical
  policy, so +-20 per batch is noise; the promotion rule is now >= +24 over >= 360 with both batches positive. Dropped: v103 (group follow
  for DH/VK/Druid) 60/60, v104/v105 (farm at the map centre first, local failures), v106 (crippled reset) 55/65, v109 (post-respawn hold)
  51/69, v110 (hold + wave ride) 57/63, v111 (boots first) 51/69. Running vs v93: v107 (chase kill shots; first batch 70/50, replicating),
  v112 (wave ride only), v113 (stutter-step kiting for ranged classes via selfAttackCooldown — the top two policies win 0.76-0.88 on the
  Ranger and Arcanist seats where we win 0.50-0.53).
- Champion 00:42-00:56 UTC: v87 = `Jordan:v87` = v76 + farm any enemy footman within 8 tiles (melee 6) instead of walking or
  waiting for a wave: 73-47 then 125-114 vs v76 (198-161 over 360). Our hero was level 1 until tick ~1500-1900 and died 4.7 times per game;
  v87 dies 3.5 times. Dueling v87: v90 (farm radius 10/8), v93 (farm while travelling); v91 (= v87 + death telemetry) ten-seat batch.

## Status at game version 33 (2026-09-15 18:20 UTC)
- **Engine change:** the league coworld is `cow_252fb6a6` (2026.9.15.1, game version 33): towers 1200/2400/4800 HP and 28/56/112 damage
  (ranges unchanged), hero/tower collision. 61% of league games time out (0 for everyone). Details in docs/ARENA_NOTES.md (top).
- **Champion:** v49a = `Jordan:v44` (promoted 18:13 UTC): tower-safe siege (out of range, footman cover, 2 allies, low tower, or late game),
  long-range kiting (Crossbowman out-ranges every tower), damage-first shop, lane commitment (no lane switch or rejoin), all-in from tick 12000.
  Local: a lone v49a Crossbowman beat nine base.bas heroes at tick 9665. Duel vs v30 (same games): 28 wins vs 20, 59 timeouts of 107.
- v30 (previous champion) won 9/41 league games on the new coworld; ladder rank 6, 1498 MMR after 42 rounds.
- Field on the new coworld (tools/field_behavior.py --coworld cow_252fb6a6): six entrants camp mid all game; red-kite, black-kite and daveey
  push side lanes and are the only ones who attack forts. Decisive games: first gate attack ~tick 10,000, 2-5 heroes at the fort.
- Duels vs v49a (120 shared games each; candidate wins / control wins / timeouts): v50 farm-when-idle 23/24/73 (wash),
  v51 join-allied-pusher 29/21/70 (+8, replication queued), v53 all-in from tick 4000 (running), v54 tower bait (running),
  v52 long-range damage shop: seat 1/2/6 batches 19/72 vs 17/72 and a slower local Crossbowman game (dropped).
- More duels vs v49a (candidate/control/timeouts per 120): v53 replication 23/18/79 (v53 total 46-34), v54 tower bait 24/25/71,
  v51 replication 32/27/61 (total 61-48), v55 = v51+v53 27/26/67, v56 = v55 all-in from tick 600 29/25/66. Nothing clears the noise
  floor (SE ~5 per 120), so v49a stays champion. v57 spell posts (Ranger/Arcanist/Lich hit towers with area spells from 7-8 tiles;
  verified: inner tower loses ~0.4 HP/tick) is in a caster-seat duel. Round 306, first with v49a: 1480 MMR, rank 7.
- **Game version 34 (~20:30 UTC):** towers 900/1200/1800 HP, 18/24/30 dmg; games decisive again. Duels vs v68 under v34 (120 each):
  v73 54/62, old diver v30 51/69, v49a 58/58, v74 (relaxed gating, all-in 6000) 56/62, v75 (fort at any distance) 65/47 then 112/121
  (level; promoted 21:47 UTC as `Jordan:v75`, kept). vs v75: v76 (fort rush once a gate is known dead) 64/54, v77 (defend own exposed
  fort) 64/56; v76 replication 65/53 (**129-107 over 240 -> promoted 22:48 UTC as `Jordan:v76`**); v78 = v76+v77 120/117 (parity, so the
  fort-defense rule is dropped). v68 ten-seat under v34: 100/240; v76 ten-seat 127/240. vs v76: v79 (stage near a dying gate) 67/53 then 119/121 (parity),
  v80 (boots first) 62/58 (parity). Round 314: 1540 (rank 5); round 315: 1511 (rank 7).
- Labels equal file numbers from v66 on (byte-unique copies of v66-v70 uploaded in order; earlier: v50=:v45 ... v65=:v60, v68 also =:v63).
- **Champion since 20:29 UTC: v68 = `Jordan:v68`** (also uploaded earlier as :v63) (v62 + Red non-Crossbowman heroes escort the allied Crossbowman; 102-85 vs v62 over 360
  shared games). Before that (19:17 UTC): v62 = `Jordan:v57` (v51 + switch to the lane whose enemy towers have the least remaining HP from tick 6000;
  33-21 vs v51 over 120 shared games, replication running). Before that (19:00 UTC): v51 = `Jordan:v46` (v49a + join an allied side-lane push): three duel batches vs v49a 29/21, 32/27, 30/18
  = 91 wins vs 66 over 360 shared games. v58 buddy-the-deepest-ally 20/25 (dropped). v59 Crossbowman survival in seat-1 batches.
- Since then (candidate/control per 120 shared games): v62 weakest-lane replication 30/35 (v62 total 63-56 over 240; kept as base),
  v63 join-mid-brawl 17/27 (dropped), v64 opportunistic tower spells no signal, v65 (weakest-lane check from tick 3000, 20% margin)
  39/26 then 32/31 vs v62 and 35/36 vs v51 (parity), v66 (more switching) 23/33 vs v62, v67 (tunnel-vision dives) 25/39 vs v62.
  Lesson: lane commitment plus fighting adjacent heroes during dives both matter; v62 stays champion (round 308: 1501 MMR, rank 7).
- Labels: v50=:v45 ... v59=:v54, v60=:v55, v61=:v56, v62=:v57, v63=:v58, v64=:v59, v65=:v60, v66=:v61.

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
