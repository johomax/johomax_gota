# Task S48 — walk out via our own outer tower instead of the diagonal through mid (write policy/v156.bas from policy/v148.bas)
Base: policy/v148.bas (champion, game version 37). Copy to policy/v156.bas and apply ONLY the edits below. All classes.
Evidence (v148 hosted baselines on version 37): heroes die mostly while walking (act 9) and the deaths cluster in mid/jungle — VK 98 of
317, DK 72 of 105, Berserk 61 of 113, Druid 73 of 250 — because the server path from our spawn to a far objective (enemy inner tower,
gate, fort) is a diagonal through the map centre where the enemy's mid pushers sit. v137 fixed the route by walking to the front allied
footman but queued behind creep waves (level). This task uses a single lane waypoint instead: on the way out, first walk to a point
just short of OUR OWN outer tower (on the lane), then continue to the objective. Own towers are always visible; route points hold tower
centres — never walk to a centre (version-37 footprints are 1.05-1.65 tiles): stop 4 tiles short of it, toward home.

Existing names: wpX(2)/wpY(2) = our own outer tower of the push lane (index 2 of the route: 0 own gate, 1 own inner, 2 own outer,
3 enemy outer, 4 enemy inner, 5 enemy gate, 6 enemy fort), homeX/homeY = our fort, oi (objective index), ox/oy/myD2, routing, fortId,
openLane, lowHp, done/act, selfX/selfY, stepToward(fx, fy, tx, ty, k) -> sx/sy (the point k tiles from (fx,fy) toward (tx,ty); if the
distance is <= k it returns (fx,fy) itself), worldTick, lastRidePrint (print pattern).

1. Init (next to `lastRidePrint = -480`): `lastViaPrint = -480`.
2. Insert immediately BEFORE the home-guard block (comment `' home guard: a respawned hero waits ...`, act 14) — i.e. after every farm,
   fight, kite, siege, ride and wait rule — the waypoint rule:
   ```
   ' walk out along our own lane: while the objective is beyond the enemy outer tower and we are still behind our own outer tower,
   ' head for a point 4 tiles short of our outer tower instead of the diagonal through mid
   if done = 0 and routing = 0 and fortId = 0 and openLane < 0 and lowHp = 0 and oi >= 4 then
     vhx = selfX - homeX
     vhy = selfY - homeY
     vox = wpX(2) - homeX
     voy = wpY(2) - homeY
     if vhx * vhx + vhy * vhy + 100 < vox * vox + voy * voy then
       stepToward(wpX(2), wpY(2), homeX, homeY, 4)
       vdx = sx - selfX
       vdy = sy - selfY
       if vdx * vdx + vdy * vdy > 9 then
         walkTo(sx, sy)
         done = 1
         act = 58
         if worldTick - lastViaPrint >= 480 then
           print "VIA " ; worldTick ; " to " ; sx ; " " ; sy
           lastViaPrint = worldTick
         end if
       end if
     end if
   end if
   ```
   Meaning: "behind our outer tower" = our squared distance from home is smaller than the outer tower's by more than ~10 tiles of
   slack (the +100); once within 3 tiles of the waypoint (or past the tower) the rule stops and the normal objective walk continues.
3. Stuck detection: `if act = 9 or act = 11 then` -> `if act = 9 or act = 11 or act = 58 then`.
4. Header line after the v148 line: `' v156 = v148 + walk out via a point 4 tiles short of our own outer tower when the objective is beyond the enemy outer tower (VIA, act 58) — avoids the diagonal through mid.`
Report edited line numbers and any deviation. Rules: int32 only, no elseif/for, NO blank line directly before `end if`/`wend`, NO
short-circuit evaluation; check vhx, vhy, vox, voy, vdx, vdy, lastViaPrint do not clash (identifiers are case-insensitive).
