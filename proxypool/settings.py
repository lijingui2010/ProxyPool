#!/usr/bin/env python3

# -*- coding: utf-8 -*-

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

# 测试API，用百度来测试
TEST_API = 'http://www.baidu.com'

# 代理池数量界限
POOL_LOWER_THRESHOLD = 100
POOL_UPPER_THRESHOLD = 1000

# 获得代理测试时间界限
GET_PROXY_TIMEOUT = 9

# 批量测试的最大值
BATCH_TEST_SIZE = 50

# 检查周期
TESTER_CYCLE = 60
POOL_LEN_CHECK_CYCLE = 20

# 三个常量PROXY_TESTER_ENABLED、POOL_ADDER_ENABLED、API_ENABLED都是布尔类型，表示测试模块、获取模块、接口模块的开关，如果都为True，则代表模块开启
PROXY_TESTER_ENABLED = True
POOL_ADDER_ENABLED = True
API_ENABLED = True

API_HOST = 'localhost'
API_PORT = 9999
