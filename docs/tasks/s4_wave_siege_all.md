# Task S4 — siege only with the wave, for every class (write policy/v28.bas from policy/v19.bas)
Towers shoot footmen first. v19 sieges any exposed tower within 9 tiles whenever no enemy hero is within 3 tiles, so a lone hero eats
tower shots between waves and dies. Change ONLY tower engagement (both act 6 rules) for ALL classes:
1. Record towerX/towerY when towerId is chosen in the scan; footmen are enumerated after towers, so in the same scan count allied footmen
   (kind 3, team = selfTeam, alive) within 3 tiles (d2 <= 9) of (towerX, towerY) as waveAtTower.
2. Allow attackTarget(towerId) only if waveAtTower >= 1 OR objectHp of that tower <= 150 OR (melee = 0 and rng > towerRange) where
   towerRange (tenths of tiles) = 50/55/60 by tier, tier = (id - 10 - (1-selfTeam)*3) mod 6.
3. When the tower rule is blocked and the hero has nothing else to attack, and the objective is that tower (otype = 1 and oid = towerId),
   wait for the next wave: stand at a point 7 tiles short of the tower along the route: stepToward(towerX, towerY, rx, ry, 7) -> walkTo(sx, sy);
   if already within 1.5 tiles of that point (d2 <= 2) then walkTo(selfX, selfY). Set act = 22 for this wait state. Do not use the hold/unstick path.
4. Everything else (heroes, footmen, fort, flee) unchanged.
Report the new variables and confirm no name clashes.
