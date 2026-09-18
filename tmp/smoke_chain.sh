#!/bin/zsh
cd /Users/jordan/Desktop/Projects/johomax/gota
for n in ${=SMOKE_VERSIONS:-232 233 234 235}; do
  echo "=== v$n start $(date -u +%H:%M:%S)"
  rm -rf runs/smoke_v$n
  DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode ./coworld/cow_126f2fcb-80a0-4b6e-8166-eb6163576db5/coworld_manifest.json policy/v$n.bas policy/v$n.bas policy/v$n.bas policy/v$n.bas policy/v$n.bas policy/v228.bas policy/v228.bas policy/v228.bas policy/v228.bas policy/v228.bas --variant competition --timeout-seconds 1500 -o runs/smoke_v$n > runs/smoke_v$n.out 2>&1
  echo "exit $?  $(date -u +%H:%M:%S)"
  python3 -c "import json;r=json.load(open('runs/smoke_v$n/results.json'));print('result', r['outcome'], r['ticks'], r['scores'])" 2>&1
  grep -il "error\|fail\|compile" runs/smoke_v$n/player_status.json runs/smoke_v$n.out 2>/dev/null | head -3
  grep -i "compile\|unexpected\|error" runs/smoke_v$n/player_status.json 2>/dev/null | head -3
done
echo "=== ALL DONE $(date -u +%H:%M:%S)"
