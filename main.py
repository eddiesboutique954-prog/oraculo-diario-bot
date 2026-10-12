"""
🚀 Orquestador Principal — Tarot YouTube Bot v4 (Resiliente y Auto-Recuperable)
"""

import sys
import os
import time
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ACTIVE_LANGUAGES
from generators.script_generator import generate_script
from generators.card_overlay import create_card_overlay
from generators.voice_generator import generate_voice
from thumbnail.creator import create_tarot_thumbnail
from video.assembler import assemble_dynamic_video, cleanup_temp_files

def _execute_pipeline_once(language="es", content_type=None, card=None, sign=None, upload=False):
    print("\n" + "=" * 60)
    print(f"[BOT VIRAL V4] GENERANDO SHORT DINÁMICO [{language.upper()}]")
    print(f"[BOT VIRAL V4] Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Generar guion viral con hook emocional
    print("[GUION] Generando guion con hook magnético...")
    script_data = generate_script(lang=language, content_type=content_type,
                                  card=card, sign=sign)

    cards = script_data.get("cards", ["La Estrella"])
    lead_card = cards[0]
    title = script_data.get("title", "Mensaje del Universo")
    hook = script_data.get("hook", "No fue casualidad que vieras esto")
    ctype = script_data.get("content_type", "tarot")

    print(f"[TIPO]   {ctype.upper()}")
    print(f"[TITULO] {title}")
    print(f"[HOOK]   {hook}")
    print(f"[CARTA]  {lead_card}")

    # 2. Voz neural y subtítulos sincronizados
    audio_path, srt_path = generate_voice(script_data["script"], lang=language)

    # 3. Capa transparente de la carta con aura y títulos de gancho
    print("[OVERLAY] Creando capa transparente con aura resplandeciente...")
    overlay_path = create_card_overlay(lead_card, hook_text=hook)

    # 4. Miniatura de alto CTR
    thumbnail_path = create_tarot_thumbnail(
        title=title,
        lang=language,
        card_name=lead_card
    )

    # 5. Ensamblaje con fondo en movimiento continuo y subtítulos
    video_path = assemble_dynamic_video(
        card_overlay_path=overlay_path,
        audio_path=audio_path,
        script_data=script_data,
        srt_path=srt_path
    )

    # 6. Subida a YouTube
    if upload:
        from youtube.uploader import upload_video_to_youtube
        result = upload_video_to_youtube(video_path, thumbnail_path, script_data)
        print(f"[YOUTUBE] Publicado exitosamente: {result.get('url', 'OK')}")
    else:
        print("\n" + "*" * 60)
        print(f"[COMPLETADO] Video Dinámico: {video_path}")
        print(f"[COMPLETADO] Miniatura:       {thumbnail_path}")
        print("*" * 60)

    cleanup_temp_files()
    return video_path, thumbnail_path

def run_pipeline_with_self_healing(language="es", content_type=None, card=None, sign=None, upload=False, max_attempts=3):
    """
    Ejecuta el pipeline con auto-recuperación interna:
    Si algún paso falla, limpia archivos temporales y reintenta
    automáticamente con un nuevo tema o configuración.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"\n🔄 [SELF-HEALING] Intento {attempt} de {max_attempts}...")
            return _execute_pipeline_once(language=language, content_type=content_type,
                                          card=card, sign=sign, upload=upload)
        except Exception as e:
            print(f"\n⚠️ [ERROR EN INTENTO {attempt}]: {e}")
            cleanup_temp_files()
            if attempt < max_attempts:
                wait_time = 10 * attempt
                print(f"⏳ Reintentando automáticamente en {wait_time}s con regeneración limpia...")
                time.sleep(wait_time)
            else:
                print("❌ [CRÍTICO] Se agotaron todos los intentos de auto-recuperación.")
                raise e

def main():
    parser = argparse.ArgumentParser(description="Bot de Tarot para YouTube Shorts v4")
    parser.add_argument("--lang", choices=["es", "en", "all"], default="es")
    parser.add_argument("--type", choices=["tarot", "zodiaco", "reflexion"], default=None,
                        dest="content_type", help="Tipo de contenido")
    parser.add_argument("--card", type=str, default=None, help="Carta específica")
    parser.add_argument("--sign", type=str, default=None, help="Signo zodiacal")
    parser.add_argument("--upload", action="store_true", help="Subir a YouTube")

    args = parser.parse_args()
    languages = ACTIVE_LANGUAGES if args.lang == "all" else [args.lang]

    for lang in languages:
        run_pipeline_with_self_healing(
            language=lang,
            content_type=args.content_type,
            card=args.card,
            sign=args.sign,
            upload=args.upload,
            max_attempts=3
        )

if __name__ == "__main__":
    main()
