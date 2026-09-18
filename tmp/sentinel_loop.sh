#!/bin/zsh
# usage: tmp/sentinel_loop.sh VERSION  — queues a sentinel (n=2 vs the current field labels) every 10 minutes for six hours
cd /Users/jordan/Desktop/Projects/johomax/gota
V=$1
for i in $(seq 1 36); do
  T=$(date -u +%H%M)
  uv run python tools/xp_league.py homo Jordan-ply_bcb80069-fb0c-4ba5-a45c-06b647870aeb:v$V --opp aaron-gota-ir-j254-warning100-0916-aaron:v1 --opp aaron-gota-ir-j254-warning100-0916:v1 --opp aaron-gota-ir-middle-rush-blue_three-0916-aaron:v1 --opp aaron-gota-ir-middle-rush-blue_three-0916:v1 --opp aaron-gota-ir-coordinated-support-anchor-0916:v1 --opp aaron-gota-ir-perimeter-blue_repair-0916-aaron:v1 --opp black-kite:v16 --opp red-kite:v34 --opp gota-g003:v2 --opp relh-gods-of-the-arena:v154 --opp khors:v1 --opp macromackie-gota:v4 --opp richard-gods-of-the-arena:v78 --opp gota-g002:v1 --opp gota-vanguard-rally-hold:v1 --opp james-botts-gota:v13 --opp nancy-goa:v2 -n 2 --tag roll-v$V-$T >> tmp/sentinel_loop.log 2>&1
  echo "$(date -u +%H:%M) queued roll-v$V-$T" >> tmp/sentinel_loop.log
  sleep 600
done
echo "sentinel loop done $(date -u +%H:%M)" >> tmp/sentinel_loop.log
