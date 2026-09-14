Task W6 (deliverable tools/replay_parse.py, pure Python 3 stdlib): parse Gods of the Arena replay files so we can study opponents.
Replay format source of truth: source/polyworld/examples/gods_of_the_arena/replays.nim (types ReplayHeader/Setup/ReplayAction/ReplayData,
the loadReplay/saveReplay procs, gameVersion constants) plus src/polyworld/tapes.nim if the byte encoding lives there.
Sample files: runs/hosted/khors-loss.replay (gzip-compressed, hosted, magic "POLYWORLDREPLAY") and runs/v5-vs-base/a_red/episode-0001/replay
(uncompressed local). Hosted replays are gzip; local ones are raw.
The script must:
 1. Decode header (game version, map hash/seed, setup: heroes with id/team/slot/lane/class), the game config JSON if embedded, and the action
    stream: per action tick, heroId, kind (walkTo x y / attackTarget id / buyItem id / useItem slot / cast ...), and the per-tick state hashes count.
 2. CLI: `python3 tools/replay_parse.py FILE --summary` prints version, ticks, heroes, action counts per hero and per kind;
    `--timeline HERO_ID [--every N]` prints that hero's walkTo targets and attackTarget ids over time (one line per N ticks);
    `--json` dumps everything to stdout as JSON.
 3. Validate against both sample files (local replay actions must match what policy/v5.bas would issue: walkTo/attackTarget/buyItem).
Do not modify anything except creating tools/replay_parse.py. Report the format you found (field layout) and the summary output for both samples.
You cannot run Docker but you CAN run python3 on the sample files.
