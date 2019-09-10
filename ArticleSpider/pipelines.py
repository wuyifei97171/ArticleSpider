# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

#继承images.pipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


import MySQLdb
import MySQLdb.cursors

#pipeline中主要是与数据库操作，将数据库持久化的
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

#用于保存json的pipline
class JsonWithEncodingPipline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8")
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipleline(object):
    #调用scrapy提供的json export 导出json文件
    def __init__(self):
        self.file = open('articleexport.json','wb') #wb是二进制的方式
        self.exporter = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','wuyifei','wuyifei123','article_spider',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = """
            INSERT INTO article(title,url,url_object_id,create_date,fav_nums)
            VALUES (%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["url_object_id"],item["create_date"],item["fav_nums"]))
        self.conn.commit()

class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    #使用这个方法可以直接获取settings.py中的值
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)

        return cls(dbpool)

    def process_item(self,item,spider):
        #使用Twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)   #处理异常

    def handle_error(self,failure):
        #处理异步处理插入的异常
        print(failure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    INSERT INTO article(title,url,url_object_id,create_date,fav_nums)
                    VALUES (%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,
                            (item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"]))

#自定义pipeline
class AritcleImagePipeline(ImagesPipeline):
    # 可以用于获取文件的实际下载地址
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            #获得results中 path 值
            for ok,value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item
