# Task S23 — escort the allied Crossbowman (write policy/v68.bas from policy/v62.bas)
Base: policy/v62.bas (champion). GAME VERSION 33 (docs/ARENA_NOTES.md top): towers 1200/2400/4800 HP, 28/56/112 dmg, range 5/5.5/6 tiles.
The Crossbowman (class 6, range 6.5) is the only unit that sieges towers without taking tower damage; the engine makes ANY policy's
Crossbowman stand at 6.5 tiles when it attacks a tower. Crossbowmen die to enemy heroes that walk out to them. Red teams always have one
(seat 1). Our own Crossbowman seat wins 50% of games, other seats ~20%.
Add ONE behaviour for Red heroes that are not the Crossbowman (selfTeam = 0 and selfClass <> 6):
1. In the scan, find the allied Crossbowman (kind 2, team = selfTeam, objectClass = 6, alive): xbX, xbY, xbAlive; and its squared distance
   to the enemy fort (enemyFortX = mapWidth - 1 - homeX, enemyFortY = mapHeight - 1 - homeY): xbFortD2.
2. Every 240 ticks (worldTick mod 240 = 0) when routing = 0 and fortId = 0 and worldTick >= 900: escort mode is on for the next 240 ticks
   (escortUntil = worldTick + 240) if xbAlive = 1 and xbFortD2 <= 3600 (the Crossbowman is within 60 tiles of the enemy fort, i.e. forward,
   pushing). Print "ESCORT " ; worldTick once when escort mode starts (track prevEscort).
3. While worldTick < escortUntil and xbAlive = 1: if my squared distance to the Crossbowman > 25 (5 tiles) and no enemy hero is within my basic
   range and towerDanger = 0: walkTo(xbX, xbY), act = 35, done = 1 — placed AFTER the fort/standoff/kite rules and BEFORE the tower rules.
   Within 5 tiles the normal rules apply: fight enemy heroes in range (the existing hero rule, whose odds check now benefits from the ally
   count), siege with the existing gating (allIn = 1 because an ally is near), etc. Do not change pushLane/oi (escort ends -> resume the lane).
4. Lane commitment, join rule, weakest-lane rule and everything else stay unchanged.
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
