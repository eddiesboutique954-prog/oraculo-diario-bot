import urllib.request
import json
import base64
import os
from nacl import encoding, public

token = os.environ.get("GITHUB_TOKEN", "")
repo = "eddiesboutique954-prog/oraculo-diario-bot"

def get_public_key():
    url = f"https://api.github.com/repos/{repo}/actions/secrets/public-key"
    req = urllib.request.Request(url, headers={"Authorization": f"token {token}", "User-Agent": "Python"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

try:
    pk = get_public_key()
    print("Public key ID:", pk["key_id"])
except Exception as e:
    print("Error getting public key:", e)
