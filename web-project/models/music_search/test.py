#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tiantian_crawler import TiantianCrawler
from netease_crawler import NeteaseCrawler

# crawler = NeteaseCrawler()
crawler = TiantianCrawler()
print crawler.query('我好想你')
