import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "youtube_token.json")

print("[AUTH] Iniciando servidor local en el puerto 8080...")
flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES,
    redirect_uri="http://localhost:8080/"
)

creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")

token_data = {
    "token": creds.token,
    "refresh_token": creds.refresh_token,
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "scopes": creds.scopes
}

with open(TOKEN_FILE, "w", encoding="utf-8") as f:
    json.dump(token_data, f, indent=2)

print("\n🎉 [EXITO TOTAL] ¡Nuevo token de YouTube capturado y guardado exitosamente!")
