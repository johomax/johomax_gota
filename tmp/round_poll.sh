#!/bin/zsh
cd /Users/jordan/Desktop/Projects/johomax/gota
want=$1; log=tmp/round$want.log
for i in $(seq 1 90); do
  r=$(uv run python tools/ladder.py 2>/dev/null | grep " Jordan " | awk '{print $5}')
  if [ -n "$r" ] && [ "$r" -ge "$want" ] 2>/dev/null; then break; fi
  sleep 120
done
echo "round poll $(date -u +%H:%M) jordan rounds=$r" > $log
uv run python tools/league_data.py --rounds 1 --out tmp/league_recent.json 2>/dev/null | tail -1 >> $log
python3 -c "
import json
for g in json.load(open('tmp/league_recent.json')):
    opp = g['players'][5] if g['team']==0 else g['players'][0]
    print(g['round'], 'seat', g['seat'], g['cls'], 'vs', opp, 'win', g['win'])" >> $log
uv run python tools/ladder.py 2>/dev/null | head -6 >> $log
echo "ROUND DONE" >> $log
