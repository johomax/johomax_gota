# Task S42 — apply the lane-wave movement discipline to every class (write policy/v138.bas from policy/v137.bas)
Base: policy/v137.bas (= v113 + S41 melee lane-wave rule, see docs/tasks/s41_melee_lane_wave.md). Copy to policy/v138.bas and apply
ONLY the edits below.
1. In the movement block that starts with the comment `' melee: move with our lane's wave toward an enemy tower ...`, remove the
   `melee = 1 and` term from its opening condition so it reads
   `if done = 0 and routing = 0 and lowHp = 0 and fortId = 0 and openLane < 0 and otype = 1 and oi >= 3 and allIn = 0 and towerDanger = 0 then`
   and change the comment to `' all classes: move with our lane's wave toward an enemy tower - catch it from far behind, never run ahead of it, hold when it is gone`.
   The block stays where it is (after the act 4 farm rule; the ranged kiting rules 45/46 and the safe-siege rule precede it).
2. Header comment line after the v137 line: `' v138 = v137 with the lane-wave movement rule for ranged classes too.`
Nothing else changes. Report the edited line numbers. Rules: NO blank line directly before `end if` or `wend`.
