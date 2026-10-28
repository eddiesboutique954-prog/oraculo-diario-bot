import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES,
    redirect_uri="urn:ietf:wg:oauth:2.0:oob"  # Permite copiar y pegar el código directamente sin requerir puertos locales
)

# Si el redirect_uri oob no está permitido por Google, usar localhost con servidor temporal
flow_local = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES,
    redirect_uri="http://localhost:8080/"
)

auth_url, _ = flow_local.authorization_url(prompt='consent', access_type='offline')
print("\n🔗 ENLACE DE AUTORIZACIÓN DE GOOGLE:")
print(auth_url)
print("\n")
