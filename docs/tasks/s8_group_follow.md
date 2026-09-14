# Task S8 — stay with the allied group (write policy/v37.bas from policy/v30.bas)
Base: policy/v30.bas (= v19 without post-respawn home guard and without the ally hold).
Replay evidence (432 games): the winning team's heroes attack the fort in every game, usually four heroes attack the final gate tower
together, and the breakthrough lane is mid 42% of the time. Only 20% of our wins came through the side lane our hero pushes alone.
So the hero should fight WITH its allies instead of pushing a side lane by itself. Change ONLY lane/objective selection:
1. In the scan, record every living allied hero position (allyX/allyY arrays, dim 9) — allies are always visible.
2. Every 120 ticks (worldTick mod 120 = 0), when not routing, compute for each lane L the number of allies within 15 tiles of ANY of the
   lane's route points 2..5 (own outer, enemy outer, enemy inner, enemy gate: routeX/routeY(L*7+p)); call it laneAllies(L) (dim 2).
   Also compute clusterLane = the lane with the most allies (ties: mid lane 1 first, then the current pushLane).
3. If laneAllies(clusterLane) >= 2 and clusterLane <> pushLane and worldTick - lastLaneTick >= 600 and enemyHeroNear = 0 and towerId = 0,
   then adoptLane(clusterLane, 2) and set laneTravel = 1 so the existing routing walks the lane road toward its first standing enemy tower.
   (adoptLane sets oi to the first standing enemy tower; if the hero is still on its own half, set oi to the index of the route point
   nearest the hero so it does not path backwards: pick the p in 0..firstOi minimizing distance to the hero.)
4. Keep the existing respawn rejoin logic unchanged.
5. Add a print when switching: print "GROUP " ; worldTick ; " lane " ; clusterLane ; " allies " ; laneAllies(clusterLane)
Report the new variables and confirm no name clashes (routeLane, routePoint, routeIndex, firstOi, laneChanged, laneTravel exist).
