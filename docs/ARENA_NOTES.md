# Gods of the Arena — mechanics notes (verified from polyworld@d03d2d1 source + local probe)

Game version 2026.9.14.3 (map generation changed on 2026-09-14; older wiki/book assume 64x64). Source commit 275ba23.

## Seating / scoring
- League `team_n` + `team_layout: blocks`: my policy fills ALL 5 seats of one team; opponent fills the other 5.
  Slots 0-4 = Red (team 0), 5-9 = Blue (team 1). Both sides get played across episodes.
- Winning team heroes score 1 each; loss 0; timeout (28,800 ticks) = 0 for everyone. Elo K=4.
- Observed league games end by fort kill in 3,500-12,500 ticks. Even with all heroes idle, footmen alone
  kill a fort in ~8,000 ticks (probe run). Timeouts are rare now; the game is a race + fights.

## Map (CURRENT league coworld cow_0752b441-af96-421d-8a1e-f8365a95e022, version 2026.9.14.4 (cow_0752b441; same map hash 6EB3A6B3 as 2026.9.14.3), map_size 116)
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
  Syntax: int32 only; `while/wend`, `if/then/else/end if` (no elseif, no for), `sub name(a,b) ... end sub` (no return values), `dim a(N)` top-level,
  `call`/direct sub call, `mod`, `and/or/not/xor` (no short-circuit), comments with `'` or `rem`. Globals persist across ticks. No strings.

## Items (id: effect, cost) — damage/HP apply to ANY class
1 ration +40hp 30g | 2 elixir +90hp 50g | 3 mana potion +60 45g | 4 poison: 35 dmg to current attack target in basic range, 40g
5 helmet +50hp 80g | 6 buckler +60hp 90g | 7 gauntlets +4dmg 70g | 8 boots +800 move/tick (~+12%) 100g | 9 amulet +70hp 120g | 10 ring +40mana 120g
11 dagger +8 110g | 12 wand +9 140g | 13 sword +10 150g | 14 bow +10 150g | 15 pauldrons +80hp 140g | 16 armor +120hp 160g
17 staff +6dmg+40hp 170g | 18 axe +14 180g | 19 crossbow +14 180g | 20 spellbook +12dmg+30mana 190g

## Local tooling
- `DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode ./coworld/cow_0752b441-af96-421d-8a1e-f8365a95e022/coworld_manifest.json <10 .bas paths> --variant competition -o runs/X`
  (~40 s per episode, 20x realtime). Results in runs/X/results.json, private prints in runs/X/logs/policy_agent_N.log.
- tools/probe.bas dumps map/objects. tools/eval.py runs A vs B both sides over seeds.

## Opponent notes (from hosted replays via tools/replay_parse.py, 2026-09-14)
- aaron-gota-ir-waveguard-r4:v2 (#1): as Blue sends VK+Arcanist+Druid up Blue lane 0 (toward Red's lane-0 towers) and Ranger+DH along lane 2;
  as Red sends DK+Warlock down lane 2, Crossbow+Lich along lane 0, Berserker mid. Heroes farm footmen near their towers and fight as a group.
  Beats a 5-stack that walks into its 3-hero group under a tower; otherwise loses the race.
- khors:v1: all five walk to (64,64) and camp mid. red-kite:v10: five-stack pushes mid together. Neither contests the side lanes.
- base.bas: nearest-enemy targeting, walks to (64,64) when idle.
