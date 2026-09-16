# Task S38 — dodge pending enemy area spells (write policy/v127.bas from policy/v113.bas)
Base: policy/v113.bas (champion; farming + stutter-step kiting). GAME VERSION 36 exposes pending casts: loop k = 0 .. spellCount() - 1 with
spellAbility(k) (ability enum from content.nim, -1 for invalid), spellCasterId(k) (0 when the enemy caster is hidden), spellX(k)/spellY(k)
(impact position or area centre in whole tiles), spellImpactTick(k) (absolute tick; subtract worldTick for the remaining ticks). Allied casts
are listed too — skip a spell whose caster id is one of our team's hero ids (Red 100-104 when selfTeam = 0, Blue 105-109 when selfTeam = 1);
a spell with casterId = 0 is an enemy's. Area strikes worth dodging (damage / radius in tiles, from content.nim and docs/ARENA_NOTES.md):
Ricochet Disc 48 / 2, Storm Eagle 95 / line, Meteor Strike 70 / 2, Arcane Meteor 120 / 3, Golem Seed 85 / ~2, Shadow Comet 100 / ~2,
Frost Lance 42, Blazing Blade 90 (melee reach), Dark Eclipse / Void Portal / Molten Fist (see content.nim: read the enum order there and
list the ability ids you treat as area strikes with their radius; single-target strikes cannot be dodged by moving and must be ignored).
Heroes have 230-780 HP, so a 100-damage impact is 15-40% of a life.

1. Each decision, scan the pending spells once: for each enemy area strike whose remaining ticks are between 3 and 40 and whose impact
   centre is within (radius + 1) tiles of us (squared-distance test in tiles), record the nearest such spell: dodgeX/dodgeY, dodgeR2,
   dodgeTicks. (Instruction budget: spellCount is small; one loop is fine.)
2. Rule, inserted right AFTER the flee rule (act 1) and BEFORE the fort rule (act 5), i.e. it pre-empts fights, farming and kiting:
   if done = 0 and dodge found and lowHp = 0 is NOT required (dodge even at low HP): step (radius + 2) tiles directly away from the impact
   centre: stepToward(selfX, selfY, 2 * selfX - dodgeX, 2 * selfY - dodgeY, radius + 2); if the result is not terrainWalkable, use
   stepToward(selfX, selfY, rx, ry, radius + 2); walkTo(sx, sy); act = 50; done = 1. If we are exactly at the centre (dx = dy = 0), step
   toward rx, ry. Print "DODGE " ; worldTick ; " " ; spellAbility once per 240 ticks (lastDodgePrint).
3. Do not dodge while sieging a fort (fortId <> 0) — ending the game matters more. Nothing else changes; keep the death telemetry print.
Report: the ability ids and radii you used (quote the content.nim lines), new variables (no case-insensitive clashes), insertion lines.
Rules: int32 only, no elseif/for, NO blank line directly before `end if` or `wend` (compile error). Keep the diff minimal.
