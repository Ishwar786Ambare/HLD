"""
Assembles PNG frames into a smooth looping animated GIF.
"""

from PIL import Image
import os, glob

BASE = r"c:\Users\ishwa\PycharmProjects\HLD\CAP Theorem & Replication\images"
FRAMES_DIR = os.path.join(BASE, "frames")
OUTPUT_GIF = os.path.join(BASE, "cap_theorem_diagram.gif")

frame_paths = sorted(glob.glob(os.path.join(FRAMES_DIR, "frame_*.png")))
if not frame_paths:
    raise FileNotFoundError(f"No frames in {FRAMES_DIR}")

print(f"Found {len(frame_paths)} frames. Building GIF...")

frames = []
for fp in frame_paths:
    img = Image.open(fp).convert("RGBA")
    w, h = img.size
    # Downsample from 2x Puppeteer capture to native resolution
    img = img.resize((w // 2, h // 2), Image.LANCZOS)
    # Flatten onto white background
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    # Convert to 256-color palette (GIF requirement)
    frames.append(
        bg.convert("P", palette=Image.ADAPTIVE, colors=256,
                   dither=Image.Dither.FLOYDSTEINBERG)
    )

# 60 frames over ~4s → 67ms per frame (≈15 fps smooth)
frames[0].save(
    OUTPUT_GIF,
    format="GIF",
    save_all=True,
    append_images=frames[1:],
    duration=135,
    loop=0,
    optimize=False,
)

size_kb = os.path.getsize(OUTPUT_GIF) / 1024
print(f"✅ Animated GIF: cap_theorem_diagram.gif  ({size_kb:.0f} KB)")

# Clean temp frames
for fp in frame_paths:
    os.remove(fp)
try:
    os.rmdir(FRAMES_DIR)
except OSError:
    pass
print("🗑️  Temp frames cleaned up.")
