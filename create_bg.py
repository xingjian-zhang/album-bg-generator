import json
import os

from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from tqdm import tqdm
import numpy as np
from pathlib import Path

ENGLISH_FONT = 'fonts/AmericanTypewriter.ttc'
ENGLISH_FONT_SIZE = 30
BACKGROUND_PATH = 'black_bg.jpg'
CANVAS_LENTH = 1000
BAND_LENTH = 175
ALBUM_LENGTH = 600
SIGMA = 40
SPACING = 20
TEXT_XY = (500, 1000)


def generate_bg(album_name: str, background_path: str = BACKGROUND_PATH):
    """Generate a desktop background given albums.

    Parameters
    ----------
    album_name : str
        Name of the album.
    background_path : str, optional
        Path of the background image, by default BACKGROUND_PATH
        
    Note
    ----
    The background_path should be 4k.
    """
    # set album fig and info path
    fig_path = f"data/image/{album_name}.png"
    info_path = f"data/info/{album_name}.json"

    # load album information
    with open(info_path) as _:
        info = json.load(_)
    text = f"{info['album']}\n{info['album artist']}\n{info['date']}\n{info['genre']}"

    # cpture major colors
    ct = ColorThief(fig_path)
    color = np.array(ct.get_color(1))
    white = np.array([255, 255, 255])
    text_color = (color + white) // 2

    color = tuple(color)
    text_color = tuple(text_color)

    # load fonts
    en_font = ImageFont.truetype(ENGLISH_FONT, size=ENGLISH_FONT_SIZE, index=0)

    # load figure
    fig = Image.open(fig_path)
    bg = Image.open(background_path)

    # set geometry
    bg_x, bg_y = bg.size
    canvas_x, canvas_y = (bg_x - CANVAS_LENTH) // 2, (bg_y - CANVAS_LENTH) // 2
    rectangle = (BAND_LENTH, BAND_LENTH, CANVAS_LENTH - BAND_LENTH,
                 CANVAS_LENTH - BAND_LENTH)
    canvas_size = (CANVAS_LENTH, CANVAS_LENTH * 2)
    fig_box = ((CANVAS_LENTH - ALBUM_LENGTH) // 2,
               (CANVAS_LENTH - ALBUM_LENGTH) // 2)

    # create canvas
    canvas = Image.new('RGBA', canvas_size)

    # create glow
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(rectangle, fill=color)
    glowed = canvas.filter(ImageFilter.GaussianBlur(SIGMA))
    draw = ImageDraw.Draw(glowed)

    # add texts
    draw.text(xy=TEXT_XY,
              text=text,
              fill=text_color,
              font=en_font,
              anchor='mm',
              align='center',
              spacing=SPACING)

    # combine layers
    glowed.paste(fig, box=fig_box)
    bg.paste(glowed, box=(canvas_x, canvas_y), mask=glowed)
    bg.save(f"build/{album_name}.png")


def main():
    paths = [Path(path).stem for path in os.listdir("data/image")]
    builts = [Path(path).stem for path in os.listdir("build")]
    for album in tqdm(paths):
        if album not in builts:
            generate_bg(album)


if __name__ == "__main__":
    main()