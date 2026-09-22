' v407 = v385 with every hero starting in the mid lane (lane 1) instead of lane 2
' v385 = v363 with every hero starting in lane 2 (the right/bottom edge lane) instead of the seat lane
' v363 = v359 (carries camp from level 10) + v361's hunter rule (non-carries flee ten seconds from an enemy hero two levels above them within twelve tiles)
' v359 = v357 with Ranger/Crossbowman camping from level 10 (other ranged from 12)
' v357 = v348 with tighter guards: at most two lane switches a game and the camp stops after three deaths
' v348 = v338: lane switches need two allies within 10 tiles of our front (not just the region), at most three switches a game, and camping stops after four deaths (v338's long-game zeros had 5-10 deaths and 4-10 switches)
' v338 = v336 camping only with a ranged hero (attack range >= 4 tiles): the Berserker camper scored 292 locally
' v336 = v334 + the v329 farmer shop list (crossbow, axe, armour): a camper needs the HP and damage richard's hero buys at each respawn
' v334 = v333 with no health retreat and no dodging while camping: from the enemy base a death plus buyback is cheaper than the walk home
' v333 = camp from level 12 when no enemy hero is within 14 tiles of the camp point, no tower condition, outer/inner sieging only (v324)
' v327 = v326: camp only while no enemy hero is within 14 tiles of the camp point (an undefended base); otherwise farm the lane
' v326 = v325: gates are siegeable too (any lane tower more than 10 tiles from the god), and the camp starts only when no lane tower stands within 14 tiles of the camp point
' v325 = v324 + base camp: from level 7 the farmer stands six tiles inside the enemy base and farms every lane's creeps at spawn; no tower or outnumbered retreats while camping
' v324 = v317 + farmers siege outer/inner enemy towers (100 XP) when two allied creeps are within 8 tiles and no enemy hero was in power range last decision
' v317 = v315: farmers other than Ranger/Crossbowman do not target healthy enemy heroes beyond three tiles
' v315 = v314 without the base defence (one hero cannot save the god in mixed rosters and loses farm time) and lane switches only every 2400 ticks when two or more allies share our region
' v314 = v312 with a pure farmer draft: Ranger > Crossbowman > Arcanist > Lich > Berserker > DH > Warlock > Druid > VK > DK, no role diversity
' v312 = v311 for mixed rosters: every seat farms (no guards), initial lane = slot mod 3, then every 1200 ticks move to the lane region with the fewest allied heroes if ours holds one or more
' v311 = v310 + floaters: slots 3-4 farm a lane whose region has no allied hero (every seat must score in mixed rosters), guard only when all three lanes are held
' v310 = v306 with the base-defence check moved ahead of the attack block (a farmer with a creep in range never reached it: relh killed our god at tick 9452 with no DEFEND print)
' v306 = v304 + base defence: farmers scroll or run home when three or more enemy heroes are within 22 tiles of our god
' v304 = v302 with the ranged-creep priority only for ranged heroes (attack range >= 4 tiles); melee farmers stand in the wave anyway
' v302 = v301 + farmers prioritise enemy ranged creeps (+150) so the whole wave dies within six tiles of them
' v301 = v300 with both guards holding home (no shadowing): the baseline still killed our god 3-4 minutes early in two of six v300 games
' v300 = v299 + the keep-to-lane-tower portal rule restored (lost in v292): farmers teleport out at the start and after buybacks
' v299 = v298: farmers buy a portal scroll first and teleport to their lane's most advanced tower from the keep
' v298 = v296: Ranger and Berserker preferred in the draft (+2), guard 4 holds home to delay enemy pushes (v295's home guards kept games at the time limit), guard 3 shadows lane 0
' v296 = v295: draft may take both carries/mages, farmers flee to their lane tower, guards shadow farmers 0/1 seven tiles behind and fight heroes only
' v295 = v294: farmers cast only above half mana and never walk home for mana, wait at spawn for health only, portal back to their own lane's tower, and hold six tiles off enemy towers
' v294 = v293 with the wave front and creep targets limited to the hero's own lane region, lane chosen at init, and a farmer-first draft (carry, mage, fighter, support, frontline)
' v293 = v292 + farmers follow their wave front (v292's fixed corner points missed the creep clash: 315-1170 XP in 21 min on lane 0)
' v292 = the 2026-09-21 baseline turned into a lane farmer for the new ladder score (XP - 200/min): three solo laners, two home guards, no building attacks.
' GotA reference policy: draft, farm, push, heal, resupply, and finish the god.
' Every GotA host function has a gameplay use here; calls remain conditional.
' Object indices last only for this decision. IDs may be remembered.
' Read the bot guide for units, LOS restrictions, and action error constants.
' Automatic spells remain enabled as a fallback between our decisions.

dim owned(22)
dim inventorySlot(22)
dim allyIds(9)
dim seenMaxHp(9)
dim castRange(3)
dim castDelay(3)

