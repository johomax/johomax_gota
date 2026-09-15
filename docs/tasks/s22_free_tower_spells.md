# Task S22 — opportunistic tower spells (write policy/v64.bas from policy/v51.bas)
Base: policy/v51.bas (champion). GAME VERSION 33 (docs/ARENA_NOTES.md top). Verified: castPoint(slot, tileX, tileY) area spells damage
towers inside their footprint from outside the tower's range, and work alongside auto-cast. v57 tried to replace fighting with spell
"posts" and lost badly; this task only ADDS free casts without changing any movement, targeting or fighting decision.
Relevant abilities (range = caster to AIM point, in tiles; area radius): Ranger (class 1) slot 2 Ricochet Disc 6.5 r2.0, slot 3 Storm Eagle
8.0-tile line toward the aim; Arcanist (class 2) slot 2 Meteor Strike 6.0 r2.0, slot 3 Arcane Meteor 7.0 r3.0; Lich (class 7) slot 3 Bound
Void 6.5 ring 0.67-2.0; Crossbowman (class 6) slot 3 Clockwork Charge 7.5-tile capsule toward the aim.
Rule (add near the end of the decide block, AFTER all existing rules have run and regardless of `done`; it issues no walkTo/attackTarget):
1. Only for classes 1, 2, 6, 7 and only when no enemy hero is within 10 tiles (nearHeroD2 > 100) — fights keep their auto-casts.
2. Target: the nearest exposed enemy tower within 8 tiles (towerId/towerX/towerY exist when within 9 tiles; require towerD2 <= 64) that is
   NOT already within our basic range (skip if rng > towerRange, the Crossbowman then uses basic attacks anyway).
3. aim = stepToward(towerX, towerY, selfX, selfY, 2) (2 tiles from the tower toward us). At most ONE castPoint per tick, tried in order:
   class 1: castPoint(3, towerX, towerY), then castPoint(2, sx, sy); class 2: castPoint(3, sx, sy), then castPoint(2, sx, sy);
   class 7: castPoint(3, sx, sy) with aim 1 tile from the tower; class 6: castPoint(3, towerX, towerY).
   Do not spend mana below 40% of selfMaxMana (keep it for fights): skip when selfMana * 100 < selfMaxMana * 40.
4. Count successful casts in a global towerCasts and include it in the existing "T" telemetry line as " tc " ; towerCasts.
Everything else stays byte-identical. Report the new variables and confirm no name clashes. No blank line directly before `end if`/`wend`.
