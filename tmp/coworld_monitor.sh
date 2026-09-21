#!/bin/zsh
cd /Users/jordan/Desktop/Projects/johomax/gota
for i in $(seq 1 72); do
  echo "== $(date -u +%H:%M)" >> tmp/monitor17.log
  uv run python tools/coworld_check.py --expect cow_126f2fcb-80a0-4b6e-8166-eb6163576db5 >> tmp/monitor17.log 2>&1
  sleep 600
done
