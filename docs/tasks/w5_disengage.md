Task W5 (candidate file policy/cand_disengage.bas): DISENGAGE WHEN OUTNUMBERED and avoid feeding.
Observed failure (hosted, vs the #1 policy): five level-1 heroes push into 3 enemy heroes + tower and die one by one; each death costs
~1,500 ticks (respawn + walk back) and gives the enemy 100 gold / 150 XP. Deaths to towers or footmen give the enemy nothing, but deaths to enemy
heroes do. Implement in v5's structure, as one coherent change:
 (a) Threat assessment each tick: enemies = alive enemy heroes within 10 tiles; allies = alive allied heroes within 8 tiles of me (excluding me).
     Define outnumbered = enemies >= allies + 2, or (enemies >= 2 and my HP < 50%).
 (b) When outnumbered and no exposed enemy fort is within 12 tiles: disengage = walk toward the previous waypoint (rx, ry) 8 tiles at a time
     (recomputed each tick) until no enemy hero is within 12 tiles, then resume normal behaviour. Ranged classes may still attackTarget an enemy
     hero that is within basic range when their HP is above 60% (fire while falling back is not possible in one tick, so pick: when the nearest
     enemy melee hero is closer than 2 tiles, walk; else attack).
 (c) Keep v5's low-HP rules, but lower the flee threshold under 20% when an enemy hero is within 6 tiles.
 (d) Everything else identical to v5. Add a print line "DISENGAGE tick enemies allies hp".
Report: the change, code regions, risks, and which telemetry confirms it. Benchmarks the orchestrator will run: RACE, CLASH (primary), BASE,
and TURTLE (python3 tools/eval.py policy/cand_disengage.bas policy/spar_turtle.bas -n 2).
