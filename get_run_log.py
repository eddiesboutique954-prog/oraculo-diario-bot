import urllib.request
import json
import zipfile
import io
import sys
import os

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

token = os.environ.get("GITHUB_TOKEN", "")
run_id = "40626380252"
url = f"https://api.github.com/repos/eddiesboutique954-prog/oraculo-diario-bot/actions/runs/{run_id}/jobs"
req = urllib.request.Request(url, headers={"Authorization": f"token {token}", "User-Agent": "Python"})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        for j in data.get("jobs", []):
            print(f"Job {j['id']} ({j['name']}): status={j['status']}, conclusion={j['conclusion']}")
            for s in j.get("steps", []):
                print(f"  Step '{s['name']}': status={s['status']}, conclusion={s['conclusion']}")

    log_url = f"https://api.github.com/repos/eddiesboutique954-prog/oraculo-diario-bot/actions/runs/{run_id}/logs"
    req_log = urllib.request.Request(log_url, headers={"Authorization": f"token {token}", "User-Agent": "Python"})
    with urllib.request.urlopen(req_log) as resp_log:
        content = resp_log.read()
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            for name in z.namelist():
                print(f"File in zip: {name}")
                if "Generar y publicar" in name or "publish" in name.lower() or "5_" in name:
                    lines = z.read(name).decode("utf-8", errors="replace").splitlines()
                    print(f"\n--- LOG FROM {name} (last 50 lines) ---")
                    for line in lines[-50:]:
                        print(line)
except Exception as e:
    print("Error:", e)
