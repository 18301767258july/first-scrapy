# -*- coding: utf-8 -*-

import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
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

class MysqlPipelines(object):
    def __init__(self):
        self.connect = MySQLdb.connect('localhost','root','zhao5254','test_scrapy',charset='utf8',use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into article(title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s)"

        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_num']))
        self.connect.commit()

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


class MysqlTwistedPipeline(object):

    def __init__(self,db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls,settings):
        # this args name is the same with MySQLdb connect function
        db_args = dict(
            host = settings['MYSQL_HOST'],
            user = settings['USER'],
            passwd = settings['PASS'],
            db = settings['DATABASE_NAME'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        db_pool = adbapi.ConnectionPool('MySQLdb',**db_args)
        return cls(db_pool)

    def process_item(self, item, spider):
        #异步执行sql语句
        query = self.db_pool.runInteraction(self.do_insert,item)
        #处理异常
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        #处理异常
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = "insert into article(title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s)"

        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_num']))


class ArticleImagePipelines(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_path = value['path']
            item["front_img_path"] = image_path
        return item

