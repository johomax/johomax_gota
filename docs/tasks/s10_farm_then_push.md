# Task S10 — farm at the own outer tower, then push (write policy/v40.bas from policy/v39.bas)
Base: policy/v39.bas (= v30 + damage-first shopping: dagger at tick 1, then boots, elixir, axe, sword, armor, crossbow, one buy per tick).
Evidence: the strongest entrant in random rosters (red-kite, +9 points as Red) buys a dagger at tick 1, waits near ITS OWN outer tower until
~tick 2500 killing every enemy footman that arrives (footman kill = 25 XP / 15 gold), buys sword/axe/armor from that income, and only then
walks down the lane and sieges the enemy towers with ~+30 damage and 2-3 extra levels. Our hero instead reaches the enemy outer tower at
~tick 1000 with no items, dies ~2.3 times per game and ends at level 3-5 with ~50 gold.
Change ONLY the early game (add a "farm phase"); the push logic afterwards stays exactly as in v39:
1. farmPhase = 1 from init until (worldTick >= 2400) or (selfLevel >= 4) or (an allied hero is sieging: any exposed enemy tower objectAlive=1
   within 9 tiles of the hero — i.e. towerId <> 0 — which means the wave already broke through). Print "FARM end" ; worldTick once when it ends.
2. During farmPhase the objective is the own outer tower point wpX(2)/wpY(2) (route index pushLane*7+2). Stand 3 tiles down-lane from it
   toward the enemy outer tower: farmX/farmY = stepToward(wpX(2), wpY(2), wpX(3), wpY(3), 3) -> (sx, sy). Decide block during farmPhase
   (put it before the normal decide block and set done = 1 when it acts):
   a. potions/flee as usual (keep the existing rules above it if they are earlier in the file; otherwise replicate the <15% flee).
   b. if an enemy hero is within 10 tiles and (enemyHeroNear > allyNear8 + 1 or selfHp*100 < selfMaxHp*50): walk back to wpX(2)/wpY(2)
      (under the tower), act = 23. Count allyNear8 = allied heroes within 8 tiles in the scan.
   c. else if an enemy hero is in basic range (bestHero <> 0): attackTarget(bestHero), act = 3.
   d. else if any enemy footman is within basic range: attack the lowest-HP one (track farmFoot like bestFoot but with d2 <= footR2 and no
      hp condition), act = 16. Melee heroes: use d2 <= 9 for footmen.
   e. else walk to (farmX, farmY) if farther than 1.5 tiles (d2 > 2), otherwise walkTo(selfX, selfY); act = 24.
3. When farmPhase ends, set oi to the first standing enemy tower objective (call firstStanding(pushLane); oi = firstOi) so the hero walks
   straight down the lane.
4. Do not change the shop, the scan (other than adding farmFoot/allyNear8), telemetry, or the normal decide block.
Report the new variables and confirm no name clashes.
