import sys
import os
import time
from playwright.sync_api import sync_playwright

def main():
    if len(sys.argv) < 6:
        print("Usage: python capture_frames.py <html_file> <frames_dir> <width> <height> <loop_ms>")
        sys.exit(1)
        
    html_file = os.path.abspath(sys.argv[1])
    frames_dir = os.path.abspath(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])
    loop_duration_ms = int(sys.argv[5])
    
    num_frames = 60
    frame_step = loop_duration_ms / num_frames
    
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        if f.endswith('.png'):
            os.remove(os.path.join(frames_dir, f))
            
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2
        )
        
        file_url = f"file:///{html_file.replace(os.sep, '/')}"
        page.goto(file_url, wait_until="networkidle")
        time.sleep(1) # wait for fonts/setup
        
        print(f"Capturing {num_frames} frames...")
        
        for i in range(num_frames):
            t = 10000 + i * frame_step
            
            page.evaluate(f"""(ms) => {{
                document.getAnimations().forEach(anim => {{
                    if(anim.effect) {{
                        anim.currentTime = ms;
                        anim.pause();
                    }}
                }});
            }}""", t)
            
            frame_path = os.path.join(frames_dir, f"frame_{i:03d}.png")
            page.screenshot(path=frame_path)
            
            if (i+1) % 10 == 0:
                print(f"  Frame {i+1}/{num_frames}")
                
        browser.close()
        print("✅ Frames saved to:", frames_dir)

if __name__ == "__main__":
    main()
