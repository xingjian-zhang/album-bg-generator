import json
import os

from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tqdm import tqdm
import numpy as np
from pathlib import Path


def generate_bg(album: str):
    album_name = f"data/image/{album}.png"
    album_info = f"data/info/{album}.json"

    album_dict = json.load(open(album_info))
    # print(album_dict)

    font = ImageFont.truetype('fonts/AmericanTypewriter.ttc',
                              size=30,
                              index=0)

    information = [
        album_dict["album"], album_dict["album artist"],
        str(album_dict["date"]), album_dict["genre"]
    ]
    information = [" ".join(_) for _ in information]
    texts = "\n".join(information)

    black_bg = Image.open("black_bg.jpg")
    color_thief = ColorThief(album_name)
    im = Image.open(album_name)
    color = np.array(color_thief.get_color(quality=1))
    white = np.array((255, 255, 255))
    mid = (color + white) / 2

    color = tuple(color)
    mid = tuple(np.array(mid, dtype=int))

    canvas_length = 1000
    band_length = 175

    x, y = black_bg.size
    x = (x - canvas_length) // 2
    y = (y - canvas_length) // 2 - 200

    canvas_size = (canvas_length, canvas_length * 2)
    rectangle_size = (band_length, band_length, canvas_length - band_length,
                      canvas_length - band_length)
    canvas = Image.new('RGBA', canvas_size)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(rectangle_size, fill=color)
    filtered = canvas.filter(ImageFilter.GaussianBlur(40))
    draw = ImageDraw.Draw(filtered)
    draw.text(xy=(500, 1000),
              text=texts,
              fill=mid,
              font=font,
              anchor='mm',
              align='center',
              spacing=20)

    im_box = ((canvas_length - 600) // 2, (canvas_length - 600) // 2)
    filtered.paste(im, box=im_box)
    black_bg.paste(filtered, mask=filtered, box=(x, y))
    black_bg.save(f"build/{album}.png")


def main():
    paths = [Path(path).stem for path in os.listdir("data/image")]
    builts = [Path(path).stem for path in os.listdir("build")]
    for album in tqdm(paths):
        if album not in builts:
            generate_bg(album)


if __name__ == "__main__":
    main()