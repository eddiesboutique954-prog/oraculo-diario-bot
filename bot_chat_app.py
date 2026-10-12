"""
🔮 Panel de Control y Chat con el Agente — Oráculo Diario
App de escritorio para monitorear el canal, publicar videos y conversar con el agente.
"""

import os
import sys
import threading
import datetime
import webbrowser
import requests
import tkinter as tk
from tkinter import scrolledtext

# ── Configuración ──────────────────────────────────────────────────────────────
BOT_DIR       = os.path.dirname(os.path.abspath(__file__))
GITHUB_TOKEN  = "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"
GITHUB_OWNER  = "eddiesboutique954-prog"
GITHUB_REPO   = "oraculo-diario-bot"
OPENROUTER_KEY = "OPENROUTER_KEY_FROM_SECRET"   # Reemplazada vía GitHub Actions secret en producción

# Modelo estable que siempre devuelve content correcto
AI_MODEL = "liquid/lfm-2.5-2.6b:free"

SYSTEM_PROMPT = """Eres el Agente Inteligente del canal "Oráculo Diario" — un canal de YouTube Shorts de tarot y espiritualidad que se publica automáticamente.

CONTEXTO REAL DEL CANAL:
- Se publican 4 Shorts diarios: 8 AM, 12 PM, 5 PM, 9 PM (Colombia, UTC-5).
- Los videos se generan con IA (guion, voz Camila, fondo cósmico, subtítulos) y se suben solos a YouTube.
- El pipeline corre en GitHub Actions: repo eddiesboutique954-prog/oraculo-diario-bot
- El dueño del canal se llama Eddie. Ofrece lecturas personalizadas a $50.000 COP / $15 USD.
- Email de contacto: eddiesboutique954@gmail.com

ERRORES CONOCIDOS Y SOLUCIONES:
- "edge-tts 403 WebSocket": Microsoft bloqueó el servicio de voz. SOLUCIÓN: el bot ya fue migrado a gTTS.
- "Process completed with exit code 1": error en la generación. Usar el botón "Publicar Short Ahora" para reintentar.
- Si GitHub Actions no disparó un video: GitHub cron puede tener hasta 15 min de retraso — es normal.

TUS CAPACIDADES:
- Responder preguntas sobre el canal, el bot y los errores.
- Explicar qué ocurrió en una publicación fallida.
- Dar recomendaciones para crecer el canal.
- El usuario puede ver el estado con el botón "Ver Estado" y forzar publicación con "Publicar Short Ahora".

REGLAS IMPORTANTES:
- Responde SIEMPRE en español.
- Sé directo y concreto. Máximo 4 líneas por respuesta.
- Nunca digas "no tengo acceso" — tienes todo el contexto necesario arriba.
- Si el usuario pregunta por un error específico, explica la causa y la solución concreta.
- Recuerda la conversación anterior para dar respuestas coherentes."""

# ── Colores ───────────────────────────────────────────────────────────────────
C_BG       = "#0f0c1b"
C_PANEL    = "#1a142e"
C_INPUT    = "#261d42"
C_GOLD     = "#ffd700"
C_PURPLE   = "#9d4edd"
C_PURPLE2  = "#7b2cbf"
C_BLUE     = "#2a1b4e"
C_GREEN    = "#00ff88"
C_CYAN     = "#00e5ff"
C_WHITE    = "#f0f0f0"
C_AGENT    = "#e0d4fd"
C_ERROR    = "#ff5555"


class OracloChatApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🔮 Oráculo Diario — Control y Chat del Agente")
        self.root.geometry("900x700")
        self.root.minsize(700, 520)
        self.root.configure(bg=C_BG)

        # Cargar ícono
        icon_path = os.path.join(BOT_DIR, "assets", "app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        # Historial de conversación para que la IA recuerde el contexto
        self.chat_history: list[dict] = []

        self._build_ui()

        self._agent("¡Hola! Soy tu Agente del canal Oráculo Diario. 🔮\n"
                    "Puedo ayudarte a:\n"
                    "• Ver el estado de las publicaciones y errores\n"
                    "• Forzar la publicación de un video ahora mismo\n"
                    "• Responder cualquier pregunta sobre el canal\n\n"
                    "¿En qué te ayudo?")

        # Al abrir, verificar estado automáticamente
        threading.Thread(target=self._auto_status, daemon=True).start()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=C_PANEL, padx=15, pady=10)
        header.pack(fill="x")

        tk.Label(header, text="🔮 Oráculo Diario Bot — Asistente Inteligente",
                 bg=C_PANEL, fg=C_GOLD, font=("Segoe UI", 14, "bold")).pack(side="left")

        self.status_dot = tk.Label(header, text="⬤ Conectado",
                                   bg=C_PANEL, fg=C_GREEN, font=("Segoe UI", 9, "bold"))
        self.status_dot.pack(side="right")

        # Botones de acción
        btns = tk.Frame(self.root, bg=C_BG, padx=12, pady=6)
        btns.pack(fill="x")

        self._btn(btns, "🔄  Ver Estado y Errores",  C_BLUE,    self._status_btn).pack(side="left", padx=4)
        self._btn(btns, "🚀  Publicar Short Ahora",  C_PURPLE2, self._publish_btn).pack(side="left", padx=4)
        self._btn(btns, "📺  Abrir Canal YouTube",   "#3a225d", self._open_channel).pack(side="right", padx=4)

        # Chat
        chat_frame = tk.Frame(self.root, bg=C_BG, padx=12, pady=4)
        chat_frame.pack(fill="both", expand=True)

        self.chat = scrolledtext.ScrolledText(
            chat_frame, wrap="word", bg="#151026", fg=C_WHITE,
            font=("Segoe UI", 11), insertbackground=C_GOLD,
            relief="flat", padx=14, pady=14, state="disabled"
        )
        self.chat.pack(fill="both", expand=True)
        self.chat.tag_config("agent",  foreground=C_AGENT)
        self.chat.tag_config("user",   foreground=C_GOLD)
        self.chat.tag_config("system", foreground=C_CYAN)
        self.chat.tag_config("error",  foreground=C_ERROR)
        self.chat.tag_config("bold",   font=("Segoe UI", 11, "bold"))

        # Input
        inp_frame = tk.Frame(self.root, bg=C_PANEL, padx=12, pady=10)
        inp_frame.pack(fill="x")

        self.entry = tk.Entry(inp_frame, bg=C_INPUT, fg=C_WHITE,
                              font=("Segoe UI", 12), relief="flat",
                              insertbackground=C_GOLD)
        self.entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self._send())
        self.entry.focus()

        self._btn(inp_frame, "Enviar  ➤", C_PURPLE, self._send,
                  font=("Segoe UI", 10, "bold"), padx=18, pady=6).pack(side="right")

    def _btn(self, parent, text, color, cmd, **kw):
        defaults = dict(font=("Segoe UI", 9, "bold"), padx=10, pady=5)
        defaults.update(kw)
        return tk.Button(parent, text=text, bg=color, fg=C_WHITE,
                         relief="flat", activebackground=C_PURPLE,
                         cursor="hand2", command=cmd, **defaults)

    # ── Chat helpers ──────────────────────────────────────────────────────────

    def _write(self, who: str, text: str, tag: str = "agent"):
        def _do():
            self.chat.config(state="normal")
            now = datetime.datetime.now().strftime("%H:%M")
            self.chat.insert("end", f"\n{who}  [{now}]\n", tag)
            self.chat.insert("end", f"{text}\n")
            self.chat.see("end")
            self.chat.config(state="disabled")
        self.root.after(0, _do)

    def _agent(self, text: str):
        self._write("🔮 Agente Oráculo Diario", text, "agent")

    def _user(self, text: str):
        self._write("👤 Tú", text, "user")

    def _sys(self, text: str):
        self._write("⚙️ Sistema", text, "system")

    # ── Enviar mensaje ────────────────────────────────────────────────────────

    def _send(self):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.entry.delete(0, "end")
        self._user(msg)
        threading.Thread(target=self._handle_message, args=(msg,), daemon=True).start()

    def _handle_message(self, text: str):
        lower = text.lower()

        # Comandos directos que no necesitan IA
        if any(w in lower for w in ["publicar", "publica", "subir video", "lanza video", "sube video"]):
            self._do_publish()
            return

        if any(w in lower for w in ["estado", "status", "errores", "error", "fallo", "qué pasó", "que paso"]):
            self._do_status()
            return

        if any(w in lower for w in ["horario", "hora", "cuándo sale", "proximo", "próximo"]):
            self._agent(
                "📅 Horarios diarios (hora Colombia):\n"
                "• ☀️  8:00 AM — Tarot del Día\n"
                "• 🌞 12:00 PM — Zodíaco / Energías\n"
                "• 🌇  5:00 PM — Reflexión y Sanación\n"
                "• 🌙  9:00 PM — Mensaje Nocturno\n\n"
                "Los videos se publican solos. Si uno falla, pulsa '🚀 Publicar Short Ahora'."
            )
            return

        # Cualquier otra pregunta → IA con historial completo
        self._ask_ai(text)

    # ── IA con historial ──────────────────────────────────────────────────────

    def _ask_ai(self, user_text: str):
        self._sys("Pensando...")

        # Agregar el mensaje del usuario al historial
        self.chat_history.append({"role": "user", "content": user_text})
        # Mantener solo los últimos 12 mensajes (6 intercambios)
        if len(self.chat_history) > 12:
            self.chat_history = self.chat_history[-12:]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.chat_history

        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/eddiesboutique954-prog/oraculo-diario-bot"
        }
        payload = {
            "model": AI_MODEL,
            "messages": messages,
            "max_tokens": 350,
            "temperature": 0.7
        }

        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers, json=payload, timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                msg_obj = data.get("choices", [{}])[0].get("message", {})
                # Fallback: algunos modelos ponen el texto en "reasoning" en vez de "content"
                answer = (msg_obj.get("content") or
                          msg_obj.get("reasoning") or
                          "Estoy activo. Usa los botones para ver el estado o publicar.")
                answer = answer.strip()
            elif resp.status_code == 429:
                answer = "Límite de solicitudes alcanzado. Espera un momento e intenta de nuevo."
            else:
                answer = (f"No pude conectar con la IA (error {resp.status_code}). "
                          "Usa los botones de arriba para las acciones principales.")

            # Guardar respuesta en historial
            self.chat_history.append({"role": "assistant", "content": answer})
            self._agent(answer)

        except requests.exceptions.Timeout:
            self._agent("La IA tardó demasiado en responder. Intenta de nuevo.")
        except Exception as e:
            self._agent(f"Error de conexión: {e}")

    # ── Estado GitHub Actions ─────────────────────────────────────────────────

    def _status_btn(self):
        threading.Thread(target=self._do_status, daemon=True).start()

    def _do_status(self):
        self._sys("Consultando estado de las últimas ejecuciones en GitHub Actions...")
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            r = requests.get(
                f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs",
                headers=headers, timeout=15
            )
            if r.status_code == 200:
                runs = r.json().get("workflow_runs", [])[:5]
                lines = ["📊 Últimas 5 ejecuciones:\n"]
                all_ok = True
                for i, run in enumerate(runs, 1):
                    conclusion = run.get("conclusion") or run.get("status", "?")
                    icon = "✅" if conclusion == "success" else \
                           "❌" if conclusion == "failure" else "🔄"
                    if conclusion == "failure":
                        all_ok = False
                    ts_utc = run.get("created_at", "")[:16].replace("T", " ")
                    lines.append(f"{icon} #{i} — {ts_utc} UTC — {conclusion}")

                if all_ok:
                    lines.append("\n✅ Todo funcionando correctamente.")
                else:
                    lines.append("\n⚠️ Hay ejecuciones fallidas. Pulsa '🚀 Publicar Short Ahora' para relanzar.")

                self._agent("\n".join(lines))
            else:
                self._agent(f"No se pudo consultar GitHub (HTTP {r.status_code}). Verifica tu conexión.")
        except Exception as e:
            self._agent(f"Error al conectar con GitHub: {e}")

    def _auto_status(self):
        """Verificación silenciosa al arrancar — solo muestra si hay errores."""
        import time
        time.sleep(2)
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            r = requests.get(
                f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs",
                headers=headers, timeout=10
            )
            if r.status_code == 200:
                runs = r.json().get("workflow_runs", [])[:3]
                failed = [run for run in runs if run.get("conclusion") == "failure"]
                if failed:
                    self._agent(
                        f"⚠️ Detecté {len(failed)} ejecución(es) fallida(s) recientemente.\n"
                        "Pulsa '🔄 Ver Estado y Errores' para más detalles,\n"
                        "o '🚀 Publicar Short Ahora' para relanzar inmediatamente."
                    )
        except Exception:
            pass

    # ── Publicar ──────────────────────────────────────────────────────────────

    def _publish_btn(self):
        threading.Thread(target=self._do_publish, daemon=True).start()

    def _do_publish(self):
        self._sys("Lanzando publicación de video en GitHub Actions...")
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            r = requests.post(
                f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
                "/actions/workflows/publish_shorts.yml/dispatches",
                headers=headers,
                json={"ref": "main", "inputs": {"lang": "es", "content_type": "tarot"}},
                timeout=15
            )
            if r.status_code == 204:
                self._agent(
                    "🎉 ¡Video enviado a publicar exitosamente!\n\n"
                    "GitHub Actions está generando ahora mismo:\n"
                    "• ✍️ Guion con IA\n"
                    "• 🎙️ Voz de Camila\n"
                    "• 🎬 Fondo cósmico animado + subtítulos\n"
                    "• 📤 Subida a YouTube\n\n"
                    "En aproximadamente 2–3 minutos aparecerá en tu canal."
                )
            else:
                self._agent(f"Hubo un error al lanzar la publicación (HTTP {r.status_code}). "
                            "Verifica que el token de GitHub siga activo.")
        except Exception as e:
            self._agent(f"Error de red al intentar publicar: {e}")

    # ── Canal ─────────────────────────────────────────────────────────────────

    def _open_channel(self):
        webbrowser.open("https://www.youtube.com/@OraculoDiario")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = OracloChatApp(root)
    root.mainloop()
