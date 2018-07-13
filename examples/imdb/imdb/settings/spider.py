# -*- coding: utf-8 -*-

# Scrapy settings for imdb project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'imdb'

SPIDER_MODULES = ['imdb.spiders']
NEWSPIDER_MODULE = 'imdb.spiders'



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
    'examples.imdb.imdb.pipelines.MysqlPipeline': 300,
}