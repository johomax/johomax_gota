#!/bin/zsh
# usage: tmp/localab.sh FILE TAG — two local episodes (seeds 2026, 2027) of 5x FILE (Red) vs 5x new baseline (Blue); prints our five heroes' XP per episode and the sum
cd /Users/jordan/Desktop/Projects/johomax/gota
M=./coworld/cow_27feb885-a1bf-48ce-8016-ec72a28c4bce/coworld_manifest.json; B=tmp/base_new.bas
F=$1; T=$2
if [ ! -f runs/ab_$T/episode-0002/results.json ]; then
  rm -rf runs/ab_$T
  DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode $M $F $F $F $F $F $B $B $B $B $B --variant competition --timeout-seconds 1500 -n 2 -o runs/ab_$T > runs/ab_$T.out 2>&1
fi
python3 -c "
import json
tot=0
for e in ('episode-0001','episode-0002'):
    r=json.load(open('runs/ab_$T/'+e+'/results.json')); x=r['total_xp']; tot+=sum(x[:5]); print('$T', e, 'seed', r.get('seed'), 'ticks', r['ticks'], r['outcome'], 'ours', x[:5], 'sum', sum(x[:5]))
print('$T TOTAL', tot)" 2>&1 | tail -3
grep -h "BASIC error" runs/ab_$T/episode-0001/logs/policy_agent_0.log 2>/dev/null | head -1
