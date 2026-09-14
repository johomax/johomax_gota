' GOTA policy v2 "waveguard": push mid behind the friendly footman front, focus
' fire enemy heroes in range, last-hit footmen, siege towers only when our
' footmen tank them, short retreats at low HP. See docs/ARENA_NOTES.md.

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

' sets (sx, sy) = point k tiles from (fx,fy) toward (tx,ty)
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
    homeX = 106
    homeY = 21
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
    homeX = 21
    homeY = 106
  end if
  melee = 0
  if selfClass = 0 or selfClass = 4 or selfClass = 5 or selfClass = 9 then
    melee = 1
  end if
  ' basic range in tenths of a tile
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
  ' engagement radii squared (tiles^2)
  heroR2 = (rng + 15) * (rng + 15) / 100
  if melee = 1 then
    heroR2 = 25
  end if
  footR2 = (rng + 10) * (rng + 10) / 100
  if melee = 1 then
    footR2 = 9
  end if
  ' hold offset behind the front
  behind = 3
  if melee = 1 then
    behind = 0
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

' ---------- current objective ----------
oi = 0
while oi < 3 and deadT(oi) = 1
  oi = oi + 1
wend
ox = objX(oi)
oy = objY(oi)
oid = objId(oi)

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
twx = 0
twy = 0
fortId = 0
objDead = 0
frontId = 0
frontD2 = 1000000
fx = 0
fy = 0
allyNear = 0

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
        allyNear = allyNear + 1
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
      if objectId(i) = oid then
        if objectHp(i) <= 0 then
          objDead = 1
        end if
      end if
      if objectAlive(i) = 1 and d2 <= 100 then
        if d2 < towerD2 then
          towerD2 = d2
          towerId = objectId(i)
          twx = x
          twy = y
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

' tower siege only when our front footman is tanking it (within 6 tiles)
if towerId <> 0 then
  ok = 0
  if frontId <> 0 then
    ex = fx - twx
    ey = fy - twy
    if ex * ex + ey * ey <= 36 then
      ok = 1
    end if
  end if
  if ok = 0 then
    towerId = 0
  end if
end if

' ---------- decide ----------
done = 0
act = 0
lowHp = 0
if selfHp * 100 < selfMaxHp * 30 then
  lowHp = 1
end if

' critical: flee home when nearly dead and threatened
if selfHp * 100 < selfMaxHp * 15 and enemyHeroNear > 0 then
  walkTo(homeX, homeY)
  done = 1
  act = 1
end if

' ranged kite on melee contact
if done = 0 and melee = 0 and nearMeleeD2 <= 4 then
  stepToward(selfX, selfY, homeX, homeY, 4)
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
  if frontId <> 0 then
    ' hold a few tiles behind the most advanced friendly footman
    off = behind
    if lowHp = 1 then
      off = 8
    end if
    if off = 0 then
      tx = fx
      ty = fy
    else
      stepToward(fx, fy, homeX, homeY, off)
      tx = sx
      ty = sy
    end if
    dx = tx - selfX
    dy = ty - selfY
    if dx * dx + dy * dy <= 2 then
      walkTo(selfX, selfY)
      act = 8
    else
      walkTo(tx, ty)
      act = 9
    end if
  else
    ' no wave nearby: move toward the objective (finds the lane)
    if lowHp = 1 then
      walkTo(homeX, homeY)
      act = 7
    else
      walkTo(ox, oy)
      act = 10
    end if
  end if
end if

if worldTick mod 480 = 0 then
  print "T " ; worldTick ; " p " ; selfX ; " " ; selfY ; " hp " ; selfHp ; "/" ; selfMaxHp ; " L" ; selfLevel ; " g" ; selfGold ; " oi " ; oi ; " act " ; act ; " eh " ; enemyHeroNear ; " fr " ; fx ; " " ; fy
end if
