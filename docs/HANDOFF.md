# HANDOFF — Gods of the Arena policy project (resumed 2026-09-16, 02:42 UTC)

## WHERE THIS STANDS (2026-09-16 04:50 UTC) — read this first
- **Champion: v148 = `Jordan:v148`** (submitted 17:05 UTC 2026-09-16 for GAME VERSION 37; ladder label confirmed 17:26 UTC; first league
  round 349 = 6/9, MMR 1514 -> 1532; round 350 = 2/8 -> 1506; round 351 = 5/8 -> 1515, rank 6; the leaders are sliding under version 37:
  relh 1579, khors 1576, richard 1567 at 18:33 UTC, only 64 points ahead). An emergency fix: every
  earlier version parks on dead tower coordinates until the timeout because version 37 no longer lists dead buildings). v148 = v139 +
  (v147) all building-targeted walks stop 3 tiles short of the building and no walk is issued within 4 tiles of a building objective
  (act 23) + a building objective that is missing from the object list while we stand within 4 tiles counts as dead (DEADOBJ; sets
  routeDead/laneTowerHp). Local seed-2026 on the new coworld: Ranger WON 7727 / 2 deaths / 0 STUCK (v139: TIMEOUT 28800 / 7 deaths /
  318 STUCK), DK WON 14074 / 4 deaths / 7 STUCK (v139: LOST 16088 / 74 STUCK). Hosted: `duel-v148-v139` (240) queued behind
  `v139-seats-v37` and `duel-v139-v113-v37` (both broken versions — they only measure the damage: v139 ten-seat 83/240 = 0.346 on
  version 37; v139 vs v113 77/172 with 17 timeouts). **v148 vs v139 duel: 174/240 = 0.725** (Xbow 23/24, Ranger 21/24, Druid 21/24,
  DH 19/24, DK 17/24, Lich 17/24, Arcanist 17/24, VK 14/24, Warlock 13/24, Berserk 12/24; STUCK 1.3/game, 6 timeouts/240, median
  game ~7900 ticks). **v148 ten-seat baseline on version 37 (17:29 UTC): 156/240 = 0.650** — Red 80/120 (DK 12, Xbow 19, Lich 14,
  Warlock 18, Berserk 17 of 24), Blue 76/120 (VK 14, Ranger 19, Arcanist 16, Druid 15, DH 12); STUCK 0-4/game; deaths Berserk 4.7,
  DH 4.8, DK 4.4 (6.5 in its losses, which last ~13600 ticks), Druid 5.2; DK tower kills 3.9/game. Red is now our stronger side (the
  version-37 buffs went to Crossbowman/Berserker/Lich). Caveat: part of the field may still be broken on version 37 (policies that
  wait to see a tower at 0 HP), so the baseline will drift as others fix theirs. Field on version 37 (tools/roster_stats.py over the
  480 v148 games): aaron-gota-ir-cadence-all 0.57 (new), gota-codex-objective-lanes 0.55, relh:v129 0.54, codex-secondary 0.53,
  richard:v50 0.49, nancy 0.48, khors 0.46, red-kite 0.44, games-bond 0.43, black-kite:v11 0.40 (was 0.575 — broken or weakened),
  Red side 0.48 league-wide in these games. Version-37 game structure (tools/replay_lanes.py on the v148 baseline, parser now accepts
  replay game version 40): winner's first gate attack median 3240 ticks (v36 ~4900), first fort attack 6406 (8037), game end 7197
  (8428) — the 6-creep waves melt towers; 3-5 heroes at the winning fort in 195/240; our hero hits the enemy fort in 156/156 wins;
  when we lose the enemy breaks mid in 42/84. Melee deaths under v37: DH median tick 4451 and VK 6783 while walking (58-62% of
  their time, ride rule only 4-6%), DK/Berserk late in mid/jungle (fort approach / escort). Creep probe (tmp/probe_creeps2.bas, seed
  2026): version-37 creeps on lanes 0 and 2 stay inside the ride rule's lane bands (x <= 13 or y <= 17; x >= 102 or y >= 98) for both
  sides — the lane test needs no change. Plan (17:50 UTC): let v148 accumulate rounds while the field is broken (black-kite 0.40),
  review v148's league record by class at ~19:50 UTC and repeat the ten-seat baseline at ~20:50 UTC to measure the field's adaptation;
  first tuning candidates for version 37 only with a strong hypothesis (laneTowerHp defaults 950/1300/1950 go into the next one).
  **User request 18:00 UTC: keep XP requests in flight at all times** (memory gota-xp-always-in-flight). Queue since then:
  `null-v148-v37` (v148 vs v148, 240 — noise calibration for version 37), `duel-v149-v148` (480; v149 = v148 + tower HP defaults
  950/1300/1950 + escort off; smoke Lich won 12565 / 2 deaths / 0 stuck — **result 240/480 = 0.500, pair sums cancel (Red rows 135/240,
  Blue rows 105/240: Red wins 56% of our mirrored games under v37); dropped**), `duel-v150-v148` (240; v150 = v148 + S47 barracks endgame:
  attack an exposed enemy barracks instead of a solo fort dive against >= 2 defenders and when idle within 12 tiles; smoke Ranger won
  7904, rules did not trigger locally — **result 114/240 = 0.475 (-12), BARR fired in 23/240 logs, act 56 rare; dropped**). Then: replications of anything positive, repeat baseline.
  **`null-v148-v37` is INVALID**: the platform merges identical policy versions in one roster into a single policy_stats entry (our
  policy appeared once, reward 0.5, nine entries), so `report` read other seats (it printed Red 239/240). Never duel a version against
  itself; calibrate with two byte-identical files under different labels (v151 = v148 re-uploaded). **`null-v151-v148` read 106/240 =
  0.442 (-28); `null-v151-v148-2` 117/240 = 0.487 (-3); caster seats `null-casters-v151-v148` (seats 2,3 x 60) 122/240 = 0.508 (+2).
  The noise band on version 37 is about +-28 per 240 games; keep the +36/360 two-batch bar.** Engine
  head moved again at ~17:55 UTC: 6ee8642 "Put creeps on the correct sides and make Radiant soldiers larger" — graphics only
  (assets.nim/graphics.nim), league coworld still cow_dd6ceed6. v152 (:v152) = v148 with the melee farm radius 8 tiles (6-creep waves),
  melee-seat duel vs v148 queued (`duel-v152-v148`, 240) — **result 117/240 = 0.487 (-6; DK/VK pair 57/120, Berserk/DH 60/120): level,
  dropped; the pre-queued replication `duel-v152-v148-2` read 118/240 (-2): combined 235/480, level.** v153 (:v153) = v148 with Blue pushing physical lane 2 (clash = 1): fair
  Blue-seat test under version 37 — `v153-blue` (seats 5-9 x 48 = 240) vs a concurrent `v148-blue` (240); compare the two Blue rates.
