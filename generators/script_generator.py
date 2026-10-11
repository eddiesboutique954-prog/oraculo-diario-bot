"""
🔮 Motor de Guiones Virales de Alta Retención
Formula probada de canales con millones de vistas:
- Hook de identidad ("Si esto llegó a tu pantalla...")
- Situación específica que la gente VIVE (traición, amor, dinero, bloqueos)
- Mensaje personal que llega al alma
- Revelación dramática de la carta
- CTA emocional, no genérico
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

# Situaciones reales de la vida que la gente vive
# Estos temas generan identificación inmediata y comentarios masivos
SITUACIONES_VIRALES_ES = [
    "alguien que te lastimó sigue pensando en ti y no puede dormir",
    "hay una traición cerca de ti que aún no descubriste",
    "el amor que esperas está más cerca de lo que crees",
    "hay dinero bloqueado que viene hacia ti esta semana",
    "una persona de tu pasado está a punto de volver",
    "alguien te envidia en silencio y está bloqueando tu energía",
    "estás a punto de tomar una decisión que cambiará tu vida",
    "el universo está cerrando un ciclo doloroso en tu vida ahora mismo",
    "alguien que perdiste no ha dejado de pensar en ti ni un solo día",
    "hay una oportunidad enorme que estás a punto de perder por miedo",
    "te están mintiendo alguien muy cercano a ti",
    "tu soledad de ahora es preparación para algo hermoso que viene",
    "alguien está hablando mal de ti a tus espaldas y la carta lo confirma",
    "llevas tiempo esperando una señal y esta carta ES esa señal",
    "hay un milagro económico que viene en los próximos 7 días",
    "la persona que amas tiene sentimientos que no te ha dicho",
    "estás cargando un peso emocional que no es tuyo soltar ya",
    "alguien del pasado necesita pedirte perdón y lo hará pronto",
    "tu intuición sobre esa persona tenía razón desde el principio",
    "hay una puerta que el universo está a punto de abrirte de golpe",
]

SITUACIONES_VIRALES_EN = [
    "someone who hurt you can't stop thinking about you",
    "there's a betrayal near you that you haven't discovered yet",
    "the love you're waiting for is closer than you think",
    "there's blocked money coming toward you this week",
    "someone from your past is about to come back",
    "someone envies you in silence and is blocking your energy",
    "you're about to make a decision that will change your life",
    "the universe is closing a painful cycle in your life right now",
    "someone you lost hasn't stopped thinking about you for a single day",
    "there's a huge opportunity you're about to miss because of fear",
    "someone very close to you is lying to you",
    "your loneliness right now is preparation for something beautiful coming",
    "someone is talking badly about you behind your back",
    "you've been waiting for a sign and this card IS that sign",
    "there's a financial miracle coming in the next 7 days",
    "the person you love has feelings they haven't told you",
    "you're carrying emotional weight that isn't yours to carry",
    "someone from your past needs to apologize and will do it soon",
    "your intuition about that person was right from the beginning",
    "there's a door the universe is about to open for you suddenly",
]

CONTENT_TYPES = ["tarot", "tarot", "tarot", "zodiaco", "reflexion"]

def get_content_type() -> str:
    return random.choice(CONTENT_TYPES)

def get_random_card(lang: str) -> str:
    return random.choice(MAJOR_ARCANA_ES if lang == "es" else MAJOR_ARCANA_EN)

def get_random_zodiac(lang: str) -> str:
    return random.choice(ZODIAC_SIGNS_ES if lang == "es" else ZODIAC_SIGNS_EN)

def get_situacion_viral(lang: str) -> str:
    pool = SITUACIONES_VIRALES_ES if lang == "es" else SITUACIONES_VIRALES_EN
    return random.choice(pool)


def _call_openrouter(system_prompt: str, user_prompt: str) -> str:
    models = [
        "liquid/lfm-2.5-2.6b:free",
        "google/gemma-3-27b-it:free",
        "nvidia/nemotron-3.5-lightning:free",
        "openrouter/auto",
    ]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://oraculo-diario.com",
        "X-Title": "Oraculo Diario Bot",
    }
    for model in models:
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 800,
                    "temperature": 0.9,
                },
                timeout=45,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            continue
    return ""


def _parse_json(raw: str) -> dict:
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return {}


# ══════════════════════════════════════════════════════════════════════════════
# TIPO 1 — TAROT EMOCIONAL (Una sola carta, situación viral)
# ══════════════════════════════════════════════════════════════════════════════
def generate_tarot_script(lang: str = "es", card: str = None, situacion: str = None) -> dict:
    if not card:
        card = get_random_card(lang)
    if not situacion:
        situacion = get_situacion_viral(lang)

    if lang == "es":
        system = (
            "Eres el estratega y guionista de YouTube Shorts #1 del mundo en el nicho de esoterismo, tarot y espiritualidad. "
            "Tus videos superan el 120% de retención de audiencia porque usas TÉCNICA DE BUCLE INFINITO (el final conecta de forma perfecta con el inicio), "
            "ganchos viscerales que activan el sesgo de confirmación y llamadas a la acción que provocan miles de comentarios. "
            "Escribes como un ser humano íntimo, empático y misterioso. CERO frases genéricas de horóscopo barato."
        )
        user = f"""Crea un guion VIRAL para un Short de 20 a 25 segundos sobre:
