# usage: uv run python tmp/wait_batches.py xp/a.json [...] — exits 0 when at least 70% of the episodes in these files are completed (polls every 60 s, up to 25 min)
import json, sys, time
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
files = sys.argv[1:]
with CoworldApiClient.from_login(server_url=get_api_server()) as c:
    for _ in range(25):
        done = 0; total = 0
        for path in files:
            for r in json.load(open(path))["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                total += det.get("episode_count") or 0; done += det.get("completed_count") or 0
        if total and done >= 0.7 * total:
            print(f"batches ready: {done}/{total} episodes completed"); sys.exit(0)
        time.sleep(60)
print(f"timeout: {done}/{total}")
