#!/bin/zsh
# usage: SMOKE_VERSIONS="289" tmp/newsmoke.sh — 5x candidate (Red) vs 5x new baseline (Blue) on the new coworld
cd /Users/jordan/Desktop/Projects/johomax/gota
M=./coworld/cow_27feb885-a1bf-48ce-8016-ec72a28c4bce/coworld_manifest.json; B=tmp/base_new.bas
for n in ${=SMOKE_VERSIONS}; do
  rm -rf runs/nsmoke_v$n; echo "=== v$n $(date -u +%H:%M:%S)"
  DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode $M policy/v$n.bas policy/v$n.bas policy/v$n.bas policy/v$n.bas policy/v$n.bas $B $B $B $B $B --variant competition --timeout-seconds 1500 -o runs/nsmoke_v$n > runs/nsmoke_v$n.out 2>&1
  echo "exit $? $(date -u +%H:%M:%S)"; python3 -c "import json;r=json.load(open('runs/nsmoke_v$n/results.json'));print('result', r.get('outcome'), r.get('ticks'), r.get('scores'))" 2>&1
  grep -i "BASIC error\|compile\|unexpected" runs/nsmoke_v$n/logs/policy_agent_0.log runs/nsmoke_v$n/player_status.json 2>/dev/null | head -3
  grep -c "" runs/nsmoke_v$n/logs/policy_agent_0.log; grep "DRAFT\|INIT\|BUYBACK" runs/nsmoke_v$n/logs/policy_agent_0.log | head -4 | cut -c1-160
done
