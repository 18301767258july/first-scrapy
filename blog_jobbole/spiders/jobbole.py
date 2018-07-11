# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = (
        'http://www.blog.jobbole.com/all-posts/',
    )

    def parse(self, response):
        #next_url.extract()[0].decode('utf8')
        urls=response.xpath('//a[@class="archive-title"]/@href')
        for url in urls:
            yield Request(url=url,callback=self.get_url_info)
        next_url=response.xpath('//*[@id="archive"]/div[21]/a[4]/@href')
        Request(url=next_url,callback=self.parse)
    def get_url_info(self,url,response):
        title=response.xpath('//div[@class="entry-header"]/h1/text()')
        zan=response.xpath('//h10/text()')
        
