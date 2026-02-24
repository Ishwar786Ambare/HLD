from PIL import Image
import sys

def convert_webp_to_gif(webp_path, gif_path):
    print(f"Loading {webp_path}...")
    try:
        im = Image.open(webp_path)
        frames = []
        try:
            while True:
                frames.append(im.copy())
                im.seek(len(frames))
        except EOFError:
            pass

        print(f"Found {len(frames)} frames. Saving as {gif_path}...")
        frames[0].save(
            gif_path,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=im.info.get('duration', 80)
        )
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python webp_to_gif.py <input.webp> <output.gif>")
    else:
        convert_webp_to_gif(sys.argv[1], sys.argv[2])
