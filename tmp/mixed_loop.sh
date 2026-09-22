#!/bin/zsh
# usage: tmp/mixed_loop.sh VERSION — every 15 minutes for six hours queue a league-format probe (our policy in each of the ten seats, n=2, random champions)
cd /Users/jordan/Desktop/Projects/johomax/gota
V=$1
for i in $(seq 1 24); do
  T=$(date -u +%H%M)
  uv run python tools/xp_mixed.py create Jordan-ply_bcb80069-fb0c-4ba5-a45c-06b647870aeb:v$V --seats 0-9 -n 2 --tag mxl-v$V-$T >> tmp/mixed_loop.log 2>&1
  echo "$(date -u +%H:%M) queued mxl-v$V-$T" >> tmp/mixed_loop.log
  sleep 900
done
echo "mixed loop v$V done $(date -u +%H:%M)" >> tmp/mixed_loop.log
