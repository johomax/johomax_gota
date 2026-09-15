#!/usr/bin/env python3
"""Read Gods of the Arena replays (Python 3 stdlib only).

Usage:
    python3 tools/replay_parse.py FILE --summary
    python3 tools/replay_parse.py FILE --timeline 100 --every 240
    python3 tools/replay_parse.py FILE --json

Layout from examples/gods_of_the_arena/replays.nim and src/polyworld/
{tapes,configs,metrics}.nim in source/polyworld (275ba23):
  Optional gzip wrapper; all numbers below are little-endian.
  File: b"POLYWORLDREPLAY", u16 fileVersion, u16 gameVersion,
        u16 gameNameBytes, gameName bytes (no terminator).
  Tape header: u16 formatVersion, u16 gameVersion, i64 createdUnixMs.
  Setup: i32 mapSeed, u64 mapHash, u16 tickRate, u16 gridTiles,
         u32 spawnIntervalTicks, u32 maximumTicks, seq[Hero].
  Hero (8 bytes): i32 id, u8 team, u8 slot, u8 lane, u8 class.
  Config: seq[Player{name: string}], then i32 seed, maxTicks,
          spawnIntervalTicks, playerSlot, dayCount; mapPreset for v26/v28.
  Map preset: i64 mapSize (v28 only), seed, lakeCrossings, jungleRoads;
              nine f32 controls listed in MAP_FLOATS; u8 campsTouchRoads.
  Actions: seq[Action], each 20 bytes: u32 tick, i32 heroId, u8 kind,
           3 padding bytes, i32 first, i32 second.
  Hashes: seq[u64], one hash per completed tick (index 0 is tick 1).
  Metrics (v18+): i32 tickRate, i32 interval, seq[Frame], seq[Row] final.
    Frame: i32 tick, seq[Row]. Row: i32 cpu (plus i32 apm in v18 only).

Flatty's 64-bit layout prefixes strings/sequences with an i64 length.
Objects serialize fieldwise, but POD sequences copy native records, including
the action padding. Both supplied samples use this little-endian 64-bit layout.
Supported game versions are those accepted by decodeReplay in replays.nim;
unknown versions are rejected. Config is typed binary, not embedded JSON.
JSON output preserves raw action payloads alongside their decoded meanings.
Commands include unsuccessful attempts; this parser does not simulate state
or verify the stored hashes against the engine.
"""

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import struct
import sys
import zlib


MAGIC = b"POLYWORLDREPLAY"
GAME = "gods_of_the_arena"
GAME_VERSIONS = {16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30}
MAX_BYTES = 64 * 1024 * 1024
MAX_ACTIONS = 10_000_000
MAX_HASHES = 100_000_000
CLASSES = (
    "VanguardKnight", "Ranger", "Arcanist", "DruidWarden", "DemonHunter",
    "DeathKnight", "Crossbowman", "Lich", "Warlock", "Berserker",
)
KINDS = {
    1: "walkTo", 2: "attackTarget", 3: "buyItem", 4: "useItem",
    5: "attackMove", 6: "castTarget", 7: "castTarget", 8: "castTarget",
    9: "castTarget", 10: "castPoint", 11: "castPoint", 12: "castPoint",
    13: "castPoint", 14: "manualSpells",
}
MAP_FLOATS = (
    "highSize castleSize roadWidth roadWobble lakeWidth lakeWobble "
    "campRadius campScatter stemLength"
)


class ReplayError(ValueError):
    """Invalid, truncated, or unsupported replay."""


class Reader:
    def __init__(self, data):
        self.data = memoryview(data)
        self.offset = 0

    def take(self, size, label):
        if size < 0 or size > len(self.data) - self.offset:
            raise ReplayError(f"truncated {label} at byte {self.offset}")
        start = self.offset
        self.offset += size
        return self.data[start:self.offset]

    def unpack(self, fmt, label):
        layout = struct.Struct("<" + fmt)
        return layout.unpack(self.take(layout.size, label))

    def number(self, fmt, label):
        return self.unpack(fmt, label)[0]

    def record(self, fmt, fields):
        return dict(zip(fields.split(), self.unpack(fmt, fields)))

    def count(self, label, item_size, limit):
        count = self.number("q", label + " length")
        if not 0 <= count <= limit:
            raise ReplayError(f"invalid {label} length {count}")
        if count * item_size > len(self.data) - self.offset:
            raise ReplayError(f"truncated {label} at byte {self.offset}")
        return count

    def string(self, label):
        size = self.count(label, 1, 4096)
        try:
            return self.take(size, label).tobytes().decode("utf-8")
        except UnicodeDecodeError as error:
            raise ReplayError(f"invalid UTF-8 in {label}") from error


