# Task S29 — threat-aware fights using objectTarget on enemy heroes (write policy/v83.bas from policy/v82.bas)
Base: policy/v82.bas (v76 + target-aware siege). GAME VERSION 36 (docs/ARENA_NOTES.md top): objectTarget(i) returns object i's current
attack target id when that target is visible to us. For enemy heroes this tells us who they are attacking: us (selfId), an ally, a footman
or a tower. v82 decides fights with raw counts (allyNear8 + 1 >= enemyHeroNear) and flees below 25% HP when any enemy hero is near.
Use the real threat instead:
1. In the enemy-hero part of the scan (heroes within 10 tiles, existing enemyHeroNear loop): count enemiesOnMe = enemy heroes whose
   objectTarget(i) = selfId, and enemiesBusy = enemy heroes within 10 tiles whose target is an allied hero or footman or a tower (target <> 0
   and <> selfId). Also remember the lowest-HP enemy hero in basic range that is NOT targeting me (busyHero/busyHeroHp) — a free kill.
2. Engage rule: replace "(allyNear8 + 1 >= enemyHeroNear or bestHeroHp * 2 < selfHp or allIn = 1)" by
   "(allyNear8 + 1 >= enemiesOnMe or bestHeroHp * 2 < selfHp or allIn = 1)". Prefer busyHero as the target when it exists and its HP is
   lower than bestHero's or bestHero is 0.
3. Flee rule: replace "selfHp * 100 < selfMaxHp * 25 and enemyHeroNear > 0 and allIn = 0" by "selfHp * 100 < selfMaxHp * 25 and enemiesOnMe > 0
   and allIn = 0" (do not flee from heroes that are busy with someone else).
4. Add " om " ; enemiesOnMe to the "T" telemetry line.
Everything else unchanged (siege gating incl. towerBusy, escort, join, fort rush, shop). Report the new variables and confirm no name clashes.
No blank line directly before `end if` or `wend`.