sub chooseHero()
  if draftTurnId <> selfId then
    exit sub
  end if
  ' v314: mixed rosters — only our own hero's XP counts, so take the best available farmer regardless of team roles
  bestClass = -1
  bestScore = -10000
  for candidate = 0 to 9
    if heroAvailable(candidate) then
      score = 10
      if candidate = Ranger then
        score = 60
      elseif candidate = Crossbowman then
        score = 55
      elseif candidate = Arcanist then
        score = 50
      elseif candidate = Lich then
        score = 45
      elseif candidate = Berserker then
        score = 40
      elseif candidate = DemonHunter then
        score = 35
      elseif candidate = Warlock then
        score = 30
      elseif candidate = DruidWarden then
        score = 25
      elseif candidate = VanguardKnight then
        score = 20
      end if
      if score > bestScore then
        bestScore = score
        bestClass = candidate
      end if
    end if
  next candidate
  if bestClass >= 0 then
    accepted = draftHero(bestClass)
    actionError = lastActionError()
    print "DRAFT " ; bestClass ; " ok " ; accepted
  end if
end sub

sub learnAbilities()
  ' Rank requirements and effects come from the host, not a stat table.
  for upgrade = 1 to 4
    if abilityPoints() = 0 then
      exit sub
    end if
    upgradeSlot = -1
    upgradeScore = -1
    for spellSlot = 0 to 3
      rank = abilityLevel(spellSlot)
      if rank < abilityMaxLevel(spellSlot) then
        if selfLevel >= abilityRequiredLevel(spellSlot) then
          if canLevelAbility(spellSlot) then
            score = 10 - rank
            if spellSlot = 1 then
              score = score + 20
            elseif spellSlot = 3 then
              score = score + 40
            elseif rank = 0 then
              score = score + 10
            end if
            if score > upgradeScore then
              upgradeScore = score
              upgradeSlot = spellSlot
            end if
          end if
        end if
      end if
    next spellSlot
    if upgradeSlot < 0 then
      exit sub
    end if
    accepted = levelAbility(upgradeSlot)
    actionError = lastActionError()
  next upgrade
end sub

sub laneTest(px, py)
  inLaneFlag = 0
  if laneIdx = 2 and (px >= 102 or py >= 98) then
    inLaneFlag = 1
  end if
  if laneIdx = 0 and (px <= 13 or py <= 17) then
    inLaneFlag = 1
  end if
  if laneIdx = 1 then
    laneS = px + py - 115
    if laneS < 0 then
      laneS = 0 - laneS
    end if
    if laneS <= 14 then
      inLaneFlag = 1
    end if
  end if
end sub

