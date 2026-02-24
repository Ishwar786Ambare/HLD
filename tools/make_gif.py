import sys
from PIL import Image
import os, glob

if len(sys.argv) < 5:
    print("Usage: python make_gif.py <frames_dir> <output_gif> <duration_ms> <bg_color_tuple>")
    print("Example: python make_gif.py ./frames ./out.gif 83 253,253,253")
    sys.exit(1)

FRAMES_DIR = os.path.abspath(sys.argv[1])
OUTPUT_GIF = os.path.abspath(sys.argv[2])
DURATION_MS = int(sys.argv[3])
bg_color_str = sys.argv[4].split(",")
if len(bg_color_str) == 3:
    BG_COLOR = (int(bg_color_str[0]), int(bg_color_str[1]), int(bg_color_str[2]), 255)
elif len(bg_color_str) == 4:
    BG_COLOR = (int(bg_color_str[0]), int(bg_color_str[1]), int(bg_color_str[2]), int(bg_color_str[3]))
else:
    BG_COLOR = (255, 255, 255, 255)

frame_paths = sorted(glob.glob(os.path.join(FRAMES_DIR, "frame_*.png")))
if not frame_paths:
    raise FileNotFoundError(f"No frames in {FRAMES_DIR}")

print(f"Found {len(frame_paths)} frames. Building GIF with duration {DURATION_MS}ms per frame...")

frames = []
for fp in frame_paths:
    img = Image.open(fp).convert("RGBA")
    w, h = img.size
    img = img.resize((w // 2, h // 2), Image.LANCZOS)
    bg = Image.new("RGBA", img.size, BG_COLOR)
    bg.paste(img, mask=img.split()[3])
    frames.append(
        bg.convert("P", palette=Image.ADAPTIVE, colors=256,
                   dither=Image.Dither.FLOYDSTEINBERG)
    )

frames[0].save(
    OUTPUT_GIF,
    format="GIF",
    save_all=True,
    append_images=frames[1:],
    duration=DURATION_MS,
    loop=0,
    optimize=False,
)

size_kb = os.path.getsize(OUTPUT_GIF) / 1024
print(f"✅ Animated GIF: {os.path.basename(OUTPUT_GIF)}  ({size_kb:.0f} KB)")

for fp in frame_paths:
    os.remove(fp)
try:
    os.rmdir(FRAMES_DIR)
except OSError:
    pass
print("🗑️ Temp frames cleaned up.")
