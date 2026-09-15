# Task S15 — join an allied side-lane pusher (write policy/v51.bas from policy/v49a.bas)
Base: policy/v49a.bas (champion for GAME VERSION 33 — read the top section of docs/ARENA_NOTES.md). Decisive games are won by heroes that
grind a side-lane gate together; the strongest entrants (red-kite, black-kite, daveey) push one side lane all game. v49a commits to its own side
lane (Red lane 2 / Blue lane 0, Crossbowman keeps that too) and never switches. Add ONE switch rule:
1. Every 600 ticks from tick 1200 on, when not fighting (enemyHeroNear = 0) and not the Crossbowman (selfClass <> 6): for each side lane L in
   (0, 2) count allied heroes within 12 tiles of any of that lane's enemy-tower route points routeX/routeY(L*7+3..5) (allies are always
   visible; collect allyX/allyY arrays, dim 9, in the scan). If some lane L <> pushLane has >= 2 such allies and the current lane has fewer,
   switch once: adoptLane(L, 2); firstStanding(L); oi = firstOi; set laneTravel = 1 so the existing routing walks there; set joinLockUntil =
   worldTick + 6000 and do not switch again before that. Print "JOIN " ; worldTick ; " lane " ; L ; " allies " ; count.
2. The existing commitment (no resistance switch, no rejoin) stays; this is the only lane change allowed.
Report the new variables and confirm no name clashes (routeLane, routePoint, routeIndex, firstOi, laneTravel, laneChanged exist).
No blank line directly before `end if` or `wend`.
