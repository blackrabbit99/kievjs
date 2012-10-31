# -*- encoding: utf-8 -*-
# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw

import math
import qrcode.image.base

from qrcode.util import get_font


def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner


class PilImage(qrcode.image.base.BaseImage):
    """PIL image builder, default format is PNG."""

    def __init__(self, border, width, box_size, version, text,
                 font=None, font_size=14, side=7, inch=2.54, resolution=300,
                 kind=None):
        if Image is None and ImageDraw is None:
            raise NotImplementedError("PIL not available")
        super(PilImage, self).__init__(border, width, box_size)

        version_keys = set([
            'LOGO', 'QR_HEAD_TEXT', 'SECOND_COLOR', 'FIRST_COLOR'])

        if (not isinstance(version, dict) or
                set(version.keys()) != version_keys):
            raise TypeError(
                "Version should be ``dict`` and require "
                "following keys: {}".format(", ".join(version_keys)))

        self.kind = kind or "PNG"
        self.version = version
        self.text = text
        self.font = font
        self.font_size = font_size

        self.box_size = int(side / inch * resolution /
                            (self.width + self.border * 2))
        self.data_size = self.width * self.box_size

        self.pixelsize = (self.width + self.border * 2) * self.box_size

        self._img = Image.new("RGBA", (self.pixelsize, self.pixelsize),
                              "white")
        self._idr = ImageDraw.Draw(self._img)

    def prepare_logo(self):
        logo = Image.open(self.version['LOGO'])
        # calculate scaling aspect taking 30% from the data area box and
        # extracting this square side
        size = int(math.sqrt(self.data_size * self.data_size * 0.25))
        prepared = logo.copy()
        prepared.thumbnail((size, size), Image.ANTIALIAS)

        def adjust_size(side):
            remains = (side / 2) % (self.box_size / 2)
            if remains > 0:
                side += self.box_size - remains
            return side

        bg_size = map(adjust_size, prepared.size)

        bg = Image.new("RGBA", bg_size, "white")

        def adjust_position(bg, prepared):
            h, w = bg.size
            h1, w1 = prepared.size
            return (h / 2 - h1 / 2, w / 2 - w1 / 2)

        if logo.mode == 'RGBA':
            bg.paste(prepared, adjust_position(bg, prepared), prepared)
        elif logo.mode == 'RGB':
            bg.paste(prepared, adjust_position(bg, prepared))

        point = map(lambda side: self.pixelsize / 2 - side / 2, bg.size)

        return bg, tuple(point)

    def prepare_text_under(self, text):
        font = get_font(self.font, self.font_size)
        font_size = self._idr.textsize(text, font=font)
        x = self._img.size[0] / 2 - font_size[0] / 2
        y = self._img.size[1] - font_size[1]
        self._idr.text((int(x), int(y)), text, font=font, fill="black")

    def prepare_text_above(self):
        text = self.version['QR_HEAD_TEXT']
        font = get_font(self.font, self.font_size)
        font_size = self._idr.textsize(text, font=font)
        x = self._img.size[0] / 2 - font_size[0] / 2
        y = 2
        self._idr.text((int(x), int(y)), text, font=font, fill="black")

    def prepare_copyright(self):
        text = u'©'
        font = get_font(self.font, self.font_size)
        font_size = self._idr.textsize(text, font=font)
        x_margin, y_margin = 5, 0
        x = self._img.size[0] - font_size[0] - x_margin
        y = self._img.size[1] - font_size[1] - y_margin
        self._idr.text((int(x), int(y)), text, font=font, fill="black")

    def drawrect(self, row, col, second=False, corners=(0, 0, 0, 0)):
        if (row in [2, 3, 4] and col in [2, 3, 4]) or \
           (row in [2, 3, 4] and col in [36, 37, 38]) or \
           (row in [36, 37, 38] and col in [2, 3, 4]):
            fill_color = self.version['SECOND_COLOR']
        else:
            fill_color = second and self.version['SECOND_COLOR'] \
                or self.version['FIRST_COLOR']

        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size

        # box = [(x, y),
        #        (x + self.box_size - 1,
        #         y + self.box_size - 1)]

        rectangle = Image.new('RGBA', (self.box_size, self.box_size),
                              fill_color)

        radius = 6
        corner = round_corner(radius, fill_color)
        if not (corners[0] | corners[1]):   # left & up
            rectangle.paste(corner, (0, 0))
        if not (corners[0] | corners[2]):   # left & bottom
            rectangle.paste(corner.rotate(90), (0, self.box_size - radius))
        if not (corners[2] | corners[3]):   # right & bottom
            rectangle.paste(corner.rotate(180),
            (self.box_size - radius, self.box_size - radius))
        if not (corners[1] | corners[3]):   # right & up
            rectangle.paste(corner.rotate(270), (self.box_size - radius, 0))

        self._img.paste(rectangle, (x, y), rectangle)

    def save(self, stream, kind=None):
        logo, point = self.prepare_logo()
        if kind is None:
            kind = self.kind
        self._img.paste(logo, point, logo)
        # self.prepare_text_under(self.text)
        # self.prepare_text_above()
        # self.prepare_copyright()
        self._img.save(stream, kind)
