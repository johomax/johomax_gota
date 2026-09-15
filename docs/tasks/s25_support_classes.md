# Task S25 — support classes stick with the allied group (write policy/v70.bas from policy/v68.bas)
Base: policy/v68.bas (champion). GAME VERSION 33 (docs/ARENA_NOTES.md top). Our worst seats are Blue's Vanguard Knight (class 0: 330 HP tank,
1.17-tile range, low damage) and Druid Warden (class 3: its Healing Bloom / Kindred Wisps auto-cast heals ALLIED heroes within ~4 tiles whenever
they are hurt, and Nature Talisman heals itself). Both are support classes that achieve nothing alone in a side lane (3/24 wins each in the
last ten-seat batch) but add real value next to allies: the Druid heals the group, the VK soaks tower shots and blocks chasers.
Add ONE behaviour for selfClass = 0 or selfClass = 3 only (Blue seats 5 and 8):
1. In the scan, collect living allied hero positions (allyX/allyY arrays exist in v68 for the join rule — reuse them; liveAllies is the count).
2. Every 240 ticks (worldTick mod 240 = 0) when routing = 0 and fortId = 0 and worldTick >= 900: find the allied hero that has the most OTHER
   allies within 12 tiles (d2 <= 144) — the group anchor. If that anchor has >= 1 such neighbour (a group of 2+) then groupUntil = worldTick + 240,
   remember anchorX/anchorY (update them every tick from the anchor's id while it is alive; anchorId). Print "GROUP " ; worldTick once when
   group mode starts (track prevGroup).
3. While worldTick < groupUntil and the anchor is alive: if my squared distance to the anchor > 16 (4 tiles) and no enemy hero is within my
   basic range and towerDanger = 0: walkTo(anchorX, anchorY), act = 36, done = 1 — placed AFTER the fort/standoff/kite rules and BEFORE the
   tower rules. Within 4 tiles the normal rules apply (fight, siege with allIn = 1 since allies are near). pushLane/oi unchanged.
4. Everything else (Crossbowman escort for Red, join rule, weakest-lane switch, all-in, shop) unchanged.
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
