"""
🎨 Compositor Cinematográfico v3 — Diseño que DETIENE el scroll
Inspirado en los canales de tarot con millones de vistas:
- Fondo negro profundo con destellos dorados
- Carta enorme, centrada, iluminada desde abajo
- Texto GRANDE en la parte superior (el hook)
- Texto de impacto en la parte inferior
- Partículas de luz flotantes
- Vignette cinematográfico muy pronunciado
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from config import TEMP_DIR
from generators.tarot_deck import get_real_tarot_card_image


def _get_fonts():
    """Fuentes con fallback seguro"""
    fonts = {}
    candidates = ["arialbd.ttf", "arial.ttf", "Arial_Bold.ttf", "Arial.ttf"]
    for name, size in [("hero", 85), ("title", 62), ("sub", 44), ("badge", 30), ("small", 24)]:
        for fname in candidates:
            try:
                fonts[name] = ImageFont.truetype(fname, size)
                break
            except:
                pass
        if name not in fonts:
            fonts[name] = ImageFont.load_default()
    return fonts


def _draw_cosmic_bg(img, width, height, dark_color=(5, 2, 12), accent=(120, 0, 200)):
    """Fondo negro cósmico con gradiente radial desde el centro"""
    draw = ImageDraw.Draw(img)
    cx, cy = width // 2, height // 2

    for y in range(height):
        t = y / height
        # Negro muy profundo con toque morado en el centro vertical
        mid = math.sin(t * math.pi)
        r = int(dark_color[0] + accent[0] * 0.08 * mid)
        g = int(dark_color[1] + accent[1] * 0.02 * mid)
        b = int(dark_color[2] + accent[2] * 0.15 * mid)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img


def _draw_particles(draw, width, height, seed=0, color=(255, 200, 0)):
    """Partículas de luz doradas flotando"""
    random.seed(seed)
    for _ in range(300):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        alpha_factor = random.uniform(0.3, 1.0)
        c = tuple(int(v * alpha_factor) for v in color)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=c)

        # Cruz de luz para partículas grandes
        if size >= 3:
            glow_len = random.randint(4, 10)
            draw.line([(x - glow_len, y), (x + glow_len, y)], fill=c, width=1)
            draw.line([(x, y - glow_len), (x, y + glow_len)], fill=c, width=1)


def _paste_card_dramatic(img, card_path, width, height):
    """Pega la carta con iluminación dramática desde abajo y marco dorado"""
    card = Image.open(card_path).convert("RGBA")

    # La carta ocupa el 65% del ancho y se centra
    target_w = int(width * 0.72)
    aspect = card.height / card.width
    target_h = int(target_w * aspect)

    # Limitar altura
    max_h = int(height * 0.58)
    if target_h > max_h:
        target_h = max_h
        target_w = int(target_h / aspect)

    card = card.resize((target_w, target_h), Image.LANCZOS)

    # Mejorar contraste y saturación de la carta
    card_rgb = card.convert("RGB")
    card_rgb = ImageEnhance.Contrast(card_rgb).enhance(1.3)
    card_rgb = ImageEnhance.Color(card_rgb).enhance(1.4)
    card = Image.merge("RGBA", (*card_rgb.split(), card.split()[3]))

    # Posición: centrada horizontalmente, a 1/3 del alto
    cx = (width - target_w) // 2
    cy = int(height * 0.27)

    # ── Resplandor exterior (glow) dorado/morado ─────────────────────
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    for off in range(50, 0, -3):
        a = int(80 * ((50 - off) / 50) ** 0.5)
        col = (255, 180, 0, a) if off > 25 else (160, 0, 255, a)
        gd.rounded_rectangle(
            [cx - off, cy - off, cx + target_w + off, cy + target_h + off],
            radius=25, fill=col
        )
    img = Image.alpha_composite(img.convert("RGBA"), glow_layer).convert("RGB")

    draw = ImageDraw.Draw(img)

    # Marco dorado grueso
    draw.rounded_rectangle(
        [cx - 12, cy - 12, cx + target_w + 12, cy + target_h + 12],
        radius=20, fill=(10, 5, 20), outline=(255, 215, 0), width=10
    )
    draw.rounded_rectangle(
        [cx - 4, cy - 4, cx + target_w + 4, cy + target_h + 4],
        radius=14, outline=(255, 240, 180), width=3
    )

    img.paste(card, (cx, cy), mask=card)
    return img, cx, cy, target_w, target_h


def _draw_hook_text(draw, width, hook_text, fonts):
    """Hook GRANDE en la parte superior — el texto que detiene el scroll"""
    if not hook_text:
        return

    # Limpiar emojis problemáticos
    clean = hook_text.replace("🔮", "").replace("✨", "").replace("💫", "").strip()
    font = fonts["title"]

    # Dividir en máximo 2 líneas de ~25 chars
    words = clean.split()
    lines, curr = [], ""
    for w in words:
        if len(curr + " " + w) <= 26:
            curr = (curr + " " + w).strip()
        else:
            if curr:
                lines.append(curr)
            curr = w
    if curr:
        lines.append(curr)
    lines = lines[:2]

    y = 70
    for line in lines:
        cx = width // 2
        # Sombra dura negra (múltiple)
        for sx, sy in [(-3, 3), (3, 3), (-3, -3), (3, -3), (0, 4)]:
            draw.text((cx + sx, y + sy), line.upper(), font=font,
                      fill=(0, 0, 0), anchor="mt")
        # Texto blanco brillante
        draw.text((cx, y), line.upper(), font=font,
                  fill=(255, 255, 255), anchor="mt")
        # Subrayado dorado
        bbox = draw.textbbox((cx, y), line.upper(), font=font, anchor="mt")
        draw.line([(bbox[0] - 10, bbox[3] + 5), (bbox[2] + 10, bbox[3] + 5)],
                  fill=(255, 215, 0), width=3)
        y += bbox[3] - bbox[1] + 20


def _draw_bottom_caption(draw, width, height, text, fonts, y_ratio=0.875):
    """Subtítulo inferior grande estilo reels virales"""
    if not text:
        return
    clean = text.replace("🔮", "").replace("✨", "").strip()
    font = fonts["sub"]
    y = int(height * y_ratio)
    cx = width // 2

    # Caja negra semitransparente detrás del texto
    bbox = draw.textbbox((cx, y), clean.upper(), font=font, anchor="mm")
    pad = 18
    draw.rounded_rectangle(
        [bbox[0] - pad, bbox[1] - pad // 2, bbox[2] + pad, bbox[3] + pad // 2],
        radius=12, fill=(0, 0, 0)
    )
    # Borde dorado fino
    draw.rounded_rectangle(
        [bbox[0] - pad, bbox[1] - pad // 2, bbox[2] + pad, bbox[3] + pad // 2],
        radius=12, outline=(255, 215, 0), width=3
    )
    # Texto amarillo-dorado
    for sx, sy in [(-2, 2), (2, 2)]:
        draw.text((cx + sx, y + sy), clean.upper(), font=font, fill=(0, 0, 0), anchor="mm")
    draw.text((cx, y), clean.upper(), font=font, fill=(255, 235, 100), anchor="mm")


def _draw_card_name(draw, width, height, card_name, fonts, card_bottom_y):
    """Nombre de la carta debajo del marco, tipografía dorada"""
    clean = card_name.replace("El ", "").replace("La ", "").replace("Los ", "").replace("The ", "")
    font = fonts["badge"]
    y = card_bottom_y + 30
    cx = width // 2

    # Línea dorada arriba
    draw.line([(cx - 150, y - 8), (cx + 150, y - 8)], fill=(255, 215, 0), width=2)

    # Texto dorado con sombra
    for sx, sy in [(-2, 2), (2, 2)]:
        draw.text((cx + sx, y + sy), f"✦ {card_name.upper()} ✦", font=font,
                  fill=(0, 0, 0), anchor="mt")
    draw.text((cx, y), f"✦ {card_name.upper()} ✦", font=font,
              fill=(255, 215, 0), anchor="mt")

    # Línea dorada abajo
    line_y = y + 38
    draw.line([(cx - 150, line_y), (cx + 150, line_y)], fill=(255, 215, 0), width=2)


def _apply_vignette(img, width, height, intensity=200):
    """Vignette cinematográfico: esquinas muy oscuras"""
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    steps = 55
    for i in range(steps):
        off = i * 9
        if off >= min(width, height) // 2:
            break
        alpha = int(intensity * (i / steps) ** 1.8)
        vd.rectangle([off, off, width - off, height - off],
                     outline=(0, 0, 0, alpha), width=9)
    return Image.alpha_composite(img.convert("RGBA"), vignette).convert("RGB")


def compose_cinematic_tarot_scene(card_name: str, scene_index: int,
                                   hook_text: str = "",
                                   caption_text: str = "",
                                   width: int = 1080,
                                   height: int = 1920,
                                   output_dir: str = TEMP_DIR,
                                   seed: int = 0) -> str:
    os.makedirs(output_dir, exist_ok=True)
    fonts = _get_fonts()

    # ── 1. Fondo cósmico ──────────────────────────────────────────────────
    img = Image.new("RGB", (width, height))
    img = _draw_cosmic_bg(img, width, height)
    draw = ImageDraw.Draw(img)
    _draw_particles(draw, width, height, seed=seed + scene_index)

    # ── 2. Carta dramática ────────────────────────────────────────────────
    card_path = get_real_tarot_card_image(card_name)
    card_bottom = height // 2  # fallback
    if card_path and os.path.exists(card_path):
        img, card_x, card_y, card_w, card_h = _paste_card_dramatic(img, card_path, width, height)
        draw = ImageDraw.Draw(img)
        card_bottom = card_y + card_h

        # Nombre de la carta debajo
        _draw_card_name(draw, width, height, card_name, fonts, card_bottom)

    # ── 3. Hook superior ─────────────────────────────────────────────────
    _draw_hook_text(draw, width, hook_text, fonts)

    # ── 4. Subtítulo inferior ────────────────────────────────────────────
    if caption_text:
        _draw_bottom_caption(draw, width, height, caption_text, fonts)

    # ── 5. Vignette cinematográfico ───────────────────────────────────────
    img = _apply_vignette(img, width, height)

    filename = os.path.join(output_dir, f"tarot_scene_{scene_index:02d}.png")
    img.save(filename, "PNG")
    print(f"[ESCENA] '{card_name}' Escena {scene_index} → {os.path.basename(filename)}")
    return filename


def build_all_real_card_scenes(cards: list, caption_lines: list = None,
                                hook: str = "",
                                output_dir: str = TEMP_DIR) -> list:
    os.makedirs(output_dir, exist_ok=True)
    captions = caption_lines or []
    seed = random.randint(0, 9999)
    paths = []

    # Solo usamos LA PRIMERA carta (una por video)
    card = cards[0] if cards else "El Mundo"

    # Escena 1 — Hook de apertura (texto grande, sin imagen o con carta pequeña)
    hook_text = hook or (captions[0] if captions else "NO FUE CASUALIDAD QUE LO VEAS HOY")
    p = compose_cinematic_tarot_scene(
        card, 1,
        hook_text=hook_text,
        caption_text=captions[1] if len(captions) > 1 else "",
        output_dir=output_dir, seed=seed
    )
    paths.append(p)

    # Escena 2 — Revelación principal
    p = compose_cinematic_tarot_scene(
        card, 2,
        hook_text=hook_text,
        caption_text=captions[2] if len(captions) > 2 else captions[0] if captions else "",
        output_dir=output_dir, seed=seed + 1
    )
    paths.append(p)

    # Escena 3 — Mensaje final / CTA
    cta = captions[-1] if captions else "ESCRIBE SI EN COMENTARIOS"
    p = compose_cinematic_tarot_scene(
        card, 3,
        hook_text=hook_text,
        caption_text=cta,
        output_dir=output_dir, seed=seed + 2
    )
    paths.append(p)

    return paths
