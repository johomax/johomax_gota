Task W3 (candidate file policy/cand_econ.bas): optimize the ITEM BUILD and gold usage for a 2000-3000 tick race with fights.
Facts: 150 start gold; footman last-hit 15g, tower 75g, hero kill 100g. Boots (id 8, 100g) first is already proven (+12% move speed).
Items apply to any class: gauntlets 7 (+4 dmg, 70g), dagger 11 (+8, 110g), sword 13 (+10, 150g), axe 18 (+14, 180g), crossbow 19 (+14, 180g),
helmet 5 (+50 hp, 80g), buckler 6 (+60hp, 90g), armor 16 (+120hp, 160g), elixir 2 (+90hp, 50g), ration 1 (+40hp, 30g).
Max-HP items also heal by the delta immediately. There is NO natural HP regen; passives heal ~20-28 HP per 8 s for some classes.
Design and implement a build order + consumable policy (e.g. buy gauntlets at 70g right after boots; buy elixir only when HP < 60%; use potions at 50%;
consider armor vs damage by class), keeping everything else identical to v5. Measure RACE, CLASH, BASE. Report win rates and mean ticks.
