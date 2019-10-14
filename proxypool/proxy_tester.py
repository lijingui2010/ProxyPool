#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientProxyConnectionError, ServerDisconnectedError, ClientResponseError, \
    ClientConnectorError, ClientOSError
from asyncio import TimeoutError
from .db import RedisClient
from .settings import TEST_API, GET_PROXY_TIMEOUT, BATCH_TEST_SIZE


class ProxyTester(object):
    def __init__(self):
        self._redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
               测试单个代理
               :param proxy: 单个代理
               :return: None
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(url=TEST_API, proxy=real_proxy, timeout=GET_PROXY_TIMEOUT) as response:
                        if response.status == 200:
                            print('代理可用', proxy)
                            self._redis.modify(proxy)
                        else:
                            print('请求响应码不合法', proxy)
                            self._redis.delete(proxy)
                except (ClientProxyConnectionError, ClientOSError, TimeoutError, ValueError):
                    self._redis.delete(proxy)
                    print('代理请求失败', proxy)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as s:
            print('test_single_proxy 发生错误', s)

    def test(self):
        """
               测试主函数
               :return: None
         """
        print('ProxyTester is working')
        try:
            proxies = self._redis.get_all()
            loop = asyncio.get_event_loop()

            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i: i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            print('测试器发生错误', e.args)
