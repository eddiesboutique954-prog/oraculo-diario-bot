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
    "The World": "m21.jpg",
    # Mapeo en Portugués
    "O Louco": "m00.jpg",
    "O Mago": "m01.jpg",
    "A Sacerdotisa": "m02.jpg",
    "A Imperatriz": "m03.jpg",
    "O Imperador": "m04.jpg",
    "O Hierofante": "m05.jpg",
    "Os Enamorados": "m06.jpg",
    "O Carro": "m07.jpg",
    "A Força": "m08.jpg",
    "O Eremita": "m09.jpg",
    "A Roda da Fortuna": "m10.jpg",
    "A Justiça": "m11.jpg",
    "O Enforcado": "m12.jpg",
    "A Morte": "m13.jpg",
    "A Temperança": "m14.jpg",
    "O Diabo": "m15.jpg",
    "A Torre": "m16.jpg",
    "A Estrela": "m17.jpg",
    "A Lua": "m18.jpg",
    "O Sol": "m19.jpg",
    "O Julgamento": "m20.jpg",
    "O Mundo": "m21.jpg",
    # Mapeo en Francés
    "Le Fou": "m00.jpg",
    "Le Mat": "m00.jpg",
    "Le Magicien": "m01.jpg",
    "Le Bateleur": "m01.jpg",
    "La Papesse": "m02.jpg",
    "L'Impératrice": "m03.jpg",
    "L'Empereur": "m04.jpg",
    "Le Pape": "m05.jpg",
    "L'Amoureux": "m06.jpg",
    "Les Amoureux": "m06.jpg",
    "Le Chariot": "m07.jpg",
    "La Force": "m08.jpg",
    "L'Hermite": "m09.jpg",
    "La Roue de Fortune": "m10.jpg",
    "La Justice": "m11.jpg",
    "Le Pendu": "m12.jpg",
    "La Mort": "m13.jpg",
    "Tempérance": "m14.jpg",
    "Le Diable": "m15.jpg",
    "La Tour": "m16.jpg",
    "La Maison Dieu": "m16.jpg",
    "L'Étoile": "m17.jpg",
    "La Lune": "m18.jpg",
    "Le Soleil": "m19.jpg",
    "Le Jugement": "m20.jpg",
    "Le Monde": "m21.jpg",
    # Mapeo en Italiano
    "Il Matto": "m00.jpg",
    "Il Mago": "m01.jpg",
    "Il Bagatto": "m01.jpg",
    "La Papessa": "m02.jpg",
    "L'Imperatrice": "m03.jpg",
    "L'Imperatore": "m04.jpg",
    "Il Papa": "m05.jpg",
    "Gli Amanti": "m06.jpg",
    "Il Carro": "m07.jpg",
    "La Forza": "m08.jpg",
    "L'Eremita": "m09.jpg",
    "La Ruota della Fortuna": "m10.jpg",
    "La Giustizia": "m11.jpg",
    "L'Appeso": "m12.jpg",
    "La Morte": "m13.jpg",
    "La Temperanza": "m14.jpg",
    "Il Diavolo": "m15.jpg",
    "La Torre": "m16.jpg",
    "La Stella": "m17.jpg",
    "La Luna": "m18.jpg",
    "Il Sole": "m19.jpg",
    "Il Giudizio": "m20.jpg",
    "Il Mondo": "m21.jpg",
    # Mapeo en Alemán
    "Der Narr": "m00.jpg",
    "Der Magier": "m01.jpg",
    "Die Hohepriesterin": "m02.jpg",
    "Die Herrscherin": "m03.jpg",
    "Der Herrscher": "m04.jpg",
    "Der Hierophant": "m05.jpg",
    "Die Liebenden": "m06.jpg",
    "Der Wagen": "m07.jpg",
    "Die Kraft": "m08.jpg",
    "Der Eremit": "m09.jpg",
    "Das Rad des Schicksals": "m10.jpg",
    "Die Gerechtigkeit": "m11.jpg",
    "Der Gehängte": "m12.jpg",
    "Der Tod": "m13.jpg",
    "Die Mäßigkeit": "m14.jpg",
    "Der Teufel": "m15.jpg",
    "Der Turm": "m16.jpg",
    "Der Stern": "m17.jpg",
    "Der Mond": "m18.jpg",
    "Die Sonne": "m19.jpg",
    "Das Gericht": "m20.jpg",
    "Die Welt": "m21.jpg"
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
