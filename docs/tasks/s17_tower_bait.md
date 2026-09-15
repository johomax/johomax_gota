# Task S17 — retreat under our own tower when threatened (write policy/v54.bas from policy/v49a.bas)
Base: policy/v49a.bas (champion for GAME VERSION 33 — read the top section of docs/ARENA_NOTES.md). Towers now deal 28/56/112 per 24 ticks,
so an enemy hero that chases us under one of OUR towers dies in a few shots (and walks 1500+ ticks back), while we get 150 XP / 100 gold.
Our non-Crossbowman heroes die 10-18 times per game, mostly to 1-2 enemy heroes; v49a only steps back 8 tiles when fleeing.
Change ONLY the threat response:
1. In the scan, remember the nearest own living tower (kind 4, team = selfTeam, objectHp > 0): ownTX/ownTY/ownTD2 (squared distance to me).
   Own objects are always visible.
2. threat = 1 when allIn = 0 and (enemyHeroNear > allyNear8 + 1 or (enemyHeroNear > 0 and selfHp * 100 < selfMaxHp * 40)).
   When threat = 1 and ownTD2 <= 1600 (own tower within 40 tiles) and fortId = 0: set baitUntil = worldTick + 240 (refresh while threat lasts).
3. While worldTick < baitUntil: the bait point is 2 tiles behind the tower toward home: stepToward(ownTX, ownTY, homeX, homeY, 2) -> (sx, sy).
   If my squared distance to the bait point > 9 then walkTo(sx, sy), act = 29 (this replaces the existing flee/step-back rules while baiting).
   If within 3 tiles of the bait point: fight — attack bestHero if any enemy hero is within my basic range, else bestFoot/farm footmen in range,
   else walkTo(selfX, selfY); act = 30. Do not kite away from the tower while baiting.
4. When baitUntil expires and no enemy hero is within 12 tiles, resume the normal objective (oi unchanged, the hero walks back to its lane).
5. Print "BAIT " ; worldTick once when a bait episode starts (baitUntil <= worldTick before setting it).
Keep everything else (siege gating, kiting for long-range classes, shop, commitment, all-in) unchanged.
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