- **VERSION-37 LEAGUE STRUCTURE (52 games, rounds 345-350, tools/league_replays.py --coworld cow_dd6ceed6): Red wins 0.62 (v36: 0.36)**;
  game end median 8279, winner's first gate attack 4896, breakthrough lanes mid 25 / lane 0 16 / lane 2 11; winning fort attackers are
  led by Xbow 22, Warlock 21, Lich 19, DK 18 (the buffed Red classes). Our split in those games: Red 13/25, **Blue 8/27** — Blue is where
  we lose now. Blue-seat candidates get fair random-roster tests against the concurrent `v148-blue` baseline: v153 (Blue lane 2) and
  v154 (Blue mid, pushLane 1). League logs of v148's 17 games: no timeouts, stuck 0-7, several games ending by tick 2400-3800.
  **Blue-seat results (240 games each, concurrent): v153 lane 2 137/240 = 0.571, v148 lane 0 (baseline) 132/240 = 0.550, v154 mid
  126/240 = 0.525 — all within the +-28 noise band: Blue lane choice is closed under version 37; v153/v154 dropped.** Queue after
  this: `duel-v152-v148` (melee farm radius 8, 240), `duel-v155-v148` + `-2` (melee-package ablation, 2 x 240), `null-v151-v148-2`,
  `v148-seats-b` (second ten-seat baseline for field drift).
  Blue telemetry under version 37 (v148 Blue baseline, 48 games per class): VK 20/48 with 6.6 deaths, DH 26/48 / 6.0, Druid 28/48 /
  5.3, Arcanist 26/48 / 4.0, Ranger 32/48 / 2.7; deaths come while walking (act 9: DH 147 of 290, VK 98 of 317) in mid/jungle and
  the enemy corner; level at tick 2400 only 2.3-2.8 for VK/DH/Druid. Same mid death march as Red melee (DK 72/105 in mid/jungle).
  Candidate v156 (S48, Codex): walk out via a point 4 tiles short of our own outer tower when the objective is beyond the enemy outer
  (VIA, act 58) — the single-waypoint version of v137's lane-hugging without queuing behind waves; test on all seats, 480 games.
  v156 smoke: Ranger fine but the rule re-fires after the waypoint (the "behind our outer tower" test stays true for a few tiles) —
  DK oscillated to a 28800 timeout with 11 deaths. v157 (:v157, per-life viaReached flag) still timed out as DK (14 deaths, VIA 26):
  the waypoint 4 tiles from the outer tower toward home can be unreachable, so "reached" never fires. v158 = v157 + reached within
  5 tiles + a 1200-tick per-life deadline (viaDeadline) — smoke: DK won 24877 with 13 deaths (v148: 14074 / 4), Ranger won 12245 with 6
  deaths (v148: 7727 / 2); the lane-0 waypoint (24,11) is unreachable and the detour costs tempo. **VIA family v156-v158 dropped, not
  dueled**; v156-v158 uploaded for label order only. v159 (:v159) = v148 + objective reset to our own outer tower on respawn
  (oi = 2): local DK won 16433 / 6 deaths, Ranger won 25830 / 12 deaths (v148: 14074 / 4 and 7727 / 2) — after each death the hero
  re-walks every dead tower position to re-infer it dead; dropped, uploaded for label order. **Lesson: three attempts to re-route the
  respawn walk-out (v137 footman anchor, v156-v158 waypoint, v159 objective reset) all cost more tempo than the mid deaths they avoid;
  stop pursuing this thread without a fundamentally different mechanism.** Trace of version-37 fillers (720 cached episodes):
  khors:v1 camps (58,58) with 3620 footman + 2643 hero commands and 803 walks per game (a pure mid farmer/fighter), codex-objective-lanes
  pushes P2 0.54 / P0 0.27; our v148 pushes P2 0.91 with first tower attack at 996 (theirs 1084-1240). Next candidate (S49, Codex):
  v160 = v148 + Druid support — the Druid's Healing Bloom (55) and Kindred Wisps (80) are auto-cast on damaged allies in range, so it
  stays within 5 tiles of the nearest allied hero when it has nothing better to do (SUP, act 59); test on seat 3 (`--seats 3 -n 120`,
  Warlock rows are a null). Also queued: `v148-blue-2` (second Blue baseline, 240). **v160 smoke (Druid vs nine base.bas): TIMEOUT
  28800, 9 deaths, 60 stuck, SUP 38 — it glued itself to the mid-camping base heroes and never pushed; with camping teammates
  (khors, base) in the league the same happens. Dropped, not dueled (uploaded for label order).** Support/follow rules join the
  "passive loses tempo" list. Round 352: 4/9 (v148 league 17/34 over rounds 349-352), rank 6 at 1518, leader relh 1592.
  **Melee-package ablation under version 37: v155 (v113 + hotfixes, no package) vs v148 on melee seats: 109/240 (-22) and 116/240 (-4) =
  225/480 (-30)** — the package is worth ~+30/480 on version 37 as it was on 36; v148 keeps it. Queued: `v148-red` (Red-seat baseline,
  240) to pair with the Blue baselines for side-specific tests. `v148-blue-2`: 136/240 = 0.567 (first Blue baseline 0.550) — v148 as
  Blue sits at ~0.56 in random rosters (`v148-blue-3`: 131/240 = 0.546; Blue over 720 games 0.554). v161 (:v161) = v148 + melee back-off when alone against >= 2 enemy heroes (S46 re-test under
  version 37): smoke DK won 13025 / 2 deaths / OUTN 4 (v148: 14074 / 4); melee-seat duel vs v148 queued (`duel-v161-v148`, 240, plus a
  pre-queued second batch `-2`). **v161: 120/240 then 111/240 = 231/480 (-18) — level/negative, dropped (same as v145 on version 36).** `v148-red`: 152/240 = 0.633 — v148 is ~0.63 as Red and ~0.56 as Blue in random rosters (side gap
  durable); **third ten-seat baseline `v148-seats-c` (19:07 UTC): 146/240 = 0.608 (Red 79/120, Blue 67/120)** — sequence 0.650,
  0.575, 0.608; field in that batch: aaron-cadence 0.575, relh:v133 0.558, codex-objective 0.537, richard:v59 (new) 0.524, khors 0.50,
  black-kite 0.45, games-bond 0.43; v148 is still the strongest entrant in random rosters. **Second v148 ten-seat baseline (`v148-seats-b`, 18:45 UTC): 138/240 = 0.575 (first 0.650)** — the field adapted
  within two hours: khors 0.58, aaron-cadence 0.58, relh:v133 0.56, codex-objective 0.56, richard 0.49, red-kite 0.39; Red wins 0.55
  of these games. Our weakest seats now DH 8/24, Warlock 9/24, VK 10/24, Druid 12/24.
  Next: ten-seat baseline for v148 DONE;
  then re-tune for version 37 (3x creeps, barracks, bigger towers).
- Previous champion v139 = `Jordan:v139` (08:45-17:40 UTC; game version 36). **Rank 2 at 1589 MMR after round
  338 (11:40 UTC; richard 1658, black-kite 1574).** v139 league record 35/53 = 0.66 (Red 16/25 = 0.64, Blue 19/28 = 0.68; v113 was 0.59
  with Red 0.42): rounds 333-338 = 6/10, 4/8, 4/8, 6/9, 8/9, 7/9. By class so far: Warlock 9/9, Ranger 6/6, Druid 5/8, DH 4/7, Lich 3/5,
  Arcanist 3/5, Berserk 2/6, DK 2/4, VK 1/2, Xbow 0/1 — melee 9/19 (v113 35/66), too few games to judge the melee seats yet.
  **14:00 UTC review (rounds 333-342, 90 games): v139 56/90 = 0.62, Red 25/43 = 0.58, Blue 31/47 = 0.66** (v113: 0.59 / Red 0.42 /
  Blue 0.72). Rounds 339-342: 3/9, 8/10, 5/9, 5/9. By class: Warlock 11/12, Arcanist 8/10, Ranger 6/6, Druid 9/13, DK 5/8, Lich 4/8,
  DH 5/11, Berserk 5/13, VK 3/7, Xbow 0/2 — melee 18/39 = 0.46 (v113 league 0.53): the league melee seats are not visibly better yet,
  the Red side is; keep v139 (duel + baseline evidence) and re-review at ~17:00 UTC. Rank 2 at 1582 (richard 1621, Games Bond 1561,
  black-kite 1547). Engine repo head moved to 46ce535 (one-line HTML report tweak; league coworld unchanged, nothing to re-verify). v139 = v113 +
  melee package (Codex S41/S43): melee heroes last-hit before hitting a healthy tower, open on enemy heroes only when adjacent /
  nearly dead / with an ally within 8 tiles, and never run ahead of their lane's front footman toward a standing enemy tower (RIDE,
  act 47; hold 49/50 when the lane has no footman). Evidence: melee-seat duels vs v113 133/240 (+26) and 122/240 (+4) = 255/480
  (+30, both positive; Berserk/DH pair +24, DK/VK pair +6), plus the earlier v135 variant of the same mechanism +12/120; hosted
  telemetry: melee deaths down 25-40% (Berserk 5.0 -> 3.1, VK 6.3 -> 3.8), levels ~unchanged, hero kills slightly down. Ranged code
  is byte-identical to v113. This is BELOW the +36/360 bar — promoted on the consistency of three positive batches and the zero
  ranged risk; if the league's melee seats (Berserk/DH/DK/VK) do not improve over the next ~10 rounds, revert to v113.
  Previous champion v113 (promoted 03:36 UTC). Lineage of confirmed gains on game version 36, all by mirrored-seat duels:
  v76 -> v87 (farm any enemy footman within 8 tiles instead of walking/waiting, 198-161 over 360) -> v93 (also farm while travelling
  between lanes, 200-160 over 360) -> v113 (stutter-step kiting for ranged classes via selfAttackCooldown, 207-153 over 360).
  Ladder: rank 4, 1536 MMR (06:15 UTC; round 327 was 2/9, round 328 10/10), up from rank 9 / 1482 at 01:16 UTC; league rounds with v113
  (324-328): 30/47. Random-roster
  baseline 0.575 (v76 0.496, v93 0.537), second in its batch behind nancy-goa:v1 0.596 and ahead of black-kite 0.565.
- **Promotion rule:** combined >= +36 over >= 360 shared games with both batches positive (two null duels of identical policies read
  +21/-15 and +12/-24 per batch, so +-25 per 240 games is noise). Always confirm a new rule fires in the hosted logs (tools/log_stats.py) first.
- **Tried on top of v113 and level or negative (16 candidates):** wider kite trigger, range-advantage kiting, melee anti-kite, escort
  variants, free elixir slot, melee flee at 40%, melee farm radius, road-following via route points (harmful), the Codex audit's fix bundle,
  stuck escalation, spell dodging (saves ~0.5 deaths/game, wins level). Passive/safety rules lose tempo; only added productive actions won.
- **Structural facts:** Blue-side classes (VK/Ranger/Arcanist/Druid/DH) win 0.71-0.88 for us, Red-side (DK/Xbow/Lich/Warlock/Berserk)
  0.29-0.58; the best opponents show the same Red weakness in shared games. Games end ~tick 8000; deaths cost ~800 ticks each; our hero
  walks 39% of the time, farms 14.5%, sieges 13.5%. Heroes snag 6 times per game on long walks (route points are tower centres — never
  walkTo a tower position).
- **Git:** commit as you go AND push to the remote (`git push origin main`, github.com/johomax/johomax_gota) after every commit or at
  least every 20 minutes — requested by the user 2026-09-16 05:32 UTC.
- **Tools:** duels `tools/xp_mixed.py duel CAND CTRL --seats 0-4 -n 12|24 --tag t`, report `tools/xp_mixed.py report xp/t.json`,
  telemetry `tools/log_stats.py xp/t.json` (act share, deaths, DEATH POSITIONS), replays `tools/replay_lanes.py`, `tools/policy_trace.py
  --ids --exact --by-class`, fillers `tools/roster_stats.py`, ladder `tools/ladder.py`, engine/coworld drift `tools/coworld_check.py`.
  Upload every policy file once, in numeric order (`uv run coworld upload-policy --file policy/vNNN.bas --tag version=vNNN`), so the
  platform label equals the file number; smoke-test Codex output locally first (blank line before `end if`/`wend` is a compile error).
