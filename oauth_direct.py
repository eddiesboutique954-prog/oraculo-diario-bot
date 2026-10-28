import sys, os, json, base64
sys.stdout.reconfigure(encoding='utf-8')
from flask import Flask, request, redirect
import requests
from nacl import encoding, public

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(BASE_DIR, "youtube_token.json")

with open(CLIENT_SECRETS_FILE, "r") as f:
    cs = json.load(f)["installed"]

CLIENT_ID = cs["client_id"]
CLIENT_SECRET = cs["client_secret"]
REDIRECT_URI = "http://localhost:8080/"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = "eddiesboutique954-prog/oraculo-diario-bot"

def update_github_secret(secret_name: str, secret_value: str) -> bool:
    try:
        pk_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/secrets/public-key"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Python"}
        r = requests.get(pk_url, headers=headers)
        if r.status_code != 200:
            print("Error getting public key:", r.text)
            return False
        pk_data = r.json()
        key_id = pk_data["key_id"]
        public_key_b64 = pk_data["key"]

        # Encrypt with libsodium
        public_key_obj = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key_obj)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

        sec_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/secrets/{secret_name}"
        body = {"encrypted_value": encrypted_b64, "key_id": key_id}
        r_put = requests.put(sec_url, headers=headers, json=body)
        print(f"Secret {secret_name} updated: HTTP {r_put.status_code}")
        return r_put.status_code in [201, 204]
    except Exception as e:
        print(f"Exception updating secret: {e}")
        return False

def trigger_workflow() -> bool:
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/publish_shorts.yml/dispatches"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "User-Agent": "Python", "Accept": "application/vnd.github.v3+json"}
        r = requests.post(url, headers=headers, json={"ref": "main", "inputs": {"lang": "es"}})
        print(f"Workflow triggered: HTTP {r.status_code}")
        return r.status_code == 204
    except Exception as e:
        print(f"Exception triggering workflow: {e}")
        return False

@app.route("/")
def index():
    code = request.args.get("code")
    if not code:
        auth_url = (
            "https://accounts.google.com/o/oauth2/auth?"
            f"client_id={CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            "response_type=code&"
            "scope=https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube&"
            "access_type=offline&"
            "prompt=consent"
        )
        return redirect(auth_url)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    if r.status_code == 200:
        tokens = r.json()
        token_data = {
            "token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scopes": ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
        }
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2)

        print("\n🎉 [EXITO LOCAL] Token guardado en youtube_token.json")
        sec_ok = update_github_secret("YOUTUBE_TOKEN_JSON", json.dumps(token_data))
        wf_ok = trigger_workflow()

        return """
        <body style='background:#0f0c1b;color:#00ff88;font-family:sans-serif;text-align:center;padding:50px;'>
            <h1>🎉 ¡AUTORIZACIÓN COMPLETADA CON ÉXITO!</h1>
            <p style='color:#f0f0f0;font-size:18px;'>El nuevo token de YouTube ha sido capturado, guardado e instalado automáticamente en GitHub.</p>
            <p style='color:#ffd700;font-size:16px;'>🚀 Un nuevo video ya se está generando y subiendo a YouTube en este instante.</p>
            <p style='color:#a0a0a0;'>Ya puedes cerrar esta pestaña y volver al chat.</p>
        </body>
        """
    else:
        return f"Error canjeando código por token: {r.text}", 400

if __name__ == "__main__":
    print("🚀 Servidor de captura OAuth iniciado en http://localhost:8080/")
    app.run(host="localhost", port=8080)
