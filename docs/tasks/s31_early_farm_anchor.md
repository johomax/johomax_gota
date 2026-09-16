# Task S31 — early-game farming anchor (write policy/v89.bas from policy/v88.bas)
Base: policy/v88.bas (= v76 + farmR2 creep farming + creeps-before-towers below level 4). GAME VERSION 36 (docs/ARENA_NOTES.md top):
games end around tick 8000; our hero is still level 1 at tick ~1500-1900, gets its first kill reward at tick ~2400 (median over 240 hosted
games) and often stands 1000-2400 ticks in "wait for the next wave" (act 22) next to the enemy outer tower at level 1, while camper
policies farm creeps from tick 300 and reach ~1.5-2x our XP. Goal: spend the first levels where the creep waves meet, not at the enemy tower.

Route points (wpX/wpY, index oi): 0 own gate, 1 own inner, 2 own outer, 3 enemy outer, 4 enemy inner, 5 enemy gate, 6 enemy fort.
Existing variables you can use: farmR2, bestFoot (lowest-HP enemy footman within farmR2), enemyHeroNear, allyNear8, nearHeroD2, bestHero,
bestHeroHp, towerDanger, towerX/towerY/towerRange (objective tower, range in tenths of tiles), fortId, openLane, allIn, routing, lowHp,
lastX/lastY (position at the previous decision), deaths.

1. Farm phase flag: farmPhase = 1 while selfLevel < 4 and worldTick < 4800 and fortId = 0 and openLane = -1 and allIn = 0 and routing = 0
   and lowHp = 0; otherwise 0. Print "FARM " ; worldTick once when it first becomes 1 and "FARMEND " ; worldTick ; " L" ; selfLevel once
   when it turns 0 after having been 1 (track with farmPrinted / farmEnded flags).
2. Anchor: in the scan, among living allied footmen (objectKind = 3, objectTeam = selfTeam, objectAlive = 1) within 40 tiles (d2 <= 1600) of
   the lane midpoint M = ((wpX(2) + wpX(3)) / 2, (wpY(2) + wpY(3)) / 2), pick the one nearest to the enemy outer tower (wpX(3), wpY(3)):
   anchorX/anchorY. With none visible use M. If the anchor lies within (towerRange / 10 + 1) tiles of a LIVING enemy tower at
   (wpX(3), wpY(3)) (use the objective tower's HP/alive knowledge already tracked: laneTowerHp / routeDead), move the anchor back along the
   line towards wp(2) until it is that far from the tower (integer stepping is fine; stepToward exists).
3. Farm-phase rules, placed AFTER the flee/fort/kite/open-lane/step-out-of-tower-range rules and BEFORE the escort and siege rules:
   a. if enemyHeroNear >= 2 and allyNear8 = 0 and not (bestHero <> 0 and bestHeroHp * 2 < selfHp): walkTo(wpX(2), wpY(2)); act = 39; done = 1.
   b. else if bestFoot <> 0: attackTarget(bestFoot); act = 4; done = 1.
   c. else if my squared distance to the anchor > 16: walkTo(anchorX, anchorY); act = 38; done = 1.
   d. else: done = 1 with NO command (the hero idles at the anchor so the engine's automatic creep acquisition fires; do not call
      walkTo(selfX, selfY), it suppresses auto-acquire).
   Towers are ignored during the farm phase (no siege, no waiting at the enemy tower); the objective index oi is not changed.
4. Death telemetry: change the existing line `print "D " ; worldTick ; " respawn #" ; deaths` to also print " at " ; lastX ; " " ; lastY.
5. Everything outside the farm phase stays exactly as in v88.
Report the new variables and confirm no name clashes with existing ones. Rules: int32 only, no elseif/for, identifiers are case-insensitive,
NO blank line directly before `end if` or `wend` (compile error). Keep the diff minimal.
