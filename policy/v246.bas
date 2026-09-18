' GOTA policy v5 "edge blitz, map-generic": all five heroes push one side lane
' as a stack. Objectives come from own tower positions (always visible) and the
' map's point symmetry (enemy = (W-1-x, H-1-y)), so no coordinates are hardcoded.
' Red pushes lane 0, Blue pushes lane 2 (mirror images). See docs/ARENA_NOTES.md.
' v46 = v45 + mass dives (2 allies near), late-game all-in (tick 22000), finish low towers, 25% flee, fight odds, damage-first shop.
' v49a = v47 (tower-safe siege + long-range kiting) committed to one lane (no lane switch/rejoin), all-in from one ally or tick 12000.
' v76 = v75 + head for an enemy fort as soon as its lane's gate is known dead, even before the fort is visible.
' v93 = v87 + keep farming footmen in basic range while travelling between lanes or rejoining (no enemy hero near, no tower danger).
' v87 = v76 + farm enemy footmen within 8 tiles (melee 6) instead of walking or waiting for a wave.
' v137 = v113 + melee heroes move with their lane's creep wave (catch it, never outrun it, hold when it is gone).
' v148 = v147 + a building objective that is not in the object list while we stand within 4 tiles counts as dead (version 37 hides dead buildings); marks routeDead/laneTowerHp.
' v246 = v228 + siege spells: every ability slot cast at the enemy tower/guard in reach when no enemy hero is within 10 tiles.
' v228 = v218 with the group focus limited to lane towers (not fort guards).
' v218 = v215 with the camped-lane (resistance) switch disabled — stay mid after the collision and push.
' v215 = v212 (v209 with the conservative ally-majority rule, no Red hold) + boots (item 8) bought before the dagger.
' v212 = v209 with a conservative ally-majority rule (ticks 600/1200 only, needs +2 allies on the other lane) — 5v5 competition fix.
' v209 = v208 (adaptive lane + defended-lane switch) + group focus (v205): siege the tower in reach whenever two allies are within 8 tiles.
' v208 = v207 + defended-lane switch: when two or more enemy heroes camp our objective tower (resistance >= 90), switch to the lane farthest from the enemies seen; lock 1500 ticks.
' v207 = v192 + adaptive lane: from tick 600 to 3000 join the lane where most allies are (two or more, more than on ours), re-checked every 600 ticks.
' v192 = v186 with Red pushing the mid lane (pushLane 1): on the guarded-gods engine Red wins only ~0.4 and mid is the breakthrough lane in half the games — Red-seat random-roster test vs a concurrent v186 Red batch.
' v186 = v177 + guard focus: when the tower in reach is a fort guard and our wave is on it, siege it regardless of nearby enemy heroes or the melee farm-first gate (act 54) — the guard siege is what the 10000-tick games turn on.
' v177 = v175 + guard objective: while the enemy fort is still shielded, the last objective is the nearest exposed guard tower (siege/wait rules apply to it: stay outside its 6-tile reach until the wave arrives); the open-lane fort walk stops once a guard is known, so the hero no longer stands in the double guard crossfire (v175 died 5-9 times per game on the guarded-gods engine).
' v175 = v148 + god-guard hotfix for the guarded-gods engine (2026-09-16 ~22:30 UTC, coworlds cow_703e69a4 / cow_126f2fcb): towers with id >= 28 are the fort's guard towers, not lane towers — they no longer feed the lane route arrays (v148 died at init with 'routex index 23'); they stay valid siege targets once exposed.
' v147 = v139 with building-aware walking for game version 37: objective, flee, unstick and fort-approach walks stop 3 tiles short of buildings; beside a building objective the hero issues no walk (act 23).
' v139 = v137 without the far catch-up trigger, plus melee farm-first and the melee hero-chase gate (v135's combat rules).

dim wpX(8)
dim wpY(8)
dim wpId(8)
dim wpKind(8)
dim routeX(20)
dim routeY(20)
dim routeId(20)
dim routeKind(20)
dim routeDead(20)
dim seenEnemyX(4)
dim seenEnemyY(4)
dim allyX(9)
dim allyY(9)
dim joinCount(2)
dim laneAllies(3)
dim laneTowerHp(8)
dim laneRemain(2)

sub loadLane(loadLaneId)
  copyPoint = 0
  while copyPoint < 7
    copyIndex = loadLaneId * 7 + copyPoint
    wpX(copyPoint) = routeX(copyIndex)
    wpY(copyPoint) = routeY(copyIndex)
    wpId(copyPoint) = routeId(copyIndex)
    wpKind(copyPoint) = routeKind(copyIndex)
    copyPoint = copyPoint + 1
  wend
end sub

sub firstStanding(firstLaneId)
  firstOi = 3
  while firstOi < 6 and routeDead(firstLaneId * 7 + firstOi) = 1
    firstOi = firstOi + 1
  wend
end sub

sub adoptLane(nextLaneId, laneReason)
  oldLane = pushLane
  pushLane = nextLaneId
  laneChanged = 1
  loadLane(pushLane)
  firstStanding(pushLane)
  oi = firstOi
  resistance = 0
  stuckTicks = 0
  stuckHits = 0
  unstick = 0
  guardId = 0
  guardX = 0
  guardY = 0
  guardD2 = 1000000
  holdTicks = 0
  if oldLane <> pushLane then
    lastLaneTick = worldTick
  end if
  if laneReason = 1 then
    print "LANE " ; worldTick ; " " ; oldLane ; " " ; pushLane ; " resistance"
  else
    print "LANE " ; worldTick ; " " ; oldLane ; " " ; pushLane ; " rejoin"
  end if
end sub