CARTA: {card}
CONFLICTO VISCERAL: {situacion}

ESTRUCTURA DE ALTO RENDIMIENTO (MÁXIMA RETENCIÓN):
1. HOOK EXPLOSIVO (0 a 2s): Empieza directamente en el segundo 0 sin saludos ni rodeos. Ejemplos de apertura:
   - "Alguien que te juró amor eterno no puede dormir esta noche..."
   - "Si te apareció esta carta a esta hora, alguien está mintiendo sobre ti..."
   - "El universo te puso esto en frente porque hay una verdad que no estás viendo..."
2. DESARROLLO EMOCIONAL (3 a 18s): Conecta con el dolor, la duda o el anhelo del espectador. Menciona '{card}' como el punto de quiebre. Habla de algo que cualquiera ha sentido: traición, segundas oportunidades, dinero inesperado, intuición confirmada.
3. BUCLE INFINITO + CTA (19 a 23s): 
   - Termina la última frase de tal manera que empalme perfectamente con el inicio del video si se repite.
   - Pide una micro-acción para reclamar: "Comenta 'Hecho está' y tus iniciales para manifestar esto hoy... por eso..." (para que buclee con el hook).

Responde ÚNICAMENTE en JSON:
{{
  "content_type": "tarot",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "titulo con alta curiosidad psicologica y emojis (max 50 chars)",
  "hook": "frase demoledora del hook inicial (max 12 palabras)",
  "script": "guion narrado de 22 segundos, fluido, humano, con ritmo y bucle",
  "caption_lines": ["subtitulo 1", "subtitulo 2", "subtitulo 3"],
  "description": "descripcion orientada a SEO y conexion emocional",
  "tags": ["tarot", "lecturadetarot", "espiritualidad", "amor", "destino", "oraculo"]
}}"""

    else:
        system = (
            "You are the most viral English tarot creator on YouTube Shorts. "
            "Your videos have 95% retention because every word touches the soul. "
            "You speak directly to the heart. Never generic. Each script feels written "
            "specifically for the person watching. You use dramatic pauses, unexpected "
            "revelations and messages people comment 'how did you know'."
        )
        user = f"""Create a VIRAL 30-second YouTube Shorts script.

TAROT CARD: {card}
EMOTIONAL SITUATION: {situacion}

