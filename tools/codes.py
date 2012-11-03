#!/usr/bin/env python

import tempfile
import qrcode


__all__ = ("generate_code",)


def generate_code(data, version=None):
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

    tmp_file = tempfile.TemporaryFile(suffix='.png')
    img.save(tmp_file)

    return tmp_file


if __name__ == "__main__":
    data = 'http://kyivjs.org.ua/api/{}'
    number = '123123'
    fh = generate_code(data.format(number))
    fh.seek(0)
    nfh = open("test.png", "w")
    nfh.write(fh.read())
    nfh.close()
