# Task S7 — farm the enemy wave while pushing (write policy/v33.bas from policy/v30.bas)
Base: policy/v30.bas (= v19 without post-respawn home guard and without the ally hold).
v19 attacks enemy footmen only when engaged (within 2.4 tiles) or for kill shots (hp <= 30 within range). A lone hero should instead kill
every enemy footman it can reach: each kill is 25 XP / 15 gold, and a dead enemy wave lets our own wave reach the enemy tower and tank it.
Change ONLY footman targeting:
1. In the scan, besides bestFoot (engaged/kill-shot), track farmFoot = the enemy footman with the lowest HP within the hero's basic range
   (d2 <= footR2 — footR2 already encodes (rng+10)^2/100 for ranged and 9 for melee; use farmR2 = (rng + 15)*(rng + 15)/100 for ranged and 16
   for melee so the hero steps a little toward it), alive only.
2. Decide block: keep the existing order (flee, kite, fort, tower-no-hero-adjacent, hero, engaged footman, tower), then add a new rule
   immediately after the second tower rule (act 6): if done = 0 and routing = 0 and farmFoot <> 0 and lowHp = 0 then attackTarget(farmFoot);
   done = 1; act = 16. This means farming happens only when no tower is attackable and no enemy hero is in range.
3. Farming must not pull the hero backwards: only consider footmen whose distance to the objective (ox, oy) is not more than 8 tiles farther
   than the hero's own distance to the objective (compare squared distances: footObjD2 <= myD2 + 16*isqrt-free approximation is fine:
   use (footDist - myDist) via isqrt calls sparingly — simpler: require the footman's d2 to the objective <= myD2 + 64 + 16 * sqrt term is
   overkill; just require footObjD2 <= myD2 * 2 + 64).
Report the new variables and confirm no name clashes.
