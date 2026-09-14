' GOTA policy v5 "edge blitz, map-generic": all five heroes push one side lane
' as a stack. Objectives come from own tower positions (always visible) and the
' map's point symmetry (enemy = (W-1-x, H-1-y)), so no coordinates are hardcoded.
' Red pushes lane 0, Blue pushes lane 2 (mirror images). See docs/ARENA_NOTES.md.
' Candidate lane adds resistance-driven lane switching and ally rejoin.

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

' ---------- mode: stack (my clones nearby) or solo (mixed team) ----------
if worldTick = 360 then
  nearAllies = 0
  i = 0
  n = objectCount()
  while i < n
    if objectKind(i) = 2 and objectTeam(i) = selfTeam and objectId(i) <> selfId then
      dx = objectX(i) - selfX
      dy = objectY(i) - selfY
      if dx * dx + dy * dy <= 400 then
        nearAllies = nearAllies + 1
      end if
    end if
    i = i + 1
  wend
  if nearAllies >= 3 then
    mode = 0
  else
    mode = 1
    mySlot = selfId - 100 - selfTeam * 5
    if mySlot mod 2 = 0 then
      soloLane = 2 - selfTeam * 2
    else
      soloLane = selfTeam * 2
    end if
    adoptLane(soloLane, 2)
    oi = 0
  end if
  print "MODE " ; mode ; " allies " ; nearAllies ; " lane " ; pushLane
end if

' ---------- telemetry ----------
if selfGold - prevGold >= 75 then
  print "K " ; worldTick ; " +" ; selfGold - prevGold
end if
if selfHp > prevHp + 150 then
  deaths = deaths + 1
  rejoinArmed = 1
  if worldTick > 1500 and mode = 0 then
    guardUntil = worldTick + 720
  end if
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
if selfGold >= 100 then
  buyItem(8)
end if
if potSlot < 0 and selfGold >= 80 then
  buyItem(2)
end if
if selfGold >= 120 then
  buyItem(7)
end if
if selfGold >= 160 then
  buyItem(11)
end if
if selfGold >= 210 then
  buyItem(16)
end if
if selfGold >= 230 then
  buyItem(18)
end if
if selfGold >= 230 then
  buyItem(19)
end if
if selfGold >= 200 then
  buyItem(13)
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
allyNear8 = 0
towerHp = 0
frontId = 0
frontD2 = 1000000
fx = 0
fy = 0
farFoot = 0
farFootHp = 1000000
objDead = 0
maxAllyD2 = -1
allyCount = 0
objStanding = 0
defenders = 0
seenEnemies = 0
liveAllies = 0
alliesWithin30 = 0
allySumX = 0
allySumY = 0
laneChanged = 0

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
    if k = 3 then
      if objectAlive(i) = 1 and d2 <= 900 then
        ex = x - ox
        ey = y - oy
        ad2 = ex * ex + ey * ey
        if ad2 < frontD2 then
          frontD2 = ad2
          frontId = objectId(i)
          fx = x
          fy = y
        end if
      end if
    end if
    if k = 2 then
      if objectId(i) <> selfId and objectAlive(i) = 1 and d2 <= 64 then
        allyNear8 = allyNear8 + 1
      end if
      if objectId(i) <> selfId and objectAlive(i) = 1 then
        liveAllies = liveAllies + 1
        allySumX = allySumX + x
        allySumY = allySumY + y
        if d2 <= 900 then
          alliesWithin30 = alliesWithin30 + 1
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
      if objectAlive(i) = 1 and d2 <= footR2 then
        if hp < farFootHp then
          farFootHp = hp
          farFoot = objectId(i)
        end if
      end if
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
      if objectAlive(i) = 1 and d2 <= 81 then
        if d2 < towerD2 then
          towerD2 = d2
          towerId = id
          towerHp = objectHp(i)
        end if
      end if
    end if
    if k = 1 then
      if objectAlive(i) = 1 and d2 <= 196 then
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
  if rejoinArmed = 1 and alliesWithin30 = 0 and centroidD2 > 144 then
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
      if mode = 1 then
        rejoinLane = soloLane
      end if
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
if rejoining = 0 and laneChanged = 0 and resistance >= 72 and worldTick - lastLaneTick >= 1500 and otype = 1 and objStanding = 1 and objDead = 0 then
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

' ---------- decide ----------
done = 0
act = 0
lowHp = 0
if selfHp * 100 < selfMaxHp * 30 then
  lowHp = 1
end if

' ================= SOLO MODE (mixed team) =================
if mode = 1 then
  waveAtTower = 0
  if towerId <> 0 and frontId <> 0 then
    i = 0
    n = objectCount()
    while i < n
      if objectId(i) = towerId then
        ex = fx - objectX(i)
        ey = fy - objectY(i)
        if ex * ex + ey * ey <= 36 then
          waveAtTower = 1
        end if
      end if
      i = i + 1
    wend
  end if
  outnum = 0
  if enemyHeroNear >= 2 and enemyHeroNear > allyNear8 + 1 then
    outnum = 1
  end if
  if selfHp * 100 < selfMaxHp * 35 and enemyHeroNear > 0 then
    outnum = 1
  end if
  if outnum = 1 then
    retreatUntil = worldTick + 48
  end if
  if nearHeroD2 <= 144 and retreatUntil > worldTick - 48 and retreatUntil < worldTick + 48 then
    retreatUntil = worldTick + 48
  end if
  if worldTick < retreatUntil and fortId = 0 then
    stepToward(selfX, selfY, rx, ry, 8)
    walkTo(sx, sy)
    done = 1
    act = 21
  end if
  if done = 0 and melee = 0 and nearMeleeD2 <= 4 then
    stepToward(selfX, selfY, rx, ry, 4)
    walkTo(sx, sy)
    done = 1
    act = 2
  end if
  if done = 0 and fortId <> 0 and selfHp * 100 >= selfMaxHp * 15 then
    attackTarget(fortId)
    done = 1
    act = 5
  end if
  if done = 0 and bestHero <> 0 and (bestHeroHp < selfHp or allyNear8 >= 1) then
    attackTarget(bestHero)
    done = 1
    act = 3
  end if
  if done = 0 and farFoot <> 0 then
    attackTarget(farFoot)
    done = 1
    act = 4
  end if
  if done = 0 and towerId <> 0 and (waveAtTower = 1 or towerHp < 150) and lowHp = 0 then
    attackTarget(towerId)
    done = 1
    act = 6
  end if
  if done = 0 then
    if frontId <> 0 then
      off = 1
      if melee = 0 then
        off = 3
      end if
      if lowHp = 1 then
        off = 8
      end if
      stepToward(fx, fy, rx, ry, off)
      dx = sx - selfX
      dy = sy - selfY
      if dx * dx + dy * dy <= 2 then
        walkTo(selfX, selfY)
        act = 8
      else
        walkTo(sx, sy)
        act = 9
      end if
    else
      if towerId <> 0 and lowHp = 0 then
        walkTo(selfX, selfY)
        act = 8
      else
        if lowHp = 1 then
          walkTo(rx, ry)
          act = 7
        else
          ok = walkTo(ox, oy)
          act = 9
        end if
      end if
    end if
    done = 1
  end if
end if

if done = 0 and routing = 0 and selfHp * 100 < selfMaxHp * 15 and enemyHeroNear > 0 then
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

' a tower in reach with no enemy hero adjacent to me: keep sieging
if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 and nearHeroD2 > 9 then
  attackTarget(towerId)
  done = 1
  act = 6
end if

if done = 0 and routing = 0 and bestHero <> 0 then
  attackTarget(bestHero)
  done = 1
  act = 3
end if

if done = 0 and routing = 0 and bestFoot <> 0 then
  attackTarget(bestFoot)
  done = 1
  act = 4
end if

if done = 0 and routing = 0 and towerId <> 0 and lowHp = 0 then
  attackTarget(towerId)
  done = 1
  act = 6
end if

if done = 0 and lowHp = 1 and routing = 0 then
  ' crippled with no way to heal: let an enemy tower reset us (towers give the enemy nothing)
  if selfHp * 100 < selfMaxHp * 20 and selfGold < 30 and potSlot < 0 and towerId <> 0 and enemyHeroNear = 0 then
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
      if allyCount > 0 and routing = 0 then
        isqrt(maxAllyD2)
        if myD + 6 < sq then
          hold = 1
        end if
      end if
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
