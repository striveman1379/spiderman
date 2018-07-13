# -*- coding: utf-8 -*-

# Scrapy settings for spider_redis project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_redis'

SPIDER_MODULES = ['spider_redis.spiders']
NEWSPIDER_MODULE = 'spider_redis.spiders'



SCHEDULER = 'spiderman.contrib.schedulers.SpidermanScheduler'



SPIDER_MIDDLEWARES = {
    'spiderman.contrib.middlewares.SpiderMiddleware': 0
}

from .backends import *

REQUESTER = {
    'MODULE': 'spiderman.contrib.requesters.redis.RedisRequester',
    'BACKEND': 'redis',
    'QUEUE_KEY': 'requester',
}


ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}