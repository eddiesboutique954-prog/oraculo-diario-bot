"""
🔑 Asistente de Configuración de YouTube OAuth2 (Flujo Directo y Seguro)
"""

import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Deshabilitar verificación estricta de state para evitar errores de sesión cruzada
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "youtube_token.json")

def setup_youtube():
    print("=" * 60)
    print("[YOUTUBE SETUP] AUTORIZACION OFICIAL")
    print("=" * 60)

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        redirect_uri="http://localhost:8080/"
    )
    
    # Iniciar servidor local
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

    print("\n[EXITO TOTAL] ¡Token de YouTube generado y guardado exitosamente!")

if __name__ == "__main__":
    setup_youtube()
