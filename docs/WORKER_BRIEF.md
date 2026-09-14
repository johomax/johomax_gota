# Brief for policy-iteration workers (Codex)

You are improving a BASIC hero policy for the game Gods of the Arena. Work ONLY inside
/Users/jordan/Desktop/Projects/johomax/gota. Do not touch git (the orchestrator commits).

## Read first (in this order)
1. docs/ARENA_NOTES.md — verified mechanics, host API, map coordinates, per-decision limits, BASIC dialect.
2. The current best policy file named in your task (e.g. policy/v4.bas). Keep its structure; make ONE focused change.
3. docs/map_kinds.txt if your change involves positions/routes (x right, y down, 0..127).
4. Engine source if you need exact semantics: source/polyworld/examples/gods_of_the_arena/sim.nim (updateHero ~line 2603,
   applyWalkTo/applyAttackTarget ~1468-1545, castAbility ~2254, tryCombatAbilities ~2491, updateTower ~1621, updateFootman ~1698),
   bots.nim (host functions), content.nim (class/ability/item numbers).

## BASIC dialect gotchas (compile errors fail the whole team's episode)
- Identifiers are CASE-INSENSITIVE and share one namespace: a scalar `ox` clashes with array `oX`. Use distinct names.
- No `elseif`, no `for`, no single-line `if x then stmt`. Blocks: `if c then` / `else` / `end if`; `while c` / `wend`.
- `sub name(a, b)` ... `end sub`; subs return nothing (write results to globals); call as `name(args)`.
- `dim arr(N)` only at top level (inclusive upper bound N). Globals persist across ticks; params are local.
- `and`/`or` do NOT short-circuit. Division by zero kills the VM for the rest of the match. int32 only.
- Per decision: 20,000 instructions, 50,000 work units (walkTo=800, object queries=4, terrain=32), print <=128 events/1024 bytes.
- Exactly one movement command per tick: walkTo(...) cancels an attack; attackTarget(...) after walkTo overrides.

## How to test (Docker via OrbStack; each episode ~5-40 s)
```bash
cd /Users/jordan/Desktop/Projects/johomax/gota
python3 tools/eval.py policy/CANDIDATE.bas policy/BEST.bas -n 3 --tag <name>   # mirror: candidate vs current best, both sides, 6 games
python3 tools/eval.py policy/CANDIDATE.bas policy/base.bas -n 2 --tag <name>-base   # sanity vs bundled baseline
```
Never run two eval.py invocations at the same time (staged player files collide). Each prints per-game rows
(side, seed index, winner A/B, ticks, per-hero total XP) and A's overall win rate. Hero telemetry prints land in
runs/<tag>/<a_red|b_red>/episode-000N/logs/policy_agent_<slot>.log (slots 0-4 red, 5-9 blue). A BASIC compile error shows
up as `BASIC error: line L, column C: ...` in those logs (or the run fails within 2 s).

## Deliverable
- Write your candidate to the path named in the task (do not overwrite the best policy).
- Report: what you changed (one paragraph), the exact eval commands and their result lines, mean ticks, anything surprising
  in the telemetry, and your recommendation (adopt / reject / needs hosted test). Be concise and factual.
