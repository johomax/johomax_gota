import json, time, subprocess, sys
from coworld.api_client import CoworldApiClient
from softmax.auth import get_api_server
files = sys.argv[1:] or ["xp/lgr4-v212.json", "xp/lgr4-v228.json"]
new = files[:1]
def dump(o): return o.model_dump() if hasattr(o, "model_dump") else o
t0 = time.time()
while time.time() - t0 < 100*60:
    done = {}
    with CoworldApiClient.from_login(server_url=get_api_server()) as c:
        for f in files:
            n = 0
            for r in json.load(open(f))["requests"]:
                det = dump(c.get_experience_request(r["id"]))
                n += sum(1 for ep in det.get("episodes", []) if ep.get("status") in ("completed", "failed", "cancelled"))
            done[f] = n
    print(time.strftime("%H:%M", time.gmtime()), done, flush=True)
    if all(v >= 144 for k, v in done.items() if k in new): break
    time.sleep(180)
print("LGR4 DONE", time.strftime("%H:%M", time.gmtime()), flush=True)
for tool in ("tools/lg_stats.py", "tools/lg_pair.py"):
    out = subprocess.run(["uv", "run", "python", tool] + (new if tool.endswith("lg_stats.py") else files), capture_output=True, text=True)
    print("=== " + tool); print("\n".join(out.stdout.strip().splitlines()[-40:])); print(out.stderr[-500:], flush=True)