sub readObject(index)
  id = objectId(index)
  kind = objectKind(index)
  team = objectTeam(index)
  hp = objectHp(index)
  if hp <= 0 then
    exit sub
  end if
  x = objectX(index)
  y = objectY(index)
  dx = x - selfX
  dy = y - selfY
  distance = dx * dx + dy * dy
  if team = selfTeam then
    if kind = 1 then
      homeX = x
      homeY = y
      enemyX = mapWidth - 1 - x
      enemyY = mapHeight - 1 - y
    elseif kind = 4 then
      ' Protected allied towers still serve as portal anchors; farmers anchor in their own lane.
      inLaneFlag = 1
      if laneIdx <= 2 then
        laneTest(x, y)
      end if
      dx = x - enemyX
      dy = y - enemyY
      score = dx * dx + dy * dy
      if score < forwardDistance and inLaneFlag = 1 then
        forwardDistance = score
        forwardX = x
        forwardY = y
      end if
    elseif kind = 2 then
      allyIds(allies) = id
      allies = allies + 1
      if id <> selfId then
        fdx = x - prevFrontX
        fdy = y - prevFrontY
        if fdx * fdx + fdy * fdy <= 100 then
          frontAllies = frontAllies + 1
        end if
        saveLane = laneIdx
        laneIdx = 0
        laneTest(x, y)
        if inLaneFlag = 1 then
          allyLane0 = allyLane0 + 1
        end if
        laneIdx = 1
        laneTest(x, y)
        if inLaneFlag = 1 then
          allyLane1 = allyLane1 + 1
        end if
        laneIdx = 2
        laneTest(x, y)
        if inLaneFlag = 1 then
          allyLane2 = allyLane2 + 1
        end if
        laneIdx = saveLane
      end if
      if id = 100 + 5 * selfTeam then
        f0Seen = 1
        f0X = x
        f0Y = y
      end if
      if id = 101 + 5 * selfTeam then
        f1Seen = 1
        f1X = x
        f1Y = y
      end if
      class = objectClass(index)
      if hp > seenMaxHp(class) then
        seenMaxHp(class) = hp
      end if
      if distance <= 100 then
        friendlyPower = friendlyPower + objectLevel(index) + 2
      end if
      missing = seenMaxHp(class) - hp
      if distance <= 16 and missing > healMissing then
        healMissing = missing
        healId = id
      end if
    elseif kind = 3 then
      if distance <= 64 then
        tanks = tanks + 1
      end if
      if laneIdx <= 2 then
        laneTest(x, y)
        if inLaneFlag = 1 then
          edx = x - enemyX
          edy = y - enemyY
          ed = edx * edx + edy * edy
          if ed < frontD then
            frontD = ed
            frontX = x
            frontY = y
          end if
        end if
      end if
    end if
    exit sub
  end if
  if kind = 3 and distance <= 36 then
    nearCreeps = nearCreeps + 1
  end if
  if kind = 3 and laneIdx >= 3 then
    exit sub
  end if
  if kind = 3 and laneIdx <= 2 and distance > 64 then
    laneTest(x, y)
    if inLaneFlag = 0 then
      exit sub
    end if
  end if
  if kind = 1 then
    enemyX = x
    enemyY = y
  end if
  if kind = 4 and distance < eTowerD then
    eTowerD = distance
    eTowerX = x
    eTowerY = y
  end if
  if kind = 4 and id < 28 then
    cdx = x - campX
    cdy = y - campY
    if cdx * cdx + cdy * cdy <= 196 then
      campTowers = campTowers + 1
    end if
  end if
  if kind = 2 then
    cdx = x - campX
    cdy = y - campY
    if cdx * cdx + cdy * cdy <= 196 then
      campHeroes = campHeroes + 1
    end if
    hdx = x - homeX
    hdy = y - homeY
    if hdx * hdx + hdy * hdy <= 484 then
      baseThreat = baseThreat + 1
    end if
  end if
  if kind = 2 and distance <= 144 then
    enemyPower = enemyPower + objectLevel(index) + 2
    if objectMana(index) >= 25 then
      enemyPower = enemyPower + 2
    end if
  end if
  ' v361: a hunter (an enemy hero two or more levels above us within twelve tiles) makes non-carries leave for ten seconds; relh's heroes farm our weak heroes (11 kills of one DH in a game)
  if kind = 2 and distance <= 144 and objectLevel(index) >= selfLevel + 2 then
    hunterUntil = worldTick + 240
  end if
  if distance < threatDistance then
    threatDistance = distance
    threatX = x
    threatY = y
  end if
  if distance > 324 or objectAlive(index) = 0 then
    exit sub
  end if
  target = objectTarget(index)
  if kind = 4 and target = selfId then
    towerAggro = 1
  end if
  ' v324: an outer or inner enemy tower (more than 30 tiles from their god) is a 100-XP target when two allied creeps are near us and no enemy hero was near last decision
  towerOk = 0
  if kind = 4 and laneIdx <= 2 and prevTanks >= 2 and prevEnemyPower = 0 then
    gdx = x - enemyX
    gdy = y - enemyY
    if gdx * gdx + gdy * gdy > 900 then
      towerOk = 1
    end if
  end if
  if kind <> 2 and kind <> 3 and towerOk = 0 then
    exit sub
  end if
  score = 1000 - distance * 2
  if kind = 1 then
    score = score + 500
  elseif kind = 2 then
    ' v317: only the ranged carries pick fights; other farmers ignore healthy heroes beyond three tiles (they die 4-11 times a game)
    if selfClass <> Ranger and selfClass <> Crossbowman and distance > 9 and hp >= selfAttackDamage * 4 then
      exit sub
    end if
    score = score + 60 - objectLevel(index) * 8
    if hp < selfAttackDamage * 4 then
      score = score + 250
    end if
  elseif kind = 3 then
    score = score + 100
    ' v302: farmers go for the enemy ranged creeps first: they die four tiles behind the melee line, outside a ranged hero's six-tile XP share
    if laneIdx <= 2 and objectClass(index) = 1 and attackRange >= 4 then
      score = score + 150
    end if
    if hp <= selfAttackDamage and selfAttackCooldown <= tickRate \ 2 then
      score = score + 400
    end if
  elseif kind = 4 then
    score = score + 80
  elseif kind = 5 then
    score = score + 40
  end if
  if target = selfId then
    score = score + 40
  end if
  if id = selfTarget then
    score = score + 60
  end if
  if id = blockedId and worldTick < blockedUntil then
    exit sub
  end if
  if score > bestScore then
    bestScore = score
    bestIndex = index
    bestId = id
    bestKind = kind
    bestHp = hp
    bestX = x
    bestY = y
    bestDistance = distance
  end if
end sub

