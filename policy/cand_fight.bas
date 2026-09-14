' GOTA policy v5 "edge blitz, map-generic": all five heroes push one side lane
' as a stack. Objectives come from own tower positions (always visible) and the
' map's point symmetry (enemy = (W-1-x, H-1-y)), so no coordinates are hardcoded.
' Red pushes lane 0, Blue pushes lane 2 (mirror images). See docs/ARENA_NOTES.md.

dim wpX(8)
dim wpY(8)
dim wpId(8)
dim wpKind(8)
dim fightAllyX(4)
dim fightAllyY(4)

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
  pushLane = 0
  if selfTeam = 1 then
    pushLane = 2
  end if
  ' clash = 1 makes both teams push lane 2 so they meet head-on (local fight benchmark only)
  clash = 0
  if clash = 1 then
    pushLane = 2
  end if
  ' own tower ids for the push lane (waypoints, in gate->inner->outer order)
  ownBase = 10 + pushLane * 6 + selfTeam * 3
  ' mirror lane own towers give enemy positions for the push lane
  mirBase = 10 + (2 - pushLane) * 6 + selfTeam * 3
  enemyBase = 10 + pushLane * 6 + (1 - selfTeam) * 3
  i = 0
  n = objectCount()
  while i < n
    if objectTeam(i) = selfTeam then
      k = objectKind(i)
      id = objectId(i)
      if k = 4 then
        tier = id - ownBase
        if tier >= 0 and tier <= 2 then
          wpX(2 - tier) = objectX(i)
          wpY(2 - tier) = objectY(i)
          wpKind(2 - tier) = 0
        end if
        tier = id - mirBase
        if tier >= 0 and tier <= 2 then
          wpX(3 + tier) = mapWidth - 1 - objectX(i)
          wpY(3 + tier) = mapHeight - 1 - objectY(i)
          wpId(3 + tier) = enemyBase + tier
          wpKind(3 + tier) = 1
        end if
      end if
      if k = 1 then
        homeX = objectX(i)
        homeY = objectY(i)
        wpX(6) = mapWidth - 1 - objectX(i)
        wpY(6) = mapHeight - 1 - objectY(i)
        wpId(6) = 2 - selfTeam
        wpKind(6) = 1
      end if
    end if
    i = i + 1
  wend
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
  print "D " ; worldTick ; " respawn #" ; deaths
end if
prevGold = selfGold
prevHp = selfHp

' ---------- shopping / consumables ----------
potSlot = -1
poisonSlot = -1
slot = 0
while slot < 6
  iid = itemId(slot)
  if iid = 4 then
    poisonSlot = slot
  end if
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
' Nearby allies define the shared fight area, including me.
fightAllies = 0
i = 0
n = objectCount()
while i < n
  if objectKind(i) = 2 and objectTeam(i) = selfTeam and objectAlive(i) = 1 then
    dx = objectX(i) - selfX
    dy = objectY(i) - selfY
    if dx * dx + dy * dy <= 64 then
      fightAllyX(fightAllies) = objectX(i)
      fightAllyY(fightAllies) = objectY(i)
      fightAllies = fightAllies + 1
    end if
  end if
  i = i + 1
wend
bestHero = 0
bestHeroHp = 1000000
enemyHeroNear = 0
nearMeleeD2 = 1000000
nearMeleeHp = 0
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
    if k = 2 then
      if objectId(i) <> selfId and objectAlive(i) = 1 and d2 <= 625 then
        ex = x - ox
        ey = y - oy
        ad2 = ex * ex + ey * ey
        if ad2 > maxAllyD2 then
          maxAllyD2 = ad2
        end if
        allyCount = allyCount + 1
      end if
    end if
  else
    if k = 2 then
      if objectAlive(i) = 1 then
        inFight = 0
        j = 0
        while j < fightAllies
          dx = x - fightAllyX(j)
          dy = y - fightAllyY(j)
          if dx * dx + dy * dy <= 144 then
            inFight = 1
          end if
          j = j + 1
        wend
        hp = objectHp(i)
        id = objectId(i)
        if inFight = 1 then
          if hp < bestHeroHp or (hp = bestHeroHp and id < bestHero) then
            bestHeroHp = hp
            bestHero = id
            bestHeroD2 = d2
          end if
        end if
      end if
      if objectAlive(i) = 1 and d2 <= 100 then
        enemyHeroNear = enemyHeroNear + 1
        c = objectClass(i)
        if c = 0 or c = 4 or c = 5 or c = 9 then
          if d2 < nearMeleeD2 then
            nearMeleeD2 = d2
            nearMeleeHp = objectHp(i)
            nmx = x
            nmy = y
          end if
        end if
      end if
    end if
    if k = 3 then
      if objectAlive(i) = 1 and d2 <= footR2 then
        hp = objectHp(i)
        if hp < bestFootHp then
          bestFootHp = hp
          bestFoot = objectId(i)
        end if
      end if
    end if
    if k = 4 then
      id = objectId(i)
      if otype = 1 and id = oid then
        if objectHp(i) <= 0 then
          objDead = 1
        end if
        ' refine the reflected position with the real one
        wpX(oi) = x
        wpY(oi) = y
      end if
      if objectAlive(i) = 1 and d2 <= 81 then
        if d2 < towerD2 then
          towerD2 = d2
          towerId = id
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

' Stock one poison only when a hero fight is nearby.
if bestHero <> 0 and poisonSlot < 0 and selfGold >= 40 then
  buyItem(4)
end if

' ---------- decide ----------
done = 0
act = 0
lowHp = 0
if selfHp * 100 < selfMaxHp * 30 then
  lowHp = 1
end if

if selfHp * 100 < selfMaxHp * 15 and enemyHeroNear > 0 then
  walkTo(rx, ry)
  done = 1
  act = 1
end if

if done = 0 and melee = 0 and nearMeleeD2 <= 4 and (selfHp * 100 < selfMaxHp * 70 or nearMeleeHp > selfHp) then
  stepToward(selfX, selfY, rx, ry, 4)
  walkTo(sx, sy)
  done = 1
  act = 2
end if

if done = 0 and bestHero <> 0 then
  ' Poison uses the attack target retained from the previous tick.
  if poisonSlot >= 0 and poisonTarget = bestHero and poisonTick = worldTick - 1 and bestHeroD2 * 100 <= rng * rng then
    poisonUsed = useItem(poisonSlot)
    if poisonUsed = 1 then
      print "P " ; worldTick ; " target " ; bestHero
    end if
  end if
  if poisonTarget <> bestHero then
    print "F " ; worldTick ; " target " ; bestHero ; " hp " ; bestHeroHp
  end if
  attackTarget(bestHero)
  poisonTarget = bestHero
  poisonTick = worldTick
  done = 1
  act = 3
end if

if done = 0 and bestFoot <> 0 then
  attackTarget(bestFoot)
  done = 1
  act = 4
end if

if done = 0 and fortId <> 0 and lowHp = 0 then
  attackTarget(fortId)
  done = 1
  act = 5
end if

if done = 0 and towerId <> 0 and lowHp = 0 then
  attackTarget(towerId)
  done = 1
  act = 6
end if

if done = 0 then
  if lowHp = 1 then
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
      if allyCount > 0 then
        isqrt(maxAllyD2)
        if myD + 6 < sq then
          hold = 1
        end if
      end if
      if hold = 1 and holdTicks < 96 then
        walkTo(selfX, selfY)
        holdTicks = holdTicks + 1
        act = 8
      else
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
