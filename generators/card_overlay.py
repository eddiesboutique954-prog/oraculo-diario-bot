"""
🎨 Compositor de Cartas Transparentes con Aura Pulsante para Animación 3D
Genera capas transparentes (PNG con canal Alfa) con la carta del tarot,
su marco dorado resplandeciente y títulos de gancho para superponer sobre
el fondo en movimiento y aplicar efectos dinámicos de cámara y zoom.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from config import TEMP_DIR
from generators.tarot_deck import get_real_tarot_card_image

def _get_fonts():
    fonts = {}
    candidates = ["arialbd.ttf", "arial.ttf", "Arial_Bold.ttf", "Arial.ttf"]
    for name, size in [("hero", 85), ("title", 64), ("sub", 44), ("badge", 32)]:
        for fname in candidates:
            try:
                fonts[name] = ImageFont.truetype(fname, size)
                break
            except:
                pass
        if name not in fonts:
            fonts[name] = ImageFont.load_default()
    return fonts

def create_card_overlay(card_name: str, hook_text: str = "",
                        width: int = 1080, height: int = 1920,
                        output_dir: str = TEMP_DIR) -> str:
    """Crea una imagen transparente PNG con la carta real y los ganchos de texto"""
    os.makedirs(output_dir, exist_ok=True)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    fonts = _get_fonts()

    card_path = get_real_tarot_card_image(card_name)
    if card_path and os.path.exists(card_path):
        card = Image.open(card_path).convert("RGBA")
        
        # Tamaño generoso de la carta
        target_w = int(width * 0.70)
        aspect = card.height / card.width
        target_h = int(target_w * aspect)
        max_h = int(height * 0.54)
        if target_h > max_h:
            target_h = max_h
            target_w = int(target_h / aspect)

        card = card.resize((target_w, target_h), Image.LANCZOS)
        card_rgb = ImageEnhance.Contrast(card.convert("RGB")).enhance(1.25)
        card_rgb = ImageEnhance.Color(card_rgb).enhance(1.35)
        card = Image.merge("RGBA", (*card_rgb.split(), card.split()[3]))

        cx = (width - target_w) // 2
        cy = int(height * 0.28)

        # Resplandor dorado místico multicapa
        draw = ImageDraw.Draw(overlay)
        for off in range(45, 0, -3):
            alpha = int(75 * ((45 - off) / 45) ** 0.6)
            draw.rounded_rectangle(
                [cx - off, cy - off, cx + target_w + off, cy + target_h + off],
                radius=25, fill=(255, 215, 0, alpha)
            )

        # Marco dorado con bisel
        draw.rounded_rectangle(
            [cx - 10, cy - 10, cx + target_w + 10, cy + target_h + 10],
            radius=18, fill=(12, 6, 22, 230), outline=(255, 215, 0, 255), width=9
        )
        draw.rounded_rectangle(
            [cx - 4, cy - 4, cx + target_w + 4, cy + target_h + 4],
            radius=12, outline=(255, 245, 190, 220), width=2
        )

        overlay.paste(card, (cx, cy), mask=card)

        # Nombre de la carta debajo con ornamento
        font_b = fonts["badge"]
        name_y = cy + target_h + 35
        mx = width // 2
        
        draw.line([(mx - 180, name_y - 10), (mx + 180, name_y - 10)], fill=(255, 215, 0, 240), width=2)
        # Sombra
        draw.text((mx + 2, name_y + 2), f"✦ {card_name.upper()} ✦", font=font_b, fill=(0, 0, 0, 255), anchor="mt")
        draw.text((mx, name_y), f"✦ {card_name.upper()} ✦", font=font_b, fill=(255, 225, 90, 255), anchor="mt")
        draw.line([(mx - 180, name_y + 45), (mx + 180, name_y + 45)], fill=(255, 215, 0, 240), width=2)

    # Hook visual en la parte superior
    if hook_text:
        clean = hook_text.replace("🔮", "").replace("✨", "").strip()
        font_t = fonts["title"]
        words = clean.split()
        lines, curr = [], ""
        for w in words:
            if len(curr + " " + w) <= 24:
                curr = (curr + " " + w).strip()
            else:
                if curr: lines.append(curr)
                curr = w
        if curr: lines.append(curr)
        lines = lines[:2]

        draw = ImageDraw.Draw(overlay)
        y = 75
        for line in lines:
            mx = width // 2
            # Sombra de alto contraste
            for sx, sy in [(-3, 3), (3, 3), (0, 4)]:
                draw.text((mx + sx, y + sy), line.upper(), font=font_t, fill=(0, 0, 0, 255), anchor="mt")
            draw.text((mx, y), line.upper(), font=font_t, fill=(255, 255, 255, 255), anchor="mt")
            bbox = draw.textbbox((mx, y), line.upper(), font=font_t, anchor="mt")
            draw.line([(bbox[0] - 8, bbox[3] + 6), (bbox[2] + 8, bbox[3] + 6)], fill=(255, 215, 0, 230), width=3)
            y += bbox[3] - bbox[1] + 20

    out_file = os.path.join(output_dir, "card_overlay.png")
    overlay.save(out_file, "PNG")
    return out_file
