from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    for f in ['arialbd.ttf', 'arial.ttf', 'DejaVuSans-Bold.ttf']:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

im = Image.new('RGBA', (1080, 1920), (10, 10, 25, 255))
draw = ImageDraw.Draw(im)

bx1, by1, bx2, by2 = 70, 1420, 1010, 1600

# Outer green glow
for off in range(14, 0, -2):
    draw.rounded_rectangle([bx1-off, by1-off, bx2+off, by2+off], radius=28, fill=(37, 211, 102, int(40*(1-off/14))))

# Main dark emerald box
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=24, fill=(6, 20, 14, 245), outline=(37, 211, 102, 255), width=5)
# Gold inner border
draw.rounded_rectangle([bx1+6, by1+6, bx2-6, by2-6], radius=20, outline=(255, 215, 0, 230), width=2)

f_header = get_font(32)
f_phone  = get_font(48)
f_sub    = get_font(26)

cx = (bx1 + bx2) // 2

# Top title: Gold & crisp
draw.text((cx, by1 + 22), "LECTURA PERSONALIZADA DE TAROT", font=f_header, fill=(255, 225, 80), anchor="mt")

# Center: Green badge + WhatsApp Phone
draw.text((cx, by1 + 72), "WhatsApp: +57 305 338 9704", font=f_phone, fill=(255, 255, 255), anchor="mt")

# Bottom: Subtext
draw.text((cx, by1 + 134), "Escribe 'SESION' para agendar tu consulta privada", font=f_sub, fill=(160, 255, 190), anchor="mt")

im.save('C:/Users/Usuario/.gemini/antigravity/scratch/tarot-youtube-bot/test_banner.png')
crop = im.crop((40, 1380, 1040, 1640))
crop.save('C:/Users/Usuario/.gemini/antigravity/scratch/tarot-youtube-bot/test_banner_crop.png')
print('Fixed banner created')
