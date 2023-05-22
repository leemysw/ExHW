# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# =====================================================
# @Project：ExHW
# @File   ：utils
# @Date   ：2023/5/20 21:21
# @Author ：leemysw
# @Modify Time      @Author    @Version    @Description
# ------------      -------    --------    ------------
# 2023/5/20 21:21   leemysw      1.0.0         Create

# =====================================================
import sys
import os
import time
import json
import socket
import signal
import functools
import itertools
import datetime
import weakref
import threading

from inspect import Signature, Parameter
from functools import wraps
from contextlib import contextmanager



ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../'


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def abspath(r_path):
    path = os.path.abspath(os.path.join(ROOT_PATH, r_path))
    sh_path = '/'.join(path.split('\\'))

    return sh_path


def srcpath(r_path):
    path = os.path.abspath(os.path.join(ROOT_PATH + 'resources/', r_path))
    sh_path = '/'.join(path.split('\\'))

    return sh_path


@contextmanager
def timeblock(label):
    start = time.time()
    try:
        yield
    finally:
        if time.time() - start != 0:
            print('{:15s} : {:5d} -- {:.6f}'.format(label, int(1 / (time.time() - start)), time.time() - start))


# ------------------------------------------------------------------- #
def runtime(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        t = time.perf_counter()
        ret = func(*args, **kwargs)
        print('\n')
        print('-------------------------------')
        print('|', datetime.datetime.now())
        print('|', func.__name__, (time.perf_counter() - t), '|')
        print('|', func.__name__, 1 / (time.perf_counter() - t), '|')
        print('-------------------------------')
        return ret

    return wrap


def retry(delays=(0, 1, 5, 30, 180, 600, 3600)):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            for delay in itertools.chain(delays, [None]):
                if delay is not None:
                    ret = func(*args, **kwargs)
                    success = int(ret.get('success', None))
                    if not success:
                        code = int(ret.get('code', None))
                        if code == 500:
                            return None
                        else:
                            time.sleep(delay)
                    else:
                        return ret

        return wrapped

    return wrapper


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def shutdown_func(sig, frame):
    print('close')
    print('=' * 50)
    print('-' * 50)
    print('=' * 50)


def shutdown(func=shutdown_func):
    for sig in [signal.SIGQUIT, signal.SIGTERM, signal.SIGKILL]:
        signal.signal(sig, func)


def check_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def make_sig(*names):
    parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    return Signature(parms)


def synchronized(func):
    """
    Decorator in order to achieve thread-safe singleton class.
    """
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


# ===========================================================================================

# ========================== 单例模式 ==========================

class SingleInstanceMetaClass(type):
    __cache = weakref.WeakValueDictionary()

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        cache_key = cls.cache(**kwargs)
        if cache_key is None:
            cache_key = 'default'

        if cache_key in cls.__cache:
            return cls.__cache[cache_key]

        new_class = cls.__new__(cls)
        new_class.__init__(*args, **kwargs)
        cls.__cache[cache_key] = new_class
        return new_class

    @staticmethod
    def cache(**kwargs):
        key = kwargs.get('name', None)
        return key

    @synchronized
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance


# ========================== 单例模式 ==========================

class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("can't instantiate directly")


class StructureMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsdict['__signature__'] = make_sig(*clsdict.get('_fields', []))
        return super().__new__(cls, clsname, bases, clsdict)


class BaseStructure_s(metaclass=StructureMeta):
    _fields = []

    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)

        for name, values in bound_values.arguments.items():
            setattr(self, name, values)


class BaseStructure:
    _fields = []
    _default = []

    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for key, value in zip(self._fields, args):
            setattr(self, key, value)

        extra_args = kwargs.keys() - self._fields
        for key in extra_args:
            setattr(self, key, kwargs.pop(key))

        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)