# Task S37 — audit policy/v113.bas for rules that cannot fire or fire wrongly (report only, change nothing)
Context: policy/v113.bas is the league champion (BASIC, one decision per tick, int32, see docs/WORKER_BRIEF2.md for the dialect and
docs/ARENA_NOTES.md top for game version 36). We found one dead block by telemetry: the "home guard after respawn" rule (act 14) checks
worldTick < guardUntil but guardUntil is never armed, so it never runs; another rule (v102) was gated on `oi < 3 and routing = 0`, which
after a respawn is never true (the objective index stays at the enemy tower and rejoin sets routing = 1). Hosted telemetry per game
(tools/log_stats.py act share): walk 39%, farm 14.5%, siege 13.5%, escort 6.4%, fight 5.1%, wait-for-wave 4.5%, open-lane 3.4%,
kite-hit 2.8%, step-out-of-tower-range 2.5%, low-HP retreat 2.2%, flee 2.1%, unstick 1.5%, melee-step 1.9%, kite-step ~0.5%, fort 1.2%,
kite (act 28) 0.4%, hold (act 8) 0%, guard (act 14) 0%, crippled reset (act 12) ~0%.

Read the whole file and report, with line numbers:
1. Rules or branches that can never execute (variables never set, conditions contradictory, timers never armed, prints never reached).
2. Rules whose gating variables mean something different from what the comment implies (e.g. `oi` after respawn, `routing`, `allIn`,
   `towerDanger`, `enemyHeroNear` radius 10 tiles vs `nearHeroD2`, `rng` in tenths of tiles vs tile^2 comparisons, world units vs tiles).
3. Unit or overflow mistakes (int32; world units are 60000 per tile; ranges in tenths of tiles; distances squared in tiles).
4. Ordering problems: an earlier rule that always pre-empts a later one so the later one is dead in practice.
5. The `hold`/`noHold`/`holdTicks` machinery (act 8): is it ever active? The `resistance` counter: is it used?
6. Anything in the shop code that cannot buy (six inventory slots; potions occupy one slot).
For each finding give: line(s), what happens, why, and a one-line proposed fix. Do NOT edit any file. Be concrete and skip style remarks.