- **RESUMED 17:03 UTC 2026-09-16 — REGIME CHANGE: league coworld is now `cow_dd6ceed6-9188-4eaa-9099-03aefcd1e5fe` (game version
  2026.9.16.2, engine 5c701f9 "Buff red heroes and tune towers" + "Simplify GotA paths and creep waves").** Facts so far (engine diff):
  barracks are buildings (object kind 5, ids 40+, 2 per lane per team, 950 HP, no attack, attackable once the lane's towers are dead);
  creeps spawn 3 per living barracks (6 per lane per team, was 2) with unit cap 360; towers 950/1300/1950 HP (damage 18/24/30
  unchanged) and footprints 1.05/1.25/1.65 tiles (was 0.42/0.55/0.70); Crossbowman 46 dmg (+9/lvl), Berserker 38 (+8), Ice Spear
  48 dmg / 6.67 tiles, Aether Siphon 30, Lion Guard 36; terrainWalkable now returns only KNOWN walkable cells (fog); fort exposure
  unchanged. Our rounds 345-348: 5/9, 0/9, 4/8, 4/9 -> rank 6 at 1514. Local v139 DK on the new coworld: LOST at 16088 with 74 STUCK
  events (parked at the enemy outer tower centre for 2400 ticks) — objective walks aim at tower centres and the bigger footprints snag
  them. Hotfix in progress: v147 = v139 with objective/flee walks stopping 3 tiles short of tower objectives. Hosted re-measurement
  queued under the new coworld: `v139-seats-v37` (240) and `duel-v139-v113-v37` (240).
- PAUSED by the user at ~14:05 UTC 2026-09-16 ("Stop for now"). Champion v139; rank 2 at 1582. All background loops
  (monitor, git pusher, scheduled 17:00 league review) were stopped at the user's request at ~15:06 UTC; nothing runs unattended.
  On resume: restart the 30-min monitor and the 20-min pusher, then run `tools/league_logs.py --only-version 139` after
  `tools/league_data.py --rounds 20`), compare v139's melee seats with v113's league record, then continue from the ideas list below.
- **In flight (10:10 UTC):** `duel-v146-v139` (480 games, all seats): v146 = v139 + Blue pushes physical lane 2 + no Crossbowman
  escort + ride walks off stuck detection — a bundle of three changes that read level-to-positive alone (+5/240 Blue, +8/480, hygiene).
  Promote only if >= +36 over 480 and no class row collapses. Today's conclusions: (1) the melee package (v139) is the only gain of
  the day (+30/480 duels, baseline 0.575 -> 0.625); (2) every defensive/safety rule loses tempo (v144 gate defence -20, v145 back-off
  when outnumbered -6, spell dodge, hold at home); (3) the caster wave-bound rule and the all-class movement rule are level or negative;
  (4) the league seats higher-rated players on Blue and Red wins only 0.36 league-wide, so our Red games decide the climb and the
  leaders' win rates are partly seat luck; (5) single rule tweaks are below the +-25/240 noise floor — use class-restricted duels
  (`--seats 0,4` melee, `2,3` casters) or 480+ games. Tools added today: tools/league_logs.py (league telemetry from private logs).
  Monitor: 30-min loop (coworld, ladder, rounds -> tmp/monitor2.log); git pusher every 20 min.
- **Detailed log of today's candidates (v135-v146), oldest first:** S39 melee wave-rider = v135 (Codex task-mu3sicj1-pbpo2i, spec docs/tasks/s39_melee_wave_rider.md).
  Why: clean per-class baseline (xp/v113-seats.json, 24 games each) Ranger 0.83 / Xbow 0.88 / Druid 0.71 / DH 0.58 / Lich 0.54 /
  Arcanist 0.50 / Warlock 0.50 / DK 0.46 / VK 0.42 / Berserk 0.33 — the earlier "Blue side dominance" was a duel artefact (mirrored
  copies face each other); the real gap is the melee classes. black-kite:v11 wins DK 0.53 / VK 0.55 / Berserk 0.59 / DH 0.56 with the
  same classes (1642 random-roster games). Replays: our melee heroes walk straight to the enemy outer tower (median first tower attack
  ~1100 ticks vs black-kite ~2400), siege at level 1, push on alone to the inner tower and die 4-6 times per game (act 9 precedes most
  deaths); they farm 9-15% of the time (act 4) and issue half as many footman attacks (DK 757/game vs 1716). v135: melee farm before
  siege, siege a healthy tower only with >= 2 footmen soaking, open on heroes only when adjacent/nearly dead/with an ally, and never
  run ahead of the front allied footman toward a standing enemy tower (RIDE, act 47). Test on melee seats only:
  `duel v135 v113 --seats 0,4 -n 30` (120 games, all DK/VK/Berserk/DH). Rounds 329: 4/8, 330: 2/8 (rank 5, 1514 MMR at 07:55 UTC;
  the two Berserker and two Lich seats all lost).
  v135 (:v135) smoke (seed 2026 vs nine base.bas): Berserk won 9332 / 1 death / farm share 42% (v113: 7022 / 1 / 21%); DK won 9382 /
  1 death but sat at level 1 beside the enemy outer tower for 3000 ticks (the two-footman gate delayed the tower kill v113 got at
  1784) and still died alone at the inner tower (ride needed tower sight + a footman within 30 tiles). Dueling anyway on melee
  seats (`duel-v135-v113`, 120 games). v136 (S40: gate restored, farm-first within 3 tiles, hold when no footman near) smoke: Berserk
  won 5061 / 1 death (best yet) but DK LOST 7683 with 7 deaths — hold fired at spawn, and the diagonal death march through mid
  continued because mid-lane footmen counted as the wave. Not uploaded/tested. v137 (S41) = v113 + lane-aware wave discipline only
  (front footman of OUR lane by a physical lane test; walk to it when ahead of it or > 20 tiles behind; hold when the lane has no
  footman; act 47 in stuck detection).
  **v135 duel result (melee seats, 120 games, done 08:25 UTC): 66/120 = 0.550 (+12, noise-level)** — DK 17/30, Berserk 20/30, VK 10/30,
  DH 19/30. Telemetry vs the v113 baseline: deaths halved (Berserk 5.0 -> 2.0, DK 4.2 -> 2.9, VK 6.3 -> 3.3) but levels fell (Berserk
  5.3 -> 3.8, DK 4.6 -> 4.2) and VK stuck events rose to 20/game: fewer deaths bought with passivity. The hosted queue currently
  finishes 120 games in ~25 minutes, so 240-game batches are affordable.
  **v137 (:v137) smoke, seed 2026 vs nine base.bas: DK WON 6003 / 1 death / tower kill 1907 (v113: 12973 / 5 deaths); Berserk WON 4564 /
  0 deaths / tower kill 1696 (v113: 7022 / 1).** RIDE targets hug the lane ((105,101), (76,99), (57,100)); no HOLDW needed. Dueling
  v113 on melee seats, 240 games (`duel-v137-v113`, seats 0,4 x 60). **Result 114/237 = 0.481 (level, dropped)**: DK 28/60, Berserk
  21/60, VK 30/60, DH 35/57. Its "walk to the front footman when > 20 tiles behind" makes heroes queue behind their own waves in the
  lane (STUCK prints every ~30 ticks while crawling at wave speed). v135's Berserk/DH pair was 39/60 vs v137's 56/117, so v135's
  combat rules (melee farm-first, melee hero-chase gate) look like the useful part.
  v138 (:v138, S42) = v137 with the movement rule for ranged classes too — smoke Warlock won 6724 / 1 death (v113 11247 / 2), Arcanist
  won 7815 / 2 deaths (v113 14507 / 3) — dueling v113 on all seats (`duel-v138-v113`, 240 games). v139 (:v139, S43) = v137 minus the
  far catch-up trigger plus v135's two melee combat rules — smoke DK won 5737 / 1 death, Berserk 5324 / 1 — dueling v113 on melee
  seats (`duel-v139-v113`, 240 games). Time check: it is ~08:10 UTC; the hosted queue finishes 240 games in ~25-30 minutes.
  **v138 result 115/240 = 0.479 (-10, dropped)**: Xbow 8/24, Ranger 9/24, Lich 5/24, Warlock 7/24 — the movement rule hurts every ranged
  class (queuing behind waves, walking back from safe range); Arcanist 13/24, Druid 15/24, VK 16/24 fine. Movement discipline stays
  melee-only if anywhere. Baseline structure (tools/replay_lanes.py on xp/v113-seats.json, 240 games): winner's breakthrough lane is
  evenly split (82/83/75), 3-4 heroes hit the winning gate in 80% of games, our hero is at the breakthrough gate in 74% of our wins;
  when we lose the enemy breaks mid in 44/102. Early-game predictors of our win: carries 0 deaths by tick 3000 -> 0.94 (2+ -> 0.33),
  casters 0 -> 0.62 / 1 -> 0.50 / 2+ -> 0.38, level 1 at tick 1920 -> 0.45 for casters; for melee nothing early predicts the result
  (they are passengers), which caps what melee work can deliver.
  **v139 first batch 133/240 = 0.554 (+26; DK 31/60, Berserk 31/60, VK 31/60, DH 40/60; both pairs positive)** — above the +-25 noise
  band, below the promotion bar. Telemetry (60 games/class): deaths Berserk 3.1 (v113 5.0), DK 2.9 (4.2), VK 3.8 (6.3), DH 3.8 (5.5);
  levels ~4.5-4.7 (v113 4.6-5.5); hero kills slightly down; stuck prints 14-22/game (act-47 walks queued behind waves). Replication
  queued (`duel-v139-v113-2`, 240 games); promote if combined >= +36 over 480 with the replication positive.
  v140 (:v140) = v113 with `clash = 1` (Blue pushes physical lane 2 too — black-kite's lane from both sides; v86 tested "other side
  lane" for BOTH sides at parity, so a Blue-only change is untested). Smoke ok (Blue Ranger INIT lane 2). Dueling v113 on all seats,
  480 games (`duel-v140-v113`); only the candidate-as-Blue rows (s5-s9) carry signal, the Red half is a null.
  **v140 duel result 240/480 = 0.500 exactly** (Blue rows 120/240: VK 24/48, Ranger 16/48, Arcanist 29/48, Druid 24/48, DH ~27/48) —
  but this design is biased: the Blue candidate meets our own v113 Red hero head-on in the same physical lane (Ranger vs the
  longer-ranged Crossbowman), which never happens in league games. Fair test queued: random-roster Blue seats, v140 vs a concurrent
  v113 baseline (`create ... --seats 5-9 -n 48`, tags `v140-blue` / `v113-blue`, 240 games each); compare the two Blue win rates.
  **Result: v140 Blue 152/240 = 0.633 (VK 29, Ranger 38, Arcanist 29, Druid 33, DH 23 of 48) vs v113 Blue 147/240 = 0.613 — level
  (+5, SE of the difference ~0.044). Lane choice for Blue is closed: dropped.** Round 333 (first with v139): 6/10 (Berserk 0/2, DH 1/3,
  Warlock 2/2, Druid/Lich/VK won); rank 4, 1544. Round 334: 4/8 (DK 1/2, Druid 1/2, Ranger W, Warlock W; DH, Lich L) -> rank 5, 1537;
  v139 league record 10/18 after two rounds. Round 335: 4/8 (Berserk W, Warlock 2/2, Druid 1/3; Arcanist, Xbow L) -> v139 14/26; rank 4,
  1532 — richard 1619 and black-kite 1609 both fell ~25 this round, the top three are within 90 points.
  v141 (:v141, S44) = v139 + the wave-bound rule for Arcanist/Lich/Warlock (Ranger/Xbow/Druid unchanged): smoke Warlock won 6724 /
  1 death, Arcanist 7908 / 2 deaths / 11 stuck (v138's far trigger caused its 40). **Dueled v139 on caster seats (`--seats 2,3 -n 60`,
  240 games): 125/240 = 0.521 — Lich/Arcanist pair 55/120 (-5), Warlock/Druid pair 70/120 (+10): level, dropped.** The wave-bound
  movement rule helps melee only.
- **LEAGUE STRUCTURE (20 rounds, 190 games, tools/league_data.py --rounds 20 + new tools/league_logs.py, 09:00 UTC):** Red wins only
  0.36 of league games (XP random rosters: 0.44). Seating is not uniform: Blue seats hold the higher-rated players in 120/165 games
  (mean current MMR Red 1512 / Blue 1534); black-kite sits Blue in 86/110 games, daveey-2 98/126, docxology 72/97, richard 105/164,
  us 98/190, while Aaron/Andre von Houck/Alex Smith sit Red ~70%. So the leaders' league win rates (black-kite 0.69, codex-secondary
  0.70) are partly seat luck, and the whole field loses on Red (black-kite 0.58 on Red in 24 games, richard 0.42, us 0.40 in 92).
  Our league record by side: Red 0.42 / Blue 0.72; by class Berserk 0.18 (17), Lich 0.23 (13), Warlock 0.46, DK 0.65, VK 0.60,
  DH 0.71, Druid 0.67, Ranger 0.82, Arcanist 0.77, Xbow 0.75. Our league win rate with/against entrants: against richard 5/20,
  black-kite 12/33, games-bond 7/20, codex-secondary 12/31; against nancy 19/23, red-kite 23/29, aaron 31/36, base 31/41; with
  aaron 8/30. In league games deaths do not separate wins from losses (4.2 vs 4.4 per game) but hero kills (4.3 vs 2.8) and level
  (6.1 vs 5.3) do. Private policy logs ARE available for league episodes (`get_episode_request_policy_log(ereq, my_pv, seat)`);
  cache in tmp/league_log_cache.json. Seating by in-game rating rank (current MMR as proxy, 139 games): P(Blue) rank1 0.82, rank2
  0.50, rank3 0.22, rank4 0.71, rank5 0.45, ..., rank9 0.19 — looks like a greedy MMR-balancing draft (the top-rated player goes
  Blue, the next two Red, ...), so being #1 brings the 64% side most of the time and #2/#3 are punished. NOTE: `tools/league_data.py` overwrites docs/league_episodes.json — monitors must pass
  `--out tmp/league_recent.json` (the 30-min monitor now does).
  League-log class detail (v87-v113, 13-20 games per class): level at tick 1920 / 3840 — Ranger 2.7 / 5.0, DK 1.9 / 2.8, Berserk
  1.5 / 2.7, Warlock 1.4 / 2.3, Lich 1.3 / 2.8. Berserk (3/17 wins) dies only 2.9 times per game with its first death at median tick
  9371 — its problem is being useless, not dying: 15% of samples waiting for a wave (act 22), 14% escorting the Crossbowman (act 35),
  10% farming. Lich (3/13): 1.8 deaths, level 2.8 at 3840, 16% escorting. The Red-side early game (first 2000 ticks at level 1) is the
  open problem; class-restricted duels (`--seats 2,3` for casters, `0,4` for melee) are the way to measure it.
  **Escort finding (league logs, 63 Red non-Xbow games): ESCORT fires in 61/63 games, median first at tick 1680 (level 1).** Games with
  escorting before tick 2400 (39): win 0.36, level 1.38 at 1920 / 2.32 at 3840; without (24): 0.46, 1.83 / 3.27. v142 (:v142) = v139
  with the escort disabled (`escortOn = 0`); smoke Lich won 6960 / 1 death / 0 ESCORT. Dueling v139 on seats 0-4 x 48 = 480 games
  (`duel-v142-v139`): only the candidate-as-Red rows (s0-s4, 240 games) carry signal, the Blue rows are a null (Blue never escorts).
  v117/v118 (escort limits) read level on all seats in 120 games each — too insensitive for a Red-only effect.
  **v142 result 248/480 = 0.517: Red rows (candidate as Red) 115/240 = 0.479; mirrored-pair effects DK 0, Xbow +2, Lich +1, Warlock
  +3, Berserk +2 = +8/480 — level, dropped.** The escort correlation was confounded. Tally today: v135-v142 tested, only the melee
  package (v139) gained. Early-game act mix in league games (ticks 0-2400): Red DK/Lich/Warlock/Berserk walk 37%, escort 19%, wait
  for wave 13%, siege 10%, farm 7%, first tower/hero reward at median tick 3343, 29/63 still level 1 at tick 2400; Ranger walks 44%,
  sieges 30%, farms 16%, first reward at 1250, level 3-4 at 2400. Blue's DPS classes kill the forward outer tower a full wave earlier.
- **Gate phase is the decisive phase (09:40 UTC):** baseline replays — in our losses our team attacked the enemy gate in 75% of games
  (their fort in 15%); in our wins the enemy attacked our gate in 69%; median 3700-3900 ticks from the first gate hit to the end
  (winner's first gate attack ~4900-5900, game end ~8400-9700). During the enemy-gate phase our hero walks 36% / sieges 8% in wins vs
  walks 47% / sieges 3% in losses (2.1 deaths in that phase either way). League replays (171 v36 games): Blue wins 0.65; breakthrough
  lanes 63/65/43; 3-5 heroes at the winning fort; long-range class among fort attackers in 130/171. Candidate: v143 (S45, Codex) =
  v139 + race-aware gate defence (hold our own gate under its tower while enemy heroes + a wave siege it and the enemy gate in our
  lane still has > 900 HP; DEF prints, acts 51/52). v143 (:v143) died at tick 1 in the smoke test: `defLane >= 0 and gateAlive(defLane)`
  still evaluates the array at -1 (NO short-circuit evaluation — nest such checks). v144 (:v144) = v143 with the check nested: smoke
  DK identical to v139 (5737 / 1 death, no errors; DEF does not trigger against nine base.bas). Dueling v139 on all seats, 240 games
  (`duel-v144-v139`). **Result 110/240 = 0.458 (-20): Ranger 6/24, Lich 7/24, Warlock 7/24, DK 10/24; DEF fired in 34 of 60
  sampled logs (acts 51/52 ~5% of samples), deaths fell to 1.85/game — the hero stays alive but the push dies. Dropped.** Third
  confirmation that safety/defensive rules lose tempo on version 36 (hold at home v109, spell dodge v127-129, gate defence v144).
  Queued: ten-seat baseline for v139 (`v139-seats`, 240 games) to refresh per-class numbers.
  **v139 ten-seat baseline (09:49 UTC): 150/240 = 0.625** (v113 0.575, v93 0.537, v76 0.496): DK 11, Xbow 23, Lich 11, Warlock 13,
  Berserk 11, VK 15, Ranger 19, Arcanist 19, Druid 16, DH 12 of 24; Red 0.575 / Blue 0.675. Telemetry: Berserk deaths 3.6 (v113 5.0),
  DK 4.5, DH 5.9 (worst; unchanged), VK levels up; DK/Berserk STUCK prints 27-33 per game (v113 6-12) — the act-47 ride walks queue
  behind waves and trip the stuck/back-off machinery (act 10 = 4% of DK/VK samples). Melee death context in that baseline: last
  sample before death has mean HP 54-74%, no enemy hero within 10 tiles in 44-62% of cases, no ally within 25 in ~45%, act 9/4/3;
  Blue melee (VK 6.1, DH 5.9 deaths) die mostly in their OWN lane mid-game (walking into the enemy push after respawns), Red melee in
  the corner approach. Candidate v145 (S46, Codex) = v139 + melee back-off when alone against >= 2 enemy heroes (act 55, OUTN) and
  ride walks removed from stuck detection; test on melee seats (`--seats 0,4 -n 60`). v145 (:v145) smoke: DK won 5717 / 1 death /
  3 stuck (v139: 8-13) / OUTN fires at 2-4 enemy heroes; Berserk won 5571 / 1 death. Dueling v139 (`duel-v145-v139`, 240 games).
  **Result 117/240 = 0.487 (-6): DK/VK pair 58/120, Berserk/DH pair 59/120; deaths down (Berserk 2.2, DK 2.7) but levels down (4.0-4.2)
  — backing off costs the XP it saves. Dropped.** Stuck prints did fall to 5-8/game with act 47 out of stuck detection (keep that
  hygiene change in the next bundle). Day tally: v135-v145 tested, one gain (v139). Single tweaks are now below the detectable floor
  (+-25/240); next step is a bundle of the individually level-to-positive changes for a larger test: v146 = v139 + Blue pushes physical
  lane 2 (v140: +5/240 as Blue) + no Crossbowman escort (v142: +8/480, Red rows 0.479 vs null) + ride walks off stuck detection.
  v146 (:v146) smoke: DK won 5826 / 1 death / 1 stuck / no ESCORT; Blue Ranger INIT lane 2, won 15935 / 5 deaths. Dueling v139 on all
  seats, 480 games (`duel-v146-v139`). **Result 233/480 = 0.485 (-14): Blue rows 115/240 with Ranger 14/48 (the Blue copy in lane 2
  meets our own Red Crossbowman head-on — the mirrored design is biased for lane changes), Red rows 118/240 (no-escort part: null).
  Dropped; v139 stays.** Lesson: test lane-choice changes with random-roster `create` batches per side, never with mirrored duels.
  12 candidates today (v135-v146); one gain (v139). The loop is in maintenance mode: monitor rounds/coworld, push git, review v139's
  league results by class after ~10 rounds (scheduled ~14:00 UTC via `tools/league_logs.py --only-version 139`); revert to v113 if
  its melee seats do not improve on v113's league record (DK 0.65, VK 0.60, DH 0.71, Berserk 0.18 over 13-20 games each).

## GAME VERSION 36 (since ~23:20 UTC 2026-09-15)
- League coworld is now `cow_fdd365d8-57ba-4e3f-8c06-f0b87cd6d870` (2026.9.15.3, game version 36): same balance as version 34, creep lanes
  route around towers, and NEW BASIC observations: objectTarget(i), objectLevel/Mana/ItemId/ItemCount/FacingX/Y/VelX/Y, spellCount()+spell*
  (see docs/ARENA_NOTES.md top). Tools retargeted; v76 verified locally (DK 11141 ticks/3 deaths, Xbow 5636/1 on seed 2026).
- `uv run python tools/coworld_check.py` reports the league coworld and engine head and warns on change (state in tmp/coworld_check.json).
- **Champion since 03:36 UTC 2026-09-16: v113 = `Jordan:v113`** = v93 + stutter-step kiting for ranged classes (Codex S34: when a melee
  threat is within 3.5 tiles, hit while selfAttackCooldown is within the windup, otherwise step 3 tiles directly away): 67-53 then 140-100 vs
  v93 = 207-153 over 360 (+54, both batches positive, 0 timeouts). Blue-side ranged seats carry it (Ranger 21/24, Arcanist 19/24, Druid
  19/24 in the replication); Red melee seats unchanged. Telemetry: ranged deaths per game fell 60-75%, kills up ~70%.
  v114 (kite trigger 4.5 tiles, 4-tile steps) vs v93: 77/43 (+34 first batch; DH 11/12, VK 10/12) — now dueling v113 directly
  (`duel-v114-v113`: 58/62, level — the +34 vs v93 was the shared kiting gain; dropped, v113's 3.5-tile/3-step parameters stay). v115 (melee
  anti-kite) 58/62 vs v113 (level, dropped). v116 (:v116, Codex S36) = v113 + keep the range advantage against shorter-ranged enemy heroes
  (acts 47/48, KITE3; local Ranger 8075 XP, 3 deaths): 61/59 vs v113 (level, dropped).
- **Side asymmetry is a class asymmetry:** in every mirrored duel of this lineage the Blue copy beats the Red copy about 2:1 (v116 batch:
  candidate 21/60 as Red, 40/60 as Blue). Red seats are DK/Xbow/Lich/Warlock/Berserk (our win rates 0.38/0.58/0.46/0.46/0.29), Blue seats
  VK/Ranger/Arcanist/Druid/DH (0.71/0.88/0.79/0.79/0.50). The upside left is on the Red classes.
- **v113 per-class telemetry (replication, 24 games each):** Ranger 0.88 win / 0.79 deaths / 13.1 kills / level 8.3 / 358 gold unspent
  (all six inventory slots hold equipment, so gold piles up); Arcanist 0.79, Druid 0.79, VK 0.71, Xbow 0.58 (148 gold unspent), DH 0.50
  (5.5 deaths), Lich 0.46, Warlock 0.46, DK 0.38 (0.8 kills, level 3.3 at game end, 19% of its time escorting the Crossbowman), Berserk 0.29
  (16% escorting, 14% waiting for a wave). v117 (:v117) = v113 with the escort limited to ranged Red heroes (Lich/Warlock), dueling v113.
  v118 (:v118) = v113 with no Red escort at all. v119 (:v119) = v113 without the sword purchase so the sixth inventory slot stays free for
  elixirs. All three level vs v113 and dropped: v117 62/58, v118 61/59, v119 59/61. The escort is irrelevant either way under version 36.
  Reading of the Red gap: Red's ranged classes kite worse by design (Lich cadence 32, Warlock range 4.5 vs Ranger 18 / 5.5) and Red's
  melee DK/Berserk get nothing from kiting. Trace over the 360 v113-v93 duel games: the fillers do no better on Red classes in these
  games (black-kite DK 0.50 / Lich 0.42 / Warlock 0.61 / Berserk 0.38; red-kite DK 0.32 / Lich 0.50 / Warlock 0.25 / Berserk 0.32) — Red
  wins only 42% of those games because Blue carries our kiting copy plus the stronger classes. No Red-specific mechanism to copy.
  relh:v88 (uploaded 03:42) scored 0.616 in 73 of those games — a new strong opponent to watch. v113 time budget: walk 39%, farm 14.5%,
  siege 13.5%, escort 6.4%, fight 5.1%; 2.6 deaths and 6.3 STUCK events per game (analysing the stuck spots).
  v120 (:v120, melee flee at 40% HP instead of 25%) 59/61 vs v113 (level, dropped); v121 (:v121, melee farming radius 8 tiles) 63/57 (level, dropped).
- **Codex audit of v113 (docs/tasks/s37_audit_dead_rules.md, report only):** the respawn rejoin never activates (rejoinArmed is set to 1
  but activation needs 2) — heroes walk straight at the far objective after every respawn (the stuck hot spots); the hold (act 8) and
  resistance lane-switch machinery are dead; unseen-lane tower HP defaults to 8400 instead of version 36's 3900 (weakest-lane switch can
  misfire); six equipment items plus a potion need seven slots; purchase flags ignore buyItem's return value; the kite rule can step away
  from an adjacent enemy it could hit when bestHero is out of basic range; a declined fight falls through to the second siege rule beside
  that enemy; rx/ry (retreat point) can point forward right after a respawn; open-lane/escort walks never enter stuck detection.
  v123 = v122 + the cheap correct fixes (tower HP defaults, kite target from enemies in basic range, no fallback siege with an enemy hero
  within 3 tiles, retreat toward home when the objective is more than 40 tiles away, escort action gated on routing = 0).
- **Stuck analysis (v113 replication, 240 games):** 6.3 STUCK events per game (1503 total); 3 games had a hero stuck for the rest of the game
  (98-172 hits). Hot spots: near our own inner tower (105,35) while walking straight at the enemy inner tower (46,104) — 171 events — and at
  spawn (110,0) walking to the enemy gate; i.e. long cross-map walkTo calls after a respawn snag on terrain/tower footprints. v122 = v113 +
  when the objective is more than 40 tiles away, walk to the nearest lane route point that is closer to the objective (road-following), walk
  home after six stuck hits, forget stuck hits after 240 ticks of movement. Local same-seed DK game: 1 stuck / 1 death / won at tick 5861
  (v113: 13 stuck / 5 deaths / 12973). **v122 first batch 67/53 vs v113 (+14)**; replication over 240 queued (`duel-v122-v113-2`).
  BUT its hosted telemetry shows STUCK per game 11.8 (v113: 6.3, max 136 hits) with deaths down to 1.80 (v113 2.59): aiming at tower-centre
  route points snags on their footprints; the win gain came with fewer deaths anyway. v123 (:v123) = v122 + audit fixes, dueling v113
  (`duel-v123-v113`). v124 (:v124) = v123 switching to the next route point at 6 tiles instead of 3, dueling v113 (`duel-v124-v113`).
  v122 replication 86/114 after 200 (-28): combined ~153-167, **dropped** — tower-centre route points hurt more than the long walks.
  v125 (:v125) = v113 + the audit fixes only (no road-following), dueling v113 (`duel-v125-v113`). v126 (:v126) = v125 + the stuck
  escalation only (walk home after six stuck hits, forget hits after 240 ticks of movement), dueling v113 (`duel-v126-v113`).
  v123 44/76 vs v113 (-32, dropped) and v124 55/65 (dropped): together with v122's replication, road-following via route points is harmful
  in every form tried. v125 (audit fixes only) 53/66 and v126 (fixes + stuck escalation) 57/63 — both dropped; the audit's "fixes" do not
  help in aggregate (the forward-pointing retreat point and the fallback-siege gate may each have been doing useful work). **v113 stays
  champion.** Fourteen candidates on top of v113 have now been level or negative; cheap tweaks are exhausted — next: genuinely new
  mechanisms (spell dodging via spellCount/spellX/spellY/spellImpactTick, Codex S38 -> v127). Engine facts for it (content.nim abilitySpec):
  every Strike has an impact area (default circle radius 90000 = 1.5 tiles; Blazing Blade/Gale Slash 120-degree sectors from the caster;
  Storm Eagle/Clockwork Charge lines; meteors larger), projectile casts fly at 45000 units/tick (0.75 tiles/tick), so impacts are
  visible several ticks ahead through the spell list. Verified area casts: Meteor Strike / Volcanic Eruption radius 2 tiles with 48 cast
  ticks, Arcane Meteor 3 tiles / 72 ticks, Ricochet Disc / Golem Seed / Withering Idol / Bone Marionette / Bound Void / Dread Totem /
  Void Portal 2 tiles / 24 ticks, Dark Eclipse ring 2.33 tiles around the caster, Inferno Aegis heal circle; Healing Bloom / Kindred Wisps
  are allied heals (never dodge). Enum order in content.nim: LionGuard=0 ... VolcanicEruption=39.
  v127 (Codex S38) delivered: dodges enemy area strikes with impact in 3-40 ticks whose centre is within radius+1 tiles (radius 2 for
  Blazing Blade/Ricochet/Meteor/Golem/Gale Slash/Withering Idol/Bone Marionette/Bound Void/Void Portal/Volcanic Eruption, 3 for Arcane
  Meteor/Dark Eclipse/Winged Boot, 6 Lodestone Surge, 9 Storm Eagle, 8 Clockwork Charge, 5 Dread Totem; default 1.5-tile projectiles are
  not dodged) by stepping radius+2 tiles away (act 50, DODGE print); placed after flee, before fort/fights/kiting. Smoke tests clean
  (Ranger 12 dodges / 4 deaths, DK 4 / 2); uploaded as :v127, dueling v113 (`duel-v127-v113`). v128 (:v128) = v127 also dodging the
  heavy projectile strikes Shadow Comet (100), Final Measure (110) and Molten Fist as 2-tile circles, dueling v113 (`duel-v128-v113`).
  v127 interim 51/56 after 107 (level). Hosted telemetry: the dodge fires 4.8 times per game (1.4% of samples), mostly for Withering Idol
  (22), Meteor Strike (10), Winged Boot (38), Bound Void (31), Ricochet Disc (6), Clockwork Charge (27), Gale Slash (18), Storm Eagle (7) —
  several of those are low-damage (40-60), so the tempo lost to stepping away roughly cancels the damage saved: v127 deaths 2.07/game
  (v113 2.59) but level wins. v129 (:v129) = v127 dodging only strikes of 70+ damage (Blazing Blade, Storm Eagle, Meteor, Arcane Meteor,
  Golem Seed, Shadow Comet, Dark Eclipse, Clockwork Charge, Bound Void, Void Portal, Volcanic Eruption), queued vs v113 (`duel-v129-v113`).
  Note: Final Measure is 20 damage (v128's inclusion of it was a misread), Molten Fist 45. Finals: v127 58/62 (level), v128 55/65
  (negative) — both dropped; dodging saves ~0.5 deaths per game but costs the tempo back. v129 is the last dodge variant to try.
  **v129 first batch 67/53 vs v113 (+14; VK 10/12, Arcanist 9/12)** — replication over 240 queued automatically (`duel-v129-v113-2`);
  promote only if combined >= +24 over 360 with the replication positive.
  v130 (:v130) = v113 with a looser side-lane join (one ally pushing the other side lane suffices when our lane has none and no ally is
  beside us; JOIN fired only 0.22 times per game): 57/63 vs v113 (level, dropped). v129 replication interim 30/30 after 60; v129's
  hosted telemetry: 3.65 dodges per game (1.0% of samples; Meteor, Bound Void, Clockwork, Void Portal, Volcanic, Shadow Comet), deaths 2.25.
  A v113 ten-seat baseline (`v113-seats`, 240) is queued behind it for per-class rates in random rosters. v129 replication 121/119
  (combined 188-172 over 360, +16 < +24): dropped — spell dodging in any form saves ~0.3-0.5 deaths per game but not games.
  **v113 ten-seat baseline `v113-seats`: 138/240 = 0.575** (Red 65/120, Blue 73/120; DK 11, Xbow 21, Lich 13, Warlock 12, Berserk 8,
  VK 10, Ranger 20, Arcanist 12, Druid 17, DH 14 of 24). Lineage in random rosters: v76 0.496 -> v93 0.537 -> v113 0.575. In that batch
  (tools/roster_stats.py) v113 ranks second: nancy-goa:v1 0.596 (161 games, a newly strong opponent), Jordan 0.575, black-kite 0.565,
  red-kite 0.523, codex-objective-lanes 0.502, relh:v95 0.500, aaron 0.495, richard:v50 0.466, gota-g001 0.452, base 0.437, khors 0.378. v131 (:v131) = v113 preferring footmen within one hit of death (hp <= selfAttackDamage) as the
  farming target — XP/gold go only to the killing blow: 57/63 vs v113 (level, dropped). Twenty candidates on top of v113 are now level or
  negative. Trace of the baseline replays: nancy-goa:v1 (0.596) is a centre camper like khors/base (walks to (56,56) all game, 4300 creep
  and 2800 hero attack commands per game) but with 847 useItem commands per game (ours: 15) — the strong campers drink potions constantly.
  Next: v132 = v113 potion economy (buy an elixir whenever gold >= 50 and none is held, drink at 70% HP instead of 55%, no sword so a slot
  stays free) — converts the 100-360 gold our ranged seats leave unspent into effective HP: 59/60 vs v113 (level, 1 timeout; dropped).
  Next low-cost tests: v133 (Druid/Warlock kite with a 3-tile trigger and 2-tile steps so the target stays inside their 4.0/4.5 range),
  v134 (after 120 ticks waiting outside a tower with no allied footman within 8 tiles, walk back toward the previous route point to meet
  the wave; act 23). v133 65/55 vs v113 but the only seats it changes did not move (Warlock 3/12, Druid 7/12) — noise, dropped.
  v134 first batch 66/54 vs v113 (+12) — but its hosted logs show the walk-back (act 23) in only 0.29% of samples (5 samples in 120
  games; waiting heroes almost always have allied footmen within 8 tiles), so v134 is behaviourally v113 and the +12 is noise. Its
  replication (`duel-v134-v113-2`, 240) therefore serves as a second null calibration: **108/132 (-24 over 240)** for two behaviourally
  identical policies. Together with the first null (+21 then -15) the per-240 noise band is about +-25, wider than binomial. **Promotion
  rule tightened again (05:46 UTC): combined >= +36 over >= 360 shared games with both batches positive** (v87 +37, v93 +40, v113 +54 pass).
  Practical consequence: only large effects are testable; small tweaks cannot be resolved with 360 games.
  Round 324 (first with v113): 6/9.
- Champion 00:56-03:36 UTC: v93 = `Jordan:v93` = v87 + keep attacking footmen in basic range while travelling between lanes
  or rejoining (no enemy hero near, no tower danger): 64-56 then 136-104 vs v87 = 200-160 over 360 shared games (+40, both batches positive,
  0 timeouts). Replay trace over the 359 v87-v76 duel games: v87 issues 1050 creep attacks per game vs v76's 533 on the same lane/path
  (team-win 0.549 vs 0.448). Pending duels vs v87: v95 (focus fire) and v96 (two-ally dive rule). Already ported onto v93 and queued vs v93:
  v97 (:v97) = v93 + two-ally dive, v98 (:v98) = v93 + focus fire; both carry the death-position telemetry (`D tick respawn #n at x y Lk`).
  v95 vs v87: 60/60 (exact parity, dropped); v96 vs v87: 51/69 (negative, dropped). vs v93: v97 (two-ally dive) 61/59 (parity, dropped),
  v98 (focus fire) 52/68 (negative, dropped). Neither dive caution nor focus fire moves the needle; farming and not wasting time do.
- **Re-death pattern (v91 logs):** 39% of deaths are re-deaths within 1500 ticks of a respawn, on our own lane or mid, mostly while walking
  back (act 9) with one enemy hero near and no ally. v100 (:v100) = v93 + never fight alone: with no ally within 8 tiles, an enemy hero within
  10 tiles we cannot burst, and none of our towers within 7 tiles, fall back toward the previous route point (act 41; Crossbowman exempt).
- **Side gap:** in random rosters v91 (= v87) wins 52/120 as Red but 71/120 as Blue; v93's duel batches win 89/180 as Red vs 111/180 as Blue
  (v76 had no gap: 59/60). Red non-Crossbowman seats (DK 0.42, Lich 0.38, Warlock 0.29, Berserk 0.38) spend 11% of their time in the
  Red-only escort rule (act 35, v68: follow the allied Crossbowman near the enemy fort) instead of farming; Blue never escorts (0.54-0.67 per class).
  v99 (:v99) = v93 with the escort walk disabled: 66/54 then 110/130 vs v93 (176-184 over 360; Red seats fell to 43/120) — dropped, the
  Red-only escort rule helps. Also queued vs v93: v100 (:v100, never fight alone, `duel-v100-v93`), v101 (:v101, level-aware fights via
  objectLevel: never start on a hero two or more levels above us unless it is low or an ally is beside us, `duel-v101-v93`), and the
  [v100 result: 55/65 vs v93, negative, dropped — retreating from 1v1s costs more than the re-deaths it avoids]
  v93 ten-seat baseline `v93-seats`: 129/240 (Red 60/120, Blue 69/120) — v76 was 119/240, so the side gap is mostly noise.
  Every file from v97 on prints `D tick respawn #n at x y Lk`.
- Champion 00:42-00:56 UTC: v87 = `Jordan:v87` = v76 + attack any enemy footman within 8 tiles (melee 6) instead of walking
  or waiting for a wave (one scan condition, `farmR2`): 73-47 then 125-114 vs v76 = 198-161 over 360 shared games (+37, both batches
  positive, 1 timeout). Telemetry: deaths 3.5/game vs v76's 4.7, level curve unchanged, first kill 2151 vs 2412. Follow-ups dueling v87:
  v93 (:v93, keep farming in basic range while travelling between lanes) 64/56 vs v87 (+8 first batch, replication `duel-v93-v87-2` running),
  v94 (:v94, melee buy armor before the big damage items) 55/65 vs v87 (negative, dropped); v95 (:v95, Codex S32 focus fire: attack the enemy hero most nearby allies
  are hitting, via objectTarget) dueling; v91 ten-seat 123/240 (Red 52/120, Blue 71/120);
  v90 (:v90, farm radius 10/8) 60/60 vs v87 (exact parity, dropped); v91 (:v91, = v87 + death-position
  telemetry) ten-seat batch `v91-seats` for a per-seat baseline and a death map (tools/log_stats.py prints DEATH POSITIONS).
  Dropped: v88 (creeps before towers below level 4) 59/61 vs v76; v89 (Codex S31 creep-front anchor) and v92 (static lane-midpoint anchor)
  idle or walk at level 1 locally, uploaded for label order only.
- **Per-class gap vs the best fillers (600 hosted games with v87+ present, tmp/roster_cache.json):** black-kite / red-kite win 0.88 / 0.76 as
  Ranger and 0.77 / 0.76 as Arcanist; we win 0.50 / 0.53 on those seats (we beat them as VK: 0.58 vs 0.45 / 0.39). Their edge is on ranged
  Blue-side classes, i.e. kiting. Our anti-melee rule for ranged heroes (act 2) just walks back 4 tiles and cancels our attack (2% of time,
  kite act 28 0.4%). Codex S34 (docs/tasks/s34_stutter_step_kiting.md) writes v113 = v93 + stutter-step kiting using selfAttackCooldown
  (hit when the cooldown is within the windup, step 3 tiles away from the melee threat otherwise). v113 (:v113) delivered and smoke-tested
  (Ranger: KITE2 active, 4100 XP vs v93's 3700 on the same seed; Arcanist fine); dueling v93 (`duel-v113-v93`). Their Rangers issue ~930
  hero-attack and ~1100 creep-attack commands per game vs our 575/475 and reach the fort in 90% of games (we: 56%), i.e. they stay alive in fights.
  v111 (boots first) 51/69 vs v93 (negative, dropped). v112 (wave ride only) 58/62 (level, dropped).
  **v113 first batch 67/53 vs v93 (+14; Xbow 10/12, Lich 9/12, Arcanist 8/12, Warlock 8/12)**; replication over 240 running
  (`duel-v113-v93-2`); promote only if combined >= +24 over 360 with the replication positive. Hosted logs confirm the rule fires (KITE2
  5-6 prints per game on every ranged class, 0 on melee) and the mechanism: deaths per game Ranger 0.58 (v87-era 2.46), Xbow 0.83 (2.38),
  Lich 1.17 (3.04), Arcanist ~1.5 (3.8); kills per game Ranger 8.1 (4.7), Xbow 7.9 (5.9), Lich 5.7 (3.3). Overall 2.42 deaths/game vs 3.56.
  v114 (:v114) = v113 with the kite trigger at 4.5 tiles (was 3.5) and 4-tile steps, queued vs v93 (`duel-v114-v93`).
  Replication interim 122/78 after 200 (Blue seats 76/96: Ranger 21/24, Arcanist 19/24, Druid 19/24, VK 17/24; Red 46/104).
  v115 (:v115, Codex S35) = v113 + melee heroes stop chasing a target that flees at >= 80% of our speed (objectVelX/Y) for 24 decisions or
  96 chase ticks (blacklist 240 ticks unless kill shot / all-in): smoke-tested (rule silent vs base.bas), dueling v113 (`duel-v115-v113`).
- **Time budget (v93 ten-seat, 4340 telemetry samples):** walking the route 43%, farming creeps 14%, sieging 9%, fighting heroes 7%, escort 6%,
  open-lane fort walk 4%, waiting for a wave 4%, low-HP retreat 3% (4.4% in losses vs 2.7% in wins). With ~3.5 deaths per game and ~800 ticks
  per death (24 dying + 192 respawn + the walk back), deaths eat roughly a third of an 8500-tick game; every death avoided is worth ~10% presence.
- **Death map (v91 ten-seat, 855 deaths in 240 games, Red frame):** 29% on the enemy inner/gate stretch, 26% on our own east-edge lane,
  20% mid/jungle. Hot cells: (40,100) 101 deaths + (50,100) 39 = the enemy INNER tower (46,104); (90,100) 85 = the enemy outer tower;
  (100,60)-(100,70) 66 = our own outer tower under enemy push. 54% of deaths happen at levels 2-4, ticks 2000-8000. Next test: v96 = v87 with
  the all-in dive needing 2 allies within 8 tiles for inner/gate towers (1 still enough for the outer tower).
- v101 (level-aware fights) 57/63 vs v93 (level, dropped). League with v93: rounds 319-322 = 24/39, 1528 MMR, rank 6 (03:11 UTC; was rank 9,
  1482 with v76/v87 at 01:16).
  Note: v93's home-guard block (act 14, 'wait at own gate up to 30 s after respawn') is dead code — guardUntil is never armed — so heroes
  walk out immediately after every respawn. v102 (:v102) = v93 + arm a 2400-tick window at each respawn during which, with an enemy hero within
  18 tiles, one of our first three route towers within 12 tiles and no ally within 8, the hero holds at that nearest tower (act 14) and fights
  from there; v103 (:v103) = v93 + v84's follow-the-largest-allied-group rule restricted to Demon Hunter, Vanguard Knight and Druid (the
  Blue-side classes that die on our own lane). v102 first batch 69/48 vs v93 — **but its telemetry shows the hold (act 14) never fired in
  any of the 120 games** (the rule required objective index < 3 and routing = 0; after a respawn the index stays at the enemy tower and the
  rejoin logic sets routing = 1), so v102 is behaviourally v93 and the +21 was noise. Its replication `duel-v102-v93-2` is therefore a
  NULL CALIBRATION of the duel method (identical behaviour on both sides): 75/98 after 173 games (-23, 3.5 binomial SE). Fillers are drawn
  per episode (12 distinct rosters per 12-episode request), so games are independent; treat +-20 over 120 as ordinary noise and keep the
  final null result 112/127 over 240 (-15). **Promotion rule tightened (03:05 UTC): combined >= +24 over >= 360 shared games with both
  batches positive** (v87 +37 and v93 +40 over 360 pass; nothing else so far would). v106 (crippled reset) 55/65 vs v93 (dropped).
  v111 (:v111) = v93 buying boots before the dagger (walking is 43% of our time) queued vs v93. v107 (chase kill shots) first batch
  70/50 vs v93 (+20; the chase rule fires in 2.5% of samples, hero kills 2.34/game vs ~2.1); replication 107/109 after 216 (level) — combined
  ~+18 over 336, below the +24 bar: dropped.
  Lesson: check that a new rule fires (act share / print) in the first hosted batch before trusting its duel. v109 (:v109) = v102 with the
  gates removed and a HOLD print; local DH/DK games show the hold firing; **duel vs v93 51/69 (negative: waiting at home loses more tempo
  than the re-deaths cost)**. v110 (hold + ride) 57/63 (level). v112 (:v112) = wave ride only, dueling v93 (`duel-v112-v93`). v103 60/60 (parity, dropped).
  v108 (:v108, Codex S33 = v102 + ride the next allied creep wave out after a respawn) inherited the same dead gates — uploaded for label
  order only; v110 = v109 + that ride rule with the gates removed (smoke-testing, then duel vs v93). v106 (:v106, crippled reset) and v107 (:v107,
  chase kill shots: attack an enemy hero within 10 tiles whose HP is at most three of our hits) queued vs v93.
- v104/v105 = v93 + farm at the map centre until level 5/tick 3000 (v104) or level 4/tick 2000 (v105), then push: locally the DK reaches
  level 3 by tick 960 (v93: 1920) but both DK games were LOST (the centre is where all enemy campers converge) and the v104 Crossbowman ended
  crippled at home (41 HP, 25 gold, no potion) for 13000 ticks — a general failure mode: 36 of 480 hosted games (v91+v93 batches) had the hero
  idle below 25% HP with under 30 gold for 1400+ ticks. v106 = v93 + crippled reset (walk into the enemy lane to respawn at full HP);
  v104/v105 also carry it but the v105 Crossbowman never reached the centre locally (stuck at level 1 until tick 2400) — both dropped
  without a duel (uploaded as :v104/:v105 for label order). v106 (:v106) dueling v93 (`duel-v106-v93`).
  because Blue-side classes die mostly on our own lane right after respawn (DH 59 of 152 deaths, VK 40, Arcanist 31; act 9 walking).
  Every hosted result so far is in this file and README.md; standings via `uv run python tools/ladder.py`.
- Previous champion v76 (`Jordan:v76`). Under version 36 (all duels since 23:30 UTC ran on it): v82 (:v82, Codex S28, target-aware siege via
  objectTarget) 59/61 then 117/123 vs v76 (176-184 over 360, level, dropped); v83 (:v83, S29) 58/62 (level, dropped); v84 (:v84, S30 group
  follow for all classes) 53/66 (negative, dropped); sanity v76 vs v68 117/121 (level). v76 ten-seat baseline on v36 (`xp/v76-seats-v36`):
  119/240 (Red 59, Blue 60; DK/Warlock 10/24 weakest, Xbow 16/24). League on v36: 5/21 (rounds 315-316), rank 8, 1489 MMR.
- **Version-36 game structure** (tools/replay_lanes.py over the 240 v76-v68 duel games): winner's first gate attack median 5732, first fort
  attack 8028, game end 8388 (version 34: 14700). Same seed/roster locally: v76 DK 25570 ticks on v34 -> 11141 on v36, so the creep-routing
  change itself speeds games up. Our hero hit the breakthrough gate in 58% of wins (68/117) and 8% of losses; in wins it issues 220 gate and 135 fort
  commands per game, in losses 79 and 15. Blue wins 55% of hosted games on v36 (Red 45%).
- **Field strength on v36** (tools/roster_stats.py, 840 hosted games): black-kite:v11 0.566 (685 games), richard:v40 0.563, khors:v1 0.552,
  games-bond:v6 0.540, red-kite:v13 0.519, relh:v67 0.504, codex-objective-lanes 0.495, base.bas 0.484, aaron:v2 0.482, gota-g001 0.476,
  nancy 0.452, daf 0.384. v76 sits at 0.496, i.e. 6-7 points behind the best fillers. black-kite pushes the same physical side lane as v76
  (Red lane 2 / Blue lane 0); richard pushes the other side lane and mid; khors camps mid and farms. `tools/policy_trace.py` aggregates what
  each policy's hero does per 1000 ticks over the cached hosted replays.
- **Lane tests done:** v85 (:v85, mid lane for both teams) 50/70 vs v76 (negative); v86 (:v86, other side lane) 62/58 (parity). The
  current push lane (Red lane 2 / Blue lane 0) stays.
- **Why we lose (tools/log_stats.py on v76-seats-v36, 240 games):** our hero dies 4.7 times per game (5.5 in losses, 3.9 in wins; DH 6.9,
  Druid 6.4, Xbow 5.0) and is still level 1 at tick 1920, level ~3.6 by tick 4000-6000 and ~5 at game end. It issues ~6400 walkTo commands
  per game but only ~530 creep attacks; the strongest fillers (black-kite, red-kite ~1400 creep attacks; khors/base ~3800) farm far more.
  Locally base.bas heroes end with 1.5-2x our XP. Hypothesis: under-levelled hero -> loses fights -> dies -> the lane push stalls.
- **Farming tests running:** v87 (:v87) = v76 + attack any enemy footman within 8 tiles (melee 6) instead of walking/waiting (farmR2);
  v88 (:v88) = v87 + below level 4 creeps come before towers (unless all-in). Local DK: v87 17191 ticks / 9 deaths / 2475 XP, v88 13687 / 3 / 1425
  (v76 11141 / 3 / 1475). **v87 first batch: 73/47 vs v76 over 120 (+26, Red 34/60, Blue 39/60, 0 timeouts)** — the largest first-batch
  gain so far; replication over 240 running (`duel-v87-v76-2`); promote if the replication is positive. v88 dueling (`duel-v88-v76`).
  v87 telemetry (120 games): deaths 3.5/game (v76 4.7), level curve unchanged (3.3-3.5 at tick 4000), first kill 2151 (v76 2412).
  v89 (:v89, Codex S31) = v88 + hold at the allied creep front until level 4: locally the hero mostly walks after a moving anchor
  (DK 1150 XP vs v76 1475, Xbow 400 vs 1175), uploaded for label order only, not dueled. v90 (:v90) = v87 with farm radius 10 tiles
  (melee 8): dueling v87 (`duel-v90-v87`, 120). v91 = v87 + death-position telemetry (no behaviour change) for a ten-seat baseline.
- **Where this stands (23:45 UTC):** the confirmed lineage is v49a (tower-safe siege, kiting, commitment, all-in) -> v51 (join a 2+ ally side
  push, 91-66 over 360) -> v68 (escort the allied Crossbowman, 102-85 over 360) -> v76 (fort rush once a gate is known dead, 129-107 over 240
  vs v75, level vs v68). Since game version 34 every further candidate (v73-v83, 12 of them) landed within noise (+/-5 over 120-240 games),
  including ideas that halved the local reference game (v80, v82). Local single-seed games vs base.bas do not predict hosted results.
  Promote only on >= +8 over >= 240 shared games with both batches positive.

## GAME VERSION 34 (since ~20:30 UTC 2026-09-15) — read first
- League coworld is now `cow_d4827721-d640-4296-b7ff-13b1d8c3bdf0` (2026.9.15.2, game version 34): towers 900/1200/1800 HP, 18/24/30 dmg
  (version 33 had 1200/2400/4800 and 28/56/112). Games end decisively again (4 timeouts in 119). Round 310 failed during the switch.
- v79 (:v79, Codex S27) = v76 + stage 9 tiles short of an enemy gate whose last seen HP <= 450 (to win the fort race): 67/53/0 vs v76 (first batch);
  replication 119/121 (186-174 over 360: parity, dropped). v80 (:v80) = v76 with boots bought first: local reference game 13941/8 deaths vs
  v76's 25570/16 but duel 62/58 vs v76 (parity, dropped). v81 (:v81) = v79 + boots first (uploaded, untested). Round 315: 1511, rank 7.
  Sanity duel v76 vs v68 (240) queued to confirm the lineage gain under v34. v76 ten-seat under v34: 127/240 (Red 63, Blue 64; seats 8-15/24, DK weakest).
  Round 314 (first with v76): 1540 MMR, rank 5. v76 ten-seat batch (v76-seats) running for per-seat targeting.
- **Champion: v76 = `Jordan:v76`** (promoted 22:48 UTC) = v75 + head for an enemy fort as soon as its lane's gate is known dead, before the fort
  is visible: 64-54 and 65-53 vs v75 (129-107 over 240). v78 = v76 + defend-own-fort (v77) was exact parity 120-117, so v77's rule is dropped.
  Previous: v75 = `Jordan:v75` (promoted 21:47 UTC) = v68 + go for the enemy fort whenever it is exposed and visible, at any distance:
  65-47 then 112-121 vs v68 (177-168 over 360: level with v68; kept as base). Round 312 (first with v75): 1510 MMR, rank 6.
  v76 (:v76, head for a fort once its gate is known dead) 64/54 vs v75; v77 (:v77, defend our exposed fort) 64/56 vs v75 — both first
  batches. v78 (:v78) = v77 + v76: 240-game duel vs v75 queued; v76 replication queued. Promote v78 if >= +8 over 240. v76 (:v76) = v75 + head for an enemy fort as soon as its
  gate is known dead (before it is visible): duel vs v75 queued. v77 (:v77, Codex S26) = v75 + defend our own exposed fort when threatened (within 60 tiles, enemy fort not exposed): smoke/upload/duel vs v75 chained. v68 under v34: ten-seat 100/240 (Red 53, Blue 47; seats 7-14/24),
  beat v73 62-53 and the old diver v30 68-51; v49a 58-58 (parity).
  v74 (:v74) = v68 with siege allowed on any tower <= 900 HP without cover and all-in from tick 6000: local DK game 15704 ticks/10 deaths vs
  v68's 27951/17 on the same seed; duel vs v68 56/62/2 (dropped). v49a vs v68 58/58/4 (parity). Under v34 nothing beats v68 yet; a ten-seat
  batch of v68 (v68-seats-v34) is running to find the weak seats under the new balance. v75 (:v75) = v68 + fort at any distance when
  exposed and visible: duel vs v68 queued. Rounds: 310 failed at the coworld switch ("only 8/12 planned slots produced scoring evidence"),
  no round created since 20:50 as of 21:21 — monitor.
- Labels equal file numbers from v66 on; upload every new file exactly once in numeric order.

## Current state (2026-09-15 18:35 UTC) — GAME VERSION 33
- League coworld `cow_252fb6a6` (2026.9.15.1, game version 33): towers 1200/2400/4800 HP, 28/56/112 dmg; 55-61% of games time out.
  Details: docs/ARENA_NOTES.md top section; new engine source in tmp/engine_new (source/polyworld origin/main).
- **Labels now equal file numbers.** Platform versions auto-increment per policy name (a ':' in --name is rejected), and identical files are
  deduplicated to their existing version, so byte-unique copies of v66-v70 (a trailing `' platform label vNN` comment, tmp/labeled/) were uploaded in
  order to land as :v66-:v70. From now on upload every policy file exactly once, in numeric order, and the label matches the file number.
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
  Crossbowman is within 8 tiles of an exposed tower or 10 tiles of an enemy hero: 32/28/60 vs v62 (no better than v68; dropped).
  v70 (:v70) = v68 + VK/Druid follow the largest allied group: seat 5/8 batches vs v68 running. v71 (:v71) = v68 with the join rule
  also for the Crossbowman: seat-1 batches vs v68 queued (local reference seed: 26893 ticks/18 deaths vs v49a's 9665/2 — v62's weakest-lane
  switch seems to pull the Crossbowman out of its lane). v72 (:v72) = v68 with that switch disabled for the Crossbowman: reproduces v49a's reference game exactly (9665/2 deaths); seat-1 batch
  result 13/48 vs v68 15/48 and v71 17/48 (all within noise; the exemption rests on the local reproduction). v70 support seats (VK/Druid)
  10/72 vs v68 6/72 (mildly positive). v73 (:v73) = v72 + v70: 54/62/4 vs v68 under game version 34 (dropped). v62 ten-seat: 49/240 (Xbow 11/24; every other seat 1-8/24, i.e. base rate);
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
