#!/bin/zsh
cd /Users/jordan/Desktop/Projects/johomax/gota
M=./coworld/cow_27feb885-a1bf-48ce-8016-ec72a28c4bce/coworld_manifest.json
B=tmp/base_new.bas
run() { name=$1; shift; rm -rf runs/$name; echo "=== $name start $(date -u +%H:%M:%S)"; DOCKER_DEFAULT_PLATFORM=linux/amd64 uv run coworld run-episode $M "$@" --variant competition --timeout-seconds 1500 -o runs/$name > runs/$name.out 2>&1; echo "exit $? $(date -u +%H:%M:%S)"; python3 -c "import json;r=json.load(open('runs/$name/results.json'));print('result', r.get('outcome'), r.get('ticks'), r.get('scores'))" 2>&1; grep -i "compile\|unexpected\|error" runs/$name/player_status.json 2>/dev/null | head -3; }
run new_base $B $B $B $B $B $B $B $B $B $B
run new_v284 policy/v284.bas policy/v284.bas policy/v284.bas policy/v284.bas policy/v284.bas $B $B $B $B $B
echo "=== ALL DONE $(date -u +%H:%M:%S)"
