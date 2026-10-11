"""
Servidor local simple para capturar el código OAuth de YouTube sin errores de mismatch
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "youtube_token.json")

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            code = params["code"][0]
            with open(CLIENT_SECRETS_FILE, "r") as f:
                client_data = json.load(f)["installed"]

            # Intercambiar código por tokens
            token_url = "https://oauth2.googleapis.com/token"
            payload = {
                "code": code,
                "client_id": client_data["client_id"],
                "client_secret": client_data["client_secret"],
                "redirect_uri": "http://localhost:8080/",
                "grant_type": "authorization_code"
            }

            res = requests.post(token_url, data=payload)
            if res.status_code == 200:
                tokens = res.json()
                final_data = {
                    "token": tokens.get("access_token"),
                    "refresh_token": tokens.get("refresh_token"),
                    "client_id": client_data["client_id"],
                    "client_secret": client_data["client_secret"]
                }
                with open(TOKEN_FILE, "w") as f:
                    json.dump(final_data, f, indent=2)

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>EXITO: Tu canal de YouTube ha quedado vinculado correctamente. Ya puedes cerrar esta ventana.</h1>")
                print("\n[VINCULADO] Token de YouTube guardado exitosamente!")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error canjeando token: " + res.text.encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code received.")

def start_server():
    server = HTTPServer(("localhost", 8080), OAuthCallbackHandler)
    print("[SERVIDOR] Escuchando en http://localhost:8080...")
    server.handle_request()

if __name__ == "__main__":
    start_server()
