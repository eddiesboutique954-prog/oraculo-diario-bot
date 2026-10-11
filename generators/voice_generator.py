"""
🎙️ Generador de Voz Mística y Subtítulos Dinámicos Sincronizados
Genera tanto el archivo MP3 como el archivo de subtítulos (.srt / .ass)
con marcas de tiempo palabra por palabra para retención máxima.
"""

import asyncio
import os
import edge_tts
from config import VOICE_CONFIG, TEMP_DIR

async def _generate_voice_and_subs(text: str, voice: str, rate: str,
                                   pitch: str, audio_path: str, srt_path: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    sub_maker = edge_tts.SubMaker()
    
    with open(audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                sub_maker.feed(chunk)
                
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(sub_maker.get_srt())

def generate_voice(text: str, lang: str = "es", output_dir: str = TEMP_DIR) -> tuple:
    os.makedirs(output_dir, exist_ok=True)
    voice = VOICE_CONFIG.get(lang, "es-CO-SalomeNeural")
    rate = VOICE_CONFIG.get("rate", "-3%")
    pitch = VOICE_CONFIG.get("pitch", "-4Hz")
    
    audio_path = os.path.join(output_dir, f"narration_{lang}.mp3")
    srt_path = os.path.join(output_dir, f"subtitles_{lang}.srt")

    print(f"[VOZ] Generando locucion y subtitulos sincronizados con {voice}...")
    asyncio.run(_generate_voice_and_subs(text, voice, rate, pitch, audio_path, srt_path))
    print(f"[VOZ] Audio: {audio_path}")
    print(f"[SUBTITULOS] Sincronizados: {srt_path}")
    return audio_path, srt_path

def get_audio_duration(audio_path: str) -> float:
    try:
        from mutagen.mp3 import MP3
        audio = MP3(audio_path)
        return float(audio.info.length)
    except Exception:
        return 30.0
