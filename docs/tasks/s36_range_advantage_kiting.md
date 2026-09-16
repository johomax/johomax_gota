# Task S36 — keep the range advantage against shorter-ranged enemy heroes (write policy/v116.bas from policy/v113.bas)
Base: policy/v113.bas (champion since 03:36 UTC: v93 + stutter-step kiting against MELEE threats within 3.5 tiles; acts 45/46, variables
windupTicks, kiteRange2, threatD2, kiteTarget/kiteTargetD2, nmx/nmy, lastKite2Print). GAME VERSION 36. Basic ranges in tenths of tiles (rng):
Crossbowman 65, Ranger 55, Lich 55, Arcanist 50, Warlock 45, Druid 40; melee 12. Class ids: VK 0, Ranger 1, Arcanist 2, Druid 3, DH 4, DK 5,
Crossbowman 6, Lich 7, Warlock 8, Berserker 9. Enemy heroes that out-range us cannot be kited by stepping back; enemies with a SHORTER
range can: stay at our max range, hit when the cooldown is within the windup, step back during recovery when they close in.

1. Scan (k = 2 enemy branch): for each living enemy hero within 10 tiles record its class range enemyRng (table above by objectClass(i)).
   Track the nearest enemy hero whose range is at least 5 (half a tile) shorter than ours: shortId, shortD2, shortX/shortY, shortRng.
2. Rule (ranged classes only, melee = 0), inserted directly AFTER the existing v113 melee kiting block and BEFORE the fallback act 2 rule:
   when done = 0 and routing = 0 and lowHp = 0 and towerDanger = 0 and shortId <> 0 and the melee kiting block did not act this decision
   (i.e. done is still 0) and shortD2 <= (shortRng + 10) * (shortRng + 10) / 100 (it is within one tile of reaching us):
   a. if selfAttackCooldown <= windupTicks + 1 and shortD2 <= rng * rng / 100: attackTarget(shortId) ; act = 47 ; done = 1
   b. else stepToward(selfX, selfY, 2 * selfX - shortX, 2 * selfY - shortY, 3) (fallback stepToward(selfX, selfY, rx, ry, 3) if not
      terrainWalkable) ; walkTo(sx, sy) ; act = 48 ; done = 1.
   Print "KITE3 " ; worldTick once per 480 ticks while active (lastKite3Print).
3. Do not touch the melee block, farming, sieging or anything else. Keep the death telemetry print.
Report new variables (no case-insensitive clashes), insertion lines and the rule order. Rules: int32 only, no elseif/for, NO blank line directly
before `end if` or `wend` (compile error). Keep the diff minimal.
