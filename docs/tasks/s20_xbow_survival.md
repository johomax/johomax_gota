# Task S20 — Crossbowman survival (write policy/v59.bas from policy/v49a.bas)
Base: policy/v49a.bas (champion for GAME VERSION 33 — read the top of docs/ARENA_NOTES.md). The Crossbowman (class 6, range 6.5) out-ranges
every tower and is our carry seat (50% team wins vs ~20% for other classes), but in league games it still dies 12.75 times per game
(each death = 216 ticks + a ~1500-tick walk) and spends 51% of its time walking, 15% fighting heroes, only 10% sieging. Telemetry shows it
takes 1v1 fights (the odds rule allows allyNear8 + 1 >= enemyHeroNear) and its 96-tick kite toward the previous waypoint is too short.
Change ONLY class-6 behaviour (guard every change with selfClass = 6):
1. Engage rule: attack an enemy hero only if allyNear8 >= 1 (an ally within 8 tiles) or bestHeroHp * 2 < selfHp (kill shot) or allIn = 1 and
   allyNear8 >= 2. Otherwise treat any enemy hero within 9 tiles as a threat.
2. Threat response (replaces the existing 96-tick kite for class 6): set kiteUntil = worldTick + 168 and retreat: if an own living tower is
   within 30 tiles (track ownTX/ownTY/ownTD2 in the scan: kind 4, team = selfTeam, objectHp > 0, nearest), walk to the point 2 tiles behind it
   toward home (stepToward(ownTX, ownTY, homeX, homeY, 2)); otherwise stepToward(selfX, selfY, rx, ry, 10). act = 28. While kiting, still take
   kill shots (bestHeroHp * 2 < selfHp) and still attack footmen in range when no enemy hero is within 6 tiles (existing footman rule).
3. Potions: for class 6, drink at selfHp * 100 < selfMaxHp * 60 (instead of 55) when an enemy hero is within 10 tiles.
4. When no enemy hero is within 9 tiles for 96 consecutive ticks, resume the normal objective (the existing rules already walk back to the tower
   and siege from 6.5 tiles).
Everything else unchanged (siege gating, commitment, all-in, shop). Report the new variables and confirm no name clashes.
No blank line directly before `end if` or `wend`.
