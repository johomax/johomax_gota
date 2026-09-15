# Task S12 — take the outer tower, then hold the line instead of diving alone (write policy/v44.bas from policy/v30.bas)
Base: policy/v30.bas (= v19 without post-respawn home guard and without the ally hold).
Evidence: our hero reaches the enemy outer tower at ~tick 1000 and usually kills it (median tick 1300), then walks on to the enemy inner/gate
towers where 70% of its deaths happen (1-2 enemy heroes, no allies within 25 tiles). Each death costs ~2200 ticks. Games are decided later
(first gate attack ~tick 4000-4300) by 3-5 heroes together.
Change ONLY the advance decision after the outer tower in our lane is dead:
1. holdLine = 1 when: routeDead(pushLane*7+3) = 1 (enemy outer tower of our lane dead), oi >= 4, allyCount < 2 (allies within 25 tiles, exists),
   the current objective tower is standing with objectHp > 400 (track objHp when the scan finds the objective tower; treat unknown/not visible as
   1000), and worldTick < 4000. Otherwise holdLine = 0.
2. While holdLine = 1 the hero stays near the dead outer tower point (wpX(3), wpY(3)), standing 4 tiles down-lane toward the inner tower
   (stepToward(wpX(3), wpY(3), wpX(4), wpY(4), 4) -> holdX/holdY), and:
   a. fights as usual (existing flee/kite/fort/hero/footman rules stay above this logic and still fire),
   b. additionally attacks ANY enemy footman within basic range (lowest HP first) — track farmFoot in the scan with d2 <= footR2 and no hp
      condition, and use it when bestFoot = 0, act = 16,
   c. otherwise walks to holdX/holdY (walkTo(selfX, selfY) when within 1.5 tiles, d2 <= 2), act = 26.
   It must NOT walk toward the inner tower objective while holdLine = 1 (guard the final "walk to objective" branch with holdLine = 0).
3. When holdLine drops to 0 (an ally arrived, the tower got low, or tick 4000) the normal push resumes unchanged.
4. Print "HOLD " ; worldTick once when holdLine turns 1 and "HOLD end " ; worldTick when it turns 0 again (track prevHold).
Report the new variables and confirm no name clashes. Remember: no blank line directly before `end if` or `wend`.
