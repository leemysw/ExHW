import os
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from utils.logger import logger
from utils.utils import abspath

from apps.get_date import GetDate
from apps.get_weather import GetWeather
from apps.write_image import WriteImage


def dither(image, th=127):
    im = image.convert('L')
    img = np.array(im)
    img = np.where(img < th, 0, 255)
    return Image.fromarray(img).convert("RGB")


def cal_text_size(text, text_size):
    font_style = ImageFont.truetype(abspath("./data/SmileySans-Oblique.ttf"), text_size, encoding="utf-8")
    left, top, right, bottom = font_style.getbbox(text)
    width, height = right - left, bottom - top
    return width, height


def image_add_text(img, text, y, x=None, space=0, text_color=(0, 0, 0), text_size=20):
    draw = ImageDraw.Draw(img)
    font_style = ImageFont.truetype(abspath("./data/SmileySans-Oblique.ttf"), text_size, encoding="utf-8")
    left, top, right, bottom = font_style.getbbox(text)
    width, height = right - left, bottom - top

    left = (128 - width) // 2 if x is None else x
    top = y + space

    draw.text((left, top), text, text_color, font=font_style)
    return img, top + height


class App:
    def __init__(self, logger=logger):
        self.logger = logger
        self.output_path = abspath("data/output.png")
        self.gw = GetWeather(logger=logger)
        self.gd = GetDate(logger=logger)
        self.wi = WriteImage(output_path=self.output_path, logger=logger)

    def draw_header(self, image):
        date = self.gd.date + " " * 3 + self.gd.weekday
        image, y = image_add_text(image, date, y=0, text_size=18)

        image_header = Image.open(abspath("data/image_header.png"))
        size = image_header.size
        height = int(size[1] * 128 / size[0])
        image_header = image_header.resize((128, height))
        image_header = dither(image_header)
        image.paste(image_header, (0, y + 5))

        temperature_now = "{} {}".format(self.gw.data_now.get("temp", "--").center(3), u"°C")
        w, h = cal_text_size(temperature_now, text_size=14)
        image, y = image_add_text(image, temperature_now, x=64 - w - 5, y=y, space=8, text_size=20)

        return image, y + height

    def draw_weather(self, image, y):
        separator = "_____________________________" * 10
        image, _ = image_add_text(image, separator, y=y - 30, text_size=10)

        icon_day_file = abspath("data/img/{}.jpg".format(self.gw.data_3d.get("iconDay", None)))
        icon_night_file = abspath("data/img/{}.jpg".format(self.gw.data_3d.get("iconNight", None)))
        text_day = self.gw.data_3d.get("textDay", "--")
        text_night = self.gw.data_3d.get("textNight", "--")
        tempmin = self.gw.data_3d.get("tempMin", "--")
        tempmax = self.gw.data_3d.get("tempMax", "--")

        y -= 8
        if os.path.isfile(icon_day_file):
            weather_image = Image.open(icon_day_file).resize((28, 28))
            image.paste(weather_image, (0, y + 5))
        if os.path.isfile(icon_night_file):
            weather_image = Image.open(icon_night_file).resize((28, 28))
            image.paste(weather_image, (100, y + 5))

        weather = "{} ~ {}".format(text_day.center(3), text_night.center(3))
        temperature = "{} {} / {} {}".format(tempmin.center(3), u"°C", tempmax.center(3), u"°C")
        image, y = image_add_text(image, weather, y=y, text_size=13)
        image, y = image_add_text(image, temperature, y=y, space=4, text_size=13)

        return image, y

    def draw_bottom(self, image, y):
        image_bottom = Image.open(abspath("data/image_bottom2.png"))
        size = image_bottom.size
        height = int(size[1] * 128 / size[0])
        image_bottom = image_bottom.resize((128, height))
        image_bottom = dither(image_bottom, th=90)

        image.paste(image_bottom, (0, 296 - height))

        return image, y

    def __call__(self, *args, **kwargs):
        while True:
            try:
                new_image = Image.new("RGB", (128, 296), color=(255, 255, 255))
                new_image, y = self.draw_header(new_image)
                new_image, y = self.draw_weather(new_image, y)
                new_image, y = self.draw_bottom(new_image, y)
                new_image.save(self.output_path)
                self.wi.write()
                self.logger.info("图片将在30min后更新， 使用ctrl + c 退出")
                time.sleep(60 * 30)
            except KeyboardInterrupt:
                self.logger.info("用户终止程序，3s后退出")
                time.sleep(3)
                break


if __name__ == '__main__':
    app = App()
    app.gw.load_data()
    app()
