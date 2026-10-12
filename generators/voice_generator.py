"""
🎙️ Generador de Voz y Subtítulos Dinámicos
Usa gTTS (Google TTS) como proveedor principal — gratuito, estable, sin WebSocket.
Genera subtítulos .srt estimados por duración del audio.
"""

import os
import re
import wave
import struct
import subprocess
from mutagen.mp3 import MP3
from config import VOICE_CONFIG, TEMP_DIR


# ── Helper: duración de audio ─────────────────────────────────────────────────

def get_audio_duration(audio_path: str) -> float:
    try:
        return float(MP3(audio_path).info.length)
    except Exception:
        return 30.0


# ── Generador de subtítulos estimados ────────────────────────────────────────

def _srt_timecode(seconds: float) -> str:
    """Convierte segundos a formato SRT hh:mm:ss,mmm"""
    ms = int((seconds % 1) * 1000)
    s = int(seconds) % 60
    m = int(seconds // 60) % 60
    h = int(seconds // 3600)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _generate_srt_from_audio(text: str, audio_path: str, srt_path: str):
    """
    Genera un .srt estimando el tiempo de cada grupo de palabras
    según la duración total del audio. Sin depender de edge-tts.
    """
    total_duration = get_audio_duration(audio_path)

    # Limpiar texto y dividir en palabras
    clean_text = re.sub(r"[*_~`#]", "", text).strip()
    words = clean_text.split()
    if not words:
        open(srt_path, "w", encoding="utf-8").close()
        return

    # Agrupar de 3 en 3 palabras por segmento (estilo Shorts/TikTok)
    GROUP_SIZE = 3
    segments = []
    for i in range(0, len(words), GROUP_SIZE):
        segments.append(" ".join(words[i:i + GROUP_SIZE]))

    seg_duration = total_duration / len(segments)

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, start=1):
            t_start = idx * seg_duration - seg_duration
            t_end   = idx * seg_duration - 0.05
            f.write(f"{idx}\n")
            f.write(f"{_srt_timecode(t_start)} --> {_srt_timecode(t_end)}\n")
            f.write(f"{seg}\n\n")

    print(f"[SUBTITULOS] {len(segments)} segmentos → {srt_path}")


# ── Generador principal con reintentos ────────────────────────────────────────

def _gtts_generate(text: str, lang_code: str, audio_path: str, retries: int = 3):
    """Genera audio MP3 con gTTS con reintentos automáticos."""
    from gtts import gTTS
    import time

    for attempt in range(1, retries + 1):
        try:
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(audio_path)
            print(f"[VOZ] Audio generado con gTTS (intento {attempt}): {audio_path}")
            return True
        except Exception as e:
            print(f"[VOZ] Intento {attempt}/{retries} fallido: {e}")
            if attempt < retries:
                time.sleep(3 * attempt)
    return False


def _ffmpeg_tts_fallback(text: str, audio_path: str):
    """
    Fallback usando espeak-ng vía FFmpeg si gTTS también falla.
    Solo disponible en Linux (GitHub Actions).
    """
    try:
        cmd = [
            "espeak-ng", "-v", "es", "-s", "150",
            "--ipa", "-q",
            "-w", audio_path.replace(".mp3", ".wav"),
            text[:500]
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=30)
        if res.returncode == 0:
            # Convertir WAV a MP3
            wav_path = audio_path.replace(".mp3", ".wav")
            subprocess.run(
                ["ffmpeg", "-y", "-i", wav_path, audio_path],
                capture_output=True
            )
            print("[VOZ] Fallback espeak-ng activado.")
            return True
    except Exception as e:
        print(f"[VOZ] espeak fallback falló: {e}")
    return False


# ── API pública ───────────────────────────────────────────────────────────────

def generate_voice(text: str, lang: str = "es", output_dir: str = TEMP_DIR) -> tuple:
    """
    Genera (audio_mp3_path, srt_path).
    Proveedor: gTTS (Google TTS) → fallback espeak-ng.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Código de idioma para gTTS
    gtts_lang = "es" if lang.startswith("es") else "en"

    audio_path = os.path.join(output_dir, f"narration_{lang}.mp3")
    srt_path   = os.path.join(output_dir, f"subtitles_{lang}.srt")

    print(f"[VOZ] Generando locucion con gTTS (idioma: {gtts_lang})...")

    ok = _gtts_generate(text, gtts_lang, audio_path)
    if not ok:
        print("[VOZ] gTTS falló, intentando espeak-ng...")
        ok = _ffmpeg_tts_fallback(text, audio_path)

    if not ok or not os.path.exists(audio_path):
        raise RuntimeError("[VOZ] No se pudo generar el audio. Todos los proveedores fallaron.")

    _generate_srt_from_audio(text, audio_path, srt_path)
    return audio_path, srt_path
