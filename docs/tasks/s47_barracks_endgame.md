# Task S47 — version 37: hit an exposed enemy barracks instead of diving a defended fort alone (write policy/v150.bas from policy/v148.bas)
Base: policy/v148.bas (champion on game version 37). Copy to policy/v150.bas and apply ONLY the edits below.
Version-37 facts: barracks are buildings of object kind 5 (ids 40+, two per lane per team, 950 HP, they never attack) and are
attackable (objectAlive(i) = 1) once every tower of their lane is dead — the same moment the fort becomes exposed. Each living
barracks spawns 3 creeps per wave, so killing one halves that lane's enemy creeps and killing both stops them. The fort (400 HP) still
ends the game, but our hero currently dives it alone (act 5) even when two or more enemy heroes defend it, and dies there.
Existing names: fortId (exposed & visible enemy fort id, 0 otherwise), allyNear8, enemyHeroNear (living enemy heroes within 10
tiles), allIn, lowHp, routing, done/act, worldTick, lastKite2Print (rate-limited print pattern), the scan loop (`while i < n`, enemy
branch `else` with `if k = 2`, `if k = 3`, `if k = 4`, `if k = 1`), d2 (squared distance to object i), x/y.

1. Scan resets (with the others before `i = 0`): `barId = 0`, `barD2 = 1000000`.
2. In the ENEMY branch add, at the same level as the `if k = 4 then` block:
   ```
   if k = 5 then
     if objectAlive(i) = 1 and d2 <= 625 and d2 < barD2 then
       barD2 = d2
       barId = objectId(i)
     end if
   end if
   ```
   (nearest attackable enemy barracks within 25 tiles).
3. Init (next to `lastRidePrint = -480`): `lastBarPrint = -480`.
4. Decision: insert immediately BEFORE the fort rule (comment `' end the game first: an exposed fort in reach beats any fight`, act = 5):
   ```
   ' version 37: a defended fort is not worth a solo dive - take the lane's barracks instead (each one feeds 3 creeps per wave)
   if done = 0 and barId <> 0 and routing = 0 and lowHp = 0 and allIn = 0 and enemyHeroNear >= 2 then
     attackTarget(barId)
     done = 1
     act = 56
     if worldTick - lastBarPrint >= 480 then
       print "BARR " ; worldTick ; " id " ; barId ; " eh " ; enemyHeroNear
       lastBarPrint = worldTick
     end if
   end if
   ```
   and immediately AFTER the second siege rule (the act = 6 rule that follows the act 4 farm rule and the melee movement block) and
   BEFORE the `' wait for the next wave just outside the tower's reach` rule (act 22), add the idle case:
   ```
   ' version 37: nothing to siege or farm but an exposed barracks in reach -> kill it
   if done = 0 and barId <> 0 and routing = 0 and lowHp = 0 and towerId = 0 and bestFoot = 0 and barD2 <= 144 then
     attackTarget(barId)
     done = 1
     act = 57
   end if
   ```
5. Header line after the v148 line: `' v150 = v148 + version-37 barracks: attack an exposed enemy barracks instead of a solo fort dive against >= 2 defenders, and when idle within 12 tiles of one (BARR, acts 56/57).`
Report the edited line numbers and any deviation. Rules: int32 only, no elseif/for, NO blank line directly before `end if`/`wend`,
NO short-circuit evaluation (guard array indices), identifiers case-insensitive — check barId, barD2, lastBarPrint do not clash.
