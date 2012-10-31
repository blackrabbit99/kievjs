#!/usr/bin/env python

import os
import tempfile

import qrcode
#from qrcode.image.custom_pil import PilImage
#from qrcode.constants import ERROR_CORRECT_M

CURRENT = os.path.abspath(os.path.dirname(__file__))
STATIC = lambda *p: os.path.join(CURRENT, "static", *p)

default_factories = {
    'pil': 'qrcode.image.pil.PilImage',
}

data = 'http://kyivjs.com/xxx'
number = '123123'


def generate_code(data, number, version=None):
    """ Main stub method for testing QR-code generation
    """
    '''
    if version is None:
        version = dict(
            LOGO=STATIC("logos/kyivjs.png"),
            QR_HEAD_TEXT="KyivJS #0",
            SECOND_COLOR="#000000",
            FIRST_COLOR="#000000"
        )

    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_M,
        box_size=10, font=STATIC("fonts/folder_rg.ttf"),
        side=40)
    qr.add_data(data)

    img = qr.make_image(image_factory=PilImage, version=version,
                        qr_text=number)
    tmp_file = tempfile.TemporaryFile(suffix='.png')
    img.save(tmp_file)

    return tmp_file

    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image()

    tmp_file = tempfile.TemporaryFile(suffix='.png')
    img.save(tmp_file)

    return tmp_file


if __name__ == "__main__":
    fh = generate_code(data, number)
    fh.seek(0)
    nfh = open("test.png", "w")
    nfh.write(fh.read())
    nfh.close()
