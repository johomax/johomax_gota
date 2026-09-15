# Task S27 — position for the fort race (write policy/v79.bas from policy/v76.bas)
Base: policy/v76.bas (champion). GAME VERSION 34 (docs/ARENA_NOTES.md top): towers 900/1200/1800 HP, 18/24/30 dmg, ranges 5/5.5/6 tiles;
fort 400 HP, no defence, exposed once its lane's three towers are dead; games are decided by who reaches the exposed fort first.
v75/v76 already rush an exposed fort (visible or once its gate is known dead). Refinement: be near the gate when it is about to fall.
1. v76 remembers enemy tower HP in laneTowerHp(lane*3 + tier) (updated whenever a tower is visible). Every tick compute nearGateLane = the
   lane whose gate (tier 2) is standing with last seen HP <= 450 and whose fort route point routeX/routeY(lane*7 + 6) is within 45 tiles of me
   (squared distance <= 2025); -1 if none.
2. When nearGateLane >= 0, fortId = 0, no enemy lane is already open (v76's openLane = -1), enemyHeroNear = 0 and towerDanger = 0 and I am
   farther than 9 tiles from that gate (squared distance to routeX/routeY(lane*7 + 5) > 81): walk to the staging point 9 tiles from the gate
   along the route toward the previous point (stepToward(gateX, gateY, routeX(lane*7 + 4), routeY(lane*7 + 4), 9) -> sx, sy), act = 40,
   done = 1 — placed right AFTER v76's open-lane fort rule (act 37) and BEFORE the tower-danger standoff. Within 9 tiles of the gate the
   normal rules apply (siege gating, fights), so the hero does not walk into the 6-tile gate range on its own.
3. Print "RACE " ; worldTick ; " lane " ; nearGateLane once per episode (track prevRace).
Everything else unchanged. Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
