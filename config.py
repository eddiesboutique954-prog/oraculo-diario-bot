"""
╔══════════════════════════════════════════════════════╗
║     🃏 TAROT YOUTUBE BOT - CONFIGURACIÓN CENTRAL     ║
║         Canal Bilingüe Español / Inglés              ║
╚══════════════════════════════════════════════════════╝
"""

import os

# ─────────────────────────────────────────
#  🔑 API KEYS
# ─────────────────────────────────────────
ANTHROPIC_API_KEY    = os.getenv("ANTHROPIC_API_KEY", "")
OPENROUTER_API_KEY   = os.getenv("OPENROUTER_API_KEY", "")

YOUTUBE_CLIENT_ID    = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET= os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REFRESH_TOKEN= os.getenv("YOUTUBE_REFRESH_TOKEN", "")

# ─────────────────────────────────────────
#  📺 CONFIGURACIÓN DEL CANAL
# ─────────────────────────────────────────
CHANNEL_NAME = "Tarot Místico"          # Nombre de tu canal
ACTIVE_LANGUAGES = ["es", "en", "pt", "fr", "it", "de"]

LANGUAGE_INFO = {
    "es": {
        "name": "Español", "native": "Español",
        "badge": "MENSAJE URGENTE", "card_label": "CARTA",
        "cta": "Comenta 'HECHO ESTÁ' para recibir esta bendición",
        "voice": "es-PE-CamilaNeural", "gtts": "es"
    },
    "en": {
        "name": "Inglés", "native": "English",
        "badge": "URGENT MESSAGE", "card_label": "CARD",
        "cta": "Comment 'CLAIM' to manifest this blessing",
        "voice": "en-US-JennyNeural", "gtts": "en"
    },
    "pt": {
        "name": "Portugués", "native": "Português",
        "badge": "MENSAGEM URGENTE", "card_label": "CARTA",
        "cta": "Comente 'ESTÁ FEITO' para selar esta energia",
        "voice": "pt-BR-FranciscaNeural", "gtts": "pt"
    },
    "fr": {
        "name": "Francés", "native": "Français",
        "badge": "MESSAGE URGENT", "card_label": "CARTE",
        "cta": "Commentez 'C'EST FAIT' pour réclamer cette bénédiction",
        "voice": "fr-FR-DeniseNeural", "gtts": "fr"
    },
    "it": {
        "name": "Italiano", "native": "Italiano",
        "badge": "MESSAGGIO URGENTE", "card_label": "CARTA",
        "cta": "Scrivi 'È FATTO' per accogliere questo messaggio",
        "voice": "it-IT-ElsaNeural", "gtts": "it"
    },
    "de": {
        "name": "Alemán", "native": "Deutsch",
        "badge": "DRINGENDE BOTSCHAFT", "card_label": "KARTE",
        "cta": "Kommentiere 'ES IST VOLLBRACHT' um diesen Segen anzunehmen",
        "voice": "de-DE-KatjaNeural", "gtts": "de"
    }
}

# ─────────────────────────────────────────
#  🎬 CONFIGURACIÓN DE VIDEO
# ─────────────────────────────────────────
VIDEO_CONFIG = {
    "width":     1080,
    "height":    1920,          # Formato Vertical (Shorts / Reels 9:16)
    "fps":       30,
    "duration":  28,            # Duración óptima para Shorts y Reels (24-28s)
    "format":    "mp4",
}

IMAGE_DISPLAY_TIME = 5

# ─────────────────────────────────────────
#  🎙️ CONFIGURACIÓN DE VOZ (gTTS & Edge-TTS)
# ─────────────────────────────────────────
VOICE_CONFIG = {
    "es": "es",
    "en": "en",
    "pt": "pt",
    "fr": "fr",
    "it": "it",
    "de": "de",
    "rate": "+0%",
    "pitch": "+0Hz",
}