sub observe()
  prevTanks = tanks
  prevEnemyPower = enemyPower
  prevCampTowers = campTowers
  campTowers = 0
  prevCampHeroes = campHeroes
  campHeroes = 0
  prevFrontX = frontX
  prevFrontY = frontY
  frontAllies = 0
  campX = enemyX + (mapWidth \ 2 - enemyX) \ 9
  campY = enemyY + (mapHeight \ 2 - enemyY) \ 9
  bestScore = -10000
  frontD = 1000000
  nearCreeps = 0
  baseThreat = 0
  allyLane0 = 0
  allyLane1 = 0
  allyLane2 = 0
  eTowerD = 1000000
  f0Seen = 0
  f1Seen = 0
  bestId = 0
  bestDistance = 1000000
  threatDistance = 1000000
  forwardDistance = 1000000
  friendlyPower = 0
  enemyPower = 0
  allies = 0
  tanks = 0
  towerAggro = 0
  healId = selfId
  healMissing = selfMaxHp - selfHp
  seenMaxHp(selfClass) = selfMaxHp
  objects = objectCount()
  ' Buildings and heroes precede creeps. Rotate the large creep tail so a
  ' crowded battlefield cannot exhaust the per-decision VM budget.
  for scan = 0 to 95
    index = scan
    if scan >= 48 then
      index = scan + scanOffset
    end if
    if index < objects then
      readObject(index)
    end if
  next scan
  ' Retain a creep target outside this scan window only after validating
  ' its remembered index against the stable ID in the fresh observation.
  if targetIndex >= 48 and targetIndex < objects and selfTarget <> 0 then
    if targetIndex < 48 + scanOffset or targetIndex >= 96 + scanOffset then
      if objectId(targetIndex) = selfTarget then
        readObject(targetIndex)
      end if
    end if
  end if
  scanOffset = scanOffset + 48
  if scanOffset >= objects - 48 then
    scanOffset = 0
  end if
  if bestId = 0 then
    exit sub
  end if
  targetIndex = bestIndex
  ' Divide large integer world units before mixing them with Q16.16 values.
  velocityX = (objectVelX(bestIndex) \ 100) / (worldScale \ 100)
  velocityY = (objectVelY(bestIndex) \ 100) / (worldScale \ 100)
  facingX = (objectFacingX(bestIndex) \ 100) / (worldScale \ 100)
  facingY = (objectFacingY(bestIndex) \ 100) / (worldScale \ 100)
  aimedAtUs = facingX * (selfX - bestX) + facingY * (selfY - bestY)
  if bestKind = 2 then
    ' Visible equipment and potion stacks help judge a close duel.
    for inspectSlot = 0 to 5
      gear = objectItemId(bestIndex, inspectSlot)
      quantity = objectItemCount(bestIndex, inspectSlot)
      if quantity > 0 and bestDistance <= 144 then
        if gear >= 5 and gear <= 20 then
          enemyPower = enemyPower + 1
        elseif gear = 1 or gear = 2 then
          enemyPower = enemyPower + 2
        end if
      end if
    next inspectSlot
  end if
end sub

sub buy(id, price, quantity)
  if owned(id) >= quantity or budget < price then
    exit sub
  end if
  if owned(id) = 0 and emptySlots = 0 then
    exit sub
  end if
  accepted = buyItem(id)
  actionError = lastActionError()
  if accepted then
    if owned(id) = 0 then
      emptySlots = emptySlots - 1
    end if
    owned(id) = owned(id) + 1
    budget = budget - price
    for boughtSlot = 0 to 5
      if itemId(boughtSlot) = id then
        inventorySlot(id) = boughtSlot
      end if
    next boughtSlot
  end if
end sub

sub inventory()
  for id = 0 to 22
    owned(id) = 0
    inventorySlot(id) = -1
  next id
  emptySlots = 0
  for itemSlot = 0 to 5
    id = itemId(itemSlot)
    if id = 0 then
      emptySlots = emptySlots + 1
    else
      owned(id) = itemCount(itemSlot)
      inventorySlot(id) = itemSlot
      if itemCooldown(itemSlot) = 0 and inOwnSpawn() = 0 then
        consume = 0
        if id = 1 and selfMaxHp - selfHp >= 60 then
          consume = threatDistance > 100 and worldTick - hurtTick > tickRate
        elseif id = 2 and selfHp * 2 < selfMaxHp then
          consume = 1
        elseif id = 22 and selfMaxMana - selfMana >= 45 then
          consume = threatDistance > 100 and worldTick - hurtTick > tickRate
        elseif id = 3 and selfMana * 3 < selfMaxMana then
          consume = bestId <> 0
        elseif id = 4 and selfTarget = bestId and bestId <> 0 then
          consume = bestDistance <= attackRange * attackRange
        end if
        if consume then
          accepted = useItem(itemSlot)
          actionError = lastActionError()
          if accepted then
            owned(id) = owned(id) - 1
            if owned(id) = 0 then
              emptySlots = emptySlots + 1
              inventorySlot(id) = -1
            end if
          end if
        end if
      end if
    end if
  next itemSlot
  if canShop() = 0 then
    exit sub
  end if
  ' Reserve three slots for recovery and travel, two for useful equipment,
  ' and one for a role-specific burst consumable. Stacks top up on return.
  budget = selfGold
  ' v336: farmer slots: scroll, potion, boots, Rune Crossbow (+14), Battle Axe (+14), Knight Armor (+120 HP), potions (v329 list)
  if laneIdx <= 2 then
    buy(21, 100, 1)
    buy(1, 30, 1)
    buy(8, 100, 1)
    buy(19, 180, 1)
    buy(18, 180, 1)
    buy(16, 160, 1)
    buy(1, 30, 3)
  else
    buy(8, 100, 1)
    buy(1, 30, 2)
    buy(21, 100, 2)
    buy(22, 45, 2)
    if role = 0 or role = 4 then
      buy(16, 160, 1)
      buy(2, 75, 2)
    elseif role = 1 then
      buy(19, 180, 1)
      buy(4, 40, 2)
    else
      buy(20, 190, 1)
      buy(3, 90, 2)
    end if
  end if
