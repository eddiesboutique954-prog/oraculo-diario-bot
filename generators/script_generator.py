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

# Matriz de situaciones con polaridad emocional extrema para máxima variedad
TEMAS_ADVERTENCIA_OSCURA = [
    ("advertencia", "alguien muy cercano a ti te está mintiendo en la cara y finge lealtad"),
    ("advertencia", "hay una energía de envidia oscura estancando tu economía en este instante"),
    ("advertencia", "esa persona de tu pasado solo quiere volver para alimentar su ego, no por amor"),
    ("advertencia", "estás a punto de cometer un error grave si confías en esa promesa vacía"),
    ("advertencia", "alguien habló de ti a tus espaldas en una reunión reciente y las cartas lo confirman"),
    ("advertencia", "un ciclo tóxico que creías superado está intentando atraparte de nuevo"),
    ("advertencia", "tu intuición te avisó sobre esa persona y preferiste ignorarla por miedo a la soledad"),
    ("advertencia", "hay dinero que se te está escapando por una fuga energética de alguien que te drena"),
]

TEMAS_BENDICION_LUZ = [
    ("bendicion", "un milagro económico inesperado tocará tu puerta en los próximos 7 días"),
    ("bendicion", "el amor de tu vida ya sabe de tu existencia y un encuentro del destino está cerca"),
    ("bendicion", "el universo está retirando de tu camino a personas falsas para darte paz verdadera"),
    ("bendicion", "una propuesta laboral o de negocio que dabas por perdida resucitará con éxito"),
    ("bendicion", "tu tristeza reciente fue solo la limpieza previa a la mayor bendición de tu año"),
    ("bendicion", "la justicia divina se está cobrando lo que te hicieron sin que tú muevas un dedo"),
    ("bendicion", "alguien que te ama en silencio finalmente romperá el orgullo y te buscará"),
    ("bendicion", "una puerta gigante de abundancia se abrirá antes de que termine esta semana"),
]

SITUACIONES_VIRALES_ES = [item[1] for item in TEMAS_ADVERTENCIA_OSCURA + TEMAS_BENDICION_LUZ]

def get_situacion_polarizada(lang: str) -> tuple:
    # 50% probabilidad de advertencia dura / 50% de bendición luminosa
    pool = TEMAS_ADVERTENCIA_OSCURA if random.random() < 0.5 else TEMAS_BENDICION_LUZ
    return random.choice(pool)

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


