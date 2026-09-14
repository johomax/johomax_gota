Task W2 (candidate file policy/cand_siege.bas): improve SIEGE ROBUSTNESS (towers/fort) and survivability during the push.
Implement as one coherent change:
 (a) tank-first ordering: when the current target is a tower and no enemy hero is near, melee classes (0,4,5,9) attack immediately while ranged
     classes only attackTarget the tower if a melee ally is within 4 tiles of the tower OR the tower's HP < 300 (otherwise hold at ~6 tiles);
     towers shoot footmen first, then the nearest hero, so the tank should be nearest;
 (b) pre-siege potion: when the next objective is a tower within 12 tiles and my HP < 70%, use a potion before engaging (buy an elixir if none, 50g);
 (c) low-HP hold: heroes under 30% HP hold 6 tiles back (already in v5) but should still attackTarget enemy footmen/heroes that come within their basic range.
Measure RACE (primary: must not be slower than v5, ideally faster), CLASH, BASE. Report win rates and mean ticks.
