# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# =====================================================
# @Project：ExHW
# @File   ：logger
# @Date   ：2023/5/20 21:19
# @Author ：leemysw
# @Modify Time      @Author    @Version    @Description
# ------------      -------    --------    ------------
# 2023/5/20 21:19   leemysw      1.0.0         Create

# =====================================================

import sys
import time
import pathlib
import logging
from typing import Optional
from logging import handlers
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from .utils import abspath

def setup_logger(name: str,
                 save_log: Optional[bool] = False,
                 filename: Optional[str] = None,
                 mode: str = 'w',
                 distributed_rank: bool = False,
                 stdout: bool = True,
                 socket: bool = False,
                 rotating_size: bool = False,
                 rotating_time: bool = False,
                 ):
    """
    日志模块

    :param name: 日志名称
    :param save_dir: 保存目录
    :param filename: 日志文件名
    :param mode: 写模式
    :param distributed_rank: 是否添加格式
    :param stdout: 是否终端输出
    :param save_log:
    :param socket:
    :param rotating_size: 是否按文件大小切割
    :param rotating_time: 是都按日期切割
    :return:
    """
    if name in logging.Logger.manager.loggerDict.keys():
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if distributed_rank:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s %(processName)-8s %(levelname)-8s| %(module)-20s| %(funcName)-15s| %(lineno)-3d | %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]: "
    )

    level = logging.DEBUG

    if stdout:
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if socket:
        socketHandler = handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        socketHandler.setLevel(level)
        socketHandler.setFormatter(formatter)
        logger.addHandler(socketHandler)

    if save_log or filename:
        if filename is None:
            filename = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + ".log"

        if not pathlib.Path(filename).parent.exists():
            pathlib.Path(filename).parent.mkdir()

        if rotating_time:
            # 每 1(interval) 天(when) 重写1个文件,保留7(backupCount) 个旧文件；when还可以是Y/m/H/M/S
            th = TimedRotatingFileHandler(filename, when='M', interval=1, backupCount=3, encoding="UTF-8")
            th.setLevel(level)
            th.setFormatter(formatter)
            logger.addHandler(th)

        if rotating_size:
            # 每 1024Bytes重写一个文件,保留2(backupCount) 个旧文件
            sh = RotatingFileHandler(filename, mode=mode, maxBytes=1024 * 1024, backupCount=5, encoding="UTF-8")
            sh.setLevel(level)
            sh.setFormatter(formatter)
            logger.addHandler(sh)

        else:
            fh = logging.FileHandler(filename, mode=mode, encoding="UTF-8")
            fh.setLevel(level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger


logger = setup_logger(name='logger', filename=abspath('logs/main.log'))
