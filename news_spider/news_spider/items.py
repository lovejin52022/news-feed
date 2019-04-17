# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    article_html = scrapy.Field()
    link_hash = scrapy.Field()
    source_url = scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
    images = scrapy.Field()
    movies = scrapy.Field()
    authors = scrapy.Field()
    publish_date = scrapy.Field()
    meta_lang = scrapy.Field()

