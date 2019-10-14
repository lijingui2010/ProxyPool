#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import time
from multiprocessing import Process

from proxypool.db import RedisClient
from proxypool.pool_adder import PoolAdder
from .proxy_tester import ProxyTester
from .settings import TESTER_CYCLE, POOL_LOWER_THRESHOLD, POOL_UPPER_THRESHOLD, POOL_LEN_CHECK_CYCLE, \
    PROXY_TESTER_ENABLED, POOL_ADDER_ENABLED, API_ENABLED, API_HOST, API_PORT
from .api import app


class Schedule(object):
    @staticmethod
    def schedule_tester(cycle=TESTER_CYCLE):
        """
               定时测试代理
        """
        tester = ProxyTester()
        while True:
            print('测试器开始运行')
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def schedule_pool_adder(lower_threshold=POOL_LOWER_THRESHOLD,
                            upper_threshold=POOL_UPPER_THRESHOLD,
                            cycle=POOL_LEN_CHECK_CYCLE):
        """
               定时获取代理 If the number of proxies less than lower_threshold, add proxy
        """
        pool_adder = PoolAdder(upper_threshold)
        redis = RedisClient()
        while True:
            print('开始抓取代理')
            if redis.queue_len < lower_threshold:
                pool_adder.add_to_queue()
            time.sleep(cycle)

    @staticmethod
    def schedule_api(host=API_HOST, port=API_PORT):
        """
               开启API
        """
        app.run(host, port)

    def run(self):
        if PROXY_TESTER_ENABLED:
            tester_process = Process(target=Schedule.schedule_tester)
            tester_process.start()

        if POOL_ADDER_ENABLED:
            adder_process = Process(target=Schedule.schedule_pool_adder)
            adder_process.start()

        if API_ENABLED:
            api_process = Process(target=Schedule.schedule_api)
            api_process.start()
            pass
