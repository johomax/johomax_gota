Task W1 (candidate file policy/cand_fight.bas): improve FIGHT MICRO in the CLASH benchmark without slowing the RACE.
Hypotheses to implement together as one coherent change (you may drop one if it clearly hurts):
 (a) team-wide focus fire: pick the enemy hero with the lowest HP among enemy heroes within 12 tiles of ANY allied hero that is within 8 tiles of me
     (all five heroes see the same enemies because vision is team-shared), tie-break by lowest id, so all five converge on one target;
 (b) poison potions: keep one Poison Potion (item 4, 40g) and useItem it on the tick after attackTarget on an enemy hero within basic range
     (it deals 35 strike damage to the current attack target; check the engine rule in sim.nim applyUseItem);
 (c) smarter kiting for ranged classes: only step back when an enemy MELEE hero is within 2 tiles AND (my HP < 70% of max OR its HP > mine);
     otherwise keep attacking. Melee classes never kite.
Measure CLASH (primary), RACE and BASE. Report win rates and mean ticks.
