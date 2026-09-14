' Probe: dump static map + visible objects to the private log.
' Print budget is 128 events/decision, so objects are spread over ticks.

sub printObj(i)
  print "O " ; worldTick ; " " ; objectId(i) ; " " ; objectKind(i) ; " " ; objectTeam(i) ; " " ; objectClass(i) ; " " ; objectX(i) ; " " ; objectY(i) ; " " ; objectHp(i) ; " " ; objectAlive(i)
end sub

if worldTick = 1 then
  print "SELF " ; selfId ; " " ; selfTeam ; " " ; selfClass ; " " ; selfX ; " " ; selfY ; " " ; selfHp ; " " ; selfMana ; " " ; selfGold ; " " ; selfLayer ; " " ; mapWidth ; " " ; mapHeight ; " " ; mapLayers
end if

if selfId = 100 or selfId = 105 then
  if worldTick >= 2 and worldTick <= 61 then
    i = (worldTick - 2) * 2
    if i < objectCount() then
      printObj(i)
    end if
    if i + 1 < objectCount() then
      printObj(i + 1)
    end if
  end if
  ph = worldTick mod 480
  if worldTick >= 480 and ph < 40 then
    if ph = 0 then
      n = 0
      i = 0
      while i < objectCount()
        if objectKind(i) = 3 then
          n = n + 1
        end if
        i = i + 1
      wend
      print "SNAP " ; worldTick ; " foot=" ; n ; " self " ; selfX ; " " ; selfY ; " hp=" ; selfHp ; " lvl=" ; selfLevel ; " gold=" ; selfGold ; " count=" ; objectCount()
    end if
    i = ph * 3
    k = 0
    while k < 3
      if i + k < objectCount() then
        if objectKind(i + k) <> 3 then
          printObj(i + k)
        end if
      end if
      k = k + 1
    wend
  end if
end if

if selfId = 100 then
  if worldTick >= 100 and worldTick <= 227 then
    row = worldTick - 100
    print "K " ; row ; " " ;
    x = 0
    while x < 128
      packed = 0
      mult = 1
      j = 0
      while j < 7
        v = 0
        if x + j < 128 then
          v = terrainKind(x + j, row) + 8 * terrainWalkable(x + j, row)
        end if
        packed = packed + v * mult
        mult = mult * 16
        j = j + 1
      wend
      print packed ; " " ;
      x = x + 7
    wend
    print ""
  end if
  if worldTick >= 228 and worldTick <= 355 then
    row = worldTick - 228
    print "H " ; row ; " " ;
    x = 0
    while x < 128
      packed = 0
      mult = 1
      j = 0
      while j < 3
        v = 0
        if x + j < 128 then
          v = terrainHeight(x + j, row)
          if v < 0 then
            v = 0
          end if
          if v > 1023 then
            v = 1023
          end if
        end if
        packed = packed + v * mult
        mult = mult * 1024
        j = j + 1
      wend
      print packed ; " " ;
      x = x + 3
    wend
    print ""
  end if
  if worldTick >= 356 and worldTick <= 483 then
    row = worldTick - 356
    print "W " ; row ; " " ;
    x = 0
    while x < 128
      packed = 0
      mult = 1
      j = 0
      while j < 7
        v = 0
        if x + j < 128 then
          v = terrainWaterDepth(x + j, row)
          if v < 0 then
            v = 0
          end if
          if v > 15 then
            v = 15
          end if
        end if
        packed = packed + v * mult
        mult = mult * 16
        j = j + 1
      wend
      print packed ; " " ;
      x = x + 7
    wend
    print ""
  end if
end if
