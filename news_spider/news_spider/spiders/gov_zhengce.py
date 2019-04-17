# -*- coding: utf-8 -*-
import scrapy
import json
from ..utils import common_parse_content
import datetime
import re

class GovZhengceSpider(scrapy.Spider):
    name = 'gov_zhengce'
    allowed_domains = ['gov.cn']
    get_url = 'http://sousuo.gov.cn/data'

    p = 0
    data = {
        't': 'zhengce',
        'timetype': 'timeqb',
        'sort': 'pubtime',
        'sortType': str(1),
        'n': '20',
        'p': '0'
    }

    def start_requests(self):
        yield scrapy.FormRequest(self.get_url, method='GET', formdata=self.data, callback=self.parse_list)
        pass

    def parse_list(self, response):
        res = json.loads(response.body.decode('utf8'))
        search = res['searchVO']
        self.p = search['currentPage']
        cat_map = search['catMap']
        if cat_map:
            zhongyangfile = cat_map['zhongyangfile']
            gongwen = cat_map['gongwen']
            otherfile = cat_map['otherfile']
            if zhongyangfile['currentNum'] > 0 or gongwen['currentNum'] > 0 or otherfile['currentNum'] > 0:
                if zhongyangfile['currentNum'] > 0:
                    for item in zhongyangfile['listVO']:
                        url = item['url']
                        yield scrapy.Request(url,
                                             callback=lambda response, item=item: self.parse_content(response, item))
                        pass
                    pass
                if gongwen['currentNum'] > 0:
                    for item in zhongyangfile['listVO']:
                        url = item['url']
                        yield scrapy.Request(url,
                                             callback=lambda response, item=item: self.parse_content(response, item))
                        pass
                    pass
                if otherfile['currentNum'] > 0:
                    for item in zhongyangfile['listVO']:
                        url = item['url']
                        yield scrapy.Request(url,
                                             callback=lambda response, item=item: self.parse_content(response, item))
                        pass
                    pass
                self.data['p'] = str(self.p + 1)
                yield scrapy.FormRequest(self.get_url, method='GET', formdata=self.data, callback=self.parse_list)
                pass

        pass

    def parse_content(self, response, item):
        self.log("===========================开始解析| %s |" % response.url)
        yield_item = common_parse_content(response.url, response.body, 'zh')
        self.log("===========================结束解析| %s |" % response.url)
        yield_item['title'] = item['title']
        if item['pubtimeStr'] :
            yield_item['publish_date'] = datetime.datetime.strptime(item['pubtimeStr'], '%Y.%m.%d')
        if item['images'] and len(item['images']) > 0 :
            images = []
            for image in item['images']:
                matchObj = re.match(r'^(https|http)(((?!de_bannerS_sjh|guohui).)*)(jpg|png|jpeg)$', image, re.I)
                if matchObj:
                    images.append(image)
            item['images'] = images
        yield yield_item