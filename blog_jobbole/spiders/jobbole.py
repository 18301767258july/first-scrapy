# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.http import Request


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = (
        'http://www.blog.jobbole.com/all-posts/',
    )

    def parse(self, response):
        #next_url.extract()[0].decode('utf8')
        urls = response.xpath('//a[@class="archive-title"]/@href')
        for url in urls:
            yield Request(url=url,callback=self.get_url_info)
        next_url = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href')
        Request(url = next_url,callback=self.parse)
    def get_url_info(self,url,response):
        title = response.xpath('//div[@class="entry-header"]/h1/text()')
        praise_num = int(response.xpath('//h10/text()'))
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(".","")
        #response.xpath('//span[contains(@class,'vote-post-up')]/text()')
         fav_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract("")[0]
        match_obj = re.match(".*(\d+.*)",fav_nums)
        if match_obj:
            fav_num = int(match_obj.group(1))
        else:
            fav_num = 0
        comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract("")[0]
        match_obj = re.match(".*(\d+.*)",comment_nums)
        if match_obj:
            comment_num = int(match_obj.group(1))
        else:
            comment_num = 0
        content = response.xpath('//div[@class="entry"]').extract()[0]
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]'/text()).extract()[0].strip().replace(".","")
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]'/a/text()).extract()
        tag_list = [element for element in tag_list if not element.strip().endwith("评论")]
        tags = ",".join(tag_list)
