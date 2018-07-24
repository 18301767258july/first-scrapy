# -*- coding: utf-8 -*-
import scrapy

import re
import datetime
from scrapy.http import Request
from urllib import parse
from blog_jobbole.items import BlogJobboleItem
from blog_jobbole.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = (
        'http://blog.jobbole.com/all-posts/',
    )

    def parse(self, response):
        #next_url.extract()[0].decode('utf8')
        post_nodes = response.xpath('//div[@class="post-thumb"]/a')
        for node in post_nodes:
            print("-----------------------------------")
            img_url = node.xpath('./img/@src').extract_first()
            print(img_url)
            post_url = node.xpath('@href').extract_first()
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_img_url":img_url},callback=self.get_url_info)
        next_url = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href').extract()[0]
        #//*[@id="post-114208"]/div[3]/div[3]/span[2]/text()
        yield Request(url = parse.urljoin(response.url,next_url),callback=self.parse)
    def get_url_info(self,response):

        article_item = BlogJobboleItem()

        front_img_url = response.meta.get("front_img_url","")
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]

        praise_nums = response.xpath('//h10/text()').extract()[0]
        match_obj = re.match(".*(\d+.*)", praise_nums)
        if match_obj:
            praise_num = int(match_obj.group(1))
        else:
            praise_num = 0

        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(".","")
        #response.xpath('//span[contains(@class,'vote-post-up')]/text()')
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        match_obj = re.match(".*(\d+).*",fav_nums)
        if match_obj:
            fav_num = int(match_obj.group(1))
        else:
            fav_num = 0
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_obj = re.match(".*(\d+).*",comment_nums)
        if match_obj:
            comment_num = int(match_obj.group(1))
        else:
            comment_num = 0
        content = response.xpath('//div[@class="entry"]').extract()[0]
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(".","")
        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        article_item["front_img_url"] = [front_img_url]
        article_item["title"] = title
        try:
            create_date = datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["praise_num"] = praise_num
        article_item["fav_num"] = fav_num
        article_item["comment_num"] = comment_num
        article_item["content"] = content
        article_item["tags"] = tags
        article_item["url"] = response.url
        article_item["url_obj_id"] = get_md5(response.url)
        yield article_item