end sub

sub dodgeWarnings()
  dodge = 0
  warnings = spellCount()
  ' Rotate unusually busy spell lists instead of starving later warnings.
  for warning = warningOffset to warningOffset + 11
    if warning < warnings then
      spell = spellAbility(warning)
      caster = spellCasterId(warning)
      hostile = caster <> selfId
      for ally = 0 to allies - 1
        if caster = allyIds(ally) then
          hostile = 0
        end if
      next ally
      ' Recovery effects are harmless, including those with hidden casters.
      if spell = 0 or spell = 2 or spell = 8 or spell = 12 then
        hostile = 0
      end if
      if spell = 13 or spell = 14 or spell = 16 or spell = 20 then
        hostile = 0
      end if
      if spell = 32 or spell = 36 then
        hostile = 0
      end if
      impact = spellImpactTick(warning) - worldTick
      warningX = spellX(warning)
      warningY = spellY(warning)
      dx = selfX - warningX
      dy = selfY - warningY
      if hostile and impact > 0 and impact <= tickRate * 3 then
        if dx * dx + dy * dy <= 9 then
          dodge = 1
          dodgeX = selfX + 3
          dodgeY = selfY + 3
          if dx < 0 then
            dodgeX = selfX - 3
          end if
          if dy < 0 then
            dodgeY = selfY - 3
          end if
        end if
      end if
    end if
  next warning
  warningOffset = warningOffset + 12
  if warningOffset >= warnings then
    warningOffset = 0
  end if
end sub

sub moveTo(goalX, goalY, marching)
  if selfRootTicks > 0 then
    exit sub
  end if
  if goalX = orderX and goalY = orderY and marching = orderMarch then
    if worldTick - orderTick < tickRate * 2 then
      exit sub
    end if
  end if
  ' Snap the requested destination to an open nearby surface. A* in the
  ' host still owns the complete route and cliff/ramp collision checks.
  routeScore = 1000000
  routeFound = 0
  floorHeight = terrainHeight(selfX, selfY)
  for offsetY = -1 to 1
    for offsetX = -1 to 1
      tileX = goalX + offsetX
      tileY = goalY + offsetY
      if tileX >= 0 and tileX < mapWidth then
        if tileY >= 0 and tileY < mapHeight then
          open = terrainWalkable(tileX, tileY)
          ground = terrainKind(tileX, tileY)
          height = terrainHeight(tileX, tileY)
          depth = terrainWaterDepth(tileX, tileY)
          if open = 0 then
            for layer = 0 to mapLayers - 1
              if terrainWalkableAt(tileX, tileY, layer) then
                open = 1
                ground = terrainKindAt(tileX, tileY, layer)
                height = terrainHeightAt(tileX, tileY, layer)
                depth = terrainWaterDepthAt(tileX, tileY, layer)
                exit for
              end if
            next layer
          end if
          if open and ground <> TerrainNone then
            elevation = height - floorHeight
            if elevation < 0 then
              elevation = -elevation
            end if
            score = (offsetX * offsetX + offsetY * offsetY) * 20
            score = score + depth * 2 + elevation
            if ground = TerrainRoad then
              score = score - 5
            end if
            if score < routeScore then
              routeScore = score
              routeX = tileX
              routeY = tileY
              routeFound = 1
            end if
          end if
        end if
      end if
    next offsetX
  next offsetY
  if routeFound = 0 then
    exit sub
  end if
  if marching then
    accepted = attackMove(routeX, routeY)
  else
    accepted = walkTo(routeX, routeY)
  end if
  actionError = lastActionError()
  orderTick = worldTick
  if accepted then
    orderX = goalX
    orderY = goalY
    orderMarch = marching
  elseif actionError = ActionNoRoute then
    ' Try the lane center on the next decision rather than retrying a wall.
    crossedMiddle = 0
    blockedId = bestId
    blockedUntil = worldTick + tickRate * 3
  end if
