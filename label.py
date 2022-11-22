import argparse
import json
import os
import subprocess

import colorthief as ct
import numpy as np
import PIL as pil
from PIL import Image, ImageColor, ImageDraw


def label_image(im_path: str, color_count: int = 5):
    SIZE = (600, 700)
    im = Image.open(im_path)
    picker = ct.ColorThief(im_path)
    cand_colors = picker.get_palette(color_count=color_count, quality=1)

    canvas = Image.new("RGB", SIZE)
    canvas.paste(im)  # Paste on the top by default

    draw = ImageDraw.Draw(canvas)
    color_width = 600 // color_count
    for color_index in range(color_count):
        bbox = (color_index * color_width, SIZE[0], SIZE[0], SIZE[1])
        draw.rectangle(bbox, fill=cand_colors[color_index])

    canvas.save("buffer.png")
    subprocess.Popen(["code", "buffer.png"])

    color = int(input(f"Select a color (1-{color_count}): "))
    with open("label/labels.csv", "a") as fp:
        fp.write(f"{im_path},{cand_colors[color - 1]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    args = parser.parse_args()
    if path := args.path:
        label_image(path)
    else:
        im_names = os.listdir("data/image")
        for im_name in im_names:
            label_image(os.path.join("data/image", im_name))