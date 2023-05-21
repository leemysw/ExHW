#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# =====================================================
# @Project：dlbase
# @File   ：backend_api
# @Date   ：2021/4/30 19:07
# @Author ：leemysw
# @Modify Time      @Author    @Version    @Description
# ------------      -------    --------    ------------
# 2021/4/30 19:07   leemysw      1.0.0         Create

# =====================================================
import logging

import requests
from .utils import Singleton


class BaseRequest(metaclass=Singleton):
    def __init__(self, logger=logging):
        self.logger = logger

    def _parse_response(self, response):
        if not response:
            self.logger.error('self-defined', 'API接口不存在')
            

        if response['code'] != 200:
            self.logger.debug(response)
            self.logger.error('self-defined', '上传数据失败')
            self.logger.error(response['code'], response['msg'])
        return response

    def _request(
            self,
            url,
            method,
            *,
            json_data: dict = None,
            data: dict = None,
            params: dict = None,
            headers: dict = None,
            files=None,
            **kwargs
    ):
        if params is None:
            params = {}
        if json_data is None:
            json_data = {}
        if data is None:
            data = {}
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        try:
            response = requests.request(url=url,
                                        method=method,
                                        params=params,
                                        json=json_data,
                                        data=data,
                                        headers=headers,
                                        files=files,
                                        **kwargs)

            return response
        except Exception:
            self.logger.exception('无法连接服务器')
            return {'success': 0, 'code': 500}

    def _get(self, url, params=None, **kwargs):
        response = self._request(url=url, method='GET', params=params, **kwargs)
        return response

    def _post(self, url, *, params=None, json_data=None, data=None, headers=None, files=None):
        
        response = self._request(url=url, method='POST', params=params, json_data=json_data, data=data, headers=headers,
                                 files=files)
        
        return response
