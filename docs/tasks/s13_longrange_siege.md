# Task S13 — long-range siege discipline (write policy/v47.bas from policy/v46.bas)
Base: policy/v46.bas. GAME VERSION 33 (read docs/ARENA_NOTES.md top section): towers now have 1200/2400/4800 HP and hit for 28/56/112 per
24 ticks; ranges 5.0/5.5/6.0 tiles. The Crossbowman (class 6, range 6.5 tiles = rng 65) out-ranges every tower; Ranger (1) and Lich (7) (rng 55)
out-range only the outer tower (tier 0). A hero attacking a tower stands at its own max range, so the Crossbowman takes no tower damage.
Our Crossbowman currently gets 3 tower kills per game but dies ~14 times, mostly to enemy heroes that walk out to it.
Change ONLY behaviour for ranged heroes with a range advantage (rng > towerRange of the objective tower; v46 already computes rng,
towerRange, towerId, towerHp, enemyHeroNear, nearHeroD2, allyNear8, rx/ry):
1. safeSiege = 1 when melee = 0 and towerId <> 0 and rng > towerRange.
2. While safeSiege = 1: if an enemy hero is within 9 tiles (nearHeroD2 <= 81) and NOT (allyNear8 >= enemyHeroNear) then disengage:
   set kiteUntil = worldTick + 96 and while worldTick < kiteUntil walk back toward the previous waypoint (stepToward(selfX, selfY, rx, ry, 8);
   walkTo(sx, sy); act = 28). Do not attack that hero unless bestHeroHp * 2 < selfHp (kill shot) — reuse the existing hero rule ordering.
3. When no enemy hero is within 9 tiles (or allies match them), attackTarget(towerId) (act 6) — the existing tower rules already allow this
   because siegeAllowed is 1 when rng > towerRange; just make sure the kite rule sits BEFORE the tower rules and AFTER the fort rule.
4. Farming between sieges: when safeSiege = 1 and the tower rule is not taken because of the kite, still attack footmen in range
   (existing bestFoot rule) if no hero is within 6 tiles.
5. Add a print "KITE " ; worldTick when a kite starts (rate-limit: only when kiteUntil <= worldTick before setting it).
Report the new variables and confirm no name clashes. Remember: no blank line directly before `end if` or `wend`.
