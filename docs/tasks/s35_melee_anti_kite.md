# Task S35 — melee heroes stop chasing enemies that kite them (write policy/v115.bas from policy/v113.bas)
Base: policy/v113.bas (= champion lineage v93 + stutter-step kiting for ranged classes; the kiting cut ranged deaths by 60-75%). GAME VERSION 36.
Melee classes (melee = 1: Vanguard Knight 0, Demon Hunter 4, Death Knight 5, Berserker 9) still die 3-6 times per game; the two best
opponents ("red-kite", "black-kite") kite melee heroes — our melee hero chases a retreating ranged hero (act 3, attackTarget(bestHero)),
never lands hits, walks into towers/creeps and dies. Version-36 observations available: objectVelX(i)/objectVelY(i) = the object's
displacement over the last tick in world units (60000 per tile), selfMoveSpeed = our unblocked speed in world units per tick,
selfAttackRange (world units), objectTarget(i). Existing: bestHero/bestHeroHp/bestHeroD2 (lowest-HP enemy hero within heroR2), chaseHero
(none in v113; ignore), enemyHeroNear, allyNear8, allIn, lowHp, farmR2/bestFoot, towerId, lastX/lastY.

1. Scan: for the enemy hero that becomes bestHero, also record bestHeroVx = objectVelX(i), bestHeroVy = objectVelY(i), bestHeroX/Y (x, y).
2. Fleeing test (melee = 1 only): the target is running away when its velocity points away from us and is fast:
   away = (bestHeroX - selfX) * bestHeroVx + (bestHeroY - selfY) * bestHeroVy  (positive when moving away; tile deltas times world units,
   int32 is fine: deltas <= 115, velocities <= ~10000)
   speed2 = bestHeroVx * bestHeroVx + bestHeroVy * bestHeroVy ; fast when speed2 * 100 >= selfMoveSpeed * selfMoveSpeed * 64 (>= 80% of ours).
   fleeing = 1 when away > 0 and fast and bestHeroD2 > selfAttackRange * selfAttackRange / (60000 * 60000) + 1 (i.e. not already in reach;
   compute the range in tiles^2 once at init as meleeReach2 = (selfAttackRange / 60000 + 1) * (selfAttackRange / 60000 + 1)).
3. Chase budget: keep chaseTicks (ticks spent with act = 3 on the same target id since the target was last in reach). When fleeing = 1 for
   24 consecutive decisions (fleeCount >= 24) OR chaseTicks >= 96 without the target coming within meleeReach2: set noChaseId = bestHero,
   noChaseUntil = worldTick + 240, print "NOCHASE " ; worldTick ; " " ; bestHero (at most once per 480 ticks).
4. Apply: while worldTick < noChaseUntil, the scan must not select noChaseId as bestHero (skip it, pick the next lowest-HP candidate) unless
   its HP * 2 < selfHp (kill shot) or allIn = 1. Reset chaseTicks/fleeCount when the target changes or comes into reach.
5. Ranged classes (melee = 0) are untouched. Keep the death telemetry print. Nothing else changes.
Report new variables (no case-insensitive clashes), insertion lines and where the skip happens in the scan. Rules: int32 only, no elseif/for,
NO blank line directly before `end if` or `wend` (compile error). Keep the diff minimal.
