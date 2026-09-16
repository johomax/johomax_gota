# Task S45 — race-aware gate defence (write policy/v143.bas from policy/v139.bas)
Base: policy/v139.bas (champion). Copy to policy/v143.bas and apply ONLY the edits below.
Evidence (240 hosted games + 171 league replays): games are mutual gate sieges — in our losses our team is at the enemy gate in 75%
of games and the enemy is at ours; the phase from the first gate hit to the end lasts ~3700 ticks; in losses our hero spends 47% of
that phase walking (act 9) and 3% sieging. A hero standing under its own gate tower (1800 HP, 30 dmg per 24 ticks) kills the enemy
wave with the tower (last hits = XP), and enemy heroes must back off. Idea: when one of OUR gate towers is under hero+wave attack
and the enemy gate in our push lane is far from falling, go and hold our gate; otherwise keep pushing.

Facts you need: our own towers are always in the object list (team = selfTeam, kind 4); tower id = 10 + lane*6 + team*3 + tier
(tier 2 = gate); own tower positions were stored at init as routeX(lane*7 + 2 - tier)/routeY(...), so our gate of lane L is at
(routeX(L*7), routeY(L*7)); homeX/homeY = our fort; laneTowerHp(lane*3 + tier) = enemy tower HP in that lane (unseen default is
large); pushLane = our lane; fortId <> 0 = enemy fort exposed; openLane >= 0 = an enemy lane is open; routing = lane travel;
stepToward(fx, fy, tx, ty, k) sets sx/sy = the point k tiles from (fx,fy) toward (tx,ty). Scan loop: `while i < n` with
`if t = selfTeam then` (allied branch: k = 3 footmen, k = 2 heroes) `else` (enemy branch: k = 2 heroes, k = 3 footmen, k = 4 towers, k = 1 forts).

1. Top-level dims (next to the other `dim` lines): `dim gateFoot(3)`, `dim gateHero(3)`, `dim gateHp(3)`, `dim gateAlive(3)`.
2. Init (first-tick block, next to `lastRidePrint = -480`): `defendUntil = 0`, `defLane = -1`, `lastDefPrint = -480`.
3. Scan resets (right before `i = 0` / `n = objectCount()`):
   ```
   gl = 0
   while gl < 3
     gateFoot(gl) = 0
     gateHero(gl) = 0
     gateHp(gl) = 0
     gateAlive(gl) = 0
     gl = gl + 1
   wend
   ```
4. In the ALLIED branch add a tower case (same level as the `if k = 3 ...` and `if k = 2 ...` blocks there):
   ```
   if k = 4 then
     towerOffset = objectId(i) - (10 + selfTeam * 3)
     gl = towerOffset / 6
     if towerOffset mod 6 = 2 and gl >= 0 and gl <= 2 then
       gateHp(gl) = objectHp(i)
       if objectHp(i) > 0 then
         gateAlive(gl) = 1
       end if
     end if
   end if
   ```
   (towerOffset is already a variable name used in the enemy tower case; reusing it here is fine.)
5. In the ENEMY branch, inside the living-footman case (`if k = 3 then` ... where `objectAlive(i) = 1`), add a lane loop counting
   enemy footmen within 10 tiles of each of our gates; and inside the living enemy-hero case (`if k = 2 then` / `if objectAlive(i) = 1 then`)
   the same within 12 tiles:
   ```
   gl = 0
   while gl < 3
     gdx = x - routeX(gl * 7)
     gdy = y - routeY(gl * 7)
     if gdx * gdx + gdy * gdy <= 100 then
       gateFoot(gl) = gateFoot(gl) + 1
     end if
     gl = gl + 1
   wend
   ```
   (for heroes: `<= 144` and `gateHero(gl) = gateHero(gl) + 1`). Guard the footman version with `if objectAlive(i) = 1 then` if the
   surrounding code does not already guarantee it.
6. After the scan loop (`wend`) and BEFORE the `' ---------- decide ----------` section, add the threat evaluation and activation:
   ```
   ' race-aware defence: which of our gates is under hero + wave attack?
   gateThreatLane = -1
   gateThreatScore = 0
   gl = 0
   while gl < 3
     if gateAlive(gl) = 1 and gateHero(gl) >= 1 and (gateFoot(gl) >= 2 or gateHp(gl) < 1200) then
       gateScore = gateFoot(gl) * 2 + gateHero(gl) * 5
       if gateScore > gateThreatScore then
         gateThreatScore = gateScore
         gateThreatLane = gl
       end if
     end if
     gl = gl + 1
   wend
   defending = 0
   if gateThreatLane >= 0 and fortId = 0 and openLane < 0 and routing = 0 and worldTick >= 2400 and laneTowerHp(pushLane * 3 + 2) > 900 then
     defendUntil = worldTick + 480
     defLane = gateThreatLane
   end if
   if worldTick < defendUntil and defLane >= 0 and gateAlive(defLane) = 1 and fortId = 0 and routing = 0 then
     defending = 1
     stepToward(routeX(defLane * 7), routeY(defLane * 7), homeX, homeY, 3)
     defX = sx
     defY = sy
   end if
   ```
   NOTE: openLane is computed inside the decide section in v139 (block `'' an enemy lane is open`). If it is not yet available at
   this point, move ONLY the `defending = 0 ... end if` activation part (not the threat loop) to just after the openLane block and
   say so in the report.
7. Escort rule (act = 35, condition contains `worldTick < escortUntil and xbAlive = 1 and xbD2 > 25`): append ` and defending = 0`.
8. Defence movement: insert immediately BEFORE the home-guard block (comment `' home guard: a respawned hero waits ...`, act 14):
   ```
   ' hold our threatened gate under its tower; farm/fight rules above keep priority
   if done = 0 and defending = 1 then
     dfx = defX - selfX
     dfy = defY - selfY
     if dfx * dfx + dfy * dfy > 36 then
       walkTo(defX, defY)
       act = 51
     else
       act = 52
     end if
     done = 1
     if worldTick - lastDefPrint >= 480 then
       print "DEF " ; worldTick ; " lane " ; defLane ; " foot " ; gateFoot(defLane) ; " hero " ; gateHero(defLane) ; " hp " ; gateHp(defLane)
       lastDefPrint = worldTick
     end if
   end if
   ```
   (act 52 issues NO command on purpose: the hero stands at the defence point and the engine auto-acquires creeps in range.)
9. Stuck detection: `if act = 9 or act = 11 or act = 47 then` -> `if act = 9 or act = 11 or act = 47 or act = 51 then`.
10. Header line after the v139 line: `' v143 = v139 + race-aware gate defence: hold our own gate under its tower while enemy heroes and a wave siege it and the enemy gate is far from falling (DEF, acts 51/52).`
Report: edits with line numbers, where the activation ended up relative to openLane, and any deviation. Rules: int32 only, no
elseif/for, NO blank line directly before `end if`/`wend`; identifiers are case-insensitive — check gl, gdx, gdy, dfx, dfy, defX,
defY, defLane, defending, defendUntil, gateScore, gateThreatLane, gateThreatScore, lastDefPrint and the four arrays do not clash.
Budget: the two lane loops run per visible enemy object (3 iterations each) — well inside 20k instructions.