GOLDEN RULES (don't break them):
1. The HOOK (first 3 seconds) must be so specific and personal that the person feels you wrote it FOR THEM. Good examples:
   - "If this video appeared on your screen today... it wasn't a coincidence"
   - "There's someone who's been wanting to tell you something for weeks and can't"
   - "The universe asked me to tell you this today specifically"
2. The DEVELOPMENT (3-25s) talks about "{situacion}" directly, as if you know exactly what the viewer is living. Mention "{card}" as the card that confirms it.
3. The MESSAGE must be something the person feels only the universe could know. Something that makes them pause and reread.
4. The final CTA must generate comments: "Type YES if this reached your heart" or "Comment your sign if you felt it"
5. Tone: mysterious, warm, intimate. Like a secret only you and the viewer share.

Respond ONLY in this exact JSON (no extra text):
{{
  "content_type": "tarot",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "scroll-stopping title with emoji max 60 chars",
  "hook": "exact opening phrase max 15 words that stops the scroll",
  "script": "complete 30-second script narrated in first person of the oracle, intimate and personal, with pauses marked with ...",
  "caption_lines": ["short impact phrase 1 max 6 words", "short impact phrase 2", "short impact phrase 3"],
  "description": "150 word YouTube description with hashtags at the end",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
}}"""

    raw = _call_openrouter(system, user)
    data = _parse_json(raw)
    data.setdefault("content_type", "tarot")
    data.setdefault("card", card)
    data.setdefault("cards", [card])
    data.setdefault("lang", lang)
    data.setdefault("title", f"🔮 {card} tiene un mensaje urgente para ti")
    data.setdefault("hook", "Si este video llegó a ti hoy... no fue casualidad")
    data.setdefault("script",
        f"Si este video llegó a ti hoy, no fue casualidad... "
        f"La carta {card} tiene algo importante que decirte. "
        f"{situacion.capitalize()}. "
        f"El universo te lo está confirmando ahora mismo. "
        f"Escribe SI en los comentarios si esto llegó a tu corazón.")
    data.setdefault("caption_lines", [
        "NO FUE CASUALIDAD",
        card.upper(),
        "ESCRIBE SI EN COMENTARIOS"
    ])
    data["situacion"] = situacion
    return data


# ══════════════════════════════════════════════════════════════════════════════
# TIPO 2 — ZODÍACO EMOCIONAL
# ══════════════════════════════════════════════════════════════════════════════
def generate_zodiaco_script(lang: str = "es", sign: str = None) -> dict:
    if not sign:
        sign = get_random_zodiac(lang)
    situacion = get_situacion_viral(lang)
    card = get_random_card(lang)

    if lang == "es":
        system = "Eres el astrólogo esotérico más viral en español. Tus mensajes de zodiaco hacen llorar a la gente porque los conoces mejor que ellos mismos."
        user = f"""Crea un SHORT viral de 30 segundos para el signo {sign}.

Situación emocional que viven ahora: {situacion}
Carta del tarot que los acompaña hoy: {card}

El video debe:
- Comenzar con "Si eres {sign}..." o "Para los {sign}..." de forma que SOLO ellos sientan que es para ellos
- Hablar de algo MUY ESPECÍFICO que los {sign} viven en este momento
- Dar un mensaje que los haga sentir vistos, comprendidos
- Terminar con "Comparte si eres {sign} y lo sentiste"

Responde SOLO en JSON:
{{
  "content_type": "zodiaco",
  "sign": "{sign}",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "titulo para {sign} con emoji maximo 60 caracteres",
  "hook": "hook inicial para {sign} maximo 15 palabras",
  "script": "guion narrado 30 segundos intimo y especifico para {sign}",
  "caption_lines": ["{sign.upper()}", "frase emocional", "CTA corto"],
  "description": "descripcion YouTube con hashtags",
  "tags": ["{sign.lower()}", "zodiaco", "tarot", "astrologia", "horoscopo"]
}}"""
    else:
        system = "You are the most viral esoteric astrologer in English. Your zodiac messages make people cry because you know them better than themselves."
        user = f"""Create a viral 30-second Short for the {sign} sign.

Emotional situation they live now: {situacion}
Tarot card accompanying them today: {card}

The video must:
- Start with "If you're {sign}..." or "For {sign}..." so ONLY they feel it's for them
- Talk about something VERY SPECIFIC that {sign} people are living right now
- Give a message that makes them feel seen and understood
- End with "Share if you're {sign} and felt this"

Respond ONLY in JSON:
{{
  "content_type": "zodiaco",
  "sign": "{sign}",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "title for {sign} with emoji max 60 chars",
  "hook": "opening hook for {sign} max 15 words",
  "script": "narrated 30 second script intimate and specific for {sign}",
  "caption_lines": ["{sign.upper()}", "emotional phrase", "short CTA"],
  "description": "YouTube description with hashtags",
  "tags": ["{sign.lower()}", "zodiac", "tarot", "astrology", "horoscope"]
}}"""

    raw = _call_openrouter(system, user)
    data = _parse_json(raw)
    data.setdefault("content_type", "zodiaco")
    data.setdefault("sign", sign)
    data.setdefault("card", card)
    data.setdefault("cards", [card])
    data.setdefault("lang", lang)
    data.setdefault("title", f"🔮 {sign}: El universo tiene algo para ti")
    data.setdefault("hook", f"Si eres {sign}, este mensaje es solo para ti")
    data.setdefault("script",
        f"Si eres {sign}, escucha bien. {situacion.capitalize()}. "
        f"La carta {card} lo confirma hoy. "
        f"El universo te está viendo y quiere que sepas que no estás solo. "
        f"Comparte si eres {sign} y lo sentiste.")
    data.setdefault("caption_lines", [sign.upper(), situacion[:25].upper() + "...", "COMPARTE SI LO SENTISTE"])
    return data


# ══════════════════════════════════════════════════════════════════════════════
# TIPO 3 — REFLEXIÓN QUE LLEGA AL ALMA
# ══════════════════════════════════════════════════════════════════════════════
def generate_reflexion_script(lang: str = "es") -> dict:
    situacion = get_situacion_viral(lang)
    card = get_random_card(lang)

    if lang == "es":
        system = "Eres un guía espiritual viral. Tus reflexiones tienen millones de vistas porque dices exactamente lo que la gente necesita escuchar pero nadie más les dice."
        user = f"""Crea una reflexión espiritual viral de 30 segundos sobre: "{situacion}"

Reglas:
- La primera frase debe hacer que quien la escuche piense "esto lo escribieron para mí"
- Sin frases vacías ni genéricas. Todo específico y emocional.
- Debe resolver algo, consolar algo, o revelar algo que la persona ya sentía pero no sabía cómo decirse a sí misma
- Tono: como un mensaje de un ser querido del otro lado, o de tu yo más sabio

Responde SOLO en JSON:
{{
  "content_type": "reflexion",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "titulo que duela bonito, maximo 60 caracteres con emoji",
  "hook": "primera frase que llega al alma, maxima 15 palabras",
  "script": "reflexion narrada 30 segundos, pausas con ..., sin frases vacias",
  "caption_lines": ["frase 1 que duele bonito", "frase 2 revelacion", "frase 3 CTA emocional"],
  "description": "descripcion YouTube con hashtags espirituales",
  "tags": ["reflexion", "espiritualidad", "despertar", "crecimientopersonal", "sanacion"]
}}"""
    else:
        system = "You are a viral spiritual guide. Your reflections get millions of views because you say exactly what people need to hear but no one else tells them."
        user = f"""Create a viral 30-second spiritual reflection about: "{situacion}"

Rules:
- The first phrase must make the listener think "this was written for me"
- No empty or generic phrases. Everything specific and emotional.
- Must resolve something, comfort something, or reveal something the person already felt but didn't know how to tell themselves
- Tone: like a message from a loved one from the other side, or from your wisest self

Respond ONLY in JSON:
{{
  "content_type": "reflexion",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "title that beautifully hurts, max 60 chars with emoji",
  "hook": "first phrase that touches the soul, max 15 words",
  "script": "narrated 30-second reflection, pauses with ..., no empty phrases",
  "caption_lines": ["phrase 1 beautiful pain", "phrase 2 revelation", "phrase 3 emotional CTA"],
  "description": "YouTube description with spiritual hashtags",
  "tags": ["reflection", "spirituality", "awakening", "personalgrowth", "healing"]
}}"""

    raw = _call_openrouter(system, user)
    data = _parse_json(raw)
    data.setdefault("content_type", "reflexion")
    data.setdefault("card", card)
    data.setdefault("cards", [card])
    data.setdefault("lang", lang)
    data.setdefault("title", f"✨ {situacion[:40]}...")
    data.setdefault("hook", situacion[:50])
    data.setdefault("script",
        f"{situacion.capitalize()}. "
        f"El universo te lo está diciendo hoy porque estás listo para escucharlo. "
        f"No es casualidad que estés leyendo esto ahora. "
        f"Escribe SI en los comentarios si esto llegó a tu corazón.")
    data.setdefault("caption_lines", [
        situacion[:22].upper() + "...",
        "NO ES CASUALIDAD",
        "ESCRIBE SI SI LO SENTISTE"
    ])
    return data


# ══════════════════════════════════════════════════════════════════════════════
# DISPATCHER PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
def generate_script(lang: str = "es", content_type: str = None,
                    card: str = None, sign: str = None) -> dict:
    ctype = content_type or get_content_type()
    print(f"[TIPO] {ctype.upper()} | Situacion: {get_situacion_viral(lang)[:50]}")

    if ctype == "tarot":
        data = generate_tarot_script(lang=lang, card=card)
    elif ctype == "zodiaco":
        data = generate_zodiaco_script(lang=lang, sign=sign)
    elif ctype == "reflexion":
        data = generate_reflexion_script(lang=lang)
    else:
        data = generate_tarot_script(lang=lang, card=card)

    data["lang"] = lang
    return data


# Alias de compatibilidad con main.py existente
def generate_tarot_script_compat(topic: str, lang: str = "es") -> dict:
    return generate_tarot_script(lang=lang)

def get_next_topic(lang: str = "es") -> str:
    return get_situacion_viral(lang)
