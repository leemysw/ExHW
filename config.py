# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# =====================================================
# @Project：ExHW
# @File   ：config
# @Date   ：2023/5/21 22:04
# @Author ：leemysw
# @Modify Time      @Author    @Version    @Description
# ------------      -------    --------    ------------
# 2023/5/21 22:04   leemysw      1.0.0         Create

# =====================================================
import yaml
from utils.utils import abspath

class Config:
    def __init__(self, conf_file = abspath("conf.yaml")):
        self.conf_file = conf_file
        self.conf = self.load_conf()

    def load_conf(self):
        with open(self.conf_file, "r") as f:
            conf = yaml.safe_load(f)

        return conf["defaults"]


config = Config()

if __name__ == '__main__':
    print(config.conf)