# ─────────────────────────────────────────
#  🃏 TEMAS DE TAROT (Rotación automática)
# ─────────────────────────────────────────
TAROT_TOPICS = {
    "es": [
        "Lectura de tarot para hoy - mensaje urgente de las cartas",
        "El arcano mayor que te define esta semana",
        "Las 3 cartas que revelan tu destino en el amor",
        "Mensaje del universo para ti hoy - tarot diario",
        "La carta que predice lo que viene en los próximos días",
        "Ritual de luna nueva - qué revelan las cartas para ti",
        "Los arcanos menores hablan: abundancia o transformación",
        "Tu guía espiritual envía un mensaje a través del tarot",
        "Las cartas revelan lo que alguien siente por ti ahora mismo",
        "El tarot y los planetas: tu energía esta semana",
    ],
    "en": [
        "Today's tarot reading - urgent message from the cards",
        "The major arcana that defines your week ahead",
        "3 cards revealing your love destiny right now",
        "Universe message for you today - daily tarot",
        "The card predicting what's coming in the next few days",
        "New moon ritual - what the cards reveal for you",
        "Minor arcana speaks: abundance or transformation ahead",
        "Your spirit guide sends a message through tarot today",
        "The cards reveal what someone truly feels about you",
        "Tarot and the planets: your energy this week",
    ]
}

# ─────────────────────────────────────────
#  🖼️ ESTILO DE IMÁGENES
# ─────────────────────────────────────────
IMAGE_STYLE = "mystical tarot card art, dark fantasy, esoteric symbols, glowing golden energy, deep purple night sky, cinematic 8k detailed"

# ─────────────────────────────────────────
#  🖼️ MINIATURAS
# ─────────────────────────────────────────
THUMBNAIL_CONFIG = {
    "width":  1280,
    "height": 720,
    "style": {
        "es": {
            "bg_color":    (15, 5, 35),
            "text_color":  (255, 215, 0),
            "accent_color":(180, 0, 255),
            "emoji":       "🔮",
        },
        "en": {
            "bg_color":    (10, 0, 30),
            "text_color":  (255, 215, 0),
            "accent_color":(200, 50, 255),
            "emoji":       "🃏",
        }
    }
}

# ─────────────────────────────────────────
#  📤 CONFIGURACIÓN DE YOUTUBE
# ─────────────────────────────────────────
YOUTUBE_CONFIG = {
    "category_id": "22",
    "privacy":     "public",
    "made_for_kids": False,
    "tags": {
        "es": ["tarot", "lectura de tarot", "tarot diario", "esoterismo", "arcanos", "tarot hoy", "espiritualidad", "predicciones", "shorts", "reels"],
        "en": ["tarot", "tarot reading", "daily tarot", "tarot cards", "esoteric", "spirituality", "tarot today", "predictions", "shorts", "reels"],
        "pt": ["tarot", "leitura de tarot", "tarot diario", "esoterismo", "arcanos", "espiritualidade", "previsoes", "shorts", "reels"],
        "fr": ["tarot", "tirage de tarot", "tarot du jour", "esoterisme", "spiritualite", "voyance", "guidance", "shorts", "reels"],
        "it": ["tarocchi", "lettura tarocchi", "tarocchi del giorno", "esoterismo", "spiritualita", "oracolo", "shorts", "reels"],
        "de": ["tarot", "tarot tageskarte", "kartenlegen", "esoterik", "spiritualitat", "orakel", "shorts", "reels"],
    }
}

# ─────────────────────────────────────────
#  📁 RUTAS DEL PROYECTO
# ─────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR    = os.path.join(BASE_DIR, "output")
ASSETS_DIR    = os.path.join(BASE_DIR, "assets")
TEMP_DIR      = os.path.join(OUTPUT_DIR, "temp")

for d in [OUTPUT_DIR, ASSETS_DIR, TEMP_DIR]:
    os.makedirs(d, exist_ok=True)
