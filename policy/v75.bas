' GOTA policy v5 "edge blitz, map-generic": all five heroes push one side lane
' as a stack. Objectives come from own tower positions (always visible) and the
' map's point symmetry (enemy = (W-1-x, H-1-y)), so no coordinates are hardcoded.
' Red pushes lane 0, Blue pushes lane 2 (mirror images). See docs/ARENA_NOTES.md.
' v46 = v45 + mass dives (2 allies near), late-game all-in (tick 22000), finish low towers, 25% flee, fight odds, damage-first shop.
' v49a = v47 (tower-safe siege + long-range kiting) committed to one lane (no lane switch/rejoin), all-in from one ally or tick 12000.
' v75 = v68 + go for the enemy fort whenever it is exposed and visible, at any distance (games are decisive again under version 34).

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
  pushLane = 2
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
      if k = 4 then
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
  heroR2 = (rng + 20) * (rng + 20) / 100
  if melee = 1 then
    heroR2 = 20
  end if
  footR2 = (rng + 10) * (rng + 10) / 100
  if melee = 1 then
    footR2 = 9
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
  print "D " ; worldTick ; " respawn #" ; deaths
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
if daggerBought = 0 and selfGold >= 110 then
  buyItem(11)
  daggerBought = 1
else
  if bootsBought = 0 and selfGold >= 100 then
    buyItem(8)
    bootsBought = 1
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
enemyHeroNear = 0
nearMeleeD2 = 1000000
nearHeroD2 = 1000000
nmx = 0
nmy = 0
bestFoot = 0
bestFootHp = 1000000
towerId = 0
towerD2 = 1000000
fortId = 0
objDead = 0
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
          end if
        end if
        c = objectClass(i)
        if c = 0 or c = 4 or c = 5 or c = 9 then
          if d2 < nearMeleeD2 then
            nearMeleeD2 = d2
            nmx = x
            nmy = y
          end if
        end if
      end if
    end if
    if k = 3 then
      hp = objectHp(i)
      if objectAlive(i) = 1 and (d2 <= 6 or (d2 <= footR2 and hp <= 30)) then
        if hp < bestFootHp then
          bestFootHp = hp
          bestFoot = objectId(i)
        end if
      end if
    end if
    if k = 4 then
      id = objectId(i)
      towerOffset = id - (10 + (1 - selfTeam) * 3)
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
        if objectHp(i) <= 0 then
          objDead = 1
        else
          objStanding = 1
        end if
        ' refine the reflected position with the real one
        wpX(oi) = x
        wpY(oi) = y
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
        end if
      end if
    end if
    if k = 1 then
      if objectAlive(i) = 1 then
        fortId = objectId(i)
      end if
      if otype = 1 and objectId(i) = oid then
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
if defenders >= 3 then
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
  walkTo(rx, ry)
  done = 1
  act = 1
end if

if done = 0 and routing = 0 and melee = 0 and nearMeleeD2 <= 4 then
  stepToward(selfX, selfY, rx, ry, 4)
  walkTo(sx, sy)
  done = 1
  act = 2
end if

' end the game first: an exposed fort in reach beats any fight
if done = 0 and fortId <> 0 and selfHp * 100 >= selfMaxHp * 15 then
  attackTarget(fortId)
  done = 1
  act = 5
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

'' step out of tower range before anything else
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

' a tower in reach with no enemy hero adjacent to me: keep sieging
if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 and nearHeroD2 > 9 and siegeAllowed = 1 and siegeKiting = 0 then
  attackTarget(towerId)
  done = 1
  act = 6
end if

if done = 0 and routing = 0 and bestHero <> 0 and (allyNear8 + 1 >= enemyHeroNear or bestHeroHp * 2 < selfHp or allIn = 1) and (siegeKiting = 0 or bestHeroHp * 2 < selfHp) then
  attackTarget(bestHero)
  done = 1
  act = 3
end if

if done = 0 and routing = 0 and bestFoot <> 0 then
  attackTarget(bestFoot)
  done = 1
  act = 4
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
        walkTo(rx, ry)
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
        ok = walkTo(ox, oy)
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

' stuck detection while advancing
if act = 9 or act = 11 then
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

if worldTick mod 480 = 0 then
  print "T " ; worldTick ; " p " ; selfX ; " " ; selfY ; " hp " ; selfHp ; "/" ; selfMaxHp ; " L" ; selfLevel ; " g" ; selfGold ; " oi " ; oi ; " act " ; act ; " eh " ; enemyHeroNear ; " al " ; allyCount
end if
