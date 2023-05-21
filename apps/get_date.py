# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# =====================================================
# @Project：ExHW
# @File   ：get_date
# @Date   ：2023/5/21 10:38
# @Author ：leemysw
# @Modify Time      @Author    @Version    @Description
# ------------      -------    --------    ------------
# 2023/5/21 10:38   leemysw      1.0.0         Create

# =====================================================

import datetime
from utils.logger import logger

class GetDate:
    def __init__(self, logger=logger):
        self.logger = logger
        self.get_date()

    def get_date(self):
        date = datetime.datetime.now()
        self.weekday = date.strftime("%A")[0:3]
        self.date = date.strftime("%y/%m/%d")



if __name__ == '__main__':
    gd = GetDate()
    print(gd.weekday, gd.date)
