# Task S19 — buddy the ally that is deepest in enemy territory (write policy/v58.bas from policy/v49a.bas)
Base: policy/v49a.bas (champion for GAME VERSION 33 — read the top of docs/ARENA_NOTES.md). Decisive games are won by heroes grinding an
enemy gate tower together; ~80% of our league rosters contain at least one strong side-lane pusher teammate (red-kite, black-kite, daveey),
usually pushing alone. Two heroes at a tower push twice as fast and split its shots; v49a's allIn already turns on when an ally is within 8 tiles.
Add ONE behaviour, for every class:
1. In the scan, for each living allied hero (kind 2, team = selfTeam, not self, always visible) compute its squared distance to the enemy fort
   (enemyFortX = mapWidth - 1 - homeX, enemyFortY = mapHeight - 1 - homeY). Track the ally with the smallest such distance: buddyId, buddyX,
   buddyY, buddyFortD2. Also compute my own myFortD2.
2. Every 240 ticks (worldTick mod 240 = 0), when routing = 0 and fortId = 0 and worldTick >= 900: choose buddy mode if buddyId <> 0 and
   buddyFortD2 <= 2500 (the ally is within 50 tiles of the enemy fort, i.e. past the enemy outer tower) and buddyFortD2 < myFortD2 - 100
   (the ally is clearly deeper than me). Set buddyUntil = worldTick + 240 and remember buddyId. Otherwise buddyUntil = 0.
   Print "BUDDY " ; worldTick ; " id " ; buddyId once when buddy mode starts (track prevBuddy).
3. While worldTick < buddyUntil and the buddy is still alive: if my squared distance to the buddy > 36 (6 tiles) and no enemy hero is in my
   basic range and towerDanger = 0 then walkTo(buddyX, buddyY), act = 34, done = 1 — placed AFTER the fort/standoff/kite rules and BEFORE the
   tower rules so fights and tower safety keep priority. Within 6 tiles of the buddy, the normal rules apply unchanged (allIn = 1 via allyNear8,
   so we siege the tower the buddy is at).
4. Buddy mode must not change pushLane, oi, or the lane-commitment logic; when it ends the hero resumes its own objective.
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
