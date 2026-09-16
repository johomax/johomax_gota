# Task S34 — stutter-step kiting for ranged classes (write policy/v113.bas from policy/v93.bas)
Base: policy/v93.bas (champion). GAME VERSION 36. Evidence: in 600 hosted games the two best policies (black-kite, red-kite) win 0.88/0.76 on
the Ranger seat and 0.77/0.76 on the Arcanist seat; v93 wins 0.50 and 0.53 there (and beats them on melee seats). Our only anti-melee rule
for ranged heroes is act 2: when a melee enemy hero is within 2 tiles, walk 4 tiles back toward the previous route point — it cancels our own
attack and fires 2% of the time. Proper kiting = hit, step away during the attack recovery, stop and hit again.

New version-36 observations (all int32, see docs/ARENA_NOTES.md top): `selfAttackCooldown` = ticks until our next basic hit could land
(includes the remaining recovery plus the next windup; an idle hero reports a full windup; MOVEMENT CANCELS A SWING, so only move while the
remaining value is larger than the windup), `selfAttackRange` (world units, 60000 per tile), `selfMoveSpeed` (world units per tick),
`objectVelX/Y(i)`, `objectTarget(i)`. Class attack cadence (ticks, from content.nim): VK 24, Ranger 18, Arcanist 30, Druid 26, DH 16, DK 28,
Crossbowman 36, Lich 32, Warlock 28, Berserker 20; windup = 45% of the cadence. Existing variables: melee (1 for VK/DH/DK/Berserker),
rng (basic range in tenths of tiles), nearMeleeD2/nmx/nmy (nearest enemy MELEE hero within 10 tiles and its position), bestHero/bestHeroHp,
bestFoot, enemyHeroNear, allyNear8, towerDanger, fortId, lowHp, routing, rx/ry (previous route point), stepToward(fx, fy, tx, ty, k) -> sx/sy.

1. Compute once at init: windupTicks = cadence * 45 / 100 for selfClass (table above). kiteRange2 = (rng - 5) * (rng - 5) / 100 (tiles^2:
   half a tile inside our basic range).
2. Each decision, for ranged heroes only (melee = 0): threatD2 = squared distance to the nearest living enemy MELEE hero (nearMeleeD2) — also
   consider enemy footmen adjacent to us (d2 <= 2) as a threat when no melee hero is within 3 tiles; kiteTarget = bestHero if it exists else
   the enemy melee hero itself if within our range, else bestFoot.
3. Rule (insert AFTER the fort rule act 5 and BEFORE the existing act 2 melee-step rule, which stays as a fallback): when melee = 0 and
   routing = 0 and lowHp = 0 and towerDanger = 0 and a melee threat is within 3.5 tiles (threatD2 <= 12):
   a. if selfAttackCooldown <= windupTicks + 1 and kiteTarget <> 0 and kiteTarget is within our basic range: attackTarget(kiteTarget) ;
      act = 45 ; done = 1 (stand and hit now)
   b. else: step directly AWAY from the threat: stepToward(selfX, selfY, 2 * selfX - nmx, 2 * selfY - nmy, 3) (i.e. 3 tiles along the line
      from the threat through us; if the result is not terrainWalkable, fall back to stepToward(selfX, selfY, rx, ry, 3)); walkTo(sx, sy) ;
      act = 46 ; done = 1.
   Print "KITE2 " ; worldTick once per 480 ticks while the rule is active (track lastKite2Print).
4. Everything else unchanged. Keep the death telemetry line as in v97+: print "D " ; worldTick ; " respawn #" ; deaths ; " at " ; lastX ; " " ; lastY ; " L" ; selfLevel.
Report: new variables (no case-insensitive clashes), insertion lines, and the rule order around act 2/act 45/46. Rules: int32 only, no elseif/for,
NO blank line directly before `end if` or `wend`. Keep the diff minimal.
