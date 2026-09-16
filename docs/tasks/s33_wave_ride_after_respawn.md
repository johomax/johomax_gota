# Task S33 — ride the next allied creep wave out after a respawn (write policy/v108.bas from policy/v102.bas)
Base: policy/v102.bas (= champion v93 + hold at the nearest own tower after a respawn while an enemy hero is within 18 tiles and no ally is
within 8; see its block above the "home guard" comment, variables guardCap/guardUntil/homeIdx/minSeenD2). GAME VERSION 36: games end ~tick
8000; 39% of our deaths are re-deaths within 1500 ticks of a respawn while walking back up our lane alone (act 9), most often 1v1 against an
enemy hero. v102 holds at home when enemies are close; this task adds the complementary behaviour for the walk out itself.

Route points (wpX/wpY, index oi): 0 own gate, 1 own inner, 2 own outer, 3 enemy outer, 4 enemy inner, 5 enemy gate, 6 enemy fort.
Existing: farmR2/bestFoot (farming), allyNear8, enemyHeroNear, nearHeroD2, towerDanger, fortId, openLane, routing, lowHp, allIn, guardCap
(= respawn tick + 2400), lastX/lastY, seenEnemies/seenEnemyX/Y.

1. Wave anchor: in the scan, among LIVING ALLIED footmen (objectKind = 3, objectTeam = selfTeam, objectAlive = 1) within 30 tiles of us
   (d2 <= 900), pick the one nearest to the enemy outer tower (wpX(3), wpY(3)) — waveX/waveY, waveFound = 1; else waveFound = 0.
   Do not add a second pass over the objects; extend the existing loop.
2. Ride phase flag: ride = 1 while worldTick < guardCap (i.e. within 2400 ticks of the last respawn) and oi <= 3 and allyNear8 = 0 and
   fortId = 0 and openLane = -1 and routing = 0 and lowHp = 0 and allIn = 0 and waveFound = 1 and our squared distance to the wave anchor
   is > 16 (more than 4 tiles behind/ahead of it) and the anchor is closer to the enemy outer tower than we are (so we never walk back
   to a wave behind us); otherwise ride = 0. Print "RIDE " ; worldTick at most once per 480 ticks while ride = 1.
3. Decide: insert AFTER v102's hold-at-home rule (act 14 block) and the flee/fort/kite/open-lane/step-out rules, BEFORE the escort/siege/
   farm rules: if done = 0 and ride = 1 then walkTo(waveX, waveY) ; act = 44 ; done = 1. (Farming within farmR2 still happens because act 4
   precedes? No — place this rule so that bestFoot farming (act 4) keeps priority: i.e. immediately AFTER the existing act 4 farming rule and
   BEFORE the siege rules. Read the file and confirm the order in your report.)
4. Nothing else changes. Report new variables (no clashes; identifiers are case-insensitive), the insertion line numbers and the rule order.
Rules: int32 only, no elseif/for, NO blank line directly before `end if` or `wend` (compile error). Keep the diff minimal.
