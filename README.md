# 🔮 Tarot YouTube Shorts Bot (Automatización 100% en la Nube)

Sistema autónomo que genera videos verticales (Shorts) de **Lectura de Tarot y Mensajes Diarios** en **Español e Inglés**, creando la miniatura, guion, voz, imágenes místicas y subiéndolos automáticamente a YouTube.

Funciona en la nube 24/7 con **GitHub Actions** (gratis) sin necesidad de tener tu computadora encendida.

---

## 📁 Estructura del Proyecto

```
tarot-youtube-bot/
├── .github/workflows/
│   └── publish_shorts.yml       # Programación en la nube (2 veces al día)
├── generators/
│   ├── script_generator.py      # Guion y prompts místicos con GPT-4o
│   ├── image_generator.py       # Imágenes oscuras/doradas con DALL-E 3
│   └── voice_generator.py       # Narración mística con Edge-TTS (Gratis)
├── thumbnail/
│   └── creator.py               # Generación automática de miniaturas con Pillow
├── video/
│   └── assembler.py             # Montaje de video vertical con FFmpeg/MoviePy
├── youtube/
│   └── uploader.py              # Subida con YouTube Data API v3 y SEO
├── config.py                    # Ajustes de canales, temas e idiomas
├── setup_youtube.py             # Asistente para conectar tu canal de YouTube
├── main.py                      # Orquestador general
└── requirements.txt             # Librerías de Python
```

---

## 🛠️ Paso 1: Probar localmente en tu PC (Opcional)

1. Abre una terminal en esta carpeta:
   ```bash
   pip install -r requirements.txt
   ```
2. Define tu API key de OpenAI en tu terminal:
   ```powershell
   $env:OPENAI_API_KEY="tu-api-key-aqui"
   ```
3. Genera un video de prueba en tu computadora (sin subirlo a YouTube):
   ```bash
   python main.py --lang es
   ```
   *(El video resultante y la miniatura aparecerán en la carpeta `output/`)*

---

## ☁️ Paso 2: Ponerlo a Trabajar en la Nube 24/7 (GitHub Actions Gratis)

Para que funcione **mientras viajas o tienes tu PC apagada**:

1. **Crea un repositorio privado en GitHub**:
   - Ve a [github.com/new](https://github.com/new)
   - Nómbralo `tarot-bot` y márcalo como **Private**.
   - Sube todos los archivos de esta carpeta a ese repositorio.

2. **Configura tus Secretos en GitHub**:
   - En tu repositorio ve a **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.
   - Añade los siguientes secretos:
     - `OPENAI_API_KEY`: Tu clave de OpenAI.
     - `YOUTUBE_TOKEN_JSON`: El contenido íntegro del archivo `youtube_token.json` (obtenido tras ejecutar `python setup_youtube.py`).

3. **¡Listo!**:
   - GitHub Actions se activará automáticamente **2 veces al día** (a las 8:00 AM y 8:00 PM).
   - Generará los 2 Shorts (uno en español y uno en inglés) y los publicará en tu canal de YouTube automáticamente.
