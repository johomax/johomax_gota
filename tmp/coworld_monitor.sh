#!/bin/zsh
cd /Users/jordan/Desktop/Projects/johomax/gota
for i in $(seq 1 72); do
  echo "== $(date -u +%H:%M)" >> tmp/monitor17.log
  uv run python tools/coworld_check.py --expect cow_e5445477-d55e-432d-ac38-bd1eae66e6d3 >> tmp/monitor17.log 2>&1
  sleep 600
done
