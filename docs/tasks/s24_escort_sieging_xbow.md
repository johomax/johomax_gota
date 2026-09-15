# Task S24 — escort the allied Crossbowman only while it is sieging (write policy/v69.bas from policy/v68.bas)
Base: policy/v68.bas (v62 + escort: Red non-Crossbowman heroes walk to within 5 tiles of the allied Crossbowman whenever it is within
60 tiles of the enemy fort). First duel vs v62: 38/28 — promising. Refine the trigger so we escort only when it matters:
1. In the scan, enemy towers are enumerated BEFORE heroes. Record every EXPOSED living enemy tower (objectAlive(i) = 1, kind 4, team <>
   selfTeam) into arrays expTX(8)/expTY(8) with a counter expTowers (cap 9).
2. When the allied Crossbowman is found (existing xbX/xbY/xbAlive code), compute xbSiege = 1 if any recorded exposed enemy tower is within
   8 tiles of it (d2 <= 64), else 0.
3. Escort trigger (replace the xbFortD2 <= 3600 test): escort when xbAlive = 1 and (xbSiege = 1 or an enemy hero is within 10 tiles of the
   Crossbowman — compute in the enemy-hero part of the scan as xbThreat using xbX/xbY; heroes enumerate after allies so xbX/xbY are known).
   Keep the 240-tick renewal, the 5-tile follow distance, act = 35 and the "ESCORT" print.
4. Everything else unchanged.
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
