#!/usr/bin/env python3

# -*- coding: utf-8 -*-
from .error import ResourceDepletionError
from .db import RedisClient
from .crawler import ProxyCrawler
from .settings import POOL_UPPER_THRESHOLD


class PoolAdder(object):
    """
        add proxy to pool
    """

    def __init__(self, threshold=POOL_UPPER_THRESHOLD):
        """
               类初始化方法
               :param threshold: 代理池的最大数量
        """
        self._threshold = threshold
        self._redis = RedisClient()
        self._crawler = ProxyCrawler()

    def is_over_threshold(self):
        """
               判断是否达到了代理池限制
        """
        if self._redis.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        if not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                proxy_count += len(raw_proxies)
                for proxy in raw_proxies:
                    if self.is_over_threshold():
                        print('IP is enough, waiting to be used')
                        break
                    self._redis.add(proxy)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError
