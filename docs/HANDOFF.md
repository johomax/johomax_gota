# HANDOFF — Gods of the Arena policy project (resumed 2026-09-16, 02:42 UTC)

## WHERE THIS STANDS (2026-09-16 04:50 UTC) — read this first
- **Champion: v113 = `Jordan:v113`** (promoted 03:36 UTC). Lineage of confirmed gains on game version 36, all by mirrored-seat duels:
  v76 -> v87 (farm any enemy footman within 8 tiles instead of walking/waiting, 198-161 over 360) -> v93 (also farm while travelling
  between lanes, 200-160 over 360) -> v113 (stutter-step kiting for ranged classes via selfAttackCooldown, 207-153 over 360).
  Ladder: rank 4, 1538 MMR (05:11 UTC), up from rank 9 / 1482 at 01:16 UTC; league rounds with v113 (324-326): 18/28. Random-roster
  baseline 0.575 (v76 0.496, v93 0.537), second in its batch behind nancy-goa:v1 0.596 and ahead of black-kite 0.565.
- **Promotion rule:** combined >= +24 over >= 360 shared games with both batches positive (a null duel of identical policies read +21
  then -15 per batch, so +-20 per 120-240 games is noise). Always confirm a new rule fires in the hosted logs (tools/log_stats.py) first.
- **Tried on top of v113 and level or negative (16 candidates):** wider kite trigger, range-advantage kiting, melee anti-kite, escort
  variants, free elixir slot, melee flee at 40%, melee farm radius, road-following via route points (harmful), the Codex audit's fix bundle,
  stuck escalation, spell dodging (saves ~0.5 deaths/game, wins level). Passive/safety rules lose tempo; only added productive actions won.
- **Structural facts:** Blue-side classes (VK/Ranger/Arcanist/Druid/DH) win 0.71-0.88 for us, Red-side (DK/Xbow/Lich/Warlock/Berserk)
  0.29-0.58; the best opponents show the same Red weakness in shared games. Games end ~tick 8000; deaths cost ~800 ticks each; our hero
  walks 39% of the time, farms 14.5%, sieges 13.5%. Heroes snag 6 times per game on long walks (route points are tower centres — never
  walkTo a tower position).
- **Tools:** duels `tools/xp_mixed.py duel CAND CTRL --seats 0-4 -n 12|24 --tag t`, report `tools/xp_mixed.py report xp/t.json`,
  telemetry `tools/log_stats.py xp/t.json` (act share, deaths, DEATH POSITIONS), replays `tools/replay_lanes.py`, `tools/policy_trace.py
  --ids --exact --by-class`, fillers `tools/roster_stats.py`, ladder `tools/ladder.py`, engine/coworld drift `tools/coworld_check.py`.
  Upload every policy file once, in numeric order (`uv run coworld upload-policy --file policy/vNNN.bas --tag version=vNNN`), so the
  platform label equals the file number; smoke-test Codex output locally first (blank line before `end if`/`wend` is a compile error).
- **In flight:** v133 (short-range kite steps) and v134 (meet the wave) dueling v113. v129-v132 dropped (level).

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
  v134 (while waiting for a wave with no creep in reach, walk back toward the previous route point to meet the wave).
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
