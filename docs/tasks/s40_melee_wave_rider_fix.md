# Task S40 — fix the melee wave rider (write policy/v136.bas from policy/v135.bas)
Base: policy/v135.bas (= v113 + S39, see docs/tasks/s39_melee_wave_rider.md). Copy it to policy/v136.bas and apply ONLY the edits below.
Local evidence (seed 2026, v135 Death Knight): the two-footman siege gate kept the hero at level 1 beside the enemy outer tower for
3000 ticks (v113 killed that tower at tick 1784 while its wave soaked it); and after the outer tower fell the hero still walked 50
tiles alone to the inner tower and died there, because the ride rule needs the objective tower visible (objStanding = 1) and an
allied footman within 30 tiles (frontFootFound = 1) — with the wave dead there was none.

1. Delete the S39 siege gate block (the three lines `if melee = 1 and siegeAllowed = 1 and waveAtTower < 2 and fortId = 0 and allIn = 0 and towerHp > 300 then` / `siegeAllowed = 0` / `end if`).
   Melee sieges under v113's rule again (any footman soaking, or fort/allIn/low tower).

2. First siege rule (act = 6, before the act 3 hero rule): its S39 tail `and (melee = 0 or bestFoot = 0 or towerHp <= 300)` becomes
   `and (melee = 0 or bestFoot = 0 or bestFootD2 > 9 or towerHp <= 300)` — a melee hero only prefers a footman over the tower when
   that footman is within 3 tiles (a quick last hit).

3. Ride rule (act = 47): remove `objStanding = 1 and` from its condition and add `and allIn = 0` (with an allied hero within 8
   tiles the existing dive logic applies). Final condition:
   `if done = 0 and melee = 1 and routing = 0 and lowHp = 0 and fortId = 0 and openLane < 0 and otype = 1 and oi >= 3 and allIn = 0 and frontFootFound = 1 and frontD2 > 16 and myD2 < frontObjD2 then`

4. New hold rule, inserted immediately AFTER the ride rule's `end if` (before the second act 6 siege rule):
   ```
   ' melee: no allied footman within 30 tiles on the way to an enemy tower -> do not trickle in alone; back off from heroes, else wait for the next wave
   if done = 0 and melee = 1 and routing = 0 and lowHp = 0 and fortId = 0 and openLane < 0 and otype = 1 and oi >= 3 and allIn = 0 and frontFootFound = 0 and towerDanger = 0 then
     if enemyHeroNear > 0 then
       stepToward(selfX, selfY, rx, ry, 6)
       walkTo(sx, sy)
       act = 50
     else
       walkTo(selfX, selfY)
       act = 49
     end if
     done = 1
     if worldTick - lastHoldPrint >= 480 then
       print "HOLDW " ; worldTick ; " act " ; act
       lastHoldPrint = worldTick
     end if
   end if
   ```
   Init `lastHoldPrint = -480` next to `lastRidePrint = -480`. stepToward(fx, fy, tx, ty, k) already exists and sets sx/sy.

5. Header comment: `' v136 = v135 with v113's siege gate restored, ride without tower sight, and a hold when no wave is near.`
Nothing else changes. Report the edits with line numbers and the final melee rule order. Rules: int32 only, no elseif/for, NO blank
line directly before `end if` or `wend` (compile error); check `lastHoldPrint` does not clash.
