"""
Receptor manual de código OAuth para YouTube
"""

import sys
import os
import json

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "youtube_token.json")

def generate_link():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        redirect_uri="http://localhost:8080/"
    )
    url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    print(f"LINK_URL: {url}")

if __name__ == "__main__":
    generate_link()
