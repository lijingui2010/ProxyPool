#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    """
            元类，在ProxyCrawler类中加入
            __CrawlFunc__和__CrawlFuncCount__
            两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxyCrawler(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval('self.{}()'.format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    '''方便起见，我们将获取代理的每个方法统一定义为以crawl开头，这样扩展的时候只需要添加crawl开头的方法即可'''


    def crawl_kuaidaili(self, page_count=4):
        """
               获取代理kuaidaili
               :param page_count: 页码
               :return: 代理
        """
        for page in range(1, page_count + 1):
            # 国内高匿代理
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                items = doc("#list table tbody tr").items()
                for item in items:
                    ip = item('td').filter(lambda i, this: pq(this).attr('data-title') == 'IP').text()
                    port = item('td').filter(lambda i, this: pq(this).attr('data-title') == 'PORT').text()
                    result = ip + ':' + port
                    yield result.replace(' ', '')


    def crawl_66ip(self, page_count=4):
        """
               获取代理66
               :param page_count: 页码
               :return: 代理
        """
        for page in range(1, page_count + 1):
            start_url = 'http://www.66ip.cn/{}.html'.format(page)
            html = get_page(start_url)
            if html:
                doc = pq(html)
                items = doc('.containerbox table tr:gt(0)').items()
                for item in items:
                    ip = item('td')[0].text
                    port = item('td')[1].text
                    result = ip + ':' + port
                    yield result.replace(' ', '')

    def crawl_xicidaili(self, page_count=4):
        """
               获取代理xicidaili
               :param page_count: 页码
               :return: 代理
        """
        for page in range(1, page_count + 1):
            start_url = 'https://www.xicidaili.com/wt/{}'.format(page)
            html = get_page(start_url)

            if html:
                doc = pq(html)
                items = doc('#ip_list tr:gt(0)').items()
                for item in items:
                    ip = item('td')[1].text
                    port = item('td')[2].text
                    result = ip + ':' + port
                    print(result.replace(' ', ''))
                    yield result.replace(' ', '')