end sub

sub spells()
  for spellSlot = 0 to 3
    charges = abilityCharges(spellSlot)
    recharge = abilityRecharge(spellSlot)
    damage = abilityDamage(spellSlot)
    healing = abilityHeal(spellSlot)
    restore = abilityRestore(spellSlot)
    cost = abilityManaCost(spellSlot)
    if abilityLevel(spellSlot) > 0 and charges > 0 then
      if abilityCooldown(spellSlot) = 0 and selfMana >= cost and (laneIdx >= 3 or selfMana * 2 >= selfMaxMana) then
        castId = 0
        if healing > 0 and healMissing >= healing \ 2 then
          if selfClass = DruidWarden and spellSlot > 0 then
            castId = healId
          elseif selfMaxHp - selfHp >= healing \ 2 then
            castId = selfId
          end if
        elseif restore > 0 and selfMaxMana - selfMana >= restore then
          castId = selfId
        elseif damage > 0 and bestId <> 0 then
          if bestDistance <= castRange(spellSlot) * castRange(spellSlot) then
            ' Save the last recharging charge for valuable targets.
            if bestKind <> 3 or charges > 1 or recharge <= tickRate then
              castId = bestId
            elseif bestHp <= damage then
              castId = bestId
            end if
          end if
        end if
        if castId <> 0 then
          if castId = bestId and spellSlot >= 2 then
            ' Area spells lead the observed movement, with a bounded lead.
            leadX = velocityX * castDelay(spellSlot)
            leadY = velocityY * castDelay(spellSlot)
            if leadX > 2 then
              leadX = 2
            elseif leadX < -2 then
              leadX = -2
            end if
            if leadY > 2 then
              leadY = 2
            elseif leadY < -2 then
              leadY = -2
            end if
            aimX = bestX + leadX
            aimY = bestY + leadY
            if aimX >= 0 and aimX < mapWidth - 1 then
              if aimY >= 0 and aimY < mapHeight - 1 then
                accepted = castPoint(spellSlot, aimX, aimY)
                actionError = lastActionError()
                if accepted then
                  exit sub
                end if
              end if
            end if
          else
            accepted = castTarget(spellSlot, castId)
            actionError = lastActionError()
            if accepted then
              exit sub
            end if
          end if
        end if
      end if
    end if
  next spellSlot
end sub

if drafting then
  chooseHero()
  end
end if

' Buy back immediately whenever affordable, including during a long respawn.
if selfHp <= 0 then
  price = buybackPrice()
  if price > 0 and selfGold >= price then
    accepted = buyback()
    actionError = lastActionError()
  end if
  initialized = 0
  end
end if
if selfChannelTicks > 0 or selfStunTicks > 0 then
  end
end if
if worldTick < nextThink then
  end
end if
nextThink = worldTick + 6
role = heroRole(selfClass)
attackRange = (selfAttackRange \ 100) / (worldScale \ 100)
speed = (selfMoveSpeed \ 100) / (worldScale \ 100)

if initialized = 0 then
  initialized = 1
  ' v407: everyone starts in mid (lane 1) — a probe of whether the field has left mid now that lane 2's edge over lane 0 shrank to +46
  laneIdx = 1
  floater = 1
  lastLaneChange = 0
  switches = 0
  spawnX = selfX
  spawnY = selfY
  homeX = selfX
  homeY = selfY
  enemyX = mapWidth - 1 - selfX
  enemyY = mapHeight - 1 - selfY
  previousHp = selfHp
  progressTick = worldTick
  previousX = selfX
  previousY = selfY
  crossedMiddle = 0
  retreating = 0
  ' The host exposes effects and costs, but not spell range or cast shape.
  ' These small tables mirror content.nim; all distances are in tiles.
  castRange(0) = 0
  castRange(1) = 1.5
  castRange(2) = 2.5
  castRange(3) = 2
  castDelay(2) = 24
  castDelay(3) = 24
  if selfClass = VanguardKnight then
    castRange(3) = 1.8
    castDelay(2) = 12
    castDelay(3) = 6
  elseif selfClass = Ranger then
    castRange(0) = 7
    castRange(1) = 6
    castRange(2) = 6.5
    castRange(3) = 8
  elseif selfClass = Arcanist then
    castRange(1) = 5.5
    castRange(2) = 6
    castRange(3) = 7
    castDelay(2) = 48
    castDelay(3) = 72
  elseif selfClass = DruidWarden then
    castRange(3) = 3.3
  elseif selfClass = DemonHunter then
    castRange(2) = 2
    castRange(3) = 5
    castDelay(2) = 6
  elseif selfClass = DeathKnight then
    castRange(2) = 2.6
    castRange(3) = 2.3
    castDelay(3) = 12
  elseif selfClass = Crossbowman then
    castRange(0) = 7
    castRange(1) = 6.6
    castRange(2) = 6
    castRange(3) = 7.5
    castDelay(2) = 12
  elseif selfClass = Lich then
    castRange(0) = 6
    castRange(1) = 6.6
    castRange(2) = 5
    castRange(3) = 6.5
  elseif selfClass = Warlock then
    castRange(1) = 4.6
    castRange(2) = 4
    castRange(3) = 5
  elseif selfClass = Berserker then
    castRange(3) = 2.1
    castDelay(2) = 12
    castDelay(3) = 48
  end if
