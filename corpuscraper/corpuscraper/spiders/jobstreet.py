# -*- coding: utf-8 -*-
import scrapy, urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

from corpuscraper.items import CorpuscraperItem


class JobstreetSpider(CrawlSpider):
    name = 'jobstreet'
    allowed_domains = ['jobstreet.com.sg']
    rules = [Rule(LinkExtractor(allow=r'en\/job\/\d+.*|en\/job-search\/job-vacancy\.php\?key='), callback='parse_item', follow=True)]

    def __init__(self, category=None, *args, **kwargs):
        super(JobstreetSpider, self).__init__(*args, **kwargs)
        category = urllib.quote(category).replace('%20', '+')
        self.start_urls = ['http://www.jobstreet.com.sg/en/job-search/job-vacancy.php?key=%s' % category]

    def parse_item(self, response):
        i = CorpuscraperItem()
        jd = response.xpath('//*[@id="job_description"]//text()').extract()
        if len(jd)>0:
            text = ' '.join(jd)
            i['jd'] = text
            i['url'] = response.url
            title = response.xpath('//*[@id="position_title"]/text()').extract()
            i['title'] = title[0]
            logging.info(i['title'])
        return i