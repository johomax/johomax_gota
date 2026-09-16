# Task S32 — focus fire with allies via objectTarget (write policy/v95.bas from policy/v87.bas)
Base: policy/v87.bas (champion since 00:42 UTC 2026-09-16). GAME VERSION 36 exposes `objectTarget(i)`: the object's current attack-target
id, or 0 when it has none or the target is not visible to our team. Hero ids are 100-104 (Red) and 105-109 (Blue); an enemy hero is any
hero whose objectTeam(i) <> selfTeam. Games are decided by hero fights around towers; concentrated damage wins them, and today our hero
picks the lowest-HP enemy hero within heroR2 on its own odds rule (act 3) regardless of what allies are hitting.

1. Scan (inside the existing object loop, k = 2 branch for heroes): for each LIVING ALLIED hero (objectTeam(i) = selfTeam, objectAlive(i) = 1,
   objectId(i) <> selfId) within 12 tiles (d2 <= 144), read t = objectTarget(i). If t is between 100 and 109 and t is not one of our own
   team's ids (Red ids 100-104 when selfTeam = 0, Blue 105-109 when selfTeam = 1), record it: keep up to 4 candidate target ids with a count
   of allies attacking each (arrays focusId(4), focusN(4), focusK entries; reset every decision). After the loop, focusTarget = the id with the
   largest count (ties: the one seen first); focusTarget = 0 when none.
2. Validate: focusTarget must be a visible living enemy hero this decision — during the scan also record for every visible enemy hero its id,
   x, y, hp (arrays already exist for seenEnemyX/Y; add seenEnemyId(9) and seenEnemyHp(9) alongside, same index). After the loop find
   focusTarget's entry; if not found set focusTarget = 0. Compute focusD2 = squared distance to it.
3. Decide: insert a rule AFTER the flee (act 1), melee-step (act 2), fort (act 5), kite (act 28), open-lane (act 37), step-out-of-tower-range
   rules and BEFORE the escort rule (act 35) and the siege rule (act 6):
   if done = 0 and routing = 0 and focusTarget <> 0 and lowHp = 0 and focusD2 <= heroR2 * 4 and towerDanger = 0 then
     attackTarget(focusTarget) ; act = 40 ; done = 1
   (heroR2 * 4 = twice the hero engage radius, so we close in on a fight allies already started). Print "FOCUS " ; worldTick ; " " ; focusTarget
   at most once every 480 ticks (track lastFocusPrint).
4. Nothing else changes; v87's farming and all other rules stay.
Report the new variables (no name clashes; identifiers are case-insensitive), the insertion line numbers, and the instruction-budget impact of the
extra scan work (must stay well under 20k instructions per decision; the loop already runs once over all objects — do not add a second full pass).
Rules: int32 only, no elseif/for, NO blank line directly before `end if` or `wend` (compile error). Keep the diff minimal.
