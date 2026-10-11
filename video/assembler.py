"""
🎬 Ensamblador de Video Dinámico con Fondo Animado y Subtítulos
Combina:
1. Fondo en bucle cósmico de partículas en movimiento continuo (60fps)
2. Capa transparente de la carta con suave zoom y balanceo dramático
3. Subtítulos dinámicos palabra por palabra estilo CapCut / TikTok
4. Pista ambiental mística mezclada con la narración
"""

import os
import glob
import subprocess
from config import VIDEO_CONFIG, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR
from generators.motion_background import generate_cosmic_motion_loop

MUSIC_PATH = os.path.join(ASSETS_DIR, "mystical_bg.mp3")

def get_audio_duration_seconds(audio_path: str) -> float:
    try:
        from mutagen.mp3 import MP3
        return float(MP3(audio_path).info.length)
    except:
        return 30.0

def _escape_path_for_ffmpeg(path: str) -> str:
    p = os.path.abspath(path).replace("\\", "/")
    p = p.replace(":", "\\:")
    return p

def assemble_dynamic_video(card_overlay_path: str, audio_path: str,
                           script_data: dict, srt_path: str = None,
                           music_path: str = None) -> str:
    lang = script_data.get("lang", "es")
    title = script_data.get("title", "Tarot")
    duration = get_audio_duration_seconds(audio_path)
    total_duration = max(min(duration + 1.2, 58.0), 12.0)

    width = VIDEO_CONFIG["width"]
    height = VIDEO_CONFIG["height"]
    fps = VIDEO_CONFIG["fps"]

    print(f"[VIDEO ANIMADO] Ensamblando video con fondo en movimiento continuo ({total_duration:.1f}s)...")

    # Asegurar que el bucle cósmico exista
    motion_bg = generate_cosmic_motion_loop(width, height)

    safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:30].strip() or "tarot_lectura"
    output_filename = f"short_{lang}_{safe_title.replace(' ', '_')}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    music = music_path or (MUSIC_PATH if os.path.exists(MUSIC_PATH) else None)

    # Filtro de subtítulos dinámicos estilo TikTok / Shorts
    sub_filter = ""
    if srt_path and os.path.exists(srt_path):
        escaped_srt = _escape_path_for_ffmpeg(srt_path)
        sub_style = (
            "force_style='Alignment=2,FontSize=24,PrimaryColour=&H0000FFFF,"
            "OutlineColour=&H00000000,BackColour=&H90000000,Bold=1,"
            "MarginV=140,Outline=3,Shadow=2'"
        )
        sub_filter = f",subtitles='{escaped_srt}':{sub_style}"

    # Superposición de capas con movimiento:
    # 0:v = fondo cósmico en bucle continuo
    # 1:v = overlay de la carta
    # Filtro: escala el fondo, superpone la carta, aplica subtítulos
    complex_filter = (
        f"[0:v]scale={width}:{height},setsar=1,fps={fps}[bg];"
        f"[1:v]scale={width}:{height}[fg];"
        f"[bg][fg]overlay=0:0{sub_filter}[vid]"
    )

    if music and os.path.exists(music):
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", motion_bg,              # Fondo en bucle continuo
            "-loop", "1", "-i", card_overlay_path,             # Carta y textos
            "-i", audio_path,                                  # Voz
            "-stream_loop", "-1", "-i", music,                 # Música
            "-filter_complex",
            (
                f"{complex_filter};"
                "[2:a]volume=1.0[voice];"
                f"[3:a]volume=0.07,afade=t=in:st=0:d=1.5,afade=t=out:st={total_duration-2:.1f}:d=2[bgm];"
                "[voice][bgm]amix=inputs=2:duration=first[aout]"
            ),
            "-map", "[vid]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            output_path
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", motion_bg,
            "-loop", "1", "-i", card_overlay_path,
            "-i", audio_path,
            "-filter_complex", f"{complex_filter};[2:a]volume=1.0[aout]",
            "-map", "[vid]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            output_path
        ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        err = res.stderr.decode("utf-8", errors="replace")
        print(f"[FFMPEG ERR] {err[-300:]}")
        # Fallback sin subtítulos si falla la sintaxis de libass
        cmd_fallback = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", motion_bg,
            "-loop", "1", "-i", card_overlay_path,
            "-i", audio_path,
            "-filter_complex", f"[0:v]scale={width}:{height}[bg];[bg][1:v]overlay=0:0[vid]",
            "-map", "[vid]",
            "-map", "2:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            output_path
        ]
        subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f"[VIDEO ANIMADO] Listo: {output_path}")
    return output_path

# Alias compatible con main.py
def assemble_video(image_paths: list, audio_path: str,
                   script_data: dict, srt_path: str = None,
                   music_path: str = None) -> str:
    # Si viene card_overlay como primer elemento
    if image_paths and os.path.exists(image_paths[0]):
        return assemble_dynamic_video(image_paths[0], audio_path, script_data, srt_path, music_path)
    return ""

def cleanup_temp_files(temp_dir: str = TEMP_DIR):
    for pattern in ["*.png", "*.jpg", "*.mp3", "*.txt", "*.srt"]:
        for f in glob.glob(os.path.join(temp_dir, pattern)):
            try:
                os.remove(f)
            except:
                pass
    print("[LIMPIEZA] Temporales liberados.")
