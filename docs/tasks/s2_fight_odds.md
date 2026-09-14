# Task S2 — fight only with the odds (write policy/v26.bas from policy/v19.bas)
v19 attacks the lowest-HP enemy hero in range regardless of odds and only flees below 15% HP; a lone hero among strangers dies ~2x per game.
Change ONLY hero-fight engagement and retreat:
1. In the scan, count allied heroes within 8 tiles (d2 <= 64, alive, not self) as allyNear8 and enemy heroes within 10 tiles (enemyHeroNear
   already exists) and the nearest enemy hero distance nearHeroD2 (exists).
2. Engage rule: attack bestHero only if (allyNear8 + 1 >= enemyHeroNear) OR (bestHeroHp * 2 < selfHp) — a kill shot is always taken.
3. Retreat rule (before the tower/hero/footman rules, after the fort rule): if enemyHeroNear >= allyNear8 + 2 (outnumbered by two) OR
   (selfHp * 100 < selfMaxHp * 40 and nearHeroD2 <= 36), set retreatUntil = worldTick + 72; while worldTick < retreatUntil and fortId = 0:
   stepToward(selfX, selfY, rx, ry, 8); walkTo(sx, sy); done = 1; act = 21. Do not retreat when an allied tower (own team, kind 4, hp > 0)
   is within 6 tiles (we are safe under it) — track ownTowerD2 in the scan.
4. Potions: keep as is.
Report the new variables and confirm no name clashes.