sub isqrt(v)
  if v <= 0 then
    sq = 0
    exit sub
  end if
  r = v
  if r > 20000 then
    r = 20000
  end if
  it = 0
  while it < 14
    r = (r + v / r) / 2
    it = it + 1
  wend
  sq = r
end sub

sub stepToward(fx, fy, tx, ty, k)
  ddx = tx - fx
  ddy = ty - fy
  isqrt(ddx * ddx + ddy * ddy)
  if sq = 0 then
    sx = fx
    sy = fy
    exit sub
  end if
  sx = fx + ddx * k / sq
  sy = fy + ddy * k / sq
  if sx < 0 then
    sx = 0
  end if
  if sy < 0 then
    sy = 0
  end if
  if sx > mapWidth - 1 then
    sx = mapWidth - 1
  end if
  if sy > mapHeight - 1 then
    sy = mapHeight - 1
  end if
end sub

' ---------- one-time init: discover own structures, derive route ----------
if inited = 0 then
  inited = 1
  pushLane = 1
  if selfTeam = 1 then
    pushLane = 0
  end if
  ' clash = 1 makes both teams push lane 2 so they meet head-on (local fight benchmark only)
  clash = 0
  if clash = 1 then
    pushLane = 2
  end if
  routeLane = 0
  while routeLane < 3
    laneTowerHp(routeLane * 3) = 1200
    laneTowerHp(routeLane * 3 + 1) = 2400
    laneTowerHp(routeLane * 3 + 2) = 4800
    routeLane = routeLane + 1
  wend
  ' Seven points per lane: own gate->outer, enemy outer->gate, enemy fort.
  ownBase = 10 + selfTeam * 3
  i = 0
  n = objectCount()
  while i < n
    if objectTeam(i) = selfTeam then
      k = objectKind(i)
      id = objectId(i)
      if k = 4 and id < 28 then
        towerOffset = id - ownBase
        routeLane = towerOffset / 6
        tier = towerOffset mod 6
        routeIndex = routeLane * 7 + 2 - tier
        routeX(routeIndex) = objectX(i)
        routeY(routeIndex) = objectY(i)
        routeKind(routeIndex) = 0
        routeIndex = (2 - routeLane) * 7 + 3 + tier
        routeX(routeIndex) = mapWidth - 1 - objectX(i)
        routeY(routeIndex) = mapHeight - 1 - objectY(i)
        routeId(routeIndex) = 10 + (2 - routeLane) * 6 + (1 - selfTeam) * 3 + tier
        routeKind(routeIndex) = 1
      end if
      if k = 1 then
        homeX = objectX(i)
        homeY = objectY(i)
        routeLane = 0
        while routeLane < 3
          routeIndex = routeLane * 7 + 6
          routeX(routeIndex) = mapWidth - 1 - objectX(i)
          routeY(routeIndex) = mapHeight - 1 - objectY(i)
          routeId(routeIndex) = 2 - selfTeam
          routeKind(routeIndex) = 1
          routeLane = routeLane + 1
        wend
      end if
    end if
    i = i + 1
  wend
  loadLane(pushLane)
  lastLaneTick = -1500
  nObj = 7
  oi = 0
  melee = 0
  if selfClass = 0 or selfClass = 4 or selfClass = 5 or selfClass = 9 then
    melee = 1
  end if
  rng = 12
  if selfClass = 1 then
    rng = 55
  end if
  if selfClass = 2 then
    rng = 50
  end if
  if selfClass = 3 then
    rng = 40
  end if
  if selfClass = 6 then
    rng = 65
  end if
  if selfClass = 7 then
    rng = 55
  end if
  if selfClass = 8 then
    rng = 45
  end if
  cadence = 24
  if selfClass = 1 then
    cadence = 18
  end if
  if selfClass = 2 then
    cadence = 30
  end if
  if selfClass = 3 then
    cadence = 26
  end if
  if selfClass = 4 then
    cadence = 16
  end if
  if selfClass = 5 or selfClass = 8 then
    cadence = 28
  end if
  if selfClass = 6 then
    cadence = 36
  end if
  if selfClass = 7 then
    cadence = 32
  end if
  if selfClass = 9 then
    cadence = 20
  end if
  windupTicks = cadence * 45 / 100
  kiteRange2 = (rng - 5) * (rng - 5) / 100
  lastKite2Print = -480
  lastRidePrint = -480
  lastHoldPrint = -480
  heroR2 = (rng + 20) * (rng + 20) / 100
  if melee = 1 then
    heroR2 = 20
  end if
  footR2 = (rng + 10) * (rng + 10) / 100
  if melee = 1 then
    footR2 = 9
  end if
  ' farm any enemy footman this close when nothing better is in reach (version 36: XP compounds, games end by tick 8000)
  farmR2 = 64
  if melee = 1 then
    farmR2 = 36
  end if
  prevGold = selfGold
  prevHp = selfHp
  deaths = 0
  print "INIT team " ; selfTeam ; " lane " ; pushLane ; " home " ; homeX ; " " ; homeY ; " route " ; wpX(0) ; "," ; wpY(0) ; " " ; wpX(1) ; "," ; wpY(1) ; " " ; wpX(2) ; "," ; wpY(2) ; " | " ; wpX(3) ; "," ; wpY(3) ; " " ; wpX(4) ; "," ; wpY(4) ; " " ; wpX(5) ; "," ; wpY(5) ; " " ; wpX(6) ; "," ; wpY(6)
end if

' ---------- telemetry ----------
if selfGold - prevGold >= 75 then
  print "K " ; worldTick ; " +" ; selfGold - prevGold
end if
if selfHp > prevHp + 150 then
  deaths = deaths + 1
  rejoinArmed = 1
  print "D " ; worldTick ; " respawn #" ; deaths ; " at " ; lastX ; " " ; lastY ; " L" ; selfLevel
end if
prevGold = selfGold
prevHp = selfHp

