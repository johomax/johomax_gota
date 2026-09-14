' GOTA policy v1 "blitz": all five heroes push mid together, focus fire the
' lowest-HP enemy hero, kill engaged footmen, siege exposed towers and the fort.
' See docs/ARENA_NOTES.md for the mechanics this relies on.

dim deadT(3)
dim objX(4)
dim objY(4)
dim objId(4)

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

if inited = 0 then
  inited = 1
  if selfTeam = 0 then
    objX(0) = 56
    objY(0) = 81
    objId(0) = 19
    objX(1) = 38
    objY(1) = 95
    objId(1) = 20
    objX(2) = 21
    objY(2) = 106
    objId(2) = 21
    objX(3) = 12
    objY(3) = 115
    objId(3) = 2
    homeX = 115
    homeY = 12
  else
    objX(0) = 71
    objY(0) = 46
    objId(0) = 16
    objX(1) = 89
    objY(1) = 32
    objId(1) = 17
    objX(2) = 106
    objY(2) = 21
    objId(2) = 18
    objX(3) = 115
    objY(3) = 12
    objId(3) = 1
    homeX = 12
    homeY = 115
  end if
  melee = 0
  if selfClass = 0 or selfClass = 4 or selfClass = 5 or selfClass = 9 then
    melee = 1
  end if
  ' acquisition radius squared (tiles) for footmen
  acq = 9
  if selfClass = 1 then
    acq = 42
  end if
  if selfClass = 2 then
    acq = 36
  end if
  if selfClass = 3 then
    acq = 25
  end if
  if selfClass = 6 then
    acq = 56
  end if
  if selfClass = 7 then
    acq = 42
  end if
  if selfClass = 8 then
    acq = 30
  end if
end if

' ---------- shopping / consumables (never consume the move/attack action) ----------
potSlot = -1
slot = 0
while slot < 6
  iid = itemId(slot)
  if iid = 1 or iid = 2 then
    potSlot = slot
  end if
  slot = slot + 1
wend
if selfHp * 2 < selfMaxHp then
  if potSlot >= 0 then
    useItem(potSlot)
  else
    if selfGold >= 50 then
      buyItem(2)
    end if
  end if
end if
if potSlot < 0 and selfGold >= 30 then
  buyItem(1)
end if
if selfGold >= 70 then
  buyItem(7)
end if
if selfGold >= 110 then
  buyItem(11)
end if
if selfGold >= 180 then
  buyItem(18)
end if
if selfGold >= 180 then
  buyItem(19)
end if
if selfGold >= 150 then
  buyItem(13)
end if
if selfGold >= 160 then
  buyItem(16)
end if

' ---------- current objective ----------
oi = 0
while oi < 3 and deadT(oi) = 1
  oi = oi + 1
wend
ox = objX(oi)
oy = objY(oi)
oid = objId(oi)

' ---------- scan visible objects ----------
bestHero = 0
bestHeroHp = 1000000
enemyHeroNear = 0
nearMeleeD2 = 1000000
nmx = 0
nmy = 0
bestFoot = 0
bestFootHp = 1000000
engFoot = 0
engFootHp = 1000000
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
      if objectId(i) <> selfId and objectAlive(i) = 1 and d2 <= 900 then
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
        hp = objectHp(i)
        if hp < bestHeroHp then
          bestHeroHp = hp
          bestHero = objectId(i)
        end if
        enemyHeroNear = enemyHeroNear + 1
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
      if objectAlive(i) = 1 then
        hp = objectHp(i)
        if d2 <= acq then
          if hp < bestFootHp then
            bestFootHp = hp
            bestFoot = objectId(i)
          end if
        end if
        if d2 <= 6 then
          if hp < engFootHp then
            engFootHp = hp
            engFoot = objectId(i)
          end if
        end if
      end if
    end if
    if k = 4 then
      if objectId(i) = oid then
        if objectHp(i) <= 0 then
          objDead = 1
        end if
      end if
      if objectAlive(i) = 1 and d2 <= 144 then
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
    end if
  end if
  i = i + 1
wend

if objDead = 1 and oi < 3 then
  deadT(oi) = 1
end if

' ---------- decide ----------
done = 0
act = 0

' retreat when low and threatened
if selfHp * 100 < selfMaxHp * 25 and enemyHeroNear > 0 then
  walkTo(homeX, homeY)
  done = 1
  act = 1
end if

' ranged kite on melee contact
if done = 0 and melee = 0 and nearMeleeD2 <= 4 then
  dx = selfX - nmx
  dy = selfY - nmy
  if dx = 0 and dy = 0 then
    dx = 1
  end if
  m = dx
  if m < 0 then
    m = -m
  end if
  mm = dy
  if mm < 0 then
    mm = -mm
  end if
  if mm > m then
    m = mm
  end if
  tx = selfX + dx * 3 / m
  ty = selfY + dy * 3 / m
  if tx < 0 then
    tx = 0
  end if
  if ty < 0 then
    ty = 0
  end if
  if tx > 127 then
    tx = 127
  end if
  if ty > 127 then
    ty = 127
  end if
  walkTo(tx, ty)
  done = 1
  act = 2
end if

if done = 0 and bestHero <> 0 then
  attackTarget(bestHero)
  done = 1
  act = 3
end if

if done = 0 and engFoot <> 0 then
  attackTarget(engFoot)
  done = 1
  act = 4
end if

if done = 0 and fortId <> 0 then
  attackTarget(fortId)
  done = 1
  act = 5
end if

if done = 0 and towerId <> 0 then
  attackTarget(towerId)
  done = 1
  act = 6
end if

if done = 0 and bestFoot <> 0 then
  attackTarget(bestFoot)
  done = 1
  act = 7
end if

if done = 0 then
  ' advance to objective, but hold if far ahead of the slowest nearby ally
  dx = ox - selfX
  dy = oy - selfY
  isqrt(dx * dx + dy * dy)
  myD = sq
  hold = 0
  if allyCount > 0 then
    isqrt(maxAllyD2)
    if myD + 8 < sq then
      hold = 1
    end if
  end if
  if hold = 1 then
    walkTo(selfX, selfY)
    act = 8
  else
    walkTo(ox, oy)
    act = 9
  end if
end if

if worldTick mod 600 = 0 then
  print "T " ; worldTick ; " p " ; selfX ; " " ; selfY ; " hp " ; selfHp ; "/" ; selfMaxHp ; " L" ; selfLevel ; " g" ; selfGold ; " oi " ; oi ; " act " ; act ; " eh " ; enemyHeroNear
end if
