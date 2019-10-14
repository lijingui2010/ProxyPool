#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import redis
from .settings import *
from random import choice
from .error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
              初始化
              :param host: Redis 地址
              :param port: Redis 端口
              :param password: Redis密码
        """
        self._db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
               添加代理，设置分数为初始分数
               :param proxy: 代理
               :param score: 分数
               :return: 添加结果
        """
        if not self._db.zscore(REDIS_KEY, proxy):
            return self._db.zadd(REDIS_KEY, {proxy: score})

    def get_one(self):
        """
               随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，选取前一半，然后随机选择一个返回,
               否则异常
               :return: 随机代理
        """
        results = self._db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(results):
            return choice(results)
        else:
            results = self._db.zrevrange(REDIS_KEY, 0, self.queue_len // 2)
            if len(results):
                return choice(results)
            else:
                raise PoolEmptyError

    def get_all(self):
        """
               获取全部代理
               :return: 全部代理列表
        """
        return self._db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def delete(self, proxy):
        """
               代理值减5分，分数小于最小值，则代理删除
               :param proxy: 代理
               :return: 修改后的代理分数
        """
        score = self._db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减5')
            return self._db.zincrby(REDIS_KEY, -5, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self._db.zrem(REDIS_KEY, proxy)

    def modify(self, proxy):
        """
               将代理设置为MAX_SCORE
               :param proxy: 代理
               :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self._db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def exists(self, proxy):
        """
              判断是否存在
              :param proxy: 代理
              :return: 是否存在
        """
        return self._db.zscore(REDIS_KEY, proxy) is not None

    @property
    def queue_len(self):
        """
              获取数量
              :return: 数量
        """
        return self._db.zcard(REDIS_KEY)