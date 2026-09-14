# Task S3 — push the least-defended lane (write policy/v27.bas from policy/v19.bas)
v19 pushes a fixed lane (Red 2, Blue 0). Enemy entrants often defend side lanes with 2-3 heroes while another lane is empty.
Change ONLY lane selection, using the existing adoptLane(lane, reason) sub (reason 1 prints "resistance"):
1. Keep the initial lane. Every 240 ticks from tick 720 on, when not fighting (enemyHeroNear = 0) and not lowHp, score each lane L:
   score = 10 * (number of standing enemy towers in lane L, from routeDead(L*7+3..5)) + 4 * (visible enemy heroes within 12 tiles of lane L's
   first standing enemy tower position routeX/routeY(L*7+firstOi)) - 3 * (allied heroes within 12 tiles of that same point)
   - 2 if L = pushLane (hysteresis). Lower is better. Use firstStanding(L) to get firstOi (it sets the global firstOi).
   Enemy hero positions: reuse seenEnemyX/seenEnemyY (array size 4 -> raise dim to 9 and guard seenEnemies < 10). Allied hero positions:
   collect allyX/allyY arrays (dim 9) in the scan.
2. If the best lane differs from pushLane and worldTick - lastLaneTick >= 1200, call adoptLane(bestLane, 1) and set laneTravel = 1
   (the existing routing code then walks the lane road). Never switch while oi >= 5 (already at the enemy gate) unless that lane has 3+
   enemy heroes near.
3. Leave the old resistance-based switch in place but it is unlikely to fire; do not remove code.
Report the new variables and confirm no name clashes (routeLane, routeIndex, firstOi, firstLaneId are used by existing subs).
