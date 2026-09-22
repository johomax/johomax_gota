#!/bin/zsh
# usage: tmp/localab.sh FILE TAG [SEED] — 5x FILE (Red) vs 5x new baseline (Blue) on the new coworld; prints our five heroes' XP and the sum
cd /Users/jordan/Desktop/Projects/johomax/gota
M=./coworld/cow_27feb885-a1bf-48ce-8016-ec72a28c4bce/coworld_manifest.json; B=tmp/base_new.bas
F=$1; T=$2; S=${3:-2026}
rm -rf runs/ab_$T_$S
DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode $M $F $F $F $F $F $B $B $B $B $B --variant competition --timeout-seconds 1500 --seed $S -o runs/ab_${T}_$S > runs/ab_${T}_$S.out 2>&1
python3 -c "
import json; r=json.load(open('runs/ab_${T}_$S/results.json')); x=r['total_xp']; print('$T seed $S ticks', r['ticks'], r['outcome'], 'ours', x[:5], 'sum', sum(x[:5]), 'base', sum(x[5:]))" 2>&1 | tail -1
grep -h "BASIC error" runs/ab_${T}_$S/logs/policy_agent_0.log 2>/dev/null | head -1
