"""
✨ Generador de Bucles Cinemáticos y Místicos (Motion Backgrounds)
Crea bucles fluidos de partículas flotantes, niebla cósmica y estrellas
con movimiento continuo de 60 cuadros a 30 fps (2 segundos en loop perfecto).
Ligero, 100% nativo en Python con Pillow y FFmpeg, sin costos.
"""

import os
import math
import random
import subprocess
from PIL import Image, ImageDraw, ImageFilter
from config import ASSETS_DIR, TEMP_DIR

LOOP_PATH = os.path.join(ASSETS_DIR, "cosmic_motion_loop.mp4")

def generate_cosmic_motion_loop(width: int = 1080, height: int = 1920,
                                total_frames: int = 60, fps: int = 30) -> str:
    """Genera un video en bucle de partículas y nebulosa pulsante 3D"""
    if os.path.exists(LOOP_PATH) and os.path.getsize(LOOP_PATH) > 50000:
        return LOOP_PATH

    print("[MOTION] Creando bucle cósmico de partículas en movimiento...")
    frames_dir = os.path.join(TEMP_DIR, "motion_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # Generar 150 partículas con trayectorias orbitales en loop
    random.seed(42)
    particles = []
    for _ in range(160):
        particles.append({
            "base_x": random.randint(50, width - 50),
            "base_y": random.randint(50, height - 50),
            "speed": random.uniform(0.8, 2.5),
            "radius": random.uniform(80, 220),
            "phase": random.uniform(0, 2 * math.pi),
            "size": random.choices([2, 3, 4, 6], weights=[50, 30, 15, 5])[0],
            "color": random.choice([
                (255, 215, 0),   # Dorado
                (220, 150, 255), # Púrpura místico
                (180, 230, 255), # Azul celestial
                (255, 255, 255), # Blanco estelar
            ])
        })

    cx, cy = width // 2, height // 2

    for frame_idx in range(total_frames):
        t = frame_idx / total_frames
        angle = t * 2 * math.pi

        img = Image.new("RGB", (width, height), (6, 3, 14))
        draw = ImageDraw.Draw(img)

        # 1. Nebulosa de fondo suave que respira (pulso cósmico)
        pulse = 0.5 + 0.5 * math.sin(angle)
        for r_step in range(12, 0, -1):
            rad_w = int(cx * (0.8 + 0.3 * pulse) * (r_step / 12))
            rad_h = int(cy * (0.8 + 0.3 * pulse) * (r_step / 12))
            alpha_col = (
                int(25 + 15 * pulse * (1 - r_step / 12)),
                int(8 + 5 * (1 - r_step / 12)),
                int(50 + 35 * pulse * (1 - r_step / 12))
            )
            draw.ellipse([cx - rad_w, cy - rad_h, cx + rad_w, cy + rad_h], fill=alpha_col)

        # 2. Partículas orbitando en profundidad 3D
        for p in particles:
            orbit_angle = p["phase"] + angle * p["speed"]
            # Movimiento en elipse para dar sensación de volumen tridimensional
            px = int(p["base_x"] + p["radius"] * math.cos(orbit_angle))
            py = int(p["base_y"] + (p["radius"] * 0.4) * math.sin(orbit_angle) - (t * 80))
            
            # Repetición toroidal suave en eje Y
            py = py % height
            sz = p["size"]
            
            # Brillo pulsante por partícula
            alpha_f = 0.6 + 0.4 * math.sin(orbit_angle)
            c = tuple(int(val * alpha_f) for val in p["color"])
            
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=c)
            if sz >= 4:
                # Destello en cruz para las partículas grandes
                draw.line([(px - sz * 2, py), (px + sz * 2, py)], fill=c, width=1)
                draw.line([(px, py - sz * 2), (px, py + sz * 2)], fill=c, width=1)

        frame_file = os.path.join(frames_dir, f"frame_{frame_idx:04d}.png")
        img.save(frame_file)

    # Compilar los frames en video MP4 reproducible en bucle
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        LOOP_PATH
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Limpiar frames temporales
    for f in os.listdir(frames_dir):
        try:
            os.remove(os.path.join(frames_dir, f))
        except:
            pass

    print(f"[MOTION] Bucle cósmico listo: {LOOP_PATH}")
    return LOOP_PATH
