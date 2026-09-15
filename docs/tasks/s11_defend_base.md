# Task S11 — defend the base when it is under attack (write policy/v41.bas from policy/v30.bas)
Base: policy/v30.bas (= v19 without post-respawn home guard and without the ally hold).
Evidence: games end with 3-5 enemy heroes converging on one lane's gate tower and then the fort (median: first gate attack tick ~4300,
fort dead ~5800). Our hero is usually deep in the enemy lane or walking back from a respawn (a death costs ~2200 ticks) while this happens.
Fights under our own towers are favourable (towers shoot enemies once their footmen are dead; enemies that die there walk 2000+ ticks back).
Change ONLY the objective selection by adding a DEFEND mode:
1. In the scan, for every own tower (kind 4, team = selfTeam, hp > 0, always visible) remember the one with the most visible enemy heroes
   within 12 tiles (count enemy heroes whose distance to that tower is <= 12 tiles: you need tower positions first — towers are enumerated
   before heroes, so store own tower positions/ids in arrays ownTX/ownTY/ownTId (dim 9, at most 9 own towers) during the scan, then in a second
   short loop over the seenEnemyX/seenEnemyY arrays (raise their dim to 9 and guard seenEnemies < 10) count threats per own tower).
   threatTower = the own tower with the highest count; threatCount = that count; also count allied heroes within 12 tiles of it (allyX/allyY
   arrays, dim 9, collected in the scan) as threatAllies.
2. Enter defend mode when threatCount >= 2 and threatCount >= threatAllies and the hero is within 60 tiles of that tower and the enemy fort
   is not exposed/visible (fortId = 0). Leave defend mode when threatCount = 0 for 240 consecutive ticks, or when fortId <> 0.
   Print "DEFEND " ; worldTick ; " tower " ; threatTowerId ; " enemies " ; threatCount once on entry and "DEFEND end" ; worldTick on exit.
3. In defend mode: objective = a point 2 tiles behind the threatened tower toward our fort (stepToward(towerX, towerY, homeX, homeY, 2));
   fight rules as usual (hero in range -> attack lowest-HP enemy hero; footmen; the existing flee rule), otherwise walkTo that point; when within
   1.5 tiles (d2 <= 2) walkTo(selfX, selfY). Set act = 25 while defending. Do not use the lane-switch/rejoin machinery for this; when defend
   mode ends, the normal objective logic resumes unchanged (oi stays where it was).
4. Melee and ranged identical. Keep telemetry lines intact.
Report the new variables and confirm no name clashes. Remember: no blank line directly before `end if` or `wend`.
