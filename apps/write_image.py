import re
import binascii

from PIL import Image

from utils import hid
from utils.logger import logger


class WriteImage:
    def __init__(self, output_path, logger=logger):
        self.logger = logger
        self.image_path = output_path

    def load_image(self):
        return Image.open(self.image_path)

    def image2hex(self, threshold=128):
        image = self.load_image()
        black_img = image.convert("L")

        bdata_list = list(black_img.getdata())
        bvalue_list = [0 if i < threshold else 1 for i in bdata_list]

        ob_list = []
        s = "0b"
        for i in range(0, len(bvalue_list)):
            s += str(bvalue_list[i])
            if (i + 1) % 8 == 0:
                ob_list.append(s)
                s = "0b"

        hex_list = ['%02x' % int(i, 2) for i in ob_list]
        return hex_list

    def hex2package(self):
        hexStr = '013e8d2508072a8825080b1080251a8025'
        nextPackage = '013e'
        lastPackage = '0128'

        hex_list = self.image2hex()
        hex_len = len(hex_list)

        hexStr += "".join([h for h in hex_list[0:47]])

        idx = 47
        packCount = int((len(hex_list) - 47) / 62)

        for i in range(0, packCount):
            hexStr += nextPackage
            for k in range(0, 62):
                hexStr += "00" if idx >= hex_len else hex_list[idx]
                idx += 1
        hexStr += lastPackage

        for k in range(0, 62):
            hexStr += "00" if idx >= hex_len else hex_list[idx]
            idx += 1

        st2 = re.findall(r'.{128}', hexStr)
        st2.append(hexStr[int(int(len(hexStr) / 128) * 128):])


        return st2


    def write(self):
        packages = self.hex2package()
        h = hid.enumerate(vid=0x1d50, pid=0x615e)
        with hid.Device(path=h[2]['path']) as d:
            d.write(binascii.unhexlify(
                '01050408011200000000000000000000000000000000000000'
                '000000000000000000000000000000000000000000000000000'
                '000000000000000000000000000'))
            pack = d.read(1000).decode()

            self.logger.info('Zephyr 版本:'.ljust(10) + pack[9:16])
            self.logger.info('ZMK 版本:'.ljust(10) + pack[18:25])
            self.logger.info('HW 版本:'.ljust(10) + pack[27:34])

            for p in packages:
                if p == '':
                    continue
                d.write(binascii.unhexlify(p))
        self.logger.info('图片刷新完成')


if __name__ == '__main__':
    wp = WriteImage()
    wp.write()
