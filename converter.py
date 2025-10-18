#!/usr/bin/env python3
import os
import shutil
from PIL import Image

source_folder = "pixel_art"
target_folder = "svg_output"
pixel_size = 1

if os.path.exists(target_folder):
    shutil.rmtree(target_folder)
os.makedirs(target_folder, exist_ok=True)

image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
total_files = len(image_files)

for idx, image_file in enumerate(image_files, start=1):
    # load image
    img_path = os.path.join(source_folder, image_file)
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size

    svg_content = [f'<svg width="{width * pixel_size}" height="{height * pixel_size}" xmlns="http://www.w3.org/2000/svg">']

    for y in range(height):
        for x in range(width):
            _, _, _, a = img.getpixel((x, y))
            if a == 0:
                continue  # skip transparent pixels
            svg_content.append(f'<path d="M{x * pixel_size},{y * pixel_size} h{pixel_size} v{pixel_size} h-{pixel_size} Z" fill="black" />')
    svg_content.append('</svg>')

    svg_filename = os.path.splitext(image_file)[0] + ".svg"
    svg_path = os.path.join(target_folder, svg_filename)
    with open(svg_path, 'w') as svg_file:
        svg_file.write('\n'.join(svg_content))

    percent = (idx / total_files) * 100
    print(f"Progress: {percent:.2f}% ({idx}/{total_files}) - Converted {image_file} to {svg_filename}")

print("Conversion complete.")