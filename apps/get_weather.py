# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# =====================================================
# @Project：ExHW
# @File   ：get_weather
# @Date   ：2023/5/20 22:26
# @Author ：leemysw
# @Modify Time      @Author    @Version    @Description
# ------------      -------    --------    ------------
# 2023/5/20 22:26   leemysw      1.0.0         Create

# =====================================================
import json
import datetime

from config import config
from utils.logger import logger
from utils.api_request import BaseRequest
from utils.utils import abspath


class GetWeather(BaseRequest):
    def __init__(self, logger=logger):
        super(GetWeather, self).__init__(logger=logger)
        self.url_now = 'https://devapi.qweather.com/v7/weather/now'
        self.url_3d = 'https://devapi.qweather.com/v7/weather/3d'

        self.location = config.conf["location"]
        self.key = config.conf["key"]

        self.params = {
            'key': self.key,
            'location': self.location,
            'language': 'zh',
            'unit': 'm'
        }
        self.update_time = datetime.datetime.now()
        self.gat_weather()

    def save_data(self):
        with open(abspath("./data/data_now.json"), "w", encoding='utf-8') as f:
            f.write(json.dumps(self.data_now))

        with open(abspath("./data/data_3d.json"), "w", encoding='utf-8') as f:
            f.write(json.dumps(self.data_3d))

    def load_data(self):
        with open(abspath("./data/data_now.json"), encoding='utf-8') as f:
            self.data_now = json.loads(f.read(), )
        with open(abspath("./data/data_3d.json"), encoding='utf-8') as f:
            self.data_3d = json.loads(f.read())

    def gat_weather(self):
        try:
            self.data_now = self._get(url=self.url_now, params=self.params).json().get("now", {})
            self.data_3d = self._get(url=self.url_3d, params=self.params).json().get("daily", [{}])[0]
            self.save_data()
            self.update_time = datetime.datetime.now()
            self.logger.info("获取天气数据成功")
        except Exception:
            self.logger.exception("获取数据出错")

    def update(self):
        diff = datetime.datetime.now() - self.update_time
        if diff.total_seconds() // 60 >= 10:
            self.gat_weather()

    def __call__(self, *args, **kwargs):
        self.update()


if __name__ == '__main__':
    gw = GetWeather()
    gw()
