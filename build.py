#!/usr/bin/env python3
import os
import fontforge
import sys

SVG_FOLDER = "./svg_output"
OUTPUT_TTF = "./ThousandMazes.ttf"
SOURCE_HEIGHT = 16  # Height of each glyph in pixels
TARGET_EM_SIZE = 16  # Target em size for the font
SIDE_BEARING = 1  # Side bearing for each glyph

def svg_folder_to_ttf(svg_folder, output_ttf):
    if not os.path.exists(svg_folder):
        print(f"Error: SVG folder '{svg_folder}' does not exist. You must run converter.py first.")
        sys.exit(1)

    font = fontforge.font()
    font.fontname = "ThousandMazes"
    font.familyname = "ThousandMazes"
    font.version = "1.0.0"
    font.fullname = "ThousandMazes"
    font.encoding = "UnicodeFull"
    font.em = TARGET_EM_SIZE

    for filename in sorted(os.listdir(svg_folder)):
        if not filename.lower().endswith('.svg'):
            continue

        basename = os.path.splitext(filename)[0]
        try:
            codepoint = int(basename, 16)
        except ValueError:
            print(f"Skipping file '{filename}': filename is not a valid hex codepoint.")
            continue

        svg_path = os.path.join(svg_folder, filename)
        print(f"Importing {svg_path} as U+{basename}")

        glyph = font.createChar(codepoint)
        glyph.importOutlines(svg_path)

        scale_factor = TARGET_EM_SIZE / SOURCE_HEIGHT
        glyph.transform(psMat.scale(scale_factor))

        glyph.correctDirection()

        xmin, ymin, xmax, ymax = glyph.boundingBox()
        width = xmax - xmin

        glyph.transform(psMat.translate(-xmin + SIDE_BEARING, 0))

        glyph.width = (int)(width + 2 * SIDE_BEARING) 

    font.generate(output_ttf)
    print(f"Font generated and saved to '{output_ttf}'")

if __name__ == "__main__":
    import psMat
    svg_folder_to_ttf(SVG_FOLDER, OUTPUT_TTF)