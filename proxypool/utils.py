#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import requests
from fake_useragent import UserAgent, FakeUserAgentError


def get_page(url, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError as e:
        print("Fake User Agent Error:", e)

    base_headers = {
        'User-Agent': ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    headers = dict(base_headers, **options)
    print('Getting', url, headers)
    try:
        response = requests.get(url, headers=headers)
        print('Getting result', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None
