from html2image import Html2Image
import os

# Create Html2Image instance with enhanced rendering flags
# --force-device-scale-factor=2 renders at 2x DPI for sharper text and graphics
# --hide-scrollbars ensures clean image without scrollbars
hti = Html2Image(custom_flags=['--force-device-scale-factor=2', '--hide-scrollbars'])

# Define correct paths
input_html = r'C:\Users\ishwa\PycharmProjects\HLD\Zookeeper & Kafka\images\zk_consistency.html'
output_dir = r'C:\Users\ishwa\PycharmProjects\HLD'
output_filename = 'zk_consistency_hq.png'

# Tell Html2Image to save the file in the correct images directory
hti.output_path = output_dir

print("Generating ultra-high-quality screenshot with 2x DPI scaling...")

# Take the screenshot at higher resolution (2880x1920) with 2x device scale factor
# This produces a much sharper image with better text clarity
# The 2x scale factor means 1440x960 logical pixels render as 2880x1920 physical pixels
hti.screenshot(
    html_file=input_html,
    save_as=output_filename,
    size=(2880, 1920)  # 2x resolution for ultra HD quality
)

final_path = os.path.join(output_dir, output_filename)
file_size = os.path.getsize(final_path) / 1024

print(f"✅ Successfully saved ultra-high-quality image!")
print(f"Location: {final_path}")
print(f"Size:     {file_size:.2f} KB")
print(f"Resolution: 2880x1920 (2x DPI scaling applied)")