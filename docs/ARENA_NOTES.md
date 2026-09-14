# Gods of the Arena — mechanics notes (verified from polyworld@d03d2d1 source + local probe)

Game version 2026.9.14.2 (map changed to 128x128 on 2026-09-14; older wiki/book assume 64x64).

## Seating / scoring
- League `team_n` + `team_layout: blocks`: my policy fills ALL 5 seats of one team; opponent fills the other 5.
  Slots 0-4 = Red (team 0), 5-9 = Blue (team 1). Both sides get played across episodes.
- Winning team heroes score 1 each; loss 0; timeout (28,800 ticks) = 0 for everyone. Elo K=4.
- Observed league games end by fort kill in 3,500-12,500 ticks. Even with all heroes idle, footmen alone
  kill a fort in ~8,000 ticks (probe run). Timeouts are rare now; the game is a race + fights.

## Map (x right, y down, tiles 0..127; walkable: grass=1, road=2, marsh=5; NOT rock=3, trees=4, wall=6)
- Red fort id 1 at (115,12), Red hero spawn (123,5). Blue fort id 2 at (12,115), Blue spawn (3,122).
- Tower id = 10 + lane*6 + team*3 + tier (tier 0 outer, 1 inner, 2 gate). Towers only attackable outer->inner->gate.
  - Lane 0 (top/left L): Red gate 12 (95,4), inner 11 (77,12), outer 10 (23,12); Blue outer 13 (8,50), inner 14 (8,85), gate 15 (4,95)
  - Lane 1 (mid diagonal, crosses lake/marsh): Red gate 18 (106,21), inner 17 (89,32), outer 16 (71,46); Blue outer 19 (56,81), inner 20 (38,95), gate 21 (21,106)
  - Lane 2 (right/bottom L): Red gate 24 (123,32), inner 23 (119,42), outer 22 (119,77); Blue outer 25 (104,115), inner 26 (50,115), gate 27 (32,123)
- Fort exposed (attackable, objectAlive=1) once ANY lane has all 3 towers dead. Fort HP 400, attack range 4.25 tiles (any class). Forts do not attack.
- ASCII maps: docs/map_kinds.txt (F/f fort, W/w towers, H/h hero spawns), map_height.txt, map_water.txt.

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
- `DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode ./coworld/cow_.../coworld_manifest.json <10 .bas paths> -o runs/X`
  (~40 s per episode, 20x realtime). Results in runs/X/results.json, private prints in runs/X/logs/policy_agent_N.log.
- tools/probe.bas dumps map/objects. tools/eval.py runs A vs B both sides over seeds.
