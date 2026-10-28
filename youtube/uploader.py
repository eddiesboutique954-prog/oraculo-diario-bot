"""
📤 Subidor Automático a YouTube
Usa YouTube Data API v3 para publicar videos automáticamente
"""

import os
import json
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import (YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET,
                    YOUTUBE_REFRESH_TOKEN, YOUTUBE_CONFIG, CHANNEL_NAME)


SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "youtube_token.json")


def get_youtube_service():
    """Crea y autentica el cliente de YouTube API"""
    creds = None

    # Intentar cargar token guardado
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
        creds = Credentials(
            token          = token_data.get("token"),
            refresh_token  = YOUTUBE_REFRESH_TOKEN or token_data.get("refresh_token"),
            token_uri      = "https://oauth2.googleapis.com/token",
            client_id      = YOUTUBE_CLIENT_ID or token_data.get("client_id"),
            client_secret  = YOUTUBE_CLIENT_SECRET or token_data.get("client_secret"),
            scopes         = SCOPES
        )

    # Refrescar token si es necesario
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save_token(creds)

    if not creds:
        raise ValueError(
            "❌ No hay credenciales de YouTube configuradas.\n"
            "   Ejecuta: python setup_youtube.py"
        )

    return build("youtube", "v3", credentials=creds)


def _save_token(creds: Credentials):
    """Guarda el token actualizado"""
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "token":         creds.token,
            "refresh_token": creds.refresh_token,
            "client_id":     creds.client_id,
            "client_secret": creds.client_secret,
        }, f, indent=2)


def upload_video_to_youtube(video_path: str, thumbnail_path: str,
                             script_data: dict) -> dict:
    """
    Sube un video a YouTube con todos sus metadatos SEO

    Args:
        video_path: ruta del video .mp4
        thumbnail_path: ruta de la miniatura .jpg
        script_data: datos del script con título, descripción, tags

    Returns:
        dict con id del video y url
    """
    lang        = script_data.get("lang", "es")
    title       = script_data.get("title", "Lectura de Tarot")
    description = script_data.get("description", "")
    tags_custom = script_data.get("tags", [])
    tags_base   = YOUTUBE_CONFIG["tags"][lang]
    all_tags    = list(set(tags_custom + tags_base))[:500]  # máx 500 tags

    # Garantizar que el título tenga el hashtag #shorts para indexación inmediata en el carrusel de Shorts
    clean_title = title.strip()
    if "#shorts" not in clean_title.lower():
        clean_title = f"{clean_title[:85]} #shorts"

    # Descripción enriquecida con #shorts en la primera línea
    full_description = f"""#shorts #tarot #tarotdiario #espiritualidad
{description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔮 {CHANNEL_NAME} — Guía Espiritual y Mensajes del Universo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ ¿QUIERES UNA LECTURA PERSONALIZADA DE TAROT PRIVADA? ✨
📲 WhatsApp: +57 305 338 9704
Escribe "SESIÓN" y agendamos tu lectura personalizada.

📌 Suscríbete para tu lectura diaria: no te pierdas los mensajes que el destino tiene para ti.
🔔 Activa la campanita para recibir cada revelación a tiempo.
✨ Deja tu comentario en este video para conectar con esta energía.

#tarot #lecturapersonalizada #tarotcolombia #esoterismo #espiritualidad #tarotdiario #arcanos #mensajedeluniverso #oraculo #shorts
"""

    print(f"\n📤 Subiendo Short a YouTube: {clean_title}")

    youtube = get_youtube_service()

    # Metadatos del video
    body = {
        "snippet": {
            "title":       clean_title[:100],
            "description": full_description[:5000],
            "tags":        all_tags,
            "categoryId":  YOUTUBE_CONFIG["category_id"],
            "defaultLanguage": lang,
        },
        "status": {
            "privacyStatus":  YOUTUBE_CONFIG["privacy"],
            "madeForKids":    YOUTUBE_CONFIG["made_for_kids"],
            "selfDeclaredMadeForKids": False,
        }
    }

    # Subir el video
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True,
                             mimetype="video/mp4")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
        notifySubscribers=True
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"   ⬆️  Subiendo... {progress}%", end="\r")

    video_id  = response["id"]
    video_url = f"https://www.youtube.com/shorts/{video_id}"
    print(f"   ✅ Short publicado en feed móvil: {video_url}")

    return {"id": video_id, "url": video_url, "title": clean_title}


def check_daily_quota() -> bool:
    """Verifica si quedan cuotas de la API de YouTube (10,000 unidades/día)"""
    # Cada upload cuesta ~1600 unidades
    # Con 4 videos/día = 6400 unidades (dentro del límite)
    return True  # Simplificado - en producción implementar contador