end if

if selfHp < previousHp then
  hurtTick = worldTick
end if
previousHp = selfHp
if selfAttacksLanded <> previousHits or selfX <> previousX or selfY <> previousY then
  progressTick = worldTick
end if
previousHits = selfAttacksLanded
previousX = selfX
previousY = selfY
if worldTick - progressTick > tickRate * 6 and selfTarget <> 0 then
  blockedId = selfTarget
  blockedUntil = worldTick + tickRate * 3
  progressTick = worldTick
end if

learnAbilities()
observe()
inventory()
spells()
dodgeWarnings()
' v312: slots 3-4 float — farm a lane whose region holds no allied hero (mixed rosters leave lanes empty), else guard home
' v313: mixed rosters — every seat farms; every 1200 ticks move to the lane region with the fewest allied heroes when ours has at least one more
if floater = 1 and worldTick >= 1200 and worldTick - lastLaneChange >= 2400 and worldTick mod 600 < 6 then
  curAllies = allyLane0
  if laneIdx = 1 then
    curAllies = allyLane1
  elseif laneIdx = 2 then
    curAllies = allyLane2
  end if
  newLane = laneIdx
  bestAllies = curAllies
  if allyLane1 < bestAllies then
    bestAllies = allyLane1
    newLane = 1
  end if
  if allyLane0 < bestAllies then
    bestAllies = allyLane0
    newLane = 0
  end if
  if allyLane2 < bestAllies then
    bestAllies = allyLane2
    newLane = 2
  end if
  if newLane <> laneIdx and curAllies >= 2 and frontAllies >= 2 and switches < 2 then
    laneIdx = newLane
    lastLaneChange = worldTick
    switches = switches + 1
    print "FLOAT " ; worldTick ; " lane " ; laneIdx ; " allies " ; allyLane0 ; " " ; allyLane1 ; " " ; allyLane2
  end if
end if

' v325: base camp — from level 7 a farmer farms the enemy creep spawns beside their god (richard v153 / relh v161 heroes reach 12000-14000 XP a game there)
camp = 0
if laneIdx <= 2 and prevCampHeroes = 0 and selfDeaths < 4 then
  if selfLevel >= 12 and attackRange >= 4 then
    camp = 1
  end if
  if selfLevel >= 10 and (selfClass = Ranger or selfClass = Crossbowman) then
    camp = 1
  end if
end if
if selfHp * 4 < selfMaxHp and camp = 0 then
  retreating = 1
end if
if laneIdx >= 3 and selfMana * 8 < selfMaxMana and bestId = 0 then
  retreating = 1
end if
if inOwnSpawn() then
  if selfHp * 10 < selfMaxHp * 9 or (laneIdx >= 3 and selfMana * 10 < selfMaxMana * 9) then
    moveTo(spawnX, spawnY, 0)
    end
  end if
  retreating = 0
end if

if dodge and selfRootTicks = 0 and camp = 0 then
  moveTo(dodgeX, dodgeY, 0)
  end
end if
if retreating then
  ' A safe scroll saves the long return trip; damage and control can punish it.
  if owned(21) > 0 and selfPortalCooldown = 0 and selfRootTicks = 0 then
    dx = selfX - homeX
    dy = selfY - homeY
    if dx * dx + dy * dy > 400 and threatDistance > 144 then
      accepted = useItemAt(inventorySlot(21), spawnX, spawnY)
      actionError = lastActionError()
      if accepted then
        end
      end if
    end if
  end if
  moveTo(spawnX, spawnY, 0)
  end
end if

if worldTick < hunterUntil and camp = 0 and selfClass <> Ranger and selfClass <> Crossbowman then
  fleeX = homeX
  fleeY = homeY
  if laneIdx <= 2 and forwardDistance < 1000000 then
    fleeX = forwardX
    fleeY = forwardY
  end if
  moveTo(fleeX, fleeY, 0)
  end
end if
if towerAggro and selfHp * 3 < selfMaxHp * 2 and tanks = 0 and camp = 0 then
  fleeX = homeX
  fleeY = homeY
  if laneIdx <= 2 and forwardDistance < 1000000 then
    fleeX = forwardX
    fleeY = forwardY
  end if
  moveTo(fleeX, fleeY, 0)
  end
