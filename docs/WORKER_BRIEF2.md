# Brief for policy workers (Codex) — solo-hero regime (2026-09-14, 23:10 UTC)

You improve a BASIC hero policy for Gods of the Arena. Work ONLY inside /Users/jordan/Desktop/Projects/johomax/gota.
Do not touch git. You cannot run Docker or any game episode: self-check the BASIC very carefully instead.

## Regime (read this, it changed today)
League episodes seat ten DIFFERENT entrants: this policy controls ONE hero with four strangers as teammates and five strangers
as enemies. The class is fixed by the seat: Red seats 0-4 -> classes 5 DeathKnight, 6 Crossbowman, 7 Lich, 8 Warlock, 9 Berserker;
Blue seats 5-9 -> classes 0 VanguardKnight, 1 Ranger, 2 Arcanist, 3 DruidWarden, 4 DemonHunter. Score = 1 if my team kills the
enemy fort. Hosted measurement (240 random-roster games, 24 per seat) of the current champion policy/v19.bas:
seat0 DK 12/24, s1 Xbow 11/24, s2 Lich 11/24, s3 Warlock 10/24, s4 Berserker 13/24, s5 VK 18/24, s6 Ranger 10/24, s7 Arcanist 16/24,
s8 Druid 15/24, s9 DH 16/24. Total 55%. A random champion wins 41% as Red and 59% as Blue (class asymmetry), so v19 adds only ~5 points.
Our hero dies ~2 times per game (losses: 2.5-4 deaths, wins: 1.6). A death costs 216 ticks + a 1500-2000 tick walk back
(heroes move ~0.1 tile/tick, the lane is ~220 tiles). Games last 6000-9000 ticks. There is NO natural HP regen.

## Verified mechanics (engine source, examples/gods_of_the_arena/sim.nim + content.nim)
- Map 116x116, point-symmetric: enemy(x,y) = (115-x,115-y). Tower id = 10 + lane*6 + team*3 + tier (tier 0 outer, 1 inner, 2 gate).
  Towers are attackable only outer->inner->gate (objectAlive(i)=1 means exposed AND hp>0; an unexposed tower still SHOOTS).
  Fort (400 HP, id 1 Red / 2 Blue) is exposed once any lane's three towers are dead; attack it from within 4.25 tiles; forts do not shoot.
- Towers: HP 600/800/1000, damage 14/18/22 every 24 ticks, ranges 5.0/5.5/6.0 tiles (outer/inner/gate). They target FOOTMEN first
  (nearest), heroes only when no enemy footman is in range. `within` = distance <= range (planar, tile = 60000 units).
- Hero basic-attack ranges (tiles): VK 1.17, Ranger 5.5, Arcanist 5.0, Druid 4.0, DH 1.25, DK 1.27, Crossbow 6.5, Lich 5.5, Warlock 4.5,
  Berserker 1.33. Attack period ticks: 24,18,30,26,16,28,36,32,28,20. Base damage: 25,25,38,22,32,30,43,36,26,35 (+5,6,8,4,7,6,8,8,5,7 per level).
  Base HP: 330,210,190,250,220,350,230,185,240,300. A hero attacking a tower stands at max(classRange, 1.75 tiles) -> the Crossbowman
  (6.5) out-ranges every tower; Ranger/Lich (5.5) out-range only the outer tower (5.0); everyone else is inside tower range while sieging.
- Footmen: 60 HP, 12 dmg / 32 ticks, 2 per lane per team every 240 ticks. Rewards go to the hero that lands the killing blow:
  footman 25xp/15g, hero 150xp/100g, tower 100xp/75g. Level-up: XP to next = 100+75*(lvl-1); level-up raises max HP (heals the delta).