# Lista priorizada de modelos 100% gratuitos en OpenRouter
FREE_MODELS_POOL = [
    "openrouter/free",                                      # Router inteligente gratuito oficial
    "liquid/lfm-2.5-2.6b:free",                             # Ultra rápido y confiable
    "google/gemma-4-31b-it:free",                           # Alta capacidad creativa
    "google/gemma-4-26b-a4b-it:free",                       # Respuesta rápida
    "nvidia/nemotron-3.5-lightning:free",                   # Excelente calidad
    "nvidia/nemotron-3-super-120b-a12b:free",               # Gran capacidad
    "poolside/laguna-s-2.1:free",                           # Modelo gratuito alternativo
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",   # Modelo de razonamiento
    "apodex/apodex-1.1-mini:free",                          # Respaldo ligero
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
            print(f"[IA] Consultando modelo gratuito: {model}...")
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
                    "temperature": 0.85,
                },
                timeout=25,
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    msg = choices[0].get("message", {})
                    # Capturar content o reasoning si viene en formato thinking
                    content = msg.get("content") or msg.get("reasoning") or ""
                    if content.strip():
                        print(f"[IA] Exito con modelo: {model}")
                        return content
            else:
                print(f"[IA] Modelo {model} devolvio codigo HTTP {resp.status_code}. Intentando siguiente...")
        except Exception as e:
            print(f"[IA] Error con modelo {model}: {e}. Conmutando a siguiente modelo...")
            continue

    print("[IA] Todos los modelos gratuitos de la lista fallaron o dieron timeout.")
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
    polaridad, situacion_auto = get_situacion_polarizada(lang)
    if not situacion:
        situacion = situacion_auto

    if lang == "es":
        instruccion_tono = (
            "ESTE VIDEO ES UNA ADVERTENCIA OSCURA Y URGENTE (tensión, peligro, traición o secreto revelado). Tono serio, de alerta y protección."
            if polaridad == "advertencia" else
            "ESTE VIDEO ES UNA BENDICIÓN DE LUZ Y ABUNDANCIA (milagro económico, amor verdadero o liberación). Tono esperanzador, victorioso y mágico."
        )
        system = (
            "Eres el estratega y guionista de YouTube Shorts #1 del mundo en el nicho de esoterismo, tarot y espiritualidad. "
            "Tus videos superan el 120% de retención de audiencia porque usas TÉCNICA DE BUCLE INFINITO (el final conecta de forma perfecta con el inicio), "
            "ganchos viscerales que activan el sesgo de confirmación y llamadas a la acción que provocan miles de comentarios. "
            "Escribes como un ser humano íntimo, empático y misterioso. CERO frases genéricas de horóscopo barato."
        )
        user = f"""Crea un guion VIRAL COMPLETO para un Short que dure EXACTAMENTE ENTRE 45 Y 52 SEGUNDOS de locución continua (debes escribir OBLIGATORIAMENTE ENTRE 110 Y 135 PALABRAS habladas).

CARTA: {card}
CONFLICTO VISCERAL: {situacion}
ENFOQUE DEL VIDEO: {instruccion_tono}

REGLAS DE RETENCIÓN MÁXIMA EN SHORTS (OBLIGATORIAS):
- NO LO HAGAS CORTO. Escribe suficiente texto para llenar entre 45 y 52 segundos de narración fluida y atrapante (110 a 135 palabras).
- El TÍTULO debe ser demoledor, con emojis de advertencia o bendición, misterio y alta curiosidad psicológica (ejemplos: "⚠️ ALGUIEN CERCA TE ENVIDIA EN SILENCIO 💔", "🔥 La Verdad Oculta que Necesitas Saber Hoy 😱", "⚡️ El Tarot te Advierte: No Ignores Esta Señal").
- El final DEBE terminar con una llamada a la acción para decretar en comentarios (ejemplo: "Escribe 'ME PROTEJO' para anular esta energía", "Comenta 'HECHO ESTÁ' para recibir tu bendición").

ESTRUCTURA VIRAL (45 a 52 SEGUNDOS):
1. HOOK EXPLOSIVO (0 a 4s): Una frase que congele el dedo del usuario y le toque una fibra sensible.
2. REVELACIÓN Y DESARROLLO (5 a 35s): Profundiza en lo que está viviendo, qué significa la carta {card}, cuál es la advertencia o bendición concreta, y qué decisión debe tomar.
3. CONSEJO PRÁCTICO + CTA VIRAL (36 a 48s): Dale una instrucción clara y ordénale comentar una palabra de poder para decretar o protegerse.

Responde ÚNICAMENTE en formato JSON:
{{
  "content_type": "tarot",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "titulo impactante de alta curiosidad con emojis (max 60 caracteres)",
  "hook": "frase demoledora del gancho inicial (max 12 palabras)",
  "script": "guion continuo y profundo de 110 a 135 palabras que llene 45 a 52 segundos de voz sin pausas vacias",
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

    # Generación de títulos y aperturas dinámicas con alta urgencia y curiosidad
    titulos_dinamicos = [
        f"⚠️ CUIDADO: La advertencia oculta de {card} 💔",
        f"🔥 {card}: La verdad que cambiará tu destino hoy 😱",
        f"⚡️ No ignores esta señal de {card}: Alguien planea algo",
        f"👁️ Lo que {card} acaba de revelar sobre tu entorno ✨",
        f"🚨 La traición que {card} te advierte antes de que sea tarde",
        f"💰 {card}: La bendición y el dinero que se destraba para ti",
        f"👑 {card}: El universo te acaba de elegir para esto 🌹",
    ]
    hooks_dinamicos = [
        f"Si la carta de {card} apareció en tu pantalla justo ahora, no fue casualidad...",
        f"El universo puso a {card} en tu camino porque alguien cerca de ti oculta algo...",
        f"Detén lo que estás haciendo: la carta de {card} trae un mensaje urgente para ti...",
        f"Antes de que termine este día, escucha con mucha atención lo que {card} anuncia...",
        f"Esta lectura con {card} no apareció frente a tus ojos por error...",
    ]

    data.setdefault("title", random.choice(titulos_dinamicos))
    data.setdefault("hook", random.choice(hooks_dinamicos))
    data.setdefault("script",
        f"{data.get('hook')} "
        f"Sientes en tu pecho que {situacion}. "
        f"La carta de {card} no miente: confirma que estás atravesando un punto de quiebre espiritual definitivo en tu vida. "
        f"Hay personas en tu entorno que fingen apoyarte, pero en el fondo envidian tu luz y tu progreso en silencio. "
        f"Sin embargo, las fuerzas del universo se están alineando a tu favor para cerrar ese ciclo de dolor y abrirte caminos de abundancia y paz. "
        f"No permitas que las dudas del pasado te frenen. "
        f"Escribe 'ME LIBERO' en los comentarios para cortar con toda mala energía y reclamar tu bendición hoy mismo.")
    data.setdefault("caption_lines", [
        f"ALERTA: {card.upper()}",
        situacion[:22].upper() + "...",
        "ESCRIBE 'ME LIBERO'"
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
        system = "Eres el astrólogo esotérico más viral en español. Tus mensajes de zodiaco provocan miles de comentarios porque tocas advertencias, traiciones y momentos clave de su vida con total precisión."
        user = f"""Crea un SHORT viral de 45 a 52 SEGUNDOS para el signo {sign} (debes escribir OBLIGATORIAMENTE ENTRE 110 Y 135 PALABRAS habladas).

