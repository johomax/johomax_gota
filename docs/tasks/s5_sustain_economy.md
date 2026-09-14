# Task S5 — sustain economy (write policy/v31.bas from policy/v30.bas)
Base: policy/v30.bas (= v19 without post-respawn home guard and without the ally hold; otherwise identical to the v19 structure in the brief).
Our hero dies ~2.3 times per game and each death costs ~2200 ticks of walking (a third of the game). Potions are cheap HP:
elixir (id 2) +90 HP for 50 gold, ration (id 1) +40 HP for 30 gold; consumables stack in one slot (8 per slot); useItem(slot) heals instantly.
v19/v30 buy boots (id 8, 100 gold) first at tick 1, leaving 50 gold, and buy an elixir only when HP < 55% with no potion in stock.
Change ONLY the shopping/consumables block:
1. Count potions in inventory: walk the 6 slots with itemId(slot); there is no item-count host call, so track stock yourself: keep a global
   potCount that you increment on a successful buy and decrement on use. A buy is successful when selfGold drops by the item cost between
   ticks — simpler: only buy when selfGold >= cost, call buyItem once per tick at most, and set potCount = potCount + 1 in the same tick;
   guard against failures by resyncing potCount = 0 whenever no slot holds item 1 or 2 (potSlot < 0).
2. Priority each tick (at most ONE buyItem call per tick): (a) if potCount < 2 and selfGold >= 50 -> buyItem(2); else (b) boots once
   (track bootsBought) when selfGold >= 100; else (c) dagger id 11 once when selfGold >= 110; else (d) axe id 18 once when selfGold >= 180;
   else (e) armor id 16 once when selfGold >= 160; keep a potion reserve: never buy equipment if it would leave less than 50 gold while potCount < 1.
3. Drinking: useItem(potSlot) when selfHp*100 < selfMaxHp*60 and (enemyHeroNear > 0 or towerId <> 0), or when selfHp*100 < selfMaxHp*45
   at any time; at most one useItem per tick. Note: enemyHeroNear/towerId are computed later in the scan, so use the values from the
   previous tick (they are globals; that is fine).
Keep the "K"/"D"/"T" telemetry intact. Report the new variables and confirm no name clashes (potSlot, slot, iid exist already).
