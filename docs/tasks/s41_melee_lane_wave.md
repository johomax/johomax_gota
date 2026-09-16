# Task S41 — melee heroes move with their lane's creep wave (write policy/v137.bas from policy/v113.bas)
Base: policy/v113.bas (champion). Copy to policy/v137.bas and apply ONLY the edits below. Ranged behaviour (melee = 0) must not change.
Evidence: our melee heroes (VK/DH/DK/Berserker, `melee = 1`) die 4-6 times per game, mostly while walking alone to a far enemy tower
(act 9): the server path from our spawn to the enemy inner tower is a diagonal through the map centre, where enemy heroes camp,
and after a wave is wiped the hero keeps pushing on alone. v135/v136 tried a wave anchor limited to 30 tiles without a lane test
and mid-lane footmen were mistaken for our wave. Lanes are physical (tower id = 10 + lane*6 + team*3 + tier): lane 0 is the
top/left L (road x <= 13 or y <= 17), lane 1 the diagonal x + y ~ 115, lane 2 the right/bottom L (x >= 102 or y >= 98). pushLane
holds our current physical lane (Red starts on 2, Blue on 0; adoptLane changes it).

Existing names: melee, routing, lowHp, fortId, openLane, otype (1 = tower/fort objective), oi (3+ = enemy structures), ox/oy/myD2
(objective and our squared distance to it, computed BEFORE the scan), allIn (allied hero within 8 tiles or tick >= 12000),
towerDanger, enemyHeroNear, rx/ry (retreat point), stepToward(fx,fy,tx,ty,k) -> sx/sy, done/act, lastKite2Print (print pattern).
Object scan: one `while i < n` loop; allied footmen are handled in `if t = selfTeam then` / `if k = 3 and objectAlive(i) = 1 then`.

1. Init (first-tick block, next to `lastKite2Print = -480`): `lastRidePrint = -480` and `lastHoldPrint = -480`.

2. Scan resets (with the other resets right before `i = 0`): `frontFound = 0`, `frontObjD2 = 1000000`, `frontX = 0`, `frontY = 0`, `frontD2 = 1000000`.
   Inside the allied-footman branch (same level as the waveAtTower block) add the lane test and the front-of-wave pick:
   ```
   inLane = 0
   if pushLane = 2 and (x >= 102 or y >= 98) then
     inLane = 1
   end if
   if pushLane = 0 and (x <= 13 or y <= 17) then
     inLane = 1
   end if
   if pushLane = 1 then
     laneS = x + y - 115
     if laneS < 0 then
       laneS = 0 - laneS
     end if
     if laneS <= 14 then
       inLane = 1
     end if
   end if
   if inLane = 1 then
     wfx = x - ox
     wfy = y - oy
     wfd2 = wfx * wfx + wfy * wfy
     if wfd2 < frontObjD2 then
       frontObjD2 = wfd2
       frontX = x
       frontY = y
       frontD2 = d2
       frontFound = 1
     end if
   end if
   ```
   (front = the living allied footman in OUR lane that is nearest to the current objective, at any distance).

3. Movement discipline for melee: insert immediately AFTER the act 4 farm rule (`... act = 4` / `end if`) and BEFORE the second
   act 6 siege rule:
   ```
   ' melee: move with our lane's wave toward an enemy tower - catch it from far behind, never run ahead of it, hold when it is gone
   if done = 0 and melee = 1 and routing = 0 and lowHp = 0 and fortId = 0 and openLane < 0 and otype = 1 and oi >= 3 and allIn = 0 and towerDanger = 0 then
     if frontFound = 1 then
       if frontD2 > 16 and (myD2 < frontObjD2 or frontD2 > 400) then
         walkTo(frontX, frontY)
         done = 1
         act = 47
         if worldTick - lastRidePrint >= 480 then
           print "RIDE " ; worldTick ; " to " ; frontX ; " " ; frontY
           lastRidePrint = worldTick
         end if
       end if
     else
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
   end if
   ```
   Meaning: ahead of the front footman (closer to the objective than it) or more than 20 tiles behind it -> walk to the footman
   (paths that hug our lane instead of the diagonal); within 20 tiles behind it -> the normal rules continue (act 9 walks to the
   objective, which is beside the front); no living footman of ours in the lane -> back off from heroes or stand and wait.

4. Stuck detection: change `if act = 9 or act = 11 then` (the block printing "STUCK") to `if act = 9 or act = 11 or act = 47 then`
   so long act-47 walks are un-stuck like objective walks (the `else` branch below it keeps `if act <> 10 then stuckTicks = 0`).

5. Header comment: `' v137 = v113 + melee heroes move with their lane's creep wave (catch it, never outrun it, hold when it is gone).`
Nothing else changes (no siege/farm/hero-rule edits). Report: new variables, insertion line numbers, the melee rule order, and any
deviation. Rules: int32 only, no elseif/for, NO blank line directly before `end if` or `wend` (compile error); identifiers are
case-insensitive — do not reuse fx/fy (stepToward parameters); check inLane, laneS, wfx, wfy, wfd2, front*, lastRidePrint,
lastHoldPrint do not clash with existing names.
