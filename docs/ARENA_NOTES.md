# Gods of the Arena — mechanics notes (verified from polyworld@d03d2d1 source + local probe)

Game version 2026.9.14.3 (map generation changed on 2026-09-14; older wiki/book assume 64x64). Source commit 275ba23.

## GUARDED GODS — engine f2ab959 (league coworld cow_126f2fcb-80a0-4b6e-8166-eb6163576db5 since ~22:30 UTC 2026-09-16; cow_703e69a4 ran round 359)
- Each fort (god) now has TWO level-three guard towers flanking it (1950 HP, gate-tier; kind 4, ids 28-29 for Red at (106,16) and (99,9), Blue mirrored, presumably ids 30-31). They are exposed once ANY lane's three towers are dead; the fort takes NO damage until both of its guards are dead (`fortExposed`).
- Creeps target lane towers, then barracks, then the nearest exposed guard. Barracks unchanged (ids 41-51 for Red).
- Any policy that derives lane/tier from tower ids must skip ids >= 28 — v148 died at init with `BASIC array 'routex' index 23` on every game (rounds 359-360: 7/17 with an idle hero). Hotfix v175.
- Engine commits since 7365e4e: "Add guarded gods and rusher policy" (06858d1, new players/rusher.bas reference bot), visibility caching (no gameplay change), tournament reports.

## League coworld cow_54d6f449 (since ~20:40 UTC 2026-09-16, engine 7365e4e): graphics-only rebuild of version 37 (procedural trees/rocks models); gameplay bit-identical (same seed-2026 game: RedTeam 14074). Local runs: use ./coworld/cow_54d6f449-6d63-464d-b742-ff720a9ce803/coworld_manifest.json.

## GAME VERSION 37 (league coworld cow_dd6ceed6-9188-4eaa-9099-03aefcd1e5fe, 2026.9.16.2, engine 5c701f9, since ~2026-09-16 16:00 UTC)
- **Dead towers and barracks are NOT enumerated in objectCount()** (sim: `value.kind in [Tower, Barracks] and hp <= 0 -> skip`). Any rule
  that waits to SEE a tower at 0 HP never fires: v113/v139 parked on dead tower coordinates until the 28800-tick timeout (318 STUCK
  prints in one local game). v148 infers "dead" when the building objective is missing from the list while we stand within 4 tiles.
- **Barracks are buildings**: object kind 5, ids 40+, two per lane per team, 950 HP, no attack, attackable once the lane's towers are dead
  (`buildingExposed`); creeps spawn 3 per living barracks per interval (6 per lane per team, was 2; unit cap 360). Killing both
  barracks of a lane stops that lane's enemy creeps. No XP/gold reward found for barracks kills in the diff (towers still 100/75).
  Fort exposure unchanged (a lane with all three towers dead). Creep targeting (`nextEnemyBuilding`): the lane's towers by tier, then
  the NEAREST surviving barracks of that lane, and the fort only when a creep passes within 4.25 tiles — so after a gate falls the
  wave spends its time on the two barracks (2 x 950 HP) before the fort; a hero that goes fort-first (400 HP, no defence from the fort
  itself) still ends the game fastest if enemy heroes do not defend it.
- **Towers**: HP 950/1300/1950 (was 900/1200/1800), damage 18/24/30 unchanged, ranges unchanged; body footprints 1.05/1.25/1.65 tiles
  (was 0.42/0.55/0.70) — walkTo at a tower centre snags every time; stop 2.5-3 tiles short (v147) or attackTarget.
- **Hero buffs**: Crossbowman 46 dmg +9/level (was 43/+8), Berserker 38 +8 (was 35/+7), Lich Ice Spear 48 dmg / 6.67 tiles (was 44 /
  6.33), Warlock Aether Siphon restore 30 (24), Death Knight Sanguine Chalice heal 36 (30).
