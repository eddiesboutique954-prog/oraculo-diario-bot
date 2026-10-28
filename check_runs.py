import urllib.request
import json
import os

token = os.environ.get("GITHUB_TOKEN", "")
url = "https://api.github.com/repos/eddiesboutique954-prog/oraculo-diario-bot/actions/runs?per_page=10"
req = urllib.request.Request(url, headers={"Authorization": f"token {token}", "User-Agent": "Python"})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        for r in data.get("workflow_runs", []):
            name = r['name'].encode('ascii', 'ignore').decode()
            print(f"Run {r['id']} at {r['created_at']}: status={r['status']}, conclusion={r['conclusion']}")
except Exception as e:
    print("Error:", e)
