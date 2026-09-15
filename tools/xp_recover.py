#!/usr/bin/env python3
"""Rebuild xp/<tag>.json files from the notes of our experience requests ("[tag] <policy_ref> seat N ...").
usage: uv run python tools/xp_recover.py [--limit 200]
"""
import argparse, json, pathlib, re
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
ROOT = pathlib.Path(__file__).resolve().parent.parent

def dump(o):
    return o.model_dump() if hasattr(o, "model_dump") else o

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=200); a = ap.parse_args()
    found = {}
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        cursor = None; seen = 0
        while seen < a.limit:
            lst = dump(c.list_experience_requests(cursor=cursor) if cursor else c.list_experience_requests())
            entries = lst.get("entries") or []
            for e in entries:
                e = dump(e); seen += 1
                det = dump(c.get_experience_request(e["id"]))
                req = det.get("requested") or {}
                m = re.match(r"\[([\w.-]+)\] (\S+) seat (\d+)", req.get("notes") or "")
                if not m: continue
                tag, ref, seat = m.group(1), m.group(2), int(m.group(3))
                found.setdefault(tag, {"candidate": ref, "n": req.get("num_episodes"), "requests": []})["requests"].append({"id": e["id"], "seat": seat})
            cursor = lst.get("next_cursor")
            if not cursor or not entries: break
    for tag, d in found.items():
        path = ROOT / "xp" / f"{tag}.json"
        cur = json.load(open(path)) if path.exists() else {"candidate": d["candidate"], "n": d["n"], "requests": []}
        ids = {r["id"] for r in cur["requests"]}
        added = [r for r in d["requests"] if r["id"] not in ids]
        if added:
            cur["requests"] += added; json.dump(cur, open(path, "w"), indent=1)
        print(f"{tag}: {len(cur['requests'])} requests (+{len(added)}) seats {sorted(r['seat'] for r in cur['requests'])}")

if __name__ == "__main__":
    main()
