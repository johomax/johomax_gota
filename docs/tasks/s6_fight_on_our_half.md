# Task S6 — fight on our half, disengage on theirs (write policy/v32.bas from policy/v30.bas)
Base: policy/v30.bas (= v19 without post-respawn home guard and without the ally hold).
Telemetry over 192 games: 434 deaths, 74% while fleeing at <15% HP (too late), 80% with 1-2 enemy heroes nearby, 70% at objective index
4-5 (enemy inner/gate tower, deep in enemy territory) with no allies within 25 tiles. An enemy killed near its own base is back in ~300 ticks;
we need ~2200. So fights are only worth taking on our half of the map or with a clear advantage.
Change ONLY the flee/engage rules in the decide block (keep fort, tower, footman rules):
1. Compute onOurHalf = 1 when the squared distance to homeX/homeY is smaller than the squared distance to the enemy fort
   (routeX/routeY(pushLane*7+6), which equals mapWidth-1-homeX, mapHeight-1-homeY).
2. Count allied heroes within 8 tiles (allyNear8) in the scan (alive, not self, d2 <= 64).
3. Replace the flee rule (act 1, currently selfHp*100 < selfMaxHp*15 and enemyHeroNear > 0) with:
   threat = enemyHeroNear > allyNear8 + 1 (outnumbered) or (enemyHeroNear > 0 and selfHp*100 < selfMaxHp*hpLimit) where
   hpLimit = 25 on our half and 50 on their half. When threat = 1 and fortId = 0 and no allied tower within 6 tiles (own kind 4 with hp > 0),
   retreat: stepToward(selfX, selfY, rx, ry, 8); walkTo(sx, sy); done = 1; act = 1; also set threatUntil = worldTick + 48 and keep
   retreating while worldTick < threatUntil (hysteresis) unless fortId <> 0.
4. Engage rule: attack bestHero only if not threat and (allyNear8 + 1 >= enemyHeroNear or bestHeroHp * 2 < selfHp).
Report the new variables and confirm no name clashes.
