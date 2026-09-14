Task W4 (candidate file policy/cand_lane.bas): LANE SWITCHING and REJOIN so the stack pushes where the enemy is NOT.
Observed failure (hosted, vs the #1 policy): our five level-1 heroes reach the enemy outer tower, meet 3 enemy heroes defending under it,
wipe, respawn at home, walk ~200 tiles back, wipe again; meanwhile the enemy farms XP and wins at ~5000 ticks. The local sparring partner
policy/spar_turtle.bas reproduces "a defended lane": v5 needs ~11,000 ticks to beat it. Goal: beat spar_turtle in < 4,000 ticks and keep RACE speed.
Implement in v5's structure (keep the map-generic route derivation), as one coherent change:
 (a) Route tables for ALL THREE lanes, derived at init from own towers + reflection (lane k own towers: ids 10+k*6+selfTeam*3+tier;
     enemy lane k tower positions = reflect(own lane (2-k) tower, same tier); fort = reflect(own fort)). Keep waypoints = own gate, inner, outer,
     then enemy outer, inner, gate, fort (7 entries per lane). Track destroyed enemy towers per lane (objDead as today) so a lane switch resumes
     at that lane's first standing tower. Mid lane crosses marsh and often has enemy heroes; treat it like the others.
 (b) Resistance detector: each tick count enemy heroes within 10 tiles of the current objective structure (or within 10 tiles of me when
     the objective is a waypoint). Keep a sticky score: score = score + (count >= 2 ? 1 : -1), clamped 0..120. When score >= 72
     (about 3 s of >= 2 defenders) AND the objective is an enemy structure that is still standing, SWITCH LANE: choose among the other two lanes
     the one whose first standing enemy tower is farther from the enemy heroes seen (tie: the side lane, not mid), reset score, keep pushing.
     Limit switches to at most one per 1,500 ticks.
 (c) Rejoin: a hero that has no living ally within 30 tiles and at least one living ally elsewhere (e.g. after respawn) should walk toward the
     centroid of living allies until within 12 tiles, and adopt the lane nearest to that centroid (min distance from the centroid to any of the
     lane's 7 route points). This keeps respawned heroes on the team's current lane.
 (d) Everything else identical to v5 (targeting, siege, kiting, shopping, stuck recovery, telemetry). Add a print line "LANE tick old new reason".
Report: the change, code regions, risks, and what telemetry lines confirm the switch/rejoin logic.
