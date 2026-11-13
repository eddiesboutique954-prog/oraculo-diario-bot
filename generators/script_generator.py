"""
🔮 Motor de Guiones Virales de Alta Retención (Arquitectura +1.000.000 Vistas)
Fórmulas probadas de los canales más virales del mundo en Tarot y Espiritualidad:
1. Thumb-Stop Hook (0-1.5s): Letras de personas especiales, advertencias urgentes y milagros en 48h.
2. Bucle Infinito (Infinite Loop): La última frase empalma de forma invisible con la primera.
3. Ritual de Comentarios Masivos: Llamadas de afirmación que generan miles de comentarios (Hecho Está, Iniciales).
4. Pacing Ultra Rápido (18-24 segundos): Máxima tasa de finalización y repetición en el feed de Shorts.
"""

import json
import random
import re
from datetime import datetime
import requests
from config import OPENROUTER_API_KEY

MAJOR_ARCANA_ES = [
    "El Loco", "El Mago", "La Sacerdotisa", "La Emperatriz", "El Emperador",
    "El Sumo Sacerdote", "Los Enamorados", "El Carro", "La Fuerza", "El Ermitaño",
    "La Rueda de la Fortuna", "La Justicia", "El Colgado", "La Muerte",
    "La Templanza", "El Diablo", "La Torre", "La Estrella", "La Luna",
    "El Sol", "El Juicio", "El Mundo"
]

MAJOR_ARCANA_EN = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death",
    "Temperance", "The Devil", "The Tower", "The Star", "The Moon",
    "The Sun", "Judgement", "The World"
]

ZODIAC_SIGNS_ES = [
    "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
    "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"
]

ZODIAC_SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

LETRAS_INICIALES_POOL = [
    "A, M o C", "S, L o J", "D, R o E", "P, F o V", "G, B o N",
    "C, J o M", "L, E o S", "A, R o D", "M, V o T", "K, Y o H"
]

FREE_MODELS_POOL = [
    "openrouter/free",
    "liquid/lfm-2.5-2.6b:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
]

def _call_openrouter(system_prompt: str, user_prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://oraculo-diario.com",
        "X-Title": "Oraculo Diario Bot",
    }
    
    for model in FREE_MODELS_POOL:
        try:
            print(f"[IA] Consultando modelo viral: {model}...")
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.85,
                },
                timeout=25,
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    msg = choices[0].get("message", {})
                    content = msg.get("content") or ""
                    # Limpiar razonamientos o bloques de pensamiento
                    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
                    if content:
                        print(f"[IA] Exito con modelo: {model}")
                        return content
        except Exception as e:
            continue
    return ""

def _parse_json(raw: str) -> dict:
    try:
        clean = re.sub(r'```json\s*', '', raw)
        clean = re.sub(r'```', '', clean)
        match = re.search(r'\{.*\}', clean, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return {}

# ══════════════════════════════════════════════════════════════════════════════
# FÓRMULAS DE ALTO IMPACTO VIRAL (+1M VISTAS)
# ══════════════════════════════════════════════════════════════════════════════

def build_viral_archetype(card: str, sign: str = None, lang: str = "es") -> dict:
    """Genera guiones de élite probados para retención >115% y viralidad masiva"""
    if not sign:
        sign = random.choice(ZODIAC_SIGNS_ES)
    iniciales = random.choice(LETRAS_INICIALES_POOL)

    archetypes = [
        # ARQUETIPO 1: INICIALES / AMOR Y OBSESIÓN OCULTA (El más compartido)
        {
            "content_type": "tarot",
            "title": f"🚨 NO deslices: Alguien con inicial {iniciales[0]} no puede olvidarte 💔 #shorts",
            "hook": f"No deslices este video. Si tu persona especial tiene las iniciales {iniciales} o es {sign}, esto es urgente.",
            "script": (
                f"No deslices este video. Si tu persona especial tiene las iniciales {iniciales} o es {sign}, esto es urgente: "
                f"anoche estuvo a punto de romper el silencio y escribirte, pero el orgullo le ganó. "
                f"La carta de {card} revela que no puede sacarte de su cabeza y mira tus fotos en secreto. "
                f"Deja sus iniciales en los comentarios para romper el orgullo que los separa. "
                f"Para tu lectura privada de 3 preguntas por $10 USD escribe al WhatsApp en pantalla, y no olvides que..."
            ),
            "caption_lines": [f"INICIALES {iniciales}", "MIRA TUS FOTOS", "COMENTA SU INICIAL"],
            "comment_ritual": f"👇 Deja las iniciales de esa persona ({iniciales}) para romper su orgullo y activar la comunicación ✨",
            "tags": ["tarot", "tarotamor", "pareja", "ex", "horoscopo", "predicciones", "shorts"]
        },
        # ARQUETIPO 2: ADVERTENCIA DE TRAICIÓN INMINENTE (Máxima curiosidad)
        {
            "content_type": "tarot",
            "title": f"⚠️ CUIDADO: La traición que {card} te va a revelar hoy 😱 #shorts",
            "hook": "Detén este video ahora mismo. Alguien muy cercano te sonríe de frente, pero oculta algo.",
            "script": (
                f"Detén este video ahora mismo. Alguien muy cercano te sonríe de frente, pero oculta una conversación que te rompería el corazón. "
                f"La carta de {card} revela que su envidia hacia ti no es por lo que tienes, sino por tu brillo. "
                f"En menos de 48 horas una coincidencia extraña te mostrará la verdad sin que muevas un solo dedo. "
                f"Comenta 'ME PROTEJO' para activar la justicia divina hoy. "
                f"Para tu consulta privada escribe al WhatsApp en pantalla, y recuerda con atención..."
            ),
            "caption_lines": ["ALERTA DE TRAICIÓN", "SE REVELA EN 48H", "ESCRIBE 'ME PROTEJO'"],
            "comment_ritual": "🛡️ Comenta 'ME PROTEJO' para sellar tu escudo energético y alejar la falsedad de tu vida hoy ✨",
            "tags": ["tarot", "advertencia", "karma", "justiciadivina", "enemigosocultos", "shorts"]
        },
        # ARQUETIPO 3: MILAGRO ECONÓMICO EN 72H (Máximo guardado en favoritos)
        {
            "content_type": "tarot",
            "title": f"💰 DINERO INESPERADO: {card} destraba tu economía antes del viernes ✨ #shorts",
            "hook": "Si este video apareció en tu inicio hoy a esta hora exacta, no es casualidad.",
            "script": (
                f"Si este video apareció en tu inicio hoy a esta hora exacta, no es casualidad: una bendición económica viene en camino. "
                f"Una puerta que dabas por cerrada se va a abrir de golpe. "
                f"La carta de {card} confirma que el dinero que necesitas para resolver esa deuda llegará antes del domingo. "
                f"Comenta 'RECLAMO CON FE' para reclamar esta abundancia en tu cuenta. "
                f"Para tu lectura privada escribe al WhatsApp en pantalla, porque el universo no se equivoca cuando te avisa que..."
            ),
            "caption_lines": ["DINERO INESPERADO", "SE ABRE TU CAMINO", "ESCRIBE 'RECLAMO'"],
            "comment_ritual": "💰 Comenta 'RECLAMO CON FE' para sellar este milagro económico en tu realidad antes del fin de semana ✨",
            "tags": ["tarot", "abundancia", "dinero", "prosperidad", "manifestacion", "shorts"]
        },
        # ARQUETIPO 4: EL KARMA DE QUIEN TE HIZO DAÑO (Vindicación emocional)
        {
            "content_type": "tarot",
            "title": f"👁️ El karma de quien te rompió el corazón ya empezó a actuar ⚖️ #shorts",
            "hook": "La persona que se burló de tus sentimientos y se fue como si nada ya empezó a pagar.",
            "script": (
                f"La persona que se burló de tus sentimientos y se fue como si nada ya empezó a pagar su karma. "
                f"Las cartas muestran que en soledad se da cuenta del grave error que cometió al perderte. "
                f"La carta de {card} confirma que la justicia divina tarda pero nunca falla, y antes de fin de mes buscará pedirte perdón. "
                f"Comenta 'HECHO ESTÁ' para devolver toda mala vibra y liberar tu paz. "
                f"Escribe al WhatsApp en pantalla para tu lectura privada de $10 dólares, y ten la certeza de que..."
            ),
            "caption_lines": ["EL KARMA ACTÚA", "ARREPENTIMIENTO REAL", "COMENTA 'HECHO ESTÁ'"],
            "comment_ritual": "⚖️ Comenta 'HECHO ESTÁ' para soltar esa carga y dejar que la justicia divina actúe a tu favor ✨",
            "tags": ["tarot", "karma", "retornodelamor", "arrepentimiento", "justicia", "shorts"]
        }
    ]

    selected = random.choice(archetypes)
    selected["card"] = card
    selected["cards"] = [card]
    selected["sign"] = sign
    selected["lang"] = lang
    return selected

def generate_tarot_script(lang: str = "es", card: str = None, situacion: str = None) -> dict:
    if not card:
        card = random.choice(MAJOR_ARCANA_ES if lang == "es" else MAJOR_ARCANA_EN)
    sign = random.choice(ZODIAC_SIGNS_ES if lang == "es" else ZODIAC_SIGNS_EN)

    # Intentar generar con IA
    system = (
        "Eres el guionista de YouTube Shorts #1 del mundo en Tarot y Espiritualidad. "
        "Tus videos superan el 120% de retención porque utilizas BUCLE INFINITO (la última frase empalma de forma imperceptible con la primera frase del hook), "
        "ganchos psicológicos demoledores con iniciales de personas o advertencias urgentes, y un llamado a comentar que genera miles de interacciones. "
        "Escribe en español íntimo, místico y visceral. Devuelve ÚNICAMENTE un objeto JSON válido."
    )
    user = f"""Crea un guion VIRAL para YouTube Shorts de 20 A 24 SEGUNDOS (50 a 60 palabras exactas habladas).
CARTA: {card}
SIGNO DESTACADO: {sign}

REGLAS DE ORO (+1M VISTAS):
1. HOOK (0 a 2s): Inicia con impacto visceral ("No deslices este video...", "Si tu persona especial tiene las iniciales...", "Detén este video ahora mismo...").
2. HISTORIA (3 a 16s): Revelación íntima que {card} destapa sobre esa persona o dinero.
3. BUCLE INFINITO + VENTA + COMENTARIO (17 a 22s):
   - Invita a comentar una afirmación (ej: 'HECHO ESTÁ' o sus iniciales).
   - Menciona: "Para tu lectura privada de 3 preguntas por $10 USD escribe al WhatsApp en pantalla".
   - La última frase debe quedar en suspenso conectando con la primera palabra del hook.

Responde SOLO en JSON:
{{
  "title": "titulo de alta curiosidad con emojis y #shorts",
  "hook": "frase de inicio demoledora",
  "script": "guion continuo de 50 a 60 palabras con bucle infinito al final",
  "caption_lines": ["FRASE 1 IMPACTO", "FRASE 2 REVELACION", "COMENTA 'HECHO ESTÁ'"],
  "comment_ritual": "texto para el comentario fijado que incita a comentar masivamente",
  "tags": ["tarot", "tarotamor", "predicciones", "horoscopo", "shorts"]
}}"""

    raw = _call_openrouter(system, user)
    ai_data = _parse_json(raw)

    # Si la IA respondió con datos válidos, los usamos enriqueciendo con metadata
    if ai_data and ai_data.get("script") and len(ai_data.get("script", "").split()) >= 35:
        ai_data.setdefault("content_type", "tarot")
        ai_data.setdefault("card", card)
        ai_data.setdefault("cards", [card])
        ai_data.setdefault("sign", sign)
        ai_data.setdefault("lang", lang)
        ai_data.setdefault("comment_ritual", "🔮 Comenta 'HECHO ESTÁ' para sellar esta energía y reclama tu lectura privada en WhatsApp ✨")
        return ai_data

    # Fallback maestro de élite: arquetipos diseñados para superar el millón de vistas
    return build_viral_archetype(card, sign, lang)

def generate_zodiaco_script(lang: str = "es", sign: str = None) -> dict:
    card = random.choice(MAJOR_ARCANA_ES if lang == "es" else MAJOR_ARCANA_EN)
    return generate_tarot_script(lang=lang, card=card)

def generate_reflexion_script(lang: str = "es") -> dict:
    card = random.choice(MAJOR_ARCANA_ES if lang == "es" else MAJOR_ARCANA_EN)
    return generate_tarot_script(lang=lang, card=card)