def read_config(reader, version):
    players = [
        {"name": reader.string("player name")}
        for _ in range(reader.count("players", 8, 256))
    ]
    config = {"players": players}
    config.update(reader.record(
        "iiiii", "seed maxTicks spawnIntervalTicks playerSlot dayCount"
    ))
    if version >= 26:
        integers = "seed lakeCrossings jungleRoads"
        if version >= 28:
            integers = "mapSize " + integers
        preset = reader.record("q" * len(integers.split()), integers)
        preset.update(reader.record("9f", MAP_FLOATS))
        flag = reader.number("B", "campsTouchRoads")
        if flag not in (0, 1):
            raise ReplayError("invalid campsTouchRoads boolean")
        preset["campsTouchRoads"] = bool(flag)
        config["mapPreset"] = preset
    return config


def read_action(reader, version):
    action = reader.record("IiB3xii", "tick heroId kindId first second")
    kind, first, second = action["kindId"], action["first"], action["second"]
    if kind not in KINDS or (version <= 20 and kind >= 6):
        raise ReplayError(f"invalid action kind {kind} for game version {version}")
    action["kind"] = KINDS[kind]
    if kind in (1, 5) or 10 <= kind <= 13:
        action.update(x=first, y=second)
    elif kind == 2 or 6 <= kind <= 9:
        action["targetId"] = first
    elif kind == 3:
        action["itemId"] = first
    elif kind == 4:
        action["slot"] = first
    elif kind == 14:
        action["enabled"] = first != 0
    if 6 <= kind <= 13:
        action["slot"] = kind - (6 if kind < 10 else 10)
    return action


def read_metrics(reader, version):
    metrics = reader.record("ii", "tickRate interval")
    row_format, row_fields = ("ii", "cpu apm") if version == 18 else ("i", "cpu")

    def rows():
        return [
            reader.record(row_format, row_fields)
            for _ in range(reader.count("metric rows", 4 * len(row_format), 256))
        ]

    metrics["frames"] = [
        {"tick": reader.number("i", "metric tick"), "rows": rows()}
        for _ in range(reader.count("metric frames", 12, 4096))
    ]
    metrics["final"] = rows()
    return metrics


def decode_replay(data):
    """Decode an uncompressed payload to JSON-compatible Python values."""
    if len(data) > MAX_BYTES:
        raise ReplayError("replay exceeds the 64 MiB file size limit")
    reader = Reader(data)
    if reader.take(len(MAGIC), "magic") != MAGIC:
        raise ReplayError("not a Polyworld replay file")
    file_version, version, name_size = reader.unpack("HHH", "file header")
    if file_version != 1:
        raise ReplayError(f"unsupported file format version {file_version}")
    if version not in GAME_VERSIONS:
        raise ReplayError(f"unsupported game version {version}")
    if name_size != len(GAME) or reader.take(name_size, "game name") != GAME.encode():
        raise ReplayError("replay is not for gods_of_the_arena")
    header = reader.record("HHq", "formatVersion gameVersion createdUnixMs")
    if header["formatVersion"] != 5:
        raise ReplayError(f"unsupported tape format version {header['formatVersion']}")
    if header["gameVersion"] != version:
        raise ReplayError("file and tape game versions disagree")
    setup = reader.record(
        "iQHHII", "mapSeed mapHash tickRate gridTiles spawnIntervalTicks maximumTicks"
    )
    heroes = [
        reader.record("iBBBB", "id team slot lane class")
        for _ in range(reader.count("heroes", 8, 256))
    ]
    setup["heroes"] = heroes
    header["setup"] = setup
    hero_ids = {hero["id"] for hero in heroes}
    if not heroes or len(hero_ids) != len(heroes):
        raise ReplayError("missing heroes or duplicate hero IDs")
    if any(h["team"] > 1 or h["lane"] > 2 or h["class"] >= len(CLASSES) for h in heroes):
        raise ReplayError("invalid hero metadata")
    if (setup["tickRate"] != 24 or not setup["mapHash"]
            or not 0 < setup["maximumTicks"] <= MAX_HASHES
            or not 0 < setup["spawnIntervalTicks"] <= 2**31 - 1):
        raise ReplayError("invalid simulation setup")

    config = read_config(reader, version)
    map_size = config.get("mapPreset", {}).get("mapSize", 128)
    if (config["seed"] != setup["mapSeed"]
            or config["maxTicks"] != setup["maximumTicks"]
            or config["spawnIntervalTicks"] != setup["spawnIntervalTicks"]
            or map_size != setup["gridTiles"]):
        raise ReplayError("config and simulation setup disagree")
    if (len(config["players"]) != len(CLASSES) or config["dayCount"] < 0
            or not 0 <= config["playerSlot"] <= len(CLASSES)):
        raise ReplayError("invalid player config")

    actions = []
    last_tick = 0
    for _ in range(reader.count("actions", 20, MAX_ACTIONS)):
        action = read_action(reader, version)
        if action["heroId"] not in hero_ids:
            raise ReplayError(f"action references unknown hero {action['heroId']}")
        if action["tick"] < last_tick:
            raise ReplayError("actions move backward in time")
        last_tick = action["tick"]
        actions.append(action)
    count = reader.count("hashes", 8, min(MAX_HASHES, setup["maximumTicks"]))
    hashes = [value[0] for value in struct.iter_unpack("<Q", reader.take(count * 8, "hashes"))]
    if last_tick > count:
        raise ReplayError("action exceeds the recorded duration")
    metrics = read_metrics(reader, version) if version >= 18 else None
    if reader.offset != len(data):
        raise ReplayError(f"{len(data) - reader.offset} unexpected trailing bytes")
    return {
        "fileHeader": {"formatVersion": file_version, "game": GAME, "gameVersion": version},
        "header": header, "config": config, "actions": actions,
        "hashes": hashes, "hashCount": count, "ticks": count, "metrics": metrics,
    }


