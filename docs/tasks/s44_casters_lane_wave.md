# Task S44 — casters share the melee "never outrun the wave" rule (write policy/v141.bas from policy/v139.bas)
Base: policy/v139.bas (= v113 + S41/S43 melee package, see docs/tasks/s43_melee_package.md). Copy to policy/v141.bas and apply ONLY
the edits below. Evidence: Arcanist (class 2), Lich (7) and Warlock (8) die 2.9-3.9 times per game; their deaths before tick 3000
cluster at the lane corner beside the enemy outer tower, where they arrive at level 1-2 ahead of any creep wave. v138 applied the
full v137 rule (with a "catch up from 20 tiles behind" trigger) to every class and hurt Ranger/Xbow/Lich/Warlock; v139 dropped that
trigger and reads +26/240 on melee seats. Ranger (1), Crossbowman (6) and Druid (3) must keep v139's behaviour exactly.

1. Init block (next to `melee = 0` / `if selfClass = 0 or selfClass = 4 or selfClass = 5 or selfClass = 9 then melee = 1`): add
   ```
   waveBound = melee
   if selfClass = 2 or selfClass = 7 or selfClass = 8 then
     waveBound = 1
   end if
   ```
2. Movement block (comment starts `' melee: never run ahead of our lane's front footman ...`): change its opening condition's
   `melee = 1` to `waveBound = 1`; update the comment to start with `' melee and casters:`. Nothing else in the block changes
   (no far trigger; the hold/back-off branch stays).
3. The two melee combat gates from S43 (first siege rule `(melee = 0 or bestFoot = 0 or towerHp <= 300)` and the hero rule
   `(melee = 0 or bestHeroD2 <= 4 or ...)`) stay keyed on `melee` — do NOT change them.
4. Header line after the v139 line: `' v141 = v139 with the wave-bound movement rule for Arcanist, Lich and Warlock as well.`
Report the edited line numbers and any deviation. Rules: int32 only, NO blank line directly before `end if`/`wend`; check
`waveBound` does not clash with an existing identifier (case-insensitive).