' ---------- shopping / consumables ----------
potSlot = -1
slot = 0
while slot < 6
  iid = itemId(slot)
  if iid = 1 or iid = 2 then
    potSlot = slot
  end if
  slot = slot + 1
wend
if selfHp * 100 < selfMaxHp * 55 then
  if potSlot >= 0 then
    useItem(potSlot)
  else
    if selfGold >= 50 then
      buyItem(2)
    else
      if selfGold >= 30 then
        buyItem(1)
      end if
    end if
  end if
end if
' damage first (dagger at tick 1), then boots, then the big damage items; one purchase per tick
' v215: boots before the dagger — the 5v5 league is a race decided by ~100 ticks (v214: Blue 11/12 with boots)
if bootsBought = 0 and selfGold >= 100 then
  buyItem(8)
  bootsBought = 1
else
  if daggerBought = 0 and selfGold >= 110 then
    buyItem(11)
    daggerBought = 1
  else
    if potSlot < 0 and selfGold >= 80 then
      buyItem(2)
    else
      if axeBought = 0 and selfGold >= 180 then
        buyItem(18)
        axeBought = 1
      else
        if swordBought = 0 and selfGold >= 150 then
          buyItem(13)
          swordBought = 1
        else
          if armorBought = 0 and selfGold >= 160 then
            buyItem(16)
            armorBought = 1
          else
            if xbowBought = 0 and selfGold >= 180 then
              buyItem(19)
              xbowBought = 1
            end if
          end if
        end if
      end if
    end if
  end if
end if

' ---------- objective ----------
if oi >= nObj then
  oi = nObj - 1
end if
ox = wpX(oi)
oy = wpY(oi)
oid = wpId(oi)
otype = wpKind(oi)
dx = ox - selfX
dy = oy - selfY
myD2 = dx * dx + dy * dy
if otype = 0 and myD2 <= 25 and oi < nObj - 1 then
  oi = oi + 1
  stuckHits = 0
  ox = wpX(oi)
  oy = wpY(oi)
  oid = wpId(oi)
  otype = wpKind(oi)
  dx = ox - selfX
  dy = oy - selfY
  myD2 = dx * dx + dy * dy
end if
' guarded gods: the fort stays shielded until both guards die — aim at the nearest known exposed guard instead
if oi = nObj - 1 and fortId = 0 and guardId <> 0 then
  gdx = guardX - selfX
  gdy = guardY - selfY
  if guardSeen = 0 and gdx * gdx + gdy * gdy <= 16 then
    guardId = 0
  else
    ox = guardX
    oy = guardY
    oid = guardId
    otype = 1
    dx = ox - selfX
    dy = oy - selfY
    myD2 = dx * dx + dy * dy
  end if
end if
if oi > 0 then
  rx = wpX(oi - 1)
  ry = wpY(oi - 1)
else
  rx = homeX
  ry = homeY
end if

' ---------- scan ----------
bestHero = 0
bestHeroHp = 1000000
bestHeroD2 = 1000000
enemyHeroNear = 0
nearMeleeD2 = 1000000
nearMeleeId = 0
nearKiteFootD2 = 1000000
nearHeroD2 = 1000000
nmx = 0
nmy = 0
bestFoot = 0
bestFootHp = 1000000
bestFootD2 = 1000000
towerId = 0
towerD2 = 1000000
towerGuard = 0
guardSeen = 0
fortId = 0
objDead = 0
objSeen = 0
maxAllyD2 = -1
allyCount = 0
objStanding = 0
defenders = 0
seenEnemies = 0
allyNear8 = 0
waveAtTower = 0
nearTowerD2 = 1000000
nearTowerRange = 0
nearTowerWave = 0
liveAllies = 0
alliesWithin30 = 0
allySumX = 0
allySumY = 0
laneChanged = 0
xbAlive = 0
frontFound = 0
frontObjD2 = 1000000
frontX = 0
frontY = 0
frontD2 = 1000000

