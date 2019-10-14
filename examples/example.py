#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import os
import sys
import requests
from bs4 import BeautifulSoup

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir)


def get_proxy():
    response = requests.get('http://localhost:9999/get')
    proxy = BeautifulSoup(response.text, 'lxml').text
    return proxy


def crawl(url, proxy):
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    try:
        response = requests.get(url=url, proxies=proxies)
        print('Getting result', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None


def main():
    proxy = get_proxy()
    html = crawl("https://www.baidu.com/", proxy)
    print(html)


if __name__ == '__main__':
    main()
