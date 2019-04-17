# -*- coding: utf-8 -*-
import scrapy
from ..utils import common_parse_content
import re

class GovSpider(scrapy.Spider):
    name = 'gov'
    allowed_domains = ['gov.cn']
    start_urls = [
        'http://sousuo.gov.cn/column/30613/0.htm',
        'http://sousuo.gov.cn/column/30902/0.htm',
        'http://sousuo.gov.cn/column/30611/0.htm',
    ]


    def parse(self, response):
        article_list = response.xpath('//ul[@class="listTxt"]/li/h4/a/@href').extract()
        for article in article_list:
            url = article
            yield scrapy.Request(url, callback=self.parse_content)
        # 进入下一页
        pages = response.xpath('//li/a[@class="next"]/@href').extract()
        if len(pages) > 0 :
            next_page = pages[0]
            yield scrapy.Request(next_page, callback=self.parse)
        pass


    def parse_content(self, response):
        self.log("===========================开始解析| %s |" % response.url)
        item = common_parse_content(response.url, response.body, 'zh')
        self.log("===========================结束解析| %s |" % response.url)
        if item['images'] and len(item['images']) > 0 :
            images = []
            for image in item['images']:
                matchObj = re.match(r'^(https|http)(((?!de_bannerS_sjh|guohui).)*)(jpg|png|jpeg)$', image, re.I)
                if matchObj:
                    images.append(image)
            item['images'] = images
        yield item
        pass