# Task S39 — melee heroes ride the wave (write policy/v135.bas from policy/v113.bas)
Base: policy/v113.bas (champion). Copy it to policy/v135.bas and apply ONLY the edits below. Ranged behaviour must not change.
Evidence: in hosted games our melee classes (VK/DH/DK/Berserker, `melee = 1`) win 0.31-0.56 while the best opponent's win 0.53-0.59
with the same classes. Ours reach the enemy outer tower at tick ~1000 ahead of any creep wave, siege it at level 1, push on alone
to the inner tower and die there 4-6 times per game (act 9 "walk to objective" precedes most deaths); they farm only 9-15% of the
time (act 4) and finish at level 4.6-5.3. The opponent's melee heroes attack twice as many footmen and touch a tower ~1300 ticks later.

Existing names you will use (all already defined in v113): melee, routing, lowHp, fortId, openLane, otype (wpKind of the objective:
1 = tower/fort, 0 = plain route point), objStanding (objective tower visible and alive), oi (0 own gate, 1 own inner, 2 own outer,
3 enemy outer, 4 enemy inner, 5 enemy gate, 6 enemy fort), ox/oy/myD2 (objective and our squared distance to it — computed BEFORE the
scan), towerId/towerHp/towerRange, waveAtTower, allIn, siegeAllowed, towerDanger, bestFoot, bestHero/bestHeroHp/bestHeroD2,
allyNear8, enemyHeroNear, nearHeroD2, done/act, worldTick, lastKite2Print (pattern for rate-limited prints).
Object scan: one `while i < n` loop; allied footmen are handled in the branch `if t = selfTeam then` / `if k = 3 and objectAlive(i) = 1 then`
(it counts waveAtTower and nearTowerWave). Towers enumerate before footmen, so towerId is valid there.

1. Init (inside the `if worldTick <= 1` / first-tick block, next to `lastKite2Print = -480`): add `lastRidePrint = -480`.

2. Scan variables (with the other resets right before `i = 0` / `n = objectCount()`): `frontFootFound = 0`, `frontObjD2 = 1000000`,
   `frontX = 0`, `frontY = 0`, `frontD2 = 1000000`.
   Inside the allied-footman branch (`if k = 3 and objectAlive(i) = 1 then`, same level as the waveAtTower block), add:
   ```
   if d2 <= 900 then
     wfx = x - ox
     wfy = y - oy
     wfd2 = wfx * wfx + wfy * wfy
     if wfd2 < frontObjD2 then
       frontObjD2 = wfd2
       frontX = x
       frontY = y
       frontD2 = d2
       frontFootFound = 1
     end if
   end if
   ```
   (the living allied footman within 30 tiles of us that is nearest to the current objective = the front of our wave).

3. Siege gate: directly after the existing block
   `siegeAllowed = 0 / if towerId <> 0 and (rng > towerRange or waveAtTower >= 1 or fortId <> 0 or allIn = 1 or towerHp <= 300) then / siegeAllowed = 1 / end if`
   add:
   ```
   if melee = 1 and siegeAllowed = 1 and waveAtTower < 2 and fortId = 0 and allIn = 0 and towerHp > 300 then
     siegeAllowed = 0
   end if
   ```
   (a melee hero only hits a healthy tower while at least two of our footmen soak it).

4. First siege rule (comment `' a tower in reach with no enemy hero adjacent to me: keep sieging`, act = 6, the one BEFORE the act 3
   hero rule): append to its condition ` and (melee = 0 or bestFoot = 0 or towerHp <= 300)` so a melee hero farms (act 4) before it
   sieges; the second act 6 rule after act 4 is unchanged.

5. Hero rule (act = 3, condition starts `if done = 0 and routing = 0 and bestHero <> 0 and (allyNear8 + 1 >= enemyHeroNear or ...`):
   append ` and (melee = 0 or bestHeroD2 <= 4 or bestHeroHp * 2 < selfHp or allIn = 1)` — a melee hero only opens on an enemy hero
   that is already adjacent (within 2 tiles), nearly dead, or when an ally is within 8 tiles.

6. Ride rule: insert immediately AFTER the act 4 farm rule (`if done = 0 and bestFoot <> 0 and (routing = 0 or ...` ... `act = 4` / `end if`)
   and BEFORE the second act 6 siege rule:
   ```
   ' melee: never run ahead of the wave at a standing enemy tower; fall back to the front footman instead
   if done = 0 and melee = 1 and routing = 0 and lowHp = 0 and fortId = 0 and openLane < 0 and otype = 1 and objStanding = 1 and oi >= 3 and frontFootFound = 1 and frontD2 > 16 and myD2 < frontObjD2 then
     walkTo(frontX, frontY)
     done = 1
     act = 47
     if worldTick - lastRidePrint >= 480 then
       print "RIDE " ; worldTick
       lastRidePrint = worldTick
     end if
   end if
   ```
   Check that openLane is computed before this point in the file (it is set in the `'' an enemy lane is open` block, which precedes
   the escort/siege rules); if it is not, say so in the report instead of moving code.

7. Update the header comment line of the new file (`' v135 = v113 + melee wave riding ...`). Nothing else changes.
Report: the new variables, each insertion with line numbers, the final rule order for melee (acts 15/35/6/3/4/47/6/22/...), and any
deviation. Rules: int32 only, no elseif/for, NO blank line directly before `end if` or `wend` (compile error), identifiers are
case-insensitive (check `wfx`, `wfy`, `wfd2` (fx/fy are stepToward parameters — do not reuse them), `frontX`, `frontY`, `frontD2`, `frontObjD2`, `frontFootFound`, `lastRidePrint` do not clash).
