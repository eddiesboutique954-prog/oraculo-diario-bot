"""
🖼️ Miniaturas Virales de Alto CTR con Carta Real del Tarot
Diseño cinematográfico: oscuro, misterioso, tipografía impactante
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from config import THUMBNAIL_CONFIG, OUTPUT_DIR
from generators.tarot_deck import get_real_tarot_card_image

def create_tarot_thumbnail(title: str, lang: str = "es",
                            card_name: str = "La Muerte",
                            bg_image_path: str = None) -> str:
    width = THUMBNAIL_CONFIG["width"]
    height = THUMBNAIL_CONFIG["height"]

    # Fondo degradado cinematográfico
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for x in range(width):
        ratio = x / width
        r = int(8 + 30 * ratio)
        g = int(3 + 12 * ratio)
        b = int(20 + 55 * ratio)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))

    # Estrellas de fondo
    random.seed(42)
    for _ in range(180):
        sx = random.randint(0, width)
        sy = random.randint(0, height)
        sz = random.randint(1, 3)
        draw.ellipse([sx-sz, sy-sz, sx+sz, sy+sz], fill=(200, 200, 255))

    # ── Carta real de tarot (derecha, grande) ─────────────────────────────
    card_path = get_real_tarot_card_image(card_name)
    if card_path and os.path.exists(card_path):
        card = Image.open(card_path).convert("RGBA")
        target_h = height - 40
        target_w = int(target_h * (card.width / card.height))
        card = card.resize((target_w, target_h), Image.LANCZOS)

        # Aura dorada
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        card_x = width - target_w - 15
        card_y = 20
        for off in range(30, 0, -4):
            alpha = int(55 * (1 - off / 30))
            gd.rounded_rectangle([card_x - off, card_y - off,
                                   card_x + target_w + off, card_y + target_h + off],
                                  radius=18, fill=(255, 215, 0, alpha))
        img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        draw = ImageDraw.Draw(img)

        # Marco dorado
        draw.rounded_rectangle([card_x - 6, card_y - 6,
                                 card_x + target_w + 6, card_y + target_h + 6],
                                radius=12, fill=(15, 8, 30), outline=(255, 215, 0), width=6)
        img.paste(card, (card_x, card_y), mask=card)
        draw = ImageDraw.Draw(img)

    # ── Tipografía izquierda ───────────────────────────────────────────────
    try:
        font_badge = ImageFont.truetype("arialbd.ttf", 28)
        font_big   = ImageFont.truetype("arialbd.ttf", 82)
        font_sub   = ImageFont.truetype("arialbd.ttf", 34)
    except:
        font_badge = font_big = font_sub = ImageFont.load_default()

    # Badge rojo de urgencia
    badge_text = "MENSAJE URGENTE" if lang == "es" else "URGENT MESSAGE"
    draw.rounded_rectangle([40, 40, 390, 88], radius=8, fill=(200, 10, 10))
    draw.text((215, 64), badge_text, font=font_badge, fill=(255, 255, 255), anchor="mm")

    # Título principal en 2-3 líneas, letras grandes doradas
    words = title.upper().replace("🔮","").replace("🌕","").replace("⚡","").replace("🌍","").strip().split()
    lines, curr = [], ""
    for w in words:
        if len(curr + " " + w) <= 13:
            curr = (curr + " " + w).strip()
        else:
            if curr: lines.append(curr)
            curr = w
    if curr: lines.append(curr)
    lines = lines[:3]

    y_start = 130
    for i, line in enumerate(lines):
        y = y_start + i * 95
        # Sombra
        draw.text((55, y + 4), line, font=font_big, fill=(0, 0, 0))
        # Texto dorado
        draw.text((52, y), line, font=font_big, fill=(255, 218, 50))

    # Nombre de la carta en la parte inferior izquierda
    draw.line([(40, height - 95), (480, height - 95)], fill=(255, 215, 0), width=2)
    card_display = f"CARTA: {card_name.upper()}" if lang == "es" else f"CARD: {card_name.upper()}"
    draw.text((52, height - 75), card_display, font=font_sub, fill=(255, 215, 0))

    # Borde exterior dorado fino
    draw.rectangle([8, 8, width - 8, height - 8], outline=(255, 215, 0), width=4)

    lang_suffix = lang
    output_path = os.path.join(OUTPUT_DIR, f"thumbnail_{lang_suffix}.jpg")
    img.save(output_path, "JPEG", quality=96)
    print(f"[MINIATURA] Miniatura cinematografica creada: {output_path}")
    return output_path
