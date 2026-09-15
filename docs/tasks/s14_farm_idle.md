# Task S14 — farm footmen whenever idle (write policy/v50.bas from policy/v49a.bas)
Base: policy/v49a.bas (champion for GAME VERSION 33 — read the top section of docs/ARENA_NOTES.md). Games now last up to 28,800 ticks and
heroes reach level 10-13; damage scales +5..+8 per level, so XP matters far more than before. v49a attacks enemy footmen only when engaged
(within 2.4 tiles) or for kill shots (hp <= 30 in range); mid campers in this league issue ~14,000 footman attack commands per game.
Change ONLY footman targeting, for all classes:
1. In the scan, track farmFoot = lowest-HP living enemy footman within farmR2, where farmR2 = (rng + 20)*(rng + 20)/100 for ranged heroes and
   25 for melee (5 tiles). Also require that the footman is NOT within (tower range + 1 tile) of any living enemy tower without our footman cover
   — simplest: skip footmen whose distance to nearTowerX/nearTowerY (v49a tracks the nearest living enemy tower) is <= (nearTowerRange/10 + 1)
   tiles when nearTowerWave = 0 and rng <= nearTowerRange.
2. Decide block: add `if done = 0 and routing = 0 and farmFoot <> 0 and lowHp = 0 and towerDanger = 0 then attackTarget(farmFoot); done = 1;
   act = 16; end if` immediately AFTER the last tower rule (act 6 / act 22 wait rule) and BEFORE the crippled-hero rule, so sieging and hero
   fights keep priority. While waiting for a wave (act 22) farming should take precedence: place the new rule BEFORE the act 22 wait rule.
3. Nothing else changes (shop, kiting, commitment, all-in stay as in v49a).
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
