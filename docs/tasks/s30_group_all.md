# Task S30 — every non-Crossbowman hero sticks with the largest allied group (write policy/v84.bas from policy/v76.bas)
Base: policy/v76.bas (champion). GAME VERSION 36 (docs/ARENA_NOTES.md top): towers 900/1200/1800 HP, 18/24/30 dmg; games are decisive
and won by groups that break a lane and reach the fort. v70 applied a "follow the largest allied group" rule to the Vanguard Knight and Druid
only and scored 10/72 vs 6/72 on those seats. Apply the same rule to every class except the Crossbowman (selfClass <> 6), on top of v76:
1. In the scan collect living allied hero positions (allyX/allyY arrays exist for the join rule; also record allyId(9)).
2. Every 240 ticks (worldTick mod 240 = 0) when routing = 0 and fortId = 0 and worldTick >= 900: the anchor is the allied hero with the most
   OTHER allies within 12 tiles (d2 <= 144); if it has >= 1 such neighbour, set groupUntil = worldTick + 240, remember anchorId and refresh
   anchorX/anchorY every tick while the anchor is alive. Print "GROUP " ; worldTick once per episode (track prevGroup).
3. While worldTick < groupUntil and the anchor is alive: if my squared distance to the anchor > 36 (6 tiles) and no enemy hero is within my
   basic range and towerDanger = 0 and no fort/open-lane rush is active (fortId = 0 and openLane = -1): walkTo(anchorX, anchorY), act = 36,
   done = 1 — placed AFTER the fort/open-lane/standoff/kite rules and BEFORE the tower rules. Within 6 tiles the normal rules apply.
4. Do not change pushLane/oi; the join, escort, weakest-lane and fort rules stay as in v76 (escort for Red non-Crossbowmen takes precedence
   when the allied Crossbowman is pushing: skip group mode while worldTick < escortUntil).
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