- Vision is team-shared (hero 10 tiles, footman 5, tower ~7, fort ~16). Enemy objects appear only when visible; own objects always.
- Death: 24 ticks dying + 192 respawn at own spawn with full HP.
- Items (id: effect, cost): 1 ration +40hp 30g, 2 elixir +90hp 50g, 7 gauntlets +4dmg 70g, 8 boots +800 move/tick 100g, 11 dagger +8dmg 110g,
  13 sword +10 150g, 16 armor +120hp 160g, 18 axe +14dmg 180g, 19 crossbow +14 180g. Any class can use any item. 6 inventory slots.

## Host API (per hero VM, one decision per tick)
Data: selfId selfTeam selfClass selfX selfY selfHp selfMaxHp selfMana selfMaxMana selfGold selfLevel worldTick mapWidth mapHeight.
objectCount(), objectId/Kind/Team/Class/X/Y/Hp/Alive(i): kinds 1 fort, 2 hero, 3 footman, 4 tower; order forts, towers, heroes, footmen.
walkTo(x,y) (800 work units; clears the attack target; returns 0 if no path), attackTarget(id) (paths into range then attacks; target dropped
when not visible), attackTarget(0) stops. buyItem(id), useItem(slot), itemId(slot). Exactly one walkTo/attackTarget per tick matters (last wins).
Limits per decision: 20,000 instructions, 50,000 work units (object queries cost 4 each, walkTo 800), print <= 128 events / 1024 bytes.
Idle hero (no move/attack target) auto-attacks CREEPS only within its range (melee 2.5 tiles).

## BASIC dialect (compile errors fail the episode)
- Identifiers are CASE-INSENSITIVE and share one namespace (scalar `ox` clashes with array `oX`). No `elseif`, no `for`, no single-line if.
  Blocks: `if c then` / `else` / `end if`; `while c` / `wend`. `sub name(a,b)` ... `end sub`, no return values (write globals). `exit sub` ok.
- `dim arr(N)` only at top level. Globals persist across ticks; sub params are local. int32 only; `and`/`or` do NOT short-circuit;
  division by zero kills the VM for the match (guard every divisor). Comments with `'`. No strings except in print.
- Distances: the code uses squared tile distances (d2). Keep that style.

## Structure of policy/v19.bas (the base you modify)
init (tick 1): reads own towers/fort, builds routeX/Y/Id/Kind for 3 lanes x 7 points (own gate, inner, outer, enemy outer, inner, gate, fort),
loads pushLane (Red 2, Blue 0) into wpX/wpY/wpId/wpKind; class range `rng` (tenths of tiles), `melee`, heroR2/footR2 thresholds.
telemetry -> shopping -> objective (oi index into the 7 points, advance when reached/destroyed; rx,ry = previous point) -> scan loop over
all objects (allies, enemy heroes -> bestHero lowest hp in range, footmen -> bestFoot engaged/kill-shot, towers -> towerId nearest exposed
within 9 tiles, fortId within 14 tiles, defenders) -> lane resistance/rejoin (stack-era logic) -> decide block (ordered rules with `done`):
flee <15% hp, kite melee (ranged), fort, tower with no enemy hero adjacent, hero, footman, tower, crippled reset, home guard after respawn,
walk to objective with hold/unstick logic -> stuck detection -> "T" telemetry every 480 ticks.
Telemetry lines the orchestrator parses: "T tick p x y hp h/m Ln gG oi N act A eh E al L", "K tick +gold", "D tick respawn #n", "STUCK ...".
Keep them intact and add new prints sparingly (<= 1024 bytes per tick).

## Deliverable
Write the new policy to the path named in your task (copy v19.bas, then make ONE focused change; keep everything else byte-identical).
Keep `clash = 0` exactly as in v19. Then reply with: the change (one paragraph), the code regions touched, risks, and what telemetry
would confirm the mechanism. Re-read your file top to bottom for dialect errors (case-insensitive name clashes with existing globals such as
ox, oy, oi, rx, ry, sx, sy, sq, dx, dy, d2, i, n, k, t, x, y, hp, id, c are the most common bug). Do not modify v19.bas, tools/, docs/, or git.
