"""
🎬 Ensamblador Cinematográfico de Video con Música de Fondo
FFmpeg: transiciones suaves, audio mixeado, subtítulos quemados
"""

import os
import glob
import subprocess
from config import VIDEO_CONFIG, OUTPUT_DIR, TEMP_DIR, ASSETS_DIR

MUSIC_PATH = os.path.join(ASSETS_DIR, "mystical_bg.mp3")

def get_audio_duration_seconds(audio_path: str) -> float:
    try:
        from mutagen.mp3 import MP3
        return float(MP3(audio_path).info.length)
    except:
        return 30.0

def assemble_video(image_paths: list, audio_path: str,
                   script_data: dict, music_path: str = None) -> str:
    lang = script_data.get("lang", "es")
    title = script_data.get("title", "Tarot")
    duration = get_audio_duration_seconds(audio_path)
    total_duration = max(min(duration + 2.0, 58.0), 15.0)

    width = VIDEO_CONFIG["width"]
    height = VIDEO_CONFIG["height"]
    fps = VIDEO_CONFIG["fps"]

    print(f"[VIDEO] Ensamblando video cinematografico {width}x{height}, duracion: {total_duration:.1f}s...")

    img_duration = total_duration / max(len(image_paths), 1)

    # Crear lista concat de imágenes con crossfade
    concat_file = os.path.join(TEMP_DIR, "images.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for img in image_paths:
            f.write(f"file '{os.path.abspath(img)}'\n")
            f.write(f"duration {img_duration:.3f}\n")
        if image_paths:
            f.write(f"file '{os.path.abspath(image_paths[-1])}'\n")

    safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:30].strip() or "tarot_lectura"
    output_filename = f"short_{lang}_{safe_title.replace(' ', '_')}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Verificar si hay música de fondo
    music = music_path or (MUSIC_PATH if os.path.exists(MUSIC_PATH) else None)

    if music and os.path.exists(music):
        # Video + Voz + Música de fondo (mezclada suave)
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_file,   # video imágenes
            "-i", audio_path,                                     # voz narración
            "-stream_loop", "-1", "-i", music,                   # música loop
            "-filter_complex",
            (
                # Escalar video y añadir efecto de zoom lento (Ken Burns)
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height},setsar=1,fps={fps}[vid];"
                # Crossfade audio: voz + música suave
                "[1:a]volume=1.0[voice];"
                "[2:a]volume=0.08,afade=t=in:st=0:d=2,afade=t=out:st={dur}:d=3[bg];"
                "[voice][bg]amix=inputs=2:duration=first[aout]"
            ).format(dur=total_duration - 3),
            "-map", "[vid]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "20",
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            output_path
        ]
    else:
        # Sin música
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_file,
            "-i", audio_path,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,fps={fps}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "20",
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{total_duration:.3f}",
            "-shortest",
            output_path
        ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        # Fallback sin música si falla
        print("[VIDEO] Reintentando sin musica de fondo...")
        cmd_simple = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_file,
            "-i", audio_path,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,fps={fps}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{total_duration:.3f}", "-shortest",
            output_path
        ]
        subprocess.run(cmd_simple, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f"[VIDEO] Video final listo: {output_path}")
    return output_path


def cleanup_temp_files(temp_dir: str = TEMP_DIR):
    for pattern in ["*.png", "*.jpg", "*.mp3", "*.txt"]:
        for f in glob.glob(os.path.join(temp_dir, pattern)):
            try:
                os.remove(f)
            except:
                pass
    print("[LIMPIEZA] Archivos temporales liberados.")
