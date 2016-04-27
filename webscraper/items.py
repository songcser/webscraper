# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_paths = scrapy.Field()
    filepath = scrapy.Field()
    filename = scrapy.Field()
    content_type = scrapy.Field()
    proxy = scrapy.Field()
