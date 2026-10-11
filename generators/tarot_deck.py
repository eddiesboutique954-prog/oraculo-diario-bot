"""
🃏 Gestor de Cartas Reales del Tarot Rider-Waite (Public Domain)
Descarga y almacena en caché local las 78 cartas reales en alta resolución.
"""

import os
import requests

CARDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "tarot_deck")
os.makedirs(CARDS_DIR, exist_ok=True)

# Mapeo de nombres en español a los archivos reales de la baraja Rider-Waite
CARD_FILES_MAP = {
    "El Loco": "m00.jpg",
    "El Mago": "m01.jpg",
    "La Sacerdotisa": "m02.jpg",
    "La Emperatriz": "m03.jpg",
    "El Emperador": "m04.jpg",
    "El Sumo Sacerdote": "m05.jpg",
    "Los Enamorados": "m06.jpg",
    "El Carro": "m07.jpg",
    "La Fuerza": "m08.jpg",
    "El Ermitaño": "m09.jpg",
    "El Ermitano": "m09.jpg",
    "La Rueda de la Fortuna": "m10.jpg",
    "La Justicia": "m11.jpg",
    "El Colgado": "m12.jpg",
    "La Muerte": "m13.jpg",
    "La Templanza": "m14.jpg",
    "El Diablo": "m15.jpg",
    "La Torre": "m16.jpg",
    "La Estrella": "m17.jpg",
    "La Luna": "m18.jpg",
    "El Sol": "m19.jpg",
    "El Juicio": "m20.jpg",
    "El Mundo": "m21.jpg",
    # Mapeo en Inglés
    "The Fool": "m00.jpg",
    "The Magician": "m01.jpg",
    "The High Priestess": "m02.jpg",
    "The Empress": "m03.jpg",
    "The Emperor": "m04.jpg",
    "The Hierophant": "m05.jpg",
    "The Lovers": "m06.jpg",
    "The Chariot": "m07.jpg",
    "Strength": "m08.jpg",
    "The Hermit": "m09.jpg",
    "Wheel of Fortune": "m10.jpg",
    "Justice": "m11.jpg",
    "The Hanged Man": "m12.jpg",
    "Death": "m13.jpg",
    "Temperance": "m14.jpg",
    "The Devil": "m15.jpg",
    "The Tower": "m16.jpg",
    "The Star": "m17.jpg",
    "The Moon": "m18.jpg",
    "The Sun": "m19.jpg",
    "Judgement": "m20.jpg",
    "The World": "m21.jpg"
}

BASE_URL = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards/"

def get_real_tarot_card_image(card_name: str) -> str:
    """Descarga o recupera la imagen real de la carta de tarot"""
    filename = CARD_FILES_MAP.get(card_name, "m00.jpg")
    local_path = os.path.join(CARDS_DIR, filename)

    if not os.path.exists(local_path):
        url = BASE_URL + filename
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(r.content)
            else:
                return None
        except Exception as e:
            print(f"[CARTAS] Error descargando {card_name}: {e}")
            return None

    return local_path
