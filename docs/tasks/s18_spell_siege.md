# Task S18 — spell siege from outside tower range (write policy/v57.bas from policy/v55.bas)
Base: policy/v55.bas (v49a + join allied pusher + all-in from tick 4000). GAME VERSION 33: towers 1200/2400/4800 HP, 28/56/112 dmg,
ranges 5.0/5.5/6.0 tiles (read the top of docs/ARENA_NOTES.md). Verified in the engine (tmp/engine_new/sim.nim): area spells cast with
castPoint(slot, tileX, tileY) damage towers and forts inside their footprint; castPoint/castTarget work for bot heroes alongside the engine's
auto-cast (they simply fail, returning 0, when the ability is on cooldown, out of charges, out of mana, or the aim point is out of range or
not visible). Host functions: castPoint(slot, x, y) [80 work], castTarget(slot, id) [80], abilityCharges(slot), abilityCooldown(slot).
Slots: 0 passive, 1 primary, 2 secondary, 3 ultimate. Relevant abilities (range in tiles from the caster to the AIM point; area radius):
- Ranger (class 1): slot 2 Ricochet Disc range 6.5, area radius 2.0, 48 dmg, cooldown 192, 32 mana; slot 3 Storm Eagle: a line from the caster
  8.0 tiles long and 1.5 wide toward the aim point, 95 dmg, cooldown 576, 80 mana.
- Arcanist (class 2): slot 2 Meteor Strike range 6.0, radius 2.0, 70 dmg, cd 216, 53 mana; slot 3 Arcane Meteor range 7.0, radius 3.0, 120 dmg,
  cd 600, 100 mana.
- Lich (class 7): slot 3 Bound Void range 6.5, RING footprint inner 0.67 / outer 2.0 tiles, 125 dmg, cd 648, 110 mana.
Mana regenerates 1 per 6 ticks; mana potion item 3 (+60 mana, 45 gold).
Add a "spell post" behaviour for classes 1, 2 and 7 only (selfClass); everything else unchanged:
1. Trigger: an exposed enemy tower is the current objective (otype = 1 and oid = towerId, towerId <> 0) and basic-attack siege is not allowed
   (siegeAllowed = 0) — i.e. exactly the situation where v55 waits (act 22). Replace that wait for these classes with:
2. Post = stepToward(towerX, towerY, rx, ry, P) -> (sx, sy) with P = 8 for the Ranger, 7 for Arcanist and Lich (P tiles from the tower along the
   route, outside the 6.0-tile gate range). Walk there (walkTo) when farther than 1.5 tiles (d2 > 2); act = 31.
3. When within 1.5 tiles of the post: aim = stepToward(towerX, towerY, selfX, selfY, A) -> (sx, sy) with A = 2 for Ranger/Arcanist, 1 for Lich
   (A tiles from the tower toward us, so the tower lies inside the area). Then, at most ONE cast per tick, try in order:
   Ranger: castPoint(3, towerX, towerY) [Storm Eagle line toward the tower] then castPoint(2, sx, sy);
   Arcanist: castPoint(3, sx, sy) then castPoint(2, sx, sy); Lich: castPoint(3, sx, sy).
   If a cast returned 1, act = 32 and done = 1. Otherwise keep attacking footmen/heroes in range via the existing rules (they come after),
   else walkTo(selfX, selfY) with act = 33. Never issue walkTo in the same tick as a successful cast.
4. Mana: in the shop block, for classes 1/2/7 buy item 3 when no slot holds item 3, selfGold >= 45 and selfMana * 100 < selfMaxMana * 50
   (one buy per tick, after the existing purchases); use it (useItem on its slot) when selfMana < 60 and the hero is at its post.
5. Print "POST " ; worldTick ; " tower " ; towerId once per post episode (rate-limit with a global postTowerId).
Keep the Crossbowman kiting, siege gating, commitment, join rule and all-in unchanged. Report new variables; confirm no name clashes;
no blank line directly before `end if` or `wend`.
