# AGENTS.md

Start here for any agent working in this repo:

1. Read `docs/ARENA_NOTES.md` (verified mechanics + host API + map coordinates) and `README.md`.
2. League participation guide: https://softmax.com/api/observatory/v2/participate?league_id=league_3c60897b-25cf-4b37-9d1a-8554c1198f28
   (saved copy: `docs/participate.md`). Coworld README: https://github.com/Metta-AI/coworld/blob/main/README.md
3. Engine source (authoritative): `source/polyworld/examples/gods_of_the_arena/{sim,bots,content}.nim` at commit d03d2d1 (sparse clone; gitignored).
4. Policy contract: one `.bas` file, int32 BASIC, one decision per tick per hero, 20k instructions / 50k work units per decision.
   Invalid syntax or division by zero fails the VM. Test locally with `tools/eval.py` before uploading.
5. Working agreement: one attributable change per version, measure locally (both sides, several seeds), then hosted XP requests
   against top league policies, then submit only when the evidence says it is better.
