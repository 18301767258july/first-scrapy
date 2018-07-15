# -*- coding: utf-8 -*-

import codecs
import json
from scrapy.exporters import JsonItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline

class BlogJobbolePipeline(object):
    def process_item(self, item, spider):
        #import pdb
        #pdb.set_trace()
        return item

class JsonWithEncodingPipeline(object):
    #自定义导出json文件的pipelines
    def __init__(self):
        self.file = codecs.open('article.json', 'w', 'utf-8')
    def process_item(self,item,spider):

        print(dict(item))
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipeline(object):
    #scrapy 自带json exporter导出 json文件
    def __init__(self):
        self.file = open('json_exporter.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding = 'utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

class ArticleImagePipelines(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_path = value['path']
            item["front_img_path"] = image_path
        return item