- Barracks positions on the seed-2026 local map (tools/probe.bas, kind 5): Red ids 41 (113,26), 43 (100,28), 45 (88,14), 47 (89,2),
  49 (97,24) + one more; Blue 44 (27,101), 48 (18,91) + others — i.e. two per lane just inside each gate tower, mirrored by point symmetry.
  Own barracks are always visible (own team); enemy barracks only when exposed and seen. Kind 5 objects sit in the object list, so
  scans keyed on kind 1-4 ignore them safely.
- `terrainWalkable(x, y)` now returns 1 only for cells the team has SEEN as walkable (fog on terrain); unknown cells read 0.
- Paths and creep waves were "simplified" (c57c1f5) and map generation changed (rock triangles, floor cuts); tower positions and
  lane route points are the same as version 36 in the seed-2026 local map.

## GAME VERSION 36 (league coworld cow_fdd365d8-57ba-4e3f-8c06-f0b87cd6d870, 2026.9.15.3, since ~2026-09-15 23:20 UTC)
- No balance change vs version 34 (towers 900/1200/1800 HP, 18/24/30 dmg). Creep lanes now route around tower collision footprints.
- New BASIC observations (bots.nim, 16 work each): objectLevel(i), objectMana(i), objectItemId(i, slot?), objectItemCount, objectFacingX/Y(i),
  objectVelX/Y(i), objectTarget(i) = the object's current attack-target id if that target is visible to us (0 otherwise; a tower's targetId
  is exposed while it lives), spellCount() and spellAbility/spellCasterId/spellX/spellY/spellImpactTick(k) for pending enemy area spells.
  Also itemCount(slot). Local reference games on this coworld: v76 DK solo 11141 ticks/3 deaths, Xbow 5636/1.
- Games are ~2x faster than version 34 with the same seed and roster (v76 DK vs base: 25570 -> 11141 ticks); hosted median end ~8400
  ticks, winner's first gate attack ~5700, first fort attack ~8000. Blue wins ~55% of hosted random-roster games.
- XP and gold go ONLY to the hero that lands the killing blow (sim.nim applyHeroHit -> gainRewards): footman 25xp/15g, hero 150/100,
  tower 100/75. Level-ups heal by the max-HP delta. Farming = last-hitting; our v76 hero was level 1 until tick ~1500-1900.
- What moved the needle under version 36 (duels, mirrored seats): v87 = attack any enemy footman within 8 tiles (melee 6) instead of
  walking/waiting: 198-161 vs v76 over 360; v93 = also keep farming footmen in basic range while travelling between lanes: 200-160 vs v87.
  Level/parity or negative: mid lane (50/70), other side lane, creeps-before-towers, wider farm radius, melee armor first, two-ally dive rule,
  focus fire via objectTarget, target-aware siege, group follow. Death map (tools/log_stats.py DEATH POSITIONS): the enemy inner tower
  (46,104 Red frame) is the deadliest cell; 39% of deaths are re-deaths within 1500 ticks of a respawn while walking back alone.
- Standings: `uv run python tools/ladder.py` (division leaderboard); the softmax CLI has no `leagues` command.

## GAME VERSION 34 (league coworld cow_d4827721-d640-4296-b7ff-13b1d8c3bdf0, 2026.9.15.2, 2026-09-15 ~20:30-23:20 UTC)
- Rebalance: towers 900/1200/1800 HP, damage 18/24/30 per 24 ticks (version 33 had 1200/2400/4800 and 28/56/112; the original 600/800/1000
  and 14/18/22). Ranges unchanged. Lion Guard heal 30, Mana Crystal restore 24. Games end decisively again (4 timeouts in 119 duel games).
- Engine commits: a6112c5 "Rebalance GotA heroes and towers", d915109 (body separation without navigation/sqrt). Replay version 34.

## GAME VERSION 33 (league coworld cow_252fb6a6-cbc3-4d4f-9fa2-8b5250a9d2a2, 2026.9.15.1, 2026-09-15 ~00:00-20:30 UTC)
- Towers: HP 1200/2400/4800 (was 600/800/1000), damage 28/56/112 per 24 ticks (was 14/18/22); ranges unchanged 5.0/5.5/6.0 tiles.
  A gate tower one-shots footmen and kills a level-1 hero in 3-5 shots. Crossbowman (6.5) still out-ranges every tower; Ranger/Lich (5.5)
  only the outer tower. Heroes/creeps now collide with tower footprints (radii 0.42/0.55/0.70 tiles); creeps resume lane paths after fights.
