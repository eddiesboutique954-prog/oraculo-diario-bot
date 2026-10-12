"""
🔮 Panel de Control y Chat con el Agente de Tarot Bot
Aplicación de escritorio interactiva para:
1. Ver el estado de publicaciones en GitHub Actions y YouTube en tiempo real.
2. Forzar la generación y publicación de un video de inmediato con 1 clic.
3. Conversar en lenguaje natural con el Agente para diagnosticar errores, cambiar temas o pedir reportes.
"""

import os
import sys
import json
import threading
import subprocess
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Configuración del bot
BOT_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_TOKEN = "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"
GITHUB_OWNER = "eddiesboutique954-prog"
GITHUB_REPO = "oraculo-diario-bot"
OPENROUTER_KEY = "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"

class TarotBotChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔮 Oráculo Diario — Centro de Control y Chat del Agente")
        self.root.geometry("860x680")
        self.root.minsize(700, 500)
        self.root.configure(bg="#0f0c1b")

        self._setup_styles()
        self._build_ui()
        self._append_agent_message(
            "¡Hola! Soy tu Agente del canal Oráculo Diario.\n"
            "Estoy monitoreando tus publicaciones automáticas en YouTube y GitHub Actions.\n\n"
            "¿Qué deseas hacer hoy? Puedes preguntarme:\n"
            "• '¿Cuál es el estado de las publicaciones?'\n"
            "• '¿Hubo algún error hoy?'\n"
            "• 'Publica un video de tarot ahora mismo'\n"
            "• '¿A qué hora sale el próximo video?'"
        )
        self.check_github_status_async()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0f0c1b")
        style.configure("Header.TLabel", background="#0f0c1b", foreground="#ffd700", font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", background="#1a142e", foreground="#e0e0e0", font=("Segoe UI", 10))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background="#7b2cbf", foreground="#ffffff")

    def _build_ui(self):
        # 1. Encabezado superior
        header_frame = tk.Frame(self.root, bg="#1a142e", padx=15, pady=12)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(header_frame, text="🔮 Oráculo Diario Bot — Asistente Inteligente",
                             bg="#1a142e", fg="#ffd700", font=("Segoe UI", 15, "bold"))
        title_lbl.pack(side="left")

        self.status_indicator = tk.Label(header_frame, text="🟢 Conectado con GitHub Actions",
                                         bg="#1a142e", fg="#00ff88", font=("Segoe UI", 10, "bold"))
        self.status_indicator.pack(side="right")

        # 2. Barra de acciones rápidas
        btn_frame = tk.Frame(self.root, bg="#0f0c1b", padx=15, pady=8)
        btn_frame.pack(fill="x")

        btn_status = tk.Button(btn_frame, text="🔄 Verificar Estado / Errores", bg="#2a1b4e", fg="#ffffff",
                               font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5,
                               command=self.check_github_status_async)
        btn_status.pack(side="left", padx=5)

        btn_publish_now = tk.Button(btn_frame, text="🚀 Publicar Short Ahora Mismo", bg="#7b2cbf", fg="#ffffff",
                                    font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5,
                                    command=self.trigger_publish_now)
        btn_publish_now.pack(side="left", padx=5)

        btn_channel = tk.Button(btn_frame, text="📺 Abrir Mi Canal en YouTube", bg="#3a225d", fg="#ffd700",
                                font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5,
                                command=self.open_channel)
        btn_channel.pack(side="right", padx=5)

        # 3. Área de chat
        chat_frame = tk.Frame(self.root, bg="#0f0c1b", padx=15, pady=5)
        chat_frame.pack(fill="both", expand=True)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap="word", bg="#151026", fg="#f0f0f0",
            font=("Segoe UI", 11), insertbackground="#ffd700",
            relief="flat", padx=15, pady=15
        )
        self.chat_display.pack(fill="both", expand=True)
        self.chat_display.config(state="disabled")

        # Configurar colores de tags de texto
        self.chat_display.tag_config("agent", foreground="#e0d4fd")
        self.chat_display.tag_config("user", foreground="#ffd700")
        self.chat_display.tag_config("system", foreground="#00e5ff")
        self.chat_display.tag_config("error", foreground="#ff5555")

        # 4. Campo de entrada de mensaje
        input_frame = tk.Frame(self.root, bg="#1a142e", padx=15, pady=10)
        input_frame.pack(fill="x")

        self.user_input = tk.Entry(input_frame, bg="#261d42", fg="#ffffff",
                                   font=("Segoe UI", 12), relief="flat", insertbackground="#ffd700")
        self.user_input.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 10))
        self.user_input.bind("<Return>", lambda event: self.send_message())

        btn_send = tk.Button(input_frame, text="Enviar ➤", bg="#9d4edd", fg="#ffffff",
                             font=("Segoe UI", 10, "bold"), relief="flat", padx=16, pady=6,
                             command=self.send_message)
        btn_send.pack(side="right")

    def _append_message(self, sender: str, text: str, tag: str = "agent"):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"\n{sender}:\n", tag)
        self.chat_display.insert("end", f"{text}\n")
        self.chat_display.see("end")
        self.chat_display.config(state="disabled")

    def _append_agent_message(self, text: str):
        self._append_message("🔮 Agente Oráculo Diario", text, "agent")

    def _append_user_message(self, text: str):
        self._append_message("👤 Tú", text, "user")

    def send_message(self):
        msg = self.user_input.get().strip()
        if not msg:
            return
        self.user_input.delete(0, "end")
        self._append_user_message(msg)

        # Procesar en segundo plano para no congelar la ventana
        threading.Thread(target=self._process_user_message, args=(msg,), daemon=True).start()

    def _process_user_message(self, text: str):
        lower = text.lower()

        # Comandos directos de acción rápida
        if any(w in lower for w in ["publicar", "subir video", "publica ahora", "lanza video"]):
            self.trigger_publish_now()
            return

        if any(w in lower for w in ["estado", "status", "error", "errores", "fallo", "falló", "qué pasó"]):
            self.check_github_status_async()
            return

        if any(w in lower for w in ["horario", "hora", "cuándo", "proximo", "próximo"]):
            self._append_agent_message(
                "📅 Horarios de publicación programados (Hora Colombia UTC-5):\n"
                "• ☀️ 8:00 AM — Tarot del Día\n"
                "• 🍽️ 12:00 PM — Zodíaco / Energías\n"
                "• 🌇 5:00 PM — Reflexión y Sanación\n"
                "• 🌙 9:00 PM — Mensaje de Advertencia / Cierre Nocturno\n\n"
                "Cada video se publica de forma 100% automática en GitHub Actions."
            )
            return

        # Para preguntas generales, consultar con la IA (OpenRouter)
        self._query_agent_ai(text)

    def _query_agent_ai(self, user_prompt: str):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }
        system_prompt = (
            "Eres el Agente de Control de 'Oráculo Diario', un canal automatizado de YouTube Shorts de tarot y espiritualidad. "
            "Responde de forma amable, empática, concisa y profesional en español. "
            "Ayuda al usuario a entender cómo funciona el bot, diagnosticar dudas sobre las publicaciones o dar consejos para crecer."
        )
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "nvidia/nemotron-3.5-lightning:free",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 400
                },
                timeout=25
            )
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                self.root.after(0, self._append_agent_message, answer)
            else:
                self.root.after(0, self._append_agent_message, "Estoy activo y monitoreando el canal. Si necesitas forzar una publicación o revisar el estado, usa los botones superiores.")
        except Exception as e:
            self.root.after(0, self._append_agent_message, f"Nota del sistema: Conectado localmente. ({e})")

    def check_github_status_async(self):
        self._append_message("⚙️ Sistema", "Consultando estado de las últimas ejecuciones en GitHub Actions...", "system")
        threading.Thread(target=self._check_github_status, daemon=True).start()

    def _check_github_status(self):
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            r = requests.get(f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs", headers=headers, timeout=15)
            if r.status_code == 200:
                runs = r.json().get("workflow_runs", [])[:3]
                report = "📊 Estado de las últimas publicaciones:\n\n"
                for idx, run in enumerate(runs, 1):
                    run_id = run.get("id")
                    status = run.get("status")
                    conclusion = run.get("conclusion") or "En ejecución"
                    icon = "✅" if conclusion == "success" else ("❌" if conclusion == "failure" else "⏳")
                    report += f"{idx}. {icon} Run #{run_id} — Estado: {status} | Resultado: {conclusion}\n"

                report += "\nSi alguna falló, puedes hacer clic en 'Publicar Short Ahora Mismo' para resolverlo de inmediato."
                self.root.after(0, self._append_agent_message, report)
            else:
                self.root.after(0, self._append_agent_message, f"No se pudo consultar GitHub Actions (Código {r.status_code}).")
        except Exception as e:
            self.root.after(0, self._append_agent_message, f"Error al conectar con GitHub: {e}")

    def trigger_publish_now(self):
        self._append_message("🚀 Acción", "Lanzando generación y publicación inmediata en GitHub Actions...", "system")
        threading.Thread(target=self._dispatch_publish, daemon=True).start()

    def _dispatch_publish(self):
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        try:
            r = requests.post(
                f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/publish_shorts.yml/dispatches",
                headers=headers,
                json={"ref": "main", "inputs": {"lang": "es", "content_type": "tarot"}},
                timeout=15
            )
            if r.status_code == 204:
                msg = (
                    "🎉 ¡Publicación lanzada exitosamente en la nube!\n\n"
                    "El bot está generando el guion, la voz de Camila, los subtítulos y subiendo el video a YouTube ahora mismo.\n"
                    "En aproximadamente 2 minutos estará publicado en tu canal."
                )
                self.root.after(0, self._append_agent_message, msg)
            else:
                self.root.after(0, self._append_agent_message, f"Hubo un inconveniente al lanzar la acción ({r.status_code}).")
        except Exception as e:
            self.root.after(0, self._append_agent_message, f"Error de conexión: {e}")

    def open_channel(self):
        import webbrowser
        webbrowser.open("https://www.youtube.com/channel/UCvjSasYQoo9DHd-u-OkUefA")

if __name__ == "__main__":
    root = tk.Tk()
    app = TarotBotChatApp(root)
    root.mainloop()
