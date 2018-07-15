# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogJobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    url_obj_id = scrapy.Field()
    praise_num = scrapy.Field()
    create_date = scrapy.Field()
    fav_num = scrapy.Field()
    comment_num = scrapy.Field()
    front_img_url = scrapy.Field()
    fromt_img_path = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    pass
