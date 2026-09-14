# Task S1 — ranged siege safety (write policy/v25.bas from policy/v19.bas)
Ranged classes (rng >= 40, i.e. melee = 0) die to towers because v19 sieges any exposed tower within 9 tiles as soon as no enemy hero is
within 3 tiles (act 6, two places in the decide block). Change ONLY tower engagement for ranged heroes:
1. Tower tier from id: tier = (id - 10 - team*3) mod 6 where team is the tower's team (1 - selfTeam); tower range tiles*10 = 50/55/60 by tier.
   "safe" = rng > towerRange (Crossbow vs all, Ranger/Lich vs outer).
2. Count allied footmen (kind 3, team = selfTeam, alive) within 3 tiles (d2 <= 9) of the candidate tower during the scan (you need the tower
   position; record towerX/towerY when towerId is chosen and count footmen in a second pass, or count footmen near each exposed tower inline
   by remembering the nearest tower first — footmen are enumerated AFTER towers, so a single pass works if you record towerX/towerY when the
   tower is chosen and test footmen against it).
3. A ranged hero attacks a tower only if safe = 1 OR waveAtTower >= 1 OR tower hp <= 150 OR fort is exposed (fortId <> 0 already handled).
4. Standoff: if a ranged hero is NOT allowed to siege and the nearest living enemy tower (hp > 0, exposed or not; check objectHp > 0) is within
   (towerRange + 5) tenths-of-tiles, i.e. d2*100 <= (towerRange+5)^2, and no allied footman is within 3 tiles of that tower, then step back
   toward the previous waypoint (stepToward(selfX, selfY, rx, ry, 6); walkTo(sx, sy)) instead of advancing; keep attacking footmen/heroes in
   range when present (existing rules above it still fire). Melee heroes: unchanged.
Report the new/changed variables and confirm no name clashes.
