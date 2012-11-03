#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qrcode

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


__all__ = ("generate_code", "generate_badge")


def generate_code(data, version=None, output=""):
    """ Main stub method for testing QR-code generation
    """

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(open(output, "w"))

    return output


def draw_text(canvas, x, y, text, font="FreeSans", size=12):
    canvas.saveState()
    canvas.setFont(font, size)
    canvas.drawString(x, y, text)
    canvas.restoreState()


def generate_badge(title=None, name=None, company=None, position=None,
                   qr_code=None, output="test.pdf"):

    page = canvas.Canvas(output)
    pdfmetrics.registerFont(TTFont("FreeSans", "fonts/FreeSans.ttf"))
    page.setFont('FreeSans', 12)

    # draw qr code
    page.drawImage(qr_code, 60, 110, width=80, height=80)

    # draw details on badge
    if title:
        draw_text(page, 150, 170, title, size=12)

    if name:
        draw_text(page, 150, 145, name, size=20)

    if position:
        draw_text(page, 150, 110, position, size=16)

    if company:
        draw_text(page, 150, 90, company, size=14)

    # draw lines
    page.setDash(4, 2)
    page.setLineWidth(.3)
    page.line(50, 210, 200 + 95 * mm, 210)
    page.line(50, 210, 50, 210 - 70 * mm)

    draw_text(
        page, 50, 750,
        u"{}, приглашение внизу страницы".format(name), size=14)
    page.line(50, 730, 160 * mm, 730)
    page.save()
    return output


if __name__ == "__main__":
    print "Generating QR Code"
    data = 'http://kyivjs.org.ua/api/{}'
    number = '123123'
    generate_code(data.format(number), output="testing/test.png")

    print "Generating PDF"
    generate_badge(
        title="KyivJS, kyivjs.org.ua",
        name="Maksym Klymyshyn",
        company="KyivJS, GVMachines",
        position="Organizers team, CTO",
        qr_code=generate_code("xxx", output="testing/test.png"),
        output="testing/test.pdf")
