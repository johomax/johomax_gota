' GOTA policy v3 "edge blitz": all five heroes push one side lane as a stack.
' Blue pushes lane 2 (bottom/right, Blue's naturally winning lane); Red pushes
' lane 0 (top/left). Waypoints then towers then fort. See docs/ARENA_NOTES.md.

dim wpX(8)
dim wpY(8)
dim wpId(8)
dim wpKind(8)

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
  if sx > 127 then
    sx = 127
  end if
  if sy > 127 then
    sy = 127
  end if
end sub

if inited = 0 then
  inited = 1
  if selfTeam = 0 then
    wpX(0) = 89
    wpY(0) = 32
    wpKind(0) = 0
    wpX(1) = 71
    wpY(1) = 46
    wpKind(1) = 0
    wpX(2) = 64
    wpY(2) = 64
    wpKind(2) = 0
    wpX(3) = 56
    wpY(3) = 81
    wpId(3) = 19
    wpKind(3) = 1
    wpX(4) = 38
    wpY(4) = 95
    wpId(4) = 20
    wpKind(4) = 1
    wpX(5) = 21
    wpY(5) = 106
    wpId(5) = 21
    wpKind(5) = 1
    wpX(6) = 12
    wpY(6) = 115
    wpId(6) = 2
    wpKind(6) = 1
    homeX = 115
    homeY = 12
  else
    wpX(0) = 38
    wpY(0) = 95
    wpKind(0) = 0
    wpX(1) = 56
    wpY(1) = 81
    wpKind(1) = 0
    wpX(2) = 64
    wpY(2) = 64
    wpKind(2) = 0
    wpX(3) = 71
    wpY(3) = 46
    wpId(3) = 16
    wpKind(3) = 1
    wpX(4) = 89
    wpY(4) = 32
    wpId(4) = 17
    wpKind(4) = 1
    wpX(5) = 106
    wpY(5) = 21
    wpId(5) = 18
    wpKind(5) = 1
    wpX(6) = 115
    wpY(6) = 12
    wpId(6) = 1
    wpKind(6) = 1
    homeX = 12
    homeY = 115
  end if
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
if otype = 0 and myD2 <= 16 and oi < nObj - 1 then
  oi = oi + 1
  ox = wpX(oi)
  oy = wpY(oi)
  oid = wpId(oi)
  otype = wpKind(oi)
  dx = ox - selfX
  dy = oy - selfY
  myD2 = dx * dx + dy * dy
end if
' retreat point = previous waypoint (or home)
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
      if objectAlive(i) = 1 and d2 <= 100 then
        enemyHeroNear = enemyHeroNear + 1
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
      if objectAlive(i) = 1 and d2 <= footR2 then
        hp = objectHp(i)
        if hp < bestFootHp then
          bestFootHp = hp
          bestFoot = objectId(i)
        end if
      end if
    end if
    if k = 4 then
      if otype = 1 and objectId(i) = oid then
        if objectHp(i) <= 0 then
          objDead = 1
        end if
      end if
      if objectAlive(i) = 1 and d2 <= 81 then
        if d2 < towerD2 then
          towerD2 = d2
          towerId = objectId(i)
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

if done = 0 and melee = 0 and nearMeleeD2 <= 4 then
  stepToward(selfX, selfY, rx, ry, 4)
  walkTo(sx, sy)
  done = 1
  act = 2
end if

if done = 0 and bestHero <> 0 then
  attackTarget(bestHero)
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
    ' hang back toward the retreat point until healed
    stepToward(selfX, selfY, rx, ry, 6)
    walkTo(sx, sy)
    act = 7
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
      if stuckTicks >= 24 then
        ' re-path around an obstacle with a jittered destination
        jx = ox + (worldTick mod 7) - 3
        jy = oy + ((worldTick / 7) mod 7) - 3
        if jx < 0 then
          jx = 0
        end if
        if jy < 0 then
          jy = 0
        end if
        if jx > 127 then
          jx = 127
        end if
        if jy > 127 then
          jy = 127
        end if
        walkTo(jx, jy)
        if stuckTicks >= 36 then
          stuckTicks = 0
        else
          stuckTicks = stuckTicks + 1
        end if
        act = 10
      else
        walkTo(ox, oy)
        act = 9
      end if
    end if
  end if
end if
' stuck detection while advancing
if act = 9 then
  if selfX = lastX and selfY = lastY then
    stuckTicks = stuckTicks + 1
  else
    stuckTicks = 0
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