def load_replay(path):
    """Read raw or gzip files, detecting compression from the bytes."""
    with Path(path).open("rb") as stream:
        compressed = stream.read(2) == b"\x1f\x8b"
        stream.seek(0)
        if compressed:
            with gzip.GzipFile(fileobj=stream) as unpacked:
                data = unpacked.read(MAX_BYTES + 1)
        else:
            data = stream.read(MAX_BYTES + 1)
    replay = decode_replay(data)
    replay["compression"] = "gzip" if compressed else "none"
    return replay


def print_summary(replay):
    header, file_header = replay["header"], replay["fileHeader"]
    setup = header["setup"]
    counts = Counter(action["kind"] for action in replay["actions"])
    kinds = list(dict.fromkeys(kind for kind in KINDS.values() if kind in counts))
    per_hero = {hero["id"]: Counter() for hero in setup["heroes"]}
    for action in replay["actions"]:
        per_hero[action["heroId"]][action["kind"]] += 1
    print(f"Version: game={header['gameVersion']} tape={header['formatVersion']} "
          f"file={file_header['formatVersion']} compression={replay['compression']}")
    print(f"Ticks: {replay['ticks']} / {setup['maximumTicks']} "
          f"({setup['tickRate']} Hz); state hashes: {replay['hashCount']}")
    print(f"Map: seed={setup['mapSeed']} hash={setup['mapHash']:016X} "
          f"grid={setup['gridTiles']}")
    print(f"Heroes: {len(setup['heroes'])}; actions: {len(replay['actions'])}")
    print("Kinds: " + (", ".join(f"{kind}={counts[kind]}" for kind in kinds) or "none"))
    rows = [["id", "team", "slot", "lane", "class", "actions"] + kinds]
    for hero in setup["heroes"]:
        counts = per_hero[hero["id"]]
        rows.append([
            hero["id"], hero["team"], hero["slot"], hero["lane"],
            f"{hero['class']}:{CLASSES[hero['class']]}", sum(counts.values()),
        ] + [counts[kind] for kind in kinds])
    widths = [max(len(str(value)) for value in column) for column in zip(*rows)]
    for row in rows:
        print("  ".join(str(value).ljust(width) for value, width in zip(row, widths)).rstrip())


def print_timeline(replay, hero_id, every=1):
    """Sample the last recorded movement/attack command, not simulated state."""
    if every < 1:
        raise ReplayError("--every must be positive")
    if hero_id not in {hero["id"] for hero in replay["header"]["setup"]["heroes"]}:
        raise ReplayError(f"unknown hero ID {hero_id}")
    actions = iter(action for action in replay["actions"]
                   if action["heroId"] == hero_id and action["kindId"] in (1, 2))
    upcoming = next(actions, None)
    current = None
    for tick in range(1, replay["ticks"] + 1, every):
        while upcoming is not None and upcoming["tick"] <= tick:
            current = upcoming
            upcoming = next(actions, None)
        if current is None:
            command = "no walkTo/attackTarget yet"
        elif current["kind"] == "walkTo":
            command = f"walkTo x={current['x']} y={current['y']} (issued={current['tick']})"
        else:
            command = f"attackTarget id={current['targetId']} (issued={current['tick']})"
        print(f"tick={tick} heroId={hero_id} {command}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", type=Path, help="raw or gzip replay")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--summary", action="store_true", help="print summary (default)")
    mode.add_argument("--timeline", type=int, metavar="HERO_ID", help="sample walkTo/attackTarget commands")
    mode.add_argument("--json", action="store_true", help="dump the complete decoded replay")
    parser.add_argument("--every", type=int, metavar="N",
                        help="timeline at ticks 1, 1+N, ...; carries last command (default: 1)")
    args = parser.parse_args(argv)
    if args.every is not None and (args.timeline is None or args.every < 1):
        parser.error("--every requires --timeline and a positive integer")
    try:
        replay = load_replay(args.file)
        if args.json:
            json.dump(replay, sys.stdout, indent=2, allow_nan=False)
            print()
        elif args.timeline is not None:
            print_timeline(replay, args.timeline, args.every or 1)
        else:
            print_summary(replay)
    except (OSError, EOFError, ValueError, zlib.error) as error:
        parser.exit(2, f"{parser.prog}: error: {error}\n")


if __name__ == "__main__":
    main()
