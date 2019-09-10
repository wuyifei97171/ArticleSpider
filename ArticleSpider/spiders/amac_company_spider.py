# -*- coding: utf-8 -*-
import scrapy


class AmacCompanySpiderSpider(scrapy.Spider):
    name = 'amac_company_spider'
    allowed_domains = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html']
    start_urls = ['http://http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html/']

    def parse(self, response):
        pass
