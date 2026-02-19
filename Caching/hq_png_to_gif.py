from PIL import Image
import os

images_dir = r"c:\Users\ishwa\PycharmProjects\HLD\Caching\images"
png_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]

for png_file in sorted(png_files):
    png_path = os.path.join(images_dir, png_file)
    gif_path = os.path.join(images_dir, png_file.replace('.png', '.gif'))
    
    img = Image.open(png_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Use ADAPTIVE palette to preserve colors better, which helps with white text
    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    
    # Disable optimization to prioritize quality
    img.save(gif_path, 'GIF', optimize=False)
    
    size_kb = os.path.getsize(gif_path) / 1024
    print(f"High Quality GIF Created: {os.path.basename(gif_path)} ({size_kb:.1f} KB)")
