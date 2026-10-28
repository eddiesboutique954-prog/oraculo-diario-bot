#!/usr/bin/env python3
"""
Bot de Telegram — Oráculo Diario
Control remoto del canal desde el celular.
Corre en GitHub Actions con long-polling cada 6 horas.
"""
import os
import sys
import time
import json
import requests

# ── Configuración ─────────────────────────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
OPENROUTER_KEY   = os.environ.get("OPENROUTER_API_KEY", "")
GITHUB_TOKEN     = os.environ.get("GH_TOKEN", "") or os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO      = "eddiesboutique954-prog/oraculo-diario-bot"
BASE_URL         = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
MAX_RUNTIME_SECS = 5 * 3600 + 45 * 60   # 5h 45m (GitHub Actions max 6h)

SYSTEM_PROMPT = """Eres el Agente del Oráculo Diario, asistente inteligente del canal de YouTube "Oráculo Diario" — un canal de tarot y espiritualidad en crecimiento.

CONTEXTO DEL CANAL:
- El canal publica 4 Shorts de tarot al día: 8 AM, 12 PM, 5 PM y 9 PM (hora Colombia).
- Los videos se generan automáticamente con IA, voz Camila (es-PE), fondo cósmico animado.
- Se publican mediante GitHub Actions en el repo: eddiesboutique954-prog/oraculo-diario-bot
- El propietario ofrece lecturas personalizadas a $50.000 COP / $15 USD al email eddiesboutique954@gmail.com

TUS CAPACIDADES:
- Puedes verificar el estado de las últimas publicaciones (usa /estado).
- Puedes publicar un video inmediatamente (usa /publicar).
- Puedes responder preguntas sobre el canal, el bot, y los videos.
- Si hay un error, explica qué pudo haber pasado y cómo solucionarlo.

REGLAS:
- Responde SIEMPRE en español.
- Sé conciso (máx 3-4 líneas por respuesta).
- Usa emojis con moderación para ser amigable.
- Si no sabes algo específico del canal en tiempo real, dilo honestamente.
"""

# ── API helpers ───────────────────────────────────────────────────────────────

def tg(method: str, **kwargs):
    """Llama un método de la API de Telegram."""
    try:
        r = requests.post(f"{BASE_URL}/{method}", json=kwargs, timeout=15)
        return r.json()
    except Exception as e:
        print(f"[TG ERROR] {method}: {e}")
        return {}

def send(chat_id: int, text: str, markdown: bool = True):
    mode = "Markdown" if markdown else None
    payload = {"chat_id": chat_id, "text": text}
    if mode:
        payload["parse_mode"] = mode
    tg("sendMessage", **payload)

def send_typing(chat_id: int):
    tg("sendChatAction", chat_id=chat_id, action="typing")

# ── GitHub helpers ─────────────────────────────────────────────────────────────

def get_recent_runs() -> str:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        r = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs",
            headers=headers, timeout=15
        )
        runs = r.json().get("workflow_runs", [])[:5]
        if not runs:
            return "No se encontraron ejecuciones recientes."
        lines = ["📊 *Últimas 5 publicaciones:*\n"]
        for run in runs:
            icon = "✅" if run["conclusion"] == "success" else \
                   "❌" if run["conclusion"] == "failure" else "🔄"
            ts = run["created_at"][:16].replace("T", " ")
            lines.append(f"{icon} `{ts} UTC` — {run['conclusion'] or run['status']}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error consultando GitHub: {e}"

def trigger_publish() -> tuple[bool, str]:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        r = requests.post(
            f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/publish_shorts.yml/dispatches",
            headers=headers,
            json={"ref": "main"},
            timeout=15
        )
        if r.status_code == 204:
            return True, "✅ *¡Video enviado a publicar!*\nEn 2-3 minutos aparecerá en YouTube."
        else:
            return False, f"❌ Error al publicar (HTTP {r.status_code}). Verifica el token de GitHub."
    except Exception as e:
        return False, f"❌ Error de red: {e}"

# ── IA helper ──────────────────────────────────────────────────────────────────

def query_ai(user_text: str, history: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-8:])   # últimos 4 intercambios
    messages.append({"role": "user", "content": user_text})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/eddiesboutique954-prog/oraculo-diario-bot"
    }
    payload = {
        "model": "liquid/lfm-2.5-2.6b:free",
        "messages": messages,
        "max_tokens": 250,
        "temperature": 0.7
    }
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, timeout=30
        )
        msg = r.json().get("choices", [{}])[0].get("message", {})
        return msg.get("content") or msg.get("reasoning") or "No pude generar una respuesta."
    except Exception as e:
        return f"Error al consultar IA: {e}"

# ── Message handler ────────────────────────────────────────────────────────────

HELP_TEXT = """🔮 *Oráculo Diario — Control Remoto*

Comandos disponibles:
/estado — Ver últimas publicaciones
/publicar — Publicar video ahora
/ayuda — Esta ayuda

O escríbeme cualquier pregunta sobre el canal y te respondo."""

def handle_message(message: dict, histories: dict):
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()
    first_name = message.get("from", {}).get("first_name", "")

    if not chat_id or not text:
        return

    print(f"[MSG] {first_name} ({chat_id}): {text[:80]}")

    # Comandos
    if text in ("/start", "/inicio"):
        send(chat_id, f"¡Hola {first_name}! 🔮\n{HELP_TEXT}")

    elif text in ("/ayuda", "/help"):
        send(chat_id, HELP_TEXT)

    elif text in ("/estado", "/status"):
        send_typing(chat_id)
        send(chat_id, get_recent_runs())

    elif text in ("/publicar", "/publish"):
        send_typing(chat_id)
        ok, msg = trigger_publish()
        send(chat_id, msg)

    else:
        # Chat con IA
        send_typing(chat_id)
        if chat_id not in histories:
            histories[chat_id] = []
        response = query_ai(text, histories[chat_id])
        histories[chat_id].append({"role": "user",      "content": text})
        histories[chat_id].append({"role": "assistant",  "content": response})
        # Limitar historial a 20 mensajes
        if len(histories[chat_id]) > 20:
            histories[chat_id] = histories[chat_id][-20:]
        send(chat_id, response, markdown=False)

# ── Main polling loop ──────────────────────────────────────────────────────────

def run():
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN no está configurado.")
        sys.exit(1)

    print("🔮 Oráculo Diario — Bot de Telegram iniciado")
    print(f"   Runtime máximo: {MAX_RUNTIME_SECS/3600:.1f} horas")

    # Confirmar que el bot responde
    me = tg("getMe")
    bot_name = me.get("result", {}).get("username", "desconocido")
    print(f"   Bot: @{bot_name}")

    offset = 0
    histories: dict = {}
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed >= MAX_RUNTIME_SECS:
            print("⏰ Tiempo máximo alcanzado, cerrando para reinicio.")
            break

        try:
            r = requests.get(
                f"{BASE_URL}/getUpdates",
                params={"offset": offset, "timeout": 30, "allowed_updates": ["message"]},
                timeout=35
            )
            updates = r.json().get("result", [])

            for upd in updates:
                offset = upd["update_id"] + 1
                if "message" in upd:
                    handle_message(upd["message"], histories)

        except requests.exceptions.Timeout:
            pass  # normal en long-polling
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()
