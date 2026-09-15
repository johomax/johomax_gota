# Task S28 — target-aware siege using objectTarget (write policy/v82.bas from policy/v76.bas)
Base: policy/v76.bas (champion). GAME VERSION 36 (docs/ARENA_NOTES.md top): towers 900/1200/1800 HP, 18/24/30 dmg every 24 ticks, ranges
5/5.5/6 tiles; towers shoot the nearest enemy FOOTMAN first and heroes only when no footman is in range. NEW host function: objectTarget(i)
returns the id of object i's current attack target when that target is visible to us (0 otherwise). For an enemy tower this tells us whether
it is shooting a footman (safe window) or a hero — including us (selfId).
v76 gates basic-attack sieging (siegeAllowed) on: out-ranging the tower, allied footmen within 3 tiles of it (waveAtTower), fort exposed,
allIn, or tower HP <= 300; otherwise it waits outside range (act 22). Replace the crude footman-cover test with the real signal:
1. In the scan, when the objective tower (towerId) is recorded, also read towerTarget = objectTarget(i). After the scan compute
   towerBusy = 1 if towerTarget <> 0 and towerTarget <> selfId (it is shooting someone else — footman or another hero), else 0.
   Also for the nearest living enemy tower (nearTower*): nearTowerTarget/nearTowerBusy the same way.
2. siegeAllowed: add "or towerBusy = 1" to the existing conditions. towerDanger (step out of range): require nearTowerBusy = 0 as well, i.e.
   only back out when the nearest living tower is idle or targeting me. Keep everything else (allIn, range advantage, low-HP finish).
3. Add a hard safety: if the objective tower's target is me (towerTarget = selfId) and selfHp * 100 < selfMaxHp * 45 and allIn = 0 and
   rng <= towerRange, step out immediately (the existing act 15 movement), even if footmen are around.
4. Count ticks sieging under towerBusy in a global busySiege and add " bs " ; busySiege to the "T" telemetry line.
Report the new variables and confirm no name clashes. No blank line directly before `end if` or `wend`.
