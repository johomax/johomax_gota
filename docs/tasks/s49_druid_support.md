# Task S49 — Druid plays support: stay with allied heroes so the engine's auto-cast heals land (write policy/v160.bas from policy/v148.bas)
Base: policy/v148.bas (champion, game version 37). Copy to policy/v160.bas and apply ONLY the edits below. Only the Druid Warden
(selfClass = 3, Blue seat 8) changes behaviour.
Mechanics: the engine auto-casts abilities every tick a hero has an attack target (or the passive/heal kinds regardless): Healing Bloom
(heal 55, cooldown 168) and Kindred Wisps (heal 80, cooldown 288) are cast on the first damaged ALLIED hero within 4.0 tiles (Healing
Bloom range 240_000? — treat "within 4 tiles" as the working radius), Golem Seed is a strike. A Druid that pushes a side lane alone
heals nobody; one that stays within a few tiles of allied heroes adds ~135 HP per 288 ticks to the group. Our Druid currently wins
12-16 of 24 with 5.3 deaths per game and the lowest kill count of the Blue casters.
Existing names: selfClass, allyX(k)/allyY(k) and liveAllies (living allied heroes, filled in the scan), allyNear8, alliesWithin30,
centroidX/centroidY (mean of living allies), enemyHeroNear, bestFoot, bestHero, towerId, fortId, routing, lowHp, done/act, worldTick,
lastKite2Print (print pattern), d2 for the object in the scan loop.

1. Init (next to `lastKite2Print = -480`): `lastSupPrint = -480`, `supOn = 0`, then after the class/melee setup add
   `if selfClass = 3 then` / `supOn = 1` / `end if`.
2. Scan: add resets `supAllyD2 = 1000000`, `supAllyX = 0`, `supAllyY = 0` before `i = 0`; inside the allied-hero branch
   (`if k = 2 then` under `if t = selfTeam then`, where `objectId(i) <> selfId and objectAlive(i) = 1`), add:
   ```
   if d2 <= 900 and d2 < supAllyD2 then
     supAllyD2 = d2
     supAllyX = x
     supAllyY = y
   end if
   ```
   (nearest living allied hero within 30 tiles).
3. Decision rule: insert immediately AFTER the act 4 farm rule and BEFORE the melee movement block (`' melee: never run ahead ...`):
   ```
   ' Druid support: with an allied hero within 30 tiles, stay within 5 tiles of the nearest one so the auto-cast heals reach the group
   if done = 0 and supOn = 1 and routing = 0 and lowHp = 0 and fortId = 0 and supAllyD2 <= 900 and supAllyD2 > 25 then
     stepToward(supAllyX, supAllyY, selfX, selfY, 3)
     walkTo(sx, sy)
     done = 1
     act = 59
     if worldTick - lastSupPrint >= 480 then
       print "SUP " ; worldTick ; " d2 " ; supAllyD2
       lastSupPrint = worldTick
     end if
   end if
   ```
   (farming, hero fights, kiting and sieging keep priority because they precede this rule; the Druid only walks toward the ally when it
   has nothing better to do and is more than 5 tiles away; it stops 3 tiles short of the ally.)
4. Stuck detection: `if act = 9 or act = 11 or act = 47 then` -> `if act = 9 or act = 11 or act = 47 or act = 59 then`.
5. Header line after the v148 line: `' v160 = v148 + Druid support: stay within 5 tiles of the nearest allied hero (within 30) so the auto-cast heals land (SUP, act 59).`
Report edited line numbers and any deviation. Rules: int32 only, no elseif/for, NO blank line directly before `end if`/`wend`, NO
short-circuit evaluation; check supOn, supAllyD2, supAllyX, supAllyY, lastSupPrint do not clash (identifiers are case-insensitive).