i = 0
n = objectCount()
while i < n
  k = objectKind(i)
  t = objectTeam(i)
  x = objectX(i)
  y = objectY(i)
  dx = x - selfX
  dy = y - selfY
  d2 = dx * dx + dy * dy
  if t = selfTeam then
    if k = 3 and objectAlive(i) = 1 then
      inLane = 0
      if pushLane = 2 and (x >= 102 or y >= 98) then
        inLane = 1
      end if
      if pushLane = 0 and (x <= 13 or y <= 17) then
        inLane = 1
      end if
      if pushLane = 1 then
        laneS = x + y - 115
        if laneS < 0 then
          laneS = 0 - laneS
        end if
        if laneS <= 14 then
          inLane = 1
        end if
      end if
      if inLane = 1 then
        wfx = x - ox
        wfy = y - oy
        wfd2 = wfx * wfx + wfy * wfy
        if wfd2 < frontObjD2 then
          frontObjD2 = wfd2
          frontX = x
          frontY = y
          frontD2 = d2
          frontFound = 1
        end if
      end if
      if towerId <> 0 then
        waveDx = x - towerX
        waveDy = y - towerY
        if waveDx * waveDx + waveDy * waveDy <= 9 then
          waveAtTower = waveAtTower + 1
        end if
      end if
      if nearTowerRange > 0 then
        waveDx = x - nearTowerX
        waveDy = y - nearTowerY
        if waveDx * waveDx + waveDy * waveDy <= 9 then
          nearTowerWave = nearTowerWave + 1
        end if
      end if
    end if
    if k = 2 then
      if objectId(i) <> selfId and objectAlive(i) = 1 then
        allyX(liveAllies) = x
        allyY(liveAllies) = y
        liveAllies = liveAllies + 1
        allySumX = allySumX + x
        allySumY = allySumY + y
        if d2 <= 64 then
          allyNear8 = allyNear8 + 1
        end if
        if d2 <= 900 then
          alliesWithin30 = alliesWithin30 + 1
        end if
        if selfTeam = 0 and selfClass <> 6 and objectClass(i) = 6 then
          xbX = x
          xbY = y
          xbAlive = 1
          xbD2 = d2
          enemyFortX = mapWidth - 1 - homeX
          enemyFortY = mapHeight - 1 - homeY
          xbDx = xbX - enemyFortX
          xbDy = xbY - enemyFortY
          xbFortD2 = xbDx * xbDx + xbDy * xbDy
        end if
      end if
      if objectId(i) <> selfId and objectAlive(i) = 1 and d2 <= 625 then
        ex = x - ox
        ey = y - oy
        ad2 = ex * ex + ey * ey
        if ad2 > maxAllyD2 and objectHp(i) > 60 then
          maxAllyD2 = ad2
        end if
        allyCount = allyCount + 1
      end if
    end if
  else
    if k = 2 then
      if objectAlive(i) = 1 then
        seenEnemyX(seenEnemies) = x
        seenEnemyY(seenEnemies) = y
        seenEnemies = seenEnemies + 1
        defendD2 = d2
        if otype = 1 then
          defendDx = x - ox
          defendDy = y - oy
          defendD2 = defendDx * defendDx + defendDy * defendDy
        end if
        if defendD2 <= 100 then
          defenders = defenders + 1
        end if
      end if
      if objectAlive(i) = 1 and d2 <= 100 then
        enemyHeroNear = enemyHeroNear + 1
        if d2 < nearHeroD2 then
          nearHeroD2 = d2
        end if
        hp = objectHp(i)
        if d2 <= heroR2 then
          if hp < bestHeroHp then
            bestHeroHp = hp
            bestHero = objectId(i)
            bestHeroD2 = d2
          end if
        end if
        c = objectClass(i)
        if c = 0 or c = 4 or c = 5 or c = 9 then
          if d2 < nearMeleeD2 then
            nearMeleeD2 = d2
            nearMeleeId = objectId(i)
            nmx = x
            nmy = y
          end if
        end if
      end if
    end if
    if k = 3 then
      if melee = 0 and objectAlive(i) = 1 and d2 <= 2 and d2 < nearKiteFootD2 then
        nearKiteFootD2 = d2
        nearKiteFootX = x
        nearKiteFootY = y
      end if
      hp = objectHp(i)
      if objectAlive(i) = 1 and (d2 <= farmR2 or (d2 <= footR2 and hp <= 30)) then
        if hp < bestFootHp then
          bestFootHp = hp
          bestFoot = objectId(i)
          bestFootD2 = d2
        end if
      end if
    end if
    if k = 4 then
      id = objectId(i)
      towerOffset = id - (10 + (1 - selfTeam) * 3)
      isGuard = 0
      if id >= 28 then
        isGuard = 1
        tier = 2
        if objectAlive(i) = 1 then
          if guardSeen = 0 or d2 < guardD2 then
            guardD2 = d2
            guardId = id
            guardX = x
            guardY = y
          end if
          guardSeen = 1
        end if
      end if
      if isGuard = 0 then
        routeLane = towerOffset / 6
        tier = towerOffset mod 6
        laneTowerHp(routeLane * 3 + tier) = objectHp(i)
        routeIndex = routeLane * 7 + 3 + tier
        routeX(routeIndex) = x
        routeY(routeIndex) = y
        if objectHp(i) <= 0 then
          routeDead(routeIndex) = 1
        end if
        if otype = 1 and id = oid then
          objSeen = 1
          if objectHp(i) <= 0 then
            objDead = 1
          else
            objStanding = 1
          end if
          ' refine the reflected position with the real one
          wpX(oi) = x
          wpY(oi) = y
        end if
      end if
      if objectHp(i) > 0 and d2 < nearTowerD2 then
        nearTowerD2 = d2
        nearTowerX = x
        nearTowerY = y
        nearTowerRange = 50 + tier * 5
      end if
      if objectAlive(i) = 1 and d2 <= 81 then
        if d2 < towerD2 then
          towerD2 = d2
          towerId = id
          towerX = x
          towerY = y
          towerHp = objectHp(i)
          towerRange = 50 + tier * 5
          towerGuard = isGuard
        end if
      end if
    end if
    if k = 1 then
      if objectAlive(i) = 1 then
        fortId = objectId(i)
      end if
      if otype = 1 and objectId(i) = oid then
        objSeen = 1
        if objectHp(i) <= 0 then
          objDead = 1
        else
          objStanding = 1
        end if
      end if
    end if
  end if
  i = i + 1
wend

' version 37: dead buildings vanish from the object list, so an unseen building objective within 4 tiles is dead
if otype = 1 and objSeen = 0 and objDead = 0 and myD2 <= 16 and oi < nObj - 1 then
  objDead = 1
  routeDead(pushLane * 7 + oi) = 1
  if oi >= 3 and oi <= 5 then
    laneTowerHp(pushLane * 3 + oi - 3) = 0
  end if
  print "DEADOBJ " ; worldTick ; " oi " ; oi
end if
if objDead = 1 and otype = 1 and oi < nObj - 1 then
  oi = oi + 1
  stuckHits = 0
end if

' towers now hit for 28/56/112: siege only out of their reach or while our footmen soak the shots
' mass dive: with two allies beside me the tower can only shoot one of us; late game a timeout is worth nothing anyway
allIn = 0
if allyNear8 >= 1 or worldTick >= 12000 then
  allIn = 1
end if
siegeAllowed = 0
if towerId <> 0 and (rng > towerRange or waveAtTower >= 1 or fortId <> 0 or allIn = 1 or towerHp <= 300) then
  siegeAllowed = 1
end if
' inside a living tower's reach with no footman cover and no range advantage -> back out first
towerDanger = 0
if allIn = 0 and nearTowerRange > 0 and rng <= nearTowerRange and nearTowerWave = 0 and nearTowerD2 * 100 <= (nearTowerRange + 8) * (nearTowerRange + 8) then
  towerDanger = 1
end if

' ---------- lane resistance / rejoin ----------
' v208: two enemy heroes camping our objective count as resistance (aaron's perimeter pair camps the mid choke)
if defenders >= 2 then
  resistance = resistance + 1
else
  resistance = resistance - 1
end if
if resistance < 0 then
  resistance = 0
end if
if resistance > 120 then
  resistance = 120
end if

' Once isolated, keep following the living allies until within 12 tiles.
rejoinStarted = 0
if liveAllies = 0 then
  rejoining = 0
else
  centroidX = allySumX / liveAllies
  centroidY = allySumY / liveAllies
  centroidDx = centroidX - selfX
  centroidDy = centroidY - selfY
  centroidD2 = centroidDx * centroidDx + centroidDy * centroidDy
  if rejoinArmed = 2 and alliesWithin30 = 0 and centroidD2 > 144 then
    rejoining = 1
    rejoinStarted = 1
    rejoinArmed = 0
    laneTravel = 0
  end if
  if rejoining = 1 then
    rejoinLane = pushLane
    nearestRouteD2 = 1000000
    routeLane = 0
    while routeLane < 3
      routePoint = 0
      while routePoint < 7
        routeIndex = routeLane * 7 + routePoint
        routeDx = routeX(routeIndex) - centroidX
        routeDy = routeY(routeIndex) - centroidY
        routeD2 = routeDx * routeDx + routeDy * routeDy
        if routeD2 < nearestRouteD2 or (routeD2 = nearestRouteD2 and routeLane = pushLane) then
          nearestRouteD2 = routeD2
          rejoinLane = routeLane
        end if
        routePoint = routePoint + 1
      wend
      routeLane = routeLane + 1
    wend
    if rejoinStarted = 1 then
      adoptLane(rejoinLane, 2)
      ' follow the lane road from home instead of walking at the ally centroid
      hdx = homeX - selfX
      hdy = homeY - selfY
      if hdx * hdx + hdy * hdy <= 400 then
        oi = 0
      end if
    end if
    rejoining = 0
  end if
end if

' Rejoin adopts team position immediately; resistance switches have a cooldown.
' v208: leave a lane whose standing objective has been defended by two or more enemy heroes for ~90 ticks; go to the lane
' farthest from every enemy hero seen this tick (the block below), at most once per 1500 ticks.
' v218: the camped-lane switch is disabled again (resistance >= 99999): in 5v5 it fired at first contact (~855) and sent our
' whole team on a 500-1000-tick detour to lane 2 while the enemy stack retreated from the collision.
if rejoining = 0 and laneChanged = 0 and resistance >= 99999 and worldTick - lastLaneTick >= 1500 and otype = 1 and objStanding = 1 and objDead = 0 then
  switchLane = pushLane
  safestD2 = -1
  routeLane = 0
  while routeLane < 3
    if routeLane <> pushLane then
      firstStanding(routeLane)
      routeIndex = routeLane * 7 + firstOi
      clearanceD2 = 1000000
      enemyIndex = 0
      while enemyIndex < seenEnemies
        routeDx = routeX(routeIndex) - seenEnemyX(enemyIndex)
        routeDy = routeY(routeIndex) - seenEnemyY(enemyIndex)
        routeD2 = routeDx * routeDx + routeDy * routeDy
        if routeD2 < clearanceD2 then
          clearanceD2 = routeD2
        end if
        enemyIndex = enemyIndex + 1
      wend
      if clearanceD2 > safestD2 or (clearanceD2 = safestD2 and switchLane = 1 and routeLane <> 1) then
        safestD2 = clearanceD2
        switchLane = routeLane
      end if
    end if
    routeLane = routeLane + 1
  wend
  adoptLane(switchLane, 1)
  laneTravel = 1
end if

' Join the other side lane only when more allies are pushing its enemy towers.
if worldTick >= 1200 and worldTick mod 600 = 0 and worldTick >= joinLockUntil and enemyHeroNear = 0 and selfClass <> 6 then
  routeLane = 0
  while routeLane < 3
    joinCount(routeLane) = 0
    joinAlly = 0
    while joinAlly < liveAllies
      joinNear = 0
      routePoint = 3
      while routePoint < 6
        routeIndex = routeLane * 7 + routePoint
        routeDx = allyX(joinAlly) - routeX(routeIndex)
        routeDy = allyY(joinAlly) - routeY(routeIndex)
        if routeDx * routeDx + routeDy * routeDy <= 144 then
          joinNear = 1
        end if
        routePoint = routePoint + 1
      wend
      joinCount(routeLane) = joinCount(routeLane) + joinNear
      joinAlly = joinAlly + 1
    wend
    routeLane = routeLane + 2
  wend
  joinLane = 2 - pushLane
  if joinCount(joinLane) >= 2 and joinCount(pushLane) < joinCount(joinLane) then
    adoptLane(joinLane, 2)
    firstStanding(joinLane)
    oi = firstOi
    laneTravel = 1
    joinLockUntil = worldTick + 6000
    print "JOIN " ; worldTick ; " lane " ; joinLane ; " allies " ; joinCount(joinLane)
  end if
end if

' v207 adaptive lane: from tick 600 to 3000, every 600 ticks, join the lane most allies are actually on (any of its seven
' route points within 12 tiles); needs two allies there and more than on our lane. The league is a race won by the team
' whose heroes converge; our fixed lane left the slot-0 hero alone (Red lane 2) or split from the mid push.
' v212: the ally-majority check runs only at ticks 600 and 1200 and needs two more allies on the other lane than on ours —
' in the league's 5v5 format all teammates are our own copies, and after a mid collision scattered them the old rule sent the
' whole team to the far lane (Red 0/12 vs black-kite, first tower 1500 ticks late).
if worldTick >= 600 and worldTick <= 1200 and worldTick mod 600 = 0 and routing = 0 and enemyHeroNear = 0 and fortId = 0 and worldTick >= joinLockUntil then
  routeLane = 0
  while routeLane < 3
    laneAllies(routeLane) = 0
    joinAlly = 0
    while joinAlly < liveAllies
      joinNear = 0
      routePoint = 0
      while routePoint < 7
        routeIndex = routeLane * 7 + routePoint
        routeDx = allyX(joinAlly) - routeX(routeIndex)
        routeDy = allyY(joinAlly) - routeY(routeIndex)
        if routeDx * routeDx + routeDy * routeDy <= 144 then
          joinNear = 1
        end if
        routePoint = routePoint + 1
      wend
      laneAllies(routeLane) = laneAllies(routeLane) + joinNear
      joinAlly = joinAlly + 1
    wend
    routeLane = routeLane + 1
  wend
  bestLane = pushLane
  routeLane = 0
  while routeLane < 3
    if laneAllies(routeLane) > laneAllies(bestLane) then
      bestLane = routeLane
    end if
    routeLane = routeLane + 1
  wend
  if bestLane <> pushLane and laneAllies(bestLane) >= 2 and laneAllies(bestLane) >= laneAllies(pushLane) + 2 then
    adoptLane(bestLane, 2)
    firstStanding(bestLane)
    oi = firstOi
    laneTravel = 1
    joinLockUntil = worldTick + 6000
    print "MAJ " ; worldTick ; " lane " ; bestLane ; " allies " ; laneAllies(bestLane) ; " mine " ; laneAllies(pushLane)
  end if
end if

' Finish a weaker lane; JOIN has precedence and active travel blocks switching.
routing = 0
if laneTravel = 1 or rejoining = 1 then
  routing = 1
end if
if worldTick >= 6000 and worldTick mod 600 = 0 and routing = 0 and enemyHeroNear = 0 and fortId = 0 and worldTick >= weakLockUntil and laneChanged = 0 then
  routeLane = 0
  while routeLane < 3
    laneRemain(routeLane) = 0
    tier = 0
    while tier < 3
      if laneTowerHp(routeLane * 3 + tier) > 0 then
        laneRemain(routeLane) = laneRemain(routeLane) + laneTowerHp(routeLane * 3 + tier)
      end if
      tier = tier + 1
    wend
    routeLane = routeLane + 1
  wend
  weakLane = pushLane
  routeLane = 0
  while routeLane < 3
    if laneRemain(routeLane) < laneRemain(weakLane) then
      weakLane = routeLane
    end if
    routeLane = routeLane + 1
  wend
  if weakLane <> pushLane and laneRemain(weakLane) * 10 <= laneRemain(pushLane) * 7 then
    adoptLane(weakLane, 2)
    firstStanding(weakLane)
    oi = firstOi
    laneTravel = 1
    weakLockUntil = worldTick + 3000
    print "WEAK " ; worldTick ; " lane " ; weakLane ; " hp " ; laneRemain(weakLane)
  end if
end if

' Use the existing walking/recovery path while leaving a lane or rejoining.
routing = 0
if laneTravel = 1 or rejoining = 1 or laneChanged = 1 then
  ox = wpX(oi)
  oy = wpY(oi)
  oid = wpId(oi)
  otype = wpKind(oi)
  dx = ox - selfX
  dy = oy - selfY
  myD2 = dx * dx + dy * dy
  if oi > 0 then
    rx = wpX(oi - 1)
    ry = wpY(oi - 1)
  else
    rx = homeX
    ry = homeY
  end if
  if laneTravel = 1 and myD2 <= 100 then
    laneTravel = 0
  end if
  if rejoining = 1 then
    ox = centroidX
    oy = centroidY
    myD2 = centroidD2
  end if
  if laneTravel = 1 or rejoining = 1 then
    routing = 1
  end if
end if

' Renew escort mode while the allied Crossbowman is pushing near the enemy fort.
if selfTeam = 0 and selfClass <> 6 then
  if worldTick mod 240 = 0 and routing = 0 and fortId = 0 and worldTick >= 900 then
    if xbAlive = 1 and xbFortD2 <= 3600 then
      escortUntil = worldTick + 240
    end if
  end if
  if worldTick < escortUntil and xbAlive = 1 then
    if prevEscort = 0 then
      print "ESCORT " ; worldTick
    end if
    prevEscort = 1
  else
    prevEscort = 0
  end if
end if

' ---------- decide ----------
done = 0
act = 0
lowHp = 0
if selfHp * 100 < selfMaxHp * 30 then
  lowHp = 1
end if

if routing = 0 and selfHp * 100 < selfMaxHp * 25 and enemyHeroNear > 0 and allIn = 0 then
  rdx = rx - selfX
  rdy = ry - selfY
  if rdx * rdx + rdy * rdy > 16 then
    stepToward(rx, ry, selfX, selfY, 3)
    walkTo(sx, sy)
  else
    walkTo(selfX, selfY)
  end if
  done = 1
  act = 1
end if

' end the game first: an exposed fort in reach beats any fight
if done = 0 and fortId <> 0 and selfHp * 100 >= selfMaxHp * 15 then
  attackTarget(fortId)
  done = 1
  act = 5
end if

' Hit during windup; step away from melee threats during recovery.
if melee = 0 then
  threatD2 = nearMeleeD2
  kiteTarget = bestHero
  kiteTargetD2 = bestHeroD2
  if kiteTarget = 0 then
    if nearMeleeId <> 0 and nearMeleeD2 <= rng * rng / 100 then
      kiteTarget = nearMeleeId
      kiteTargetD2 = nearMeleeD2
    else
      kiteTarget = bestFoot
      kiteTargetD2 = bestFootD2
    end if
  end if
  if nearMeleeD2 > 9 and nearKiteFootD2 <= 2 then
    threatD2 = nearKiteFootD2
    nmx = nearKiteFootX
    nmy = nearKiteFootY
  end if
  if done = 0 and routing = 0 and lowHp = 0 and towerDanger = 0 and threatD2 <= 12 then
    if selfAttackCooldown <= windupTicks + 1 and kiteTarget <> 0 and kiteTargetD2 <= rng * rng / 100 then
      attackTarget(kiteTarget)
      act = 45
      done = 1
    else
      stepToward(selfX, selfY, 2 * selfX - nmx, 2 * selfY - nmy, 3)
      if terrainWalkable(sx, sy) = 0 then
        stepToward(selfX, selfY, rx, ry, 3)
      end if
      walkTo(sx, sy)
      act = 46
      done = 1
    end if
    if worldTick - lastKite2Print >= 480 then
      print "KITE2 " ; worldTick
      lastKite2Print = worldTick
    end if
  end if
end if

if done = 0 and routing = 0 and melee = 0 and nearMeleeD2 <= 4 then
  stepToward(selfX, selfY, rx, ry, 4)
  walkTo(sx, sy)
  done = 1
  act = 2
end if

' Outrange the tower, but retreat for 96 ticks after an unsupported hero threat.
safeSiege = 0
if melee = 0 and towerId <> 0 and rng > towerRange then
  safeSiege = 1
end if
siegeKiting = 0
if done = 0 and routing = 0 and safeSiege = 1 then
  if nearHeroD2 <= 81 and allyNear8 < enemyHeroNear then
    if kiteUntil <= worldTick then
      print "KITE " ; worldTick
    end if
    kiteUntil = worldTick + 96
  end if
  if worldTick < kiteUntil then
    siegeKiting = 1
    ' Let the existing rules take kill shots or farm when heroes are beyond 6 tiles.
    if (bestHero = 0 or bestHeroHp * 2 >= selfHp) and (bestFoot = 0 or nearHeroD2 <= 36) then
      stepToward(selfX, selfY, rx, ry, 8)
      walkTo(sx, sy)
      done = 1
      act = 28
    end if
  end if
end if

'' an enemy lane is open (gate seen dead) but the fort is not visible yet: head for that fort
openLane = -1
routeLane = 0
while routeLane < 3
  if routeDead(routeLane * 7 + 5) = 1 then
    openLane = routeLane
  end if
  routeLane = routeLane + 1
wend
if done = 0 and routing = 0 and fortId = 0 and openLane >= 0 and guardId = 0 and towerDanger = 0 and enemyHeroNear = 0 then
  stepToward(routeX(openLane * 7 + 6), routeY(openLane * 7 + 6), selfX, selfY, 3)
  walkTo(sx, sy)
  done = 1
  act = 37
end if

' step out of tower range before anything else
if done = 0 and towerDanger = 1 and fortId = 0 then
  stepToward(selfX, selfY, rx, ry, 6)
  walkTo(sx, sy)
  done = 1
  act = 15
end if

' Close to the Crossbowman unless an enemy hero is already in basic range.
if done = 0 and selfTeam = 0 and selfClass <> 6 and worldTick < escortUntil and xbAlive = 1 and xbD2 > 25 and nearHeroD2 > rng * rng / 100 and towerDanger = 0 then
  walkTo(xbX, xbY)
  act = 35
  done = 1
end if

' fort guard with our wave on it: siege it through the defenders
if done = 0 and routing = 0 and towerId <> 0 and towerGuard = 1 and lowHp = 0 and waveAtTower >= 1 then
  attackTarget(towerId)
  done = 1
  act = 54
end if

' v209 group focus (from v205): with two allies beside me and an enemy tower in reach, siege it regardless of heroes or
' footmen — against aaron's camping pair this read Red 21/72 vs 1/72 for the hero-chase behaviour.
' v228: the group focus does not apply to fort guards — vs black-kite:v16 our Blue stack tunnelled the guard under the
' defenders' fire and died (v186, without this rule, fights the defenders first and kills the guards by 3198).
if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 and allyNear8 >= 2 and towerGuard = 0 then
  attackTarget(towerId)
  done = 1
  act = 55
end if

' a tower in reach with no enemy hero adjacent to me: keep sieging
if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 and nearHeroD2 > 9 and siegeAllowed = 1 and siegeKiting = 0 and (melee = 0 or bestFoot = 0 or towerHp <= 300) then
  attackTarget(towerId)
  done = 1
  act = 6
end if

if done = 0 and routing = 0 and bestHero <> 0 and (allyNear8 + 1 >= enemyHeroNear or bestHeroHp * 2 < selfHp or allIn = 1) and (siegeKiting = 0 or bestHeroHp * 2 < selfHp) and (melee = 0 or bestHeroD2 <= 4 or bestHeroHp * 2 < selfHp or allIn = 1) then
  attackTarget(bestHero)
  done = 1
  act = 3
end if

if done = 0 and bestFoot <> 0 and (routing = 0 or (bestFootD2 <= footR2 and enemyHeroNear = 0 and towerDanger = 0)) then
  attackTarget(bestFoot)
  done = 1
  act = 4
end if