Situación emocional que viven ahora: {situacion}
Carta del tarot que los acompaña hoy: {card}

REGLAS DE RETENCIÓN MÁXIMA:
- NO LO HAGAS CORTO. Escribe un guion completo de 110 a 135 palabras que llene entre 45 y 52 segundos de locución continua.
- Comienza con un hook directo: "Si eres {sign}, detén lo que estás haciendo..." o "Cuidado si naciste bajo el signo de {sign}..."
- El TÍTULO NO debe ser genérico. Usa títulos de alto impacto y advertencia (ejemplos: "⚠️ CUIDADO si eres {sign}: Algo oculto se revela hoy 💔", "🔥 {sign}: La advertencia que no debes ignorar 😱", "⚡️ El universo te frena, {sign}: Lee esto antes de dormir ✨").
- Termina ordenando comentar una palabra para decretar (ejemplo: "Si eres {sign}, escribe 'ACEPTO' para activar tu protección").

Responde SOLO en formato JSON:
{{
  "content_type": "zodiaco",
  "sign": "{sign}",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "titulo de alta curiosidad y misterio para {sign} con emojis (max 60 caracteres)",
  "hook": "hook inicial impactante para {sign} (max 15 palabras)",
  "script": "guion narrado de 110 a 135 palabras intimo, revelador y profundo para {sign} de 45 a 52 segundos",
  "caption_lines": ["{sign.upper()}", "frase emocional", "CTA de poder"],
  "description": "descripcion YouTube con hashtags",
  "tags": ["{sign.lower()}", "zodiaco", "tarot", "astrologia", "horoscopo", "prediccion"]
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
    titulos_zodiaco = [
        f"⚠️ CUIDADO si eres {sign}: Algo oculto se revela hoy 💔",
        f"🔥 {sign}: La advertencia del tarot que no debes ignorar 😱",
        f"⚡️ El universo te frena, {sign}: Alguien habla a tus espaldas ✨",
        f"👁️ {sign}: Hay dinero y verdad que se destraban para ti 💰",
        f"🚨 {sign}: La carta de {card} trae un aviso urgente a tu vida",
    ]
    data.setdefault("title", random.choice(titulos_zodiaco))
    data.setdefault("hook", f"Si eres {sign}, detén lo que estás haciendo y escucha bien...")
    data.setdefault("script",
        f"{data.get('hook')} "
        f"El universo me pidió darte este mensaje urgente: {situacion}. "
        f"La carta de {card} confirma que tu intuición no se equivocaba respecto a esa persona o esa situación que te quitaba el sueño. "
        f"Ha habido traiciones y miradas de envidia a tu alrededor que intentaban bloquear tu brillo y tus finanzas. "
        f"Pero hoy el ciclo se invierte: lo que te quitaron regresará multiplicado y verás con tus propios ojos cómo la justicia divina actúa a tu favor. "
        f"Si eres {sign}, escribe 'ACEPTO' en los comentarios para activar tu decreto de protección y bendición ahora.")
    data.setdefault("caption_lines", [f"ALERTA {sign.upper()}", situacion[:22].upper() + "...", "ESCRIBE 'ACEPTO'"])
    return data


# ══════════════════════════════════════════════════════════════════════════════
# TIPO 3 — REFLEXIÓN QUE LLEGA AL ALMA
# ══════════════════════════════════════════════════════════════════════════════
def generate_reflexion_script(lang: str = "es") -> dict:
    situacion = get_situacion_viral(lang)
    card = get_random_card(lang)

    if lang == "es":
        system = "Eres un guía espiritual viral. Tus reflexiones provocan miles de comentarios porque tocas heridas reales, envidias silenciadas y verdades que nadie se atreve a decir."
        user = f"""Crea una reflexión espiritual y viral de 45 A 52 SEGUNDOS sobre: "{situacion}" (debes escribir OBLIGATORIAMENTE ENTRE 110 Y 135 PALABRAS habladas).

REGLAS DE RETENCIÓN MÁXIMA:
- NO LO HAGAS CORTO. Escribe suficiente texto para llenar entre 45 y 52 segundos de narración profunda (110 a 135 palabras).
- La primera frase debe congelar el dedo del usuario: "Alguien que te lastimó en silencio...", "Hay una envidia que te rodea..."
- TÍTULO: Debe generar misterio y tensión emocional con emojis (ejemplo: "✨ la verdad sobre quién te envidia en silencio 🍞", "⚠️ No ignores este aviso antes de que sea tarde 💔").
- Final: Invita a decretar en comentarios (ejemplo: "Escribe 'CORTO CON TODO MAL' para proteger tu paz").

Responde SOLO en formato JSON:
{{
  "content_type": "reflexion",
  "card": "{card}",
  "cards": ["{card}"],
  "title": "titulo impactante y misterioso con emojis (max 60 caracteres)",
  "hook": "primera frase demoledora (max 15 palabras)",
  "script": "reflexion narrada de 110 a 135 palabras continua, profunda y sanadora de 45 a 52 segundos",
  "caption_lines": ["frase 1 de impacto", "frase 2 revelacion", "frase 3 CTA de poder"],
  "description": "descripcion YouTube con hashtags espirituales",
  "tags": ["reflexion", "espiritualidad", "despertar", "crecimientopersonal", "sanacion", "karma"]
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
    titulos_reflexion = [
        f"✨ La verdad sobre quién te envidia en silencio 💔",
        f"⚠️ CUIDADO: Hay alguien que habló de ti a tus espaldas 🍞",
        f"🔥 La justicia divina se está cobrando lo que te hicieron ✨",
        f"👁️ Hay un dinero y una verdad que no te querían contar 💰",
        f"⚡️ No ignores este aviso antes de irte a dormir hoy 🌙",
    ]
    data.setdefault("title", random.choice(titulos_reflexion))
    data.setdefault("hook", "Alguien que te lastimó en silencio no puede dejar de pensar en ti...")
    data.setdefault("script",
        f"{data.get('hook')} "
        f"El universo te lo está mostrando hoy porque {situacion}. "
        f"Has soportado cargas y silencios que nadie más conoce, entregando tu lealtad a personas que no supieron valorar tu corazón. "
        f"Pero escucha con claridad: la carta de {card} anuncia que la deuda kármica ha sido saldada. "
        f"Toda lágrima derramada en secreto se convertirá en una victoria que verán quienes intentaron verte caer. "
        f"No permitas que el rencor contamine tu luz. "
        f"Escribe 'CORTO CON TODO MAL' en los comentarios para sellar tu protección y recibir tu bendición hoy.")
    data.setdefault("caption_lines", [
        "JUSTICIA DIVINA",
        situacion[:22].upper() + "...",
        "ESCRIBE 'CORTO CON TODO MAL'"
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
