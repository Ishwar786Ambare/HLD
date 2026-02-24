import sys
import os
import time
from playwright.sync_api import sync_playwright

def main():
    if len(sys.argv) < 5:
        print("Usage: python capture_static.py <html_file> <output_png> <width> <height>")
        sys.exit(1)
        
    html_file = os.path.abspath(sys.argv[1])
    output_png = os.path.abspath(sys.argv[2])
    width = int(sys.argv[3])
    height = int(sys.argv[4])
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2
        )
        
        file_url = f"file:///{html_file.replace(os.sep, '/')}"
        page.goto(file_url, wait_until="networkidle")
        time.sleep(1) # wait for fonts/setup
        
        page.screenshot(path=output_png)
        browser.close()
        print("✅ Static high-res PNG saved to:", output_png)

if __name__ == "__main__":
    main()