' melee: never run ahead of our lane's front footman toward an enemy tower; hold when the lane has no footman
if done = 0 and melee = 1 and routing = 0 and lowHp = 0 and fortId = 0 and openLane < 0 and otype = 1 and oi >= 3 and allIn = 0 and towerDanger = 0 then
  if frontFound = 1 then
    if frontD2 > 16 and myD2 < frontObjD2 then
      walkTo(frontX, frontY)
      done = 1
      act = 47
      if worldTick - lastRidePrint >= 480 then
        print "RIDE " ; worldTick ; " to " ; frontX ; " " ; frontY
        lastRidePrint = worldTick
      end if
    end if
  else
    if enemyHeroNear > 0 then
      stepToward(selfX, selfY, rx, ry, 6)
      walkTo(sx, sy)
      act = 50
    else
      walkTo(selfX, selfY)
      act = 49
    end if
    done = 1
    if worldTick - lastHoldPrint >= 480 then
      print "HOLDW " ; worldTick ; " act " ; act
      lastHoldPrint = worldTick
    end if
  end if
end if

if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 and siegeAllowed = 1 and siegeKiting = 0 then
  attackTarget(towerId)
  done = 1
  act = 6
end if

' wait for the next wave just outside the tower's reach
if done = 0 and routing = 0 and towerId <> 0 and siegeAllowed = 0 and otype = 1 and oid = towerId then
  stepToward(towerX, towerY, rx, ry, towerRange / 10 + 2)
  dx = sx - selfX
  dy = sy - selfY
  if dx * dx + dy * dy <= 2 then
    walkTo(selfX, selfY)
  else
    walkTo(sx, sy)
  end if
  done = 1
  act = 22
end if

if done = 0 and lowHp = 1 and routing = 0 then
  ' crippled with no way to heal: let an enemy tower reset us (towers give the enemy nothing)
  if selfHp * 100 < selfMaxHp * 20 and selfGold < 30 and potSlot < 0 and towerId <> 0 and enemyHeroNear = 0 and rng > towerRange then
    attackTarget(towerId)
    done = 1
    act = 12
  end if
end if
' home guard: a respawned hero waits at its own gate tower until allies gather (max 30 s), no solo trickle
if done = 0 and routing = 0 and worldTick < guardUntil and oi < 3 and fortId = 0 then
  if allyCount >= 2 then
    guardUntil = 0
  else
    dx = wpX(0) - selfX
    dy = wpY(0) - selfY
    if dx * dx + dy * dy <= 9 then
      walkTo(selfX, selfY)
    else
      walkTo(wpX(0), wpY(0))
    end if
    done = 1
    act = 14
  end if
end if
if done = 0 then
  if lowHp = 1 and routing = 0 then
    stepToward(selfX, selfY, rx, ry, 6)
    walkTo(sx, sy)
    act = 7
  else
    if unstick > 0 then
      ' back off toward the previous waypoint to get a fresh path
      unstick = unstick - 1
      stepToward(selfX, selfY, rx, ry, 6)
      ok = walkTo(sx, sy)
      if ok = 0 then
        stepToward(rx, ry, selfX, selfY, 3)
        walkTo(sx, sy)
      end if
      act = 10
    else
      isqrt(myD2)
      myD = sq
      hold = 0

      if noHold > 0 then
        noHold = noHold - 1
        hold = 0
      end if
      if hold = 1 and holdTicks < 96 then
        walkTo(selfX, selfY)
        holdTicks = holdTicks + 1
        act = 8
      else
        if holdTicks >= 96 then
          noHold = 240
        end if
        holdTicks = 0
        if otype = 1 and myD2 <= 16 then
          ' beside a building objective with nothing to do: do not walk into its footprint (version 37 footprints are 1.05-1.65 tiles)
          act = 23
        else
          if otype = 1 then
            stepToward(ox, oy, selfX, selfY, 3)
            ok = walkTo(sx, sy)
          else
            ok = walkTo(ox, oy)
          end if
          if ok = 0 then
            stepToward(selfX, selfY, ox, oy, 8)
            ok = walkTo(sx, sy)
            act = 11
          else
            act = 9
          end if
        end if
      end if
    end if
  end if
end if

' stuck detection while advancing
if act = 9 or act = 11 or act = 47 then
  if selfX = lastX and selfY = lastY then
    stuckTicks = stuckTicks + 1
  else
    stuckTicks = 0
  end if
  if stuckTicks >= 16 then
    stuckTicks = 0
    unstick = 20
    stuckHits = stuckHits + 1
    print "STUCK " ; worldTick ; " at " ; selfX ; " " ; selfY ; " -> " ; ox ; " " ; oy ; " hits " ; stuckHits
    if stuckHits >= 3 and otype = 0 and oi < nObj - 1 then
      oi = oi + 1
      stuckHits = 0
    end if
  end if
else
  if act <> 10 then
    stuckTicks = 0
  end if
end if
lastX = selfX
lastY = selfY

' v246: siege spells — the engine only auto-casts in hero combat; relh's heroes cast every tick and clear the fort guards
' ~150 ticks faster than us. With an enemy tower/guard within 9 tiles and no enemy hero within 10, fire every ability slot at it
' (castTarget for target abilities, castPoint on its tile for area abilities; invalid casts simply fail). Costs mana only.
if towerId <> 0 and nearHeroD2 > 100 and towerHp > 0 and lowHp = 0 then
  castTarget(1, towerId)
  castTarget(2, towerId)
  castTarget(3, towerId)
  castPoint(2, towerX, towerY)
  castPoint(3, towerX, towerY)
end if

if worldTick mod 480 = 0 then
  print "T " ; worldTick ; " p " ; selfX ; " " ; selfY ; " hp " ; selfHp ; "/" ; selfMaxHp ; " L" ; selfLevel ; " g" ; selfGold ; " oi " ; oi ; " act " ; act ; " eh " ; enemyHeroNear ; " al " ; allyCount
end if
