#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from flask import Flask, g

from proxypool.db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/get')
def get_proxy():
    """
       获取随机可用代理
       :return: 随机代理
    """
    redis_cli = get_conn()
    return redis_cli.get_one()


@app.route('/count')
def get_counts():
    """
       获取代理池总量
       :return: 代理池总量
    """
    redis_cli = get_conn()
    return str(redis_cli.queue_len)


if __name__ == '__main__':
    app.run()