end if
if enemyPower > friendlyPower + 6 and threatDistance < 64 and camp = 0 then
  if selfHp * 4 < selfMaxHp * 3 then
  fleeX = homeX
  fleeY = homeY
  if laneIdx <= 2 and forwardDistance < 1000000 then
    fleeX = forwardX
    fleeY = forwardY
  end if
    moveTo(fleeX, fleeY, 0)
    end
  end if
end if

if bestId <> 0 then
  ' Finish a windup before kiting; never cancel every swing with movement.
  if bestKind = 2 and aimedAtUs > 0 and attackRange >= 3 then
    if bestDistance < 4 and selfAttackCooldown > tickRate \ 2 then
      if selfAttacksLanded > 0 and speed > 0 then
        kiteStep = (selfMoveSpeed * tickRate) \ worldScale
        if kiteStep < 1 then
          kiteStep = 1
        elseif kiteStep > 4 then
          kiteStep = 4
        end if
        kiteX = selfX + kiteStep
        kiteY = selfY + kiteStep
        if bestX >= selfX then
          kiteX = selfX - kiteStep
        end if
        if bestY >= selfY then
          kiteY = selfY - kiteStep
        end if
        moveTo(kiteX, kiteY, 0)
        end
      end if
    end if
  end if
  if selfTarget <> bestId then
    accepted = attackTarget(bestId)
    actionError = lastActionError()
    if accepted = 0 then
      blockedId = bestId
      blockedUntil = worldTick + tickRate * 3
    else
      orderTick = 0
    end if
  end if
  end
end if

' v292: ladder score = lifetime XP - 200 per simulated minute (floored at 0, team mean). A lane's eight enemy creeps per
' wave give 360 XP/min shared within six tiles: one hero per lane nets +160/min, two in a lane net nothing. Slots 0-2 farm
' lanes 0/2/mid solo at the creep clash points; slots 3-4 hold between our god and the centre and never touch the farm.
' Nobody attacks buildings or the god: the game must not end while the farmers are ahead of the clock.
goalX = mapWidth \ 2
goalY = mapHeight \ 2
if laneIdx = 0 then
  goalX = mapWidth \ 10
  goalY = mapHeight \ 10
elseif laneIdx = 1 then
  goalX = mapWidth * 9 \ 10
  goalY = mapHeight * 9 \ 10
elseif laneIdx >= 3 then
  goalX = homeX + (mapWidth \ 2 - homeX) \ 3
  goalY = homeY + (mapHeight \ 2 - homeY) \ 3
  ' v296: guards shadow the side-lane farmers nine tiles toward home (outside the six-tile XP share) and fight heroes only
  gSeen = 0
  if gSeen = 1 then
    goalX = gX
    goalY = gY
    if homeX > gX then
      goalX = gX + 7
    else
      goalX = gX - 7
    end if
    if homeY > gY then
      goalY = gY + 7
    else
      goalY = gY - 7
    end if
  end if
end if
' v293: a farmer stands where its wave meets the enemy's — the allied creep nearest the enemy god within 25 tiles
if laneIdx <= 2 and frontD < 1000000 then
  goalX = frontX
  goalY = frontY
  ' v295: never follow the wave under an enemy tower (2x damage now): hold six tiles back toward home
  if eTowerD < 1000000 then
    tdx = frontX - eTowerX
    tdy = frontY - eTowerY
    if tdx * tdx + tdy * tdy <= 100 then
      if homeX > frontX then
        goalX = frontX + 6
      else
        goalX = frontX - 6
      end if
      if homeY > frontY then
        goalY = frontY + 6
      else
        goalY = frontY - 6
      end if
    end if
  end if
end if
' v300: portal from the keep to the lane's most advanced tower (the rule from the baseline was lost in v292); fires at the start and after every buyback
if laneIdx <= 2 and canShop() = 1 and owned(21) > 0 and selfPortalCooldown = 0 and forwardDistance < 1000000 and inventorySlot(21) >= 0 then
  pdx = selfX - forwardX
  pdy = selfY - forwardY
  if pdx * pdx + pdy * pdy > 400 and threatDistance > 144 then
    accepted = useItemAt(inventorySlot(21), forwardX, forwardY)
    if accepted then
      print "PORTAL " ; worldTick ; " to " ; forwardX ; " " ; forwardY
      end
    end if
  end if
end if
if worldTick mod 240 < 6 then
  print "F " ; worldTick ; " lane " ; laneIdx ; " cls " ; selfClass ; " at " ; selfX ; " " ; selfY ; " L" ; selfLevel ; " goal " ; goalX ; " " ; goalY ; " tanks " ; tanks ; " ecreeps6 " ; nearCreeps ; " hp " ; selfHp ; " deaths " ; selfDeaths
end if
if camp = 1 then
  goalX = campX
  goalY = campY
end if
moveTo(goalX, goalY, 1)
