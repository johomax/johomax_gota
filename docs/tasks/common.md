Read /Users/jordan/Desktop/Projects/johomax/gota/docs/WORKER_BRIEF.md first, then docs/ARENA_NOTES.md, then the base policy
/Users/jordan/Desktop/Projects/johomax/gota/policy/v5.bas (the current best: five heroes push one side lane as a stack, Red lane 0 / Blue lane 2,
objectives derived from own tower positions + point symmetry, focus fire, footman last-hits, siege, kiting, stuck recovery).

Benchmarks (run from /Users/jordan/Desktop/Projects/johomax/gota, one at a time, never two evals concurrently):
  RACE  : python3 tools/eval.py policy/<cand>.bas policy/v5.bas -n 3 --tag <cand>-race      (mirror lanes never meet: pure speed; must not get worse)
  CLASH : python3 tools/eval.py policy/<cand>.bas policy/v5.bas -n 3 --tag <cand>-clash --clash   (both teams pushed into lane 2 so they collide: fight quality)
  BASE  : python3 tools/eval.py policy/<cand>.bas policy/base.bas -n 1 --tag <cand>-base   (sanity vs bundled baseline; must stay 2/2)
Each prints per-game rows (side, seed idx, winner A/B, ticks, per-hero total XP) and A's win rate. Read hero telemetry in
runs/<tag>/*/episode-*/logs/policy_agent_<slot>.log (lines: T tick pos hp level gold objective act enemies allies; K kill rewards; D respawns; STUCK).
`clash = 0` must remain in your candidate exactly as in v5 (the harness flips it). A compile error appears within 2 s as `BASIC error: line L ...`.

Deliverable: write policy/<cand>.bas (one focused change on top of v5, keep everything else byte-identical where possible),
run RACE, CLASH and BASE, and reply with: the change (one paragraph), the three result lines verbatim, mean ticks, telemetry observations,
and adopt/reject recommendation. Do not modify v5.bas, tools/, docs/, or git.
