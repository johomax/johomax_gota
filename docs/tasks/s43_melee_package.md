# Task S43 — melee package: chase gate + farm-first + never outrun the lane wave (write policy/v139.bas from policy/v137.bas)
Base: policy/v137.bas (= v113 + S41 lane-aware wave rule for melee; see docs/tasks/s41_melee_lane_wave.md). Copy to policy/v139.bas
and apply ONLY the edits below. Hosted evidence: v135 (docs/tasks/s39) halved melee deaths and scored +12/120; v137 (movement only)
is level — its "walk to the front footman when more than 20 tiles behind" makes heroes queue behind their own creep waves in the
lane. v139 keeps v137's lane-aware anchor but drops that far trigger, and adds v135's two combat rules for melee.

1. Ride trigger: in the melee movement block (comment `' melee: move with our lane's wave ...`), change
   `if frontD2 > 16 and (myD2 < frontObjD2 or frontD2 > 400) then` to `if frontD2 > 16 and myD2 < frontObjD2 then`
   (only "ahead of our lane's front footman" pulls the hero back; a hero behind the wave walks normally).
   Update the block comment to `' melee: never run ahead of our lane's front footman toward an enemy tower; hold when the lane has no footman`.

2. First siege rule (act = 6, the one BEFORE the act 3 hero rule; condition starts
   `if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 and nearHeroD2 > 9 and siegeAllowed = 1 and siegeKiting = 0 then`):
   append ` and (melee = 0 or bestFoot = 0 or towerHp <= 300)` — a melee hero last-hits footmen before hitting a healthy tower
   (the second act 6 rule after act 4 is unchanged).

3. Hero rule (act = 3, condition starts `if done = 0 and routing = 0 and bestHero <> 0 and (allyNear8 + 1 >= enemyHeroNear or ...`):
   append ` and (melee = 0 or bestHeroD2 <= 4 or bestHeroHp * 2 < selfHp or allIn = 1)` — a melee hero only opens on an enemy hero
   that is already adjacent (within 2 tiles), nearly dead, or when an ally is within 8 tiles (no chasing kiters).

4. Header line after the v137 line: `' v139 = v137 without the far catch-up trigger, plus melee farm-first and the melee hero-chase gate (v135's combat rules).`
Nothing else changes. Report the edited line numbers and any deviation. Rules: NO blank line directly before `end if`/`wend`.
