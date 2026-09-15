# Task S21 — finish the lane whose enemy towers are weakest (write policy/v62.bas from policy/v51.bas)
Base: policy/v51.bas (champion; v49a + join a side lane where 2+ allies push). GAME VERSION 33 (docs/ARENA_NOTES.md top): towers have
1200/2400/4800 HP, 55-65% of games time out and a timeout scores 0 like a loss, so only ENDING the game in our favour matters.
Tower HP is readable whenever a tower is visible to our team (objectHp), and allies/footmen give vision across lanes.
Add ONE lane-choice rule:
1. Remember the last seen HP of every enemy tower: array laneTowerHp(8) indexed lane*3 + tier (tier 0 outer, 1 inner, 2 gate), initialised at
   tick 1 to 1200/2400/4800 by tier; in the scan (enemy towers: k = 4, team <> selfTeam, tower id -> lane/tier as the existing code does with
   towerOffset/routeLane/tier), set laneTowerHp(routeLane*3 + tier) = objectHp(i) whenever the tower is visible (hp <= 0 means dead).
2. laneRemain(L) = sum of laneTowerHp over the standing tiers of lane L (values > 0). Compute for the three lanes every 600 ticks from
   tick 6000 on, when routing = 0, enemyHeroNear = 0, fortId = 0 and worldTick >= weakLockUntil.
3. weakLane = the lane with the smallest laneRemain (ties: keep pushLane). If weakLane <> pushLane and laneRemain(weakLane) * 10 <=
   laneRemain(pushLane) * 7 (at least 30% less HP to chew through) then: adoptLane(weakLane, 2); firstStanding(weakLane); oi = firstOi;
   laneTravel = 1; weakLockUntil = worldTick + 3000; print "WEAK " ; worldTick ; " lane " ; weakLane ; " hp " ; laneRemain(weakLane).
4. Keep v51's join rule (it may also switch lanes; give the join rule precedence in the same tick by placing this rule after it and skipping
   when laneChanged = 1). Everything else unchanged.
Report the new variables and confirm no name clashes (routeLane, tier, towerOffset, firstOi, laneTravel, laneChanged exist).
No blank line directly before `end if` or `wend`.
