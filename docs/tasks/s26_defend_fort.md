# Task S26 — defend our own exposed fort (write policy/v77.bas from policy/v75.bas)
Base: policy/v75.bas (champion). GAME VERSION 34 (docs/ARENA_NOTES.md top): towers 900/1200/1800 HP, 18/24/30 dmg; games end decisively
(few timeouts), so preventing a loss now keeps the game alive for our own push. The fort has 400 HP, does not shoot, and is exposed once any of
its three lane towers are all dead (objectAlive(i) = 1 for a fort means exposed and alive; own objects are always visible).
v75 already rushes the ENEMY fort at any distance when exposed. Add the mirror for OUR fort:
1. In the scan, for our own fort (kind 1, team = selfTeam): ownFortX/ownFortY (= homeX/homeY already), ownFortExposed = objectAlive(i),
   ownFortHp = objectHp(i). Count enemy heroes within 15 tiles of our fort (enemy hero branch: d2 to homeX/homeY <= 225) as fortThreats and
   enemy footmen within 8 tiles of it as fortCreeps.
2. defendFort = 1 when ownFortExposed = 1 and (fortThreats >= 1 or fortCreeps >= 2) and the enemy fort is NOT exposed/visible (fortId = 0)
   and my squared distance to home <= 3600 (within 60 tiles — otherwise I cannot arrive in time). Print "FORTDEF " ; worldTick once per
   episode (track prevFortDef).
3. While defendFort = 1: this overrides lane/escort/join logic — placed right AFTER the enemy-fort attack rule (act 5) and BEFORE everything
   else: if an enemy hero is within my basic range, attack the lowest-HP one (bestHero rule semantics); else if an enemy footman within basic
   range, attack the lowest-HP one; else if my squared distance to (homeX, homeY) > 9, walkTo(homeX, homeY), act = 38; else walkTo(selfX, selfY),
   act = 39. done = 1 in all cases.
4. When defendFort drops to 0 the normal behaviour resumes (oi unchanged).
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
