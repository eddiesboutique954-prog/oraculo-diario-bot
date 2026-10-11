"""
🚀 Orquestador Principal — Tarot YouTube Bot v3
"""

import sys
import os
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ACTIVE_LANGUAGES
from generators.script_generator import generate_script
from generators.image_generator import build_all_real_card_scenes
from generators.voice_generator import generate_voice
from thumbnail.creator import create_tarot_thumbnail
from video.assembler import assemble_video, cleanup_temp_files


def run_pipeline(language="es", content_type=None, card=None, sign=None, upload=False):
    print("\n" + "=" * 60)
    print(f"[BOT VIRAL] INICIANDO SHORT [{language.upper()}]")
    print(f"[BOT VIRAL] Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Generar guion emocional con situación viral
    print("[GUION] Generando guion emocional viral...")
    script_data = generate_script(lang=language, content_type=content_type,
                                  card=card, sign=sign)

    cards = script_data.get("cards", ["La Luna"])
    title = script_data.get("title", "Mensaje del Universo")
    hook = script_data.get("hook", "")
    ctype = script_data.get("content_type", "tarot")
    situacion = script_data.get("situacion", "")

    print(f"[TIPO]   {ctype.upper()}")
    print(f"[TITULO] {title}")
    print(f"[HOOK]   {hook}")
    print(f"[CARTA]  {cards[0]}")
    if situacion:
        print(f"[TEMA]   {situacion[:60]}")

    # 2. Voz neural
    audio_path = generate_voice(script_data["script"], lang=language)

    # 3. Escenas cinematográficas (1 sola carta)
    print("[ESCENAS] Componiendo escenas cinematograficas...")
    captions = script_data.get("caption_lines", [])
    image_paths = build_all_real_card_scenes(
        cards,
        caption_lines=captions,
        hook=hook
    )

    # 4. Miniatura viral
    lead_card = cards[0] if cards else "La Luna"
    thumbnail_path = create_tarot_thumbnail(
        title=title,
        lang=language,
        card_name=lead_card
    )

    # 5. Ensamblaje FFmpeg con música
    video_path = assemble_video(image_paths, audio_path, script_data)

    # 6. Subida YouTube opcional
    if upload:
        try:
            from youtube.uploader import upload_video_to_youtube
            result = upload_video_to_youtube(video_path, thumbnail_path, script_data)
            print(f"[YOUTUBE] Publicado: {result.get('url', 'OK')}")
        except Exception as e:
            print(f"[YOUTUBE] Error: {e}")
            print(f"[YOUTUBE] Video guardado en: {video_path}")
    else:
        print("\n" + "*" * 60)
        print(f"[LISTO] Video: {video_path}")
        print(f"[LISTO] Miniatura: {thumbnail_path}")
        print("*" * 60)

    cleanup_temp_files()
    return video_path, thumbnail_path


def main():
    parser = argparse.ArgumentParser(description="Bot de Tarot para YouTube Shorts")
    parser.add_argument("--lang", choices=["es", "en", "all"], default="es")
    parser.add_argument("--type", choices=["tarot", "zodiaco", "reflexion"], default=None,
                        dest="content_type", help="Tipo de contenido")
    parser.add_argument("--card", type=str, default=None, help="Carta especifica")
    parser.add_argument("--sign", type=str, default=None, help="Signo zodiacal especifico")
    parser.add_argument("--upload", action="store_true", help="Subir a YouTube")

    args = parser.parse_args()
    languages = ACTIVE_LANGUAGES if args.lang == "all" else [args.lang]

    for lang in languages:
        run_pipeline(language=lang, content_type=args.content_type,
                     card=args.card, sign=args.sign, upload=args.upload)


if __name__ == "__main__":
    main()
