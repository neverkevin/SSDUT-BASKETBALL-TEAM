#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tiantian_crawler import TiantianCrawler
from netease_crawler import NeteaseCrawler

# crawler = NeteaseCrawler()
crawler = NeteaseCrawler()
print crawler.query(u'我好想你', id='252999')
# print crawler.query(u'我好想你')
