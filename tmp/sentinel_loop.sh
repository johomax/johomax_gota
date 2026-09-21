#!/bin/zsh
# usage: tmp/sentinel_loop.sh VERSION  — every 10 minutes for six hours, queue an n=2 sentinel vs the current field labels (tmp/field_labels.json + red-kite, g003)
cd /Users/jordan/Desktop/Projects/johomax/gota
V=$1
for i in $(seq 1 36); do
  T=$(date -u +%H%M)
  uv run python tools/field_watch.py --rounds 10 >> tmp/sentinel_loop.log 2>&1
  OPPS=$(python3 -c "import json; ls=set(json.load(open('tmp/field_labels.json'))); ls|={'red-kite:v34','gota-g003:v2'}; print(' '.join('--opp '+l for l in sorted(ls)))")
  uv run python tools/xp_league.py homo Jordan-ply_bcb80069-fb0c-4ba5-a45c-06b647870aeb:v$V ${=OPPS} -n 2 --tag roll-v$V-$T >> tmp/sentinel_loop.log 2>&1
  echo "$(date -u +%H:%M) queued roll-v$V-$T ($OPPS)" >> tmp/sentinel_loop.log
  sleep 600
done
echo "sentinel loop v$V done $(date -u +%H:%M)" >> tmp/sentinel_loop.log