- Fort HP still 400, FortRange 4.25 tiles, forts do not shoot; fort sight radius 14. Footmen unchanged (60 HP, 12 dmg/32 ticks).
- Rewards unchanged (footman 25xp/15g, hero 150/100, tower 100/75). Idle auto-acquire is creeps only. Ranger base HP 200 (was 210).
- Consequence: 61% of league games time out (0 for everyone); decisive games are long group sieges (first gate attack ~tick 10,000,
  2-5 heroes at the fort). Our v30 died 15-22 times per game there and won 9/41. Engine source for this version: tmp/engine_new/*.nim
  (from source/polyworld origin/main).

## Seating / scoring
- League `team_n` + `team_layout: blocks`: my policy fills ALL 5 seats of one team; opponent fills the other 5.
  Slots 0-4 = Red (team 0), 5-9 = Blue (team 1). Both sides get played across episodes.
- Winning team heroes score 1 each; loss 0; timeout (28,800 ticks) = 0 for everyone. Elo K=4.
- Observed league games end by fort kill in 3,500-12,500 ticks. Even with all heroes idle, footmen alone
  kill a fort in ~8,000 ticks (probe run). Timeouts are rare now; the game is a race + fights.

## Map (CURRENT league coworld cow_9d9d7070-2210-4899-81de-f39401b32162, version 2026.9.14.5, game version 30, map hash 48422D57, map_size 116;
## changed from cow_0752b441 / hash 6EB3A6B3 around 2026-09-15 00:00 UTC — towers, forts and spawns are at the SAME coordinates, terrain differs)
The participate guide names cow_d7a245f0 (2026.9.14.2, a 128x128 map) but the league's hosted episodes run cow_975af671
(map hash 000000006EB3A6B3). Always test with `coworld/cow_975af671-.../coworld_manifest.json --variant competition`.
- Coordinates 0..115 (mapWidth = mapHeight = 116). Walkable: grass=1, road=2, marsh=5; NOT rock=3, trees=4, wall=6. Roads ~6 tiles wide.
- The map is point-symmetric: enemy(x,y) = (115-x, 115-y); Red lane k mirrors Blue lane 2-k.
- Red fort id 1 at (105,10), Red hero spawn (112,4). Blue fort id 2 at (10,105), Blue spawn (3,111).
- Tower id = 10 + lane*6 + team*3 + tier (tier 0 outer, 1 inner, 2 gate). Towers only attackable outer->inner->gate.
  - Lane 0 (top/left L): Red gate 12 (86,4), inner 11 (69,11), outer 10 (20,11); Blue outer 13 (7,46), inner 14 (7,77), gate 15 (4,86)
  - Lane 1 (mid diagonal, crosses lake/marsh): Red gate 18 (96,19), inner 17 (81,29), outer 16 (64,42); Blue outer 19 (51,73), inner 20 (34,86), gate 21 (19,96)
  - Lane 2 (right/bottom L): Red gate 24 (111,29), inner 23 (108,38), outer 22 (108,69); Blue outer 25 (95,104), inner 26 (46,104), gate 27 (29,111)
- BFS route lengths spawn->through own lane->enemy towers->fort: side lanes 219 tiles, mid 203 tiles.
- Own-team structures are always visible, so a policy can read its own tower positions at tick 1 and derive enemy positions by reflection.
- Fort exposed (attackable, objectAlive=1) once ANY lane has all 3 towers dead. Fort HP 400, attack range 4.25 tiles (any class). Forts do not attack.
- ASCII maps: docs/map_kinds.txt (F/f fort, W/w towers, H/h hero spawns), map_height.txt, map_water.txt. tools/mapcheck.py checks points/routes.
- Engine pathing snags heroes on tree/rock corners when a walkTo target sits inside or beside obstacles: use tower courts / road centers as waypoints,
  check walkTo's return value, and re-path (step back toward the previous waypoint) when the position stops changing.

## Units (60_000 world units = 1 tile; TickRate 24)
- Hero ids: Red 100-104, Blue 105-109 (slot = id-100 / id-105). Red classes by slot: 5 DeathKnight, 6 Crossbowman, 7 Lich, 8 Warlock, 9 Berserker.
  Blue: 0 VanguardKnight, 1 Ranger, 2 Arcanist, 3 DruidWarden, 4 DemonHunter. Melee = 0,4,5,9.
- Basic attack range (tiles): VK 1.17, Ranger 5.5, Arcanist 5.0, Druid 4.0, DH 1.25, DK 1.27, Crossbow 6.5, Lich 5.5, Warlock 4.5, Berserker 1.33.
  Attack period ticks: 24,18,30,26,16,28,36,32,28,20. Damage = base + (lvl-1)*perLvl + items. Damage lands at 45% of swing.
- HP/lvl, dmg/lvl per class in source content.nim. Max level 20. XP to next = 100 + 75*(lvl-1).
- Rewards go to the hero that lands the killing hit: footman 25xp/15g, hero 150xp/100g, tower 100xp/75g. Start 150 gold.
- Death: 24 ticks dying + 192 ticks respawn at own spawn, full HP/mana, cooldowns cleared; long walk back.
- Mana regen 1 per 6 ticks (4/s).
- Footmen: 60 HP, 12 dmg per 32 ticks, move 5500/tick (~2.2 tiles/s). 2 per lane per team every 240 ticks (12 total), cap 120.
  They chase nearest visible enemy within 5 tiles (keep target to 8), attack exposed towers within 7, fort within 4.25.
- Towers: HP 600/800/1000, dmg 14/18/22 per 24 ticks, range 5/5.5/6 tiles; target FOOTMEN FIRST, then heroes (nearest).
- Vision is TEAM-SHARED: hero radius 10 tiles, footman 5, tower ~7-8, fort ~16; occluded by trees/rock/height.
  Own-team objects are always in the object list; enemy objects only when visible. All my 5 heroes see the same enemies.

## BASIC host surface (per hero VM, one decision per tick)
- Data: selfId selfTeam selfClass selfX selfY selfHp selfMaxHp selfMana selfMaxMana selfGold selfLevel worldTick selfLayer mapWidth mapHeight mapLayers
- objectCount(), objectId/Kind/Team/Class/X/Y/Hp/Alive(i). Enumeration order: forts(2), towers(18), heroes(10), footmen. Kinds 1 fort 2 hero 3 footman 4 tower.
  objectAlive: towers/forts = exposed & hp>0; heroes/footmen = hp>0 & not dying. Dead towers still enumerate with hp 0 when visible.
- walkTo(x,y) [800 work]: server pathfinding; CLEARS attack target; while walking NO auto-acquire.
- attackTarget(id) [20]: any living enemy id (validated against world, not fog) but the target is dropped next tick if not visible.
  Hero paths into own range then attacks. attackTarget(0) clears target (stops).
- buyItem(id), useItem(slot): work anywhere on the map, any time alive. Equipment unique (no class restriction!), consumables stack 8.
- castTarget(slot,id), castPoint(slot,x,y), abilityCharges/Cooldown/Recharge(slot) [slots 0..3 = passive, primary, secondary, ultimate].
  Abilities are ALSO auto-cast by the engine on the current attack target (passive self-heal whenever hp<max; ult>secondary>primary).
- terrainKind/Walkable/Height/WaterDepth(x,y) [32 work each] (+At(x,y,layer)).
- Idle hero (no move target, no attack target) auto-acquires CREEPS ONLY: melee within 2.5 tiles, ranged within its range.
- Limits per decision: 20,000 instructions, 50,000 work units, 128 print events, 1024 print bytes. Division by zero = VM dies for the match.
  Syntax gotcha: a blank line directly before `end if`/`wend` fails to compile ("unexpected block terminator"). int32 only; `while/wend`, `if/then/else/end if` (no elseif, no for), `sub name(a,b) ... end sub` (no return values), `dim a(N)` top-level,
  `call`/direct sub call, `mod`, `and/or/not/xor` (no short-circuit), comments with `'` or `rem`. Globals persist across ticks. No strings.

## Items (id: effect, cost) — damage/HP apply to ANY class
1 ration +40hp 30g | 2 elixir +90hp 50g | 3 mana potion +60 45g | 4 poison: 35 dmg to current attack target in basic range, 40g
5 helmet +50hp 80g | 6 buckler +60hp 90g | 7 gauntlets +4dmg 70g | 8 boots +800 move/tick (~+12%) 100g | 9 amulet +70hp 120g | 10 ring +40mana 120g
11 dagger +8 110g | 12 wand +9 140g | 13 sword +10 150g | 14 bow +10 150g | 15 pauldrons +80hp 140g | 16 armor +120hp 160g
17 staff +6dmg+40hp 170g | 18 axe +14 180g | 19 crossbow +14 180g | 20 spellbook +12dmg+30mana 190g

## Local tooling
- Local episodes are deterministic per seed (default seed 2026; `-n N` increments it): identical policies reproduce identical games, so a
  single local game is an exact A/B for that seed. On seed 2026 the v49a Crossbowman beats nine base.bas heroes at tick 9665 with 2 deaths;
  removing its kiting (v61) gives 18945/10 deaths, heavier kiting (v59) 23360/9, the damage-only shop (v52b) 17144/11.
- `DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode ./coworld/cow_0752b441-af96-421d-8a1e-f8365a95e022/coworld_manifest.json <10 .bas paths> --variant competition -o runs/X`
  (~40 s per episode, 20x realtime). Results in runs/X/results.json, private prints in runs/X/logs/policy_agent_N.log.
- tools/probe.bas dumps map/objects. tools/eval.py runs A vs B both sides over seeds.

## Opponent notes (from hosted replays via tools/replay_parse.py, 2026-09-14)
- aaron-gota-ir-waveguard-r4:v2 (#1): as Blue sends VK+Arcanist+Druid up Blue lane 0 (toward Red's lane-0 towers) and Ranger+DH along lane 2;
  as Red sends DK+Warlock down lane 2, Crossbow+Lich along lane 0, Berserker mid. Heroes farm footmen near their towers and fight as a group.
  Beats a 5-stack that walks into its 3-hero group under a tower; otherwise loses the race.
- khors:v1: all five walk to (64,64) and camp mid. red-kite:v10: five-stack pushes mid together. Neither contests the side lanes.
- base.bas: nearest-enemy targeting, walks to (64,64) when idle.

## Policy engineering lessons (2026-09-14)
- No natural HP regen: a hero at low HP with no gold stays useless; potions, level-ups (max-HP delta heals) or a respawn are the only resets.
- Rejoin after respawn must be armed once by the respawn event; re-evaluating "rejoin" every tick resets the objective index and strands the hero at home.
- Do not walk to ally centroids (often inside rock/lake); follow the lane road (own gate -> inner -> outer) instead.
- Footman farming near enemy barracks stalls the push: attack footmen only when engaged (<= 2.4 tiles) or for kill shots (hp <= 30 in range).
- Lane switching pays off only against static defenders; against a pushing enemy stack it loses the race. Lane choice vs Aaron matters more.

## REGIME CHANGE (observed 2026-09-14 ~21:00 UTC): league seating is now `distinct_teammates: true`
Each league episode seats 10 DIFFERENT entrants: my policy controls ONE hero (its class is set by the seat: Red seat s -> class 5+s,
Blue seat s -> class s) alongside four other entrants' heroes. Score = 1 if my team's fort kill happens. Stack-only logic (cohesion
holds, regroup, lane switching with allies) is counterproductive here. XP A/B tests must use rosters with `{"random": true}` in the
other nine seats (tools/xp.py mixed) to model the league; five-clone rosters no longer reflect ladder play.
