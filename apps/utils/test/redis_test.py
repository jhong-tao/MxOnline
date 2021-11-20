#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
==================================================
@Project -> File   ：MxOnline -> redis_test.py
@IDE    ：PyCharm
@Author ：jhong.tao
@Date   ：2021/6/7 10:34
@Desc   ：redis 使用测试
==================================================
"""
"""
启动redis服务：redis-server.exe
启动redis客户端：redis-cli.exe
插入k-v键值对：set "key" "value"
查询k-v键值对：get "key"
"""
import redis

# 实例化redis客户端对象
r = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
r.set('mobile', '123')
r.expire('mobile', 30)  # 设置键值对的过期时间，意思30秒过后redis自动删除这个键值对
print(r.get('mobile'))
