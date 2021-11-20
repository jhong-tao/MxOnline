#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> db_utils.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：
==================================================
"""
import redis
from MxOnline.settings import REDIS_HOST, REDIS_PORT


def redis_set(key, value, expire_time):
    """
    redis_set函数用来存储k-v键值对数据到redis中
    :param key: key ->string
    :param value: value ->string
    :param expire_time: expire time 过期时间，输入分钟数
    :return: None
    """
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf-8', decode_responses=True)
    r.set(str(key), value)
    r.expire(str(key), expire_time*60)


def redis_get(key):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf-8', decode_responses=True)
    return r.get(str(key))
     
