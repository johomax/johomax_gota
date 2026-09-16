# Task S46 — melee: back off when outnumbered; ride walks do not trip the stuck machinery (write policy/v145.bas from policy/v139.bas)
Base: policy/v139.bas (champion). Copy to policy/v145.bas and apply ONLY the edits below. Ranged behaviour (melee = 0) must not change.
Evidence (v139 ten-seat baseline, 240 hosted games): VK dies 6.1 times per game, DH 5.9, DK 4.5, Berserk 3.6; the last telemetry
sample before a death (up to 480 ticks earlier) shows mean HP 54-74%, no ally within 25 tiles in ~45% of cases, and the hero
walking (act 9) or farming (act 4). Deaths are bursts by two or more enemy heroes; the only reaction today is the 30%-HP flee (act 1/7),
which is too late for melee. Also DK/Berserk log 27-33 STUCK prints per game (v113: 6-12) because act-47 ride walks queue behind
our own creep wave; each STUCK sets `unstick = 20` and the fallback then walks 6 tiles back (act 10 = 4% of DK samples).

Existing names: melee, routing, lowHp, fortId, allIn (ally within 8 tiles or tick >= 12000), enemyHeroNear (living enemy heroes within
10 tiles), allyNear8, nearHeroD2, rx/ry (retreat point = previous route point / home), stepToward(fx,fy,tx,ty,k) -> sx/sy, done/act,
lastKite2Print (rate-limited print pattern), worldTick.

1. Init (first-tick block, next to `lastRidePrint = -480`): `lastOutnPrint = -480`.
2. Outnumbered rule: insert immediately AFTER the act 1 flee rule (`if routing = 0 and selfHp * 100 < selfMaxHp * 25 and enemyHeroNear > 0 and allIn = 0 then` ... `act = 1` / `end if`)
   and BEFORE the fort rule (`' end the game first: an exposed fort in reach beats any fight`):
   ```
   ' melee: alone against two or more enemy heroes -> back off toward the previous route point before the burst, not at 30% HP
   if done = 0 and melee = 1 and routing = 0 and fortId = 0 and allIn = 0 and enemyHeroNear >= 2 and allyNear8 = 0 then
     stepToward(selfX, selfY, rx, ry, 6)
     if terrainWalkable(sx, sy) = 0 then
       stepToward(selfX, selfY, homeX, homeY, 6)
     end if
     walkTo(sx, sy)
     done = 1
     act = 55
     if worldTick - lastOutnPrint >= 480 then
       print "OUTN " ; worldTick ; " eh " ; enemyHeroNear
       lastOutnPrint = worldTick
     end if
   end if
   ```
   (allIn = 0 already excludes the case with an ally within 8 tiles; keep both terms anyway for clarity.)
3. Stuck detection: change `if act = 9 or act = 11 or act = 47 then` back to `if act = 9 or act = 11 then` (ride walks toward a moving
   footman must not trigger STUCK/unstick back-offs).
4. Header line after the v139 line: `' v145 = v139 + melee back off when alone against two or more enemy heroes (OUTN, act 55); ride walks no longer trip the stuck machinery.`
Report the edited line numbers and any deviation. Rules: int32 only, no elseif/for, NO blank line directly before `end if`/`wend`;
NO short-circuit evaluation (never index an array with a variable that may be -1 in the same condition); check lastOutnPrint does not clash.
