"""
🎙️ Generador de Voz Mística (Edge-TTS - 100% GRATIS)
Compatible con consolas Windows sin errores de codificación.
"""

import asyncio
import os
import edge_tts
from config import VOICE_CONFIG, TEMP_DIR

async def _generate_voice_async(text: str, voice: str, rate: str,
                                 pitch: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)

def generate_voice(text: str, lang: str = "es", output_dir: str = TEMP_DIR) -> str:
    os.makedirs(output_dir, exist_ok=True)
    voice = VOICE_CONFIG.get(lang, "es-MX-DaliaNeural")
    rate = VOICE_CONFIG.get("rate", "-5%")
    pitch = VOICE_CONFIG.get("pitch", "-10Hz")
    output = os.path.join(output_dir, f"narration_{lang}.mp3")

    print(f"[VOZ] Generando locucion con {voice}...")
    asyncio.run(_generate_voice_async(text, voice, rate, pitch, output))
    print(f"[VOZ] Audio generado exitosamente: {output}")
    return output

def get_audio_duration(audio_path: str) -> float:
    try:
        from mutagen.mp3 import MP3
        audio = MP3(audio_path)
        return float(audio.info.length)
    except Exception:
        return 30.0
