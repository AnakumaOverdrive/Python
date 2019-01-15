# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class CcpgPipeline(object):

	collection_name = 'scrapy_items'

	def __init__(self, dbname):
		self.dbname = dbname
		self.conn = None
	
	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			#dbname=crawler.settings.get('Ccpg.db'),
			dbname = 'Ccpg.db'
		)
			
	def open_spider(self, spider):
		if spider.name == "ccpg" or spider.name == "ccpg_details":
			if path.exists(self.dbname):
				self.conn=sqlite3.connect(self.dbname)
			else:
				self.conn=self.create_table() 
	
	def close_spider(self, spider):
		if spider.name == "ccpg" or spider.name == "ccpg_details":
			if self.conn is not None:
				self.conn.commit()
				self.conn.close()
				self.conn=None
		
	#pipeline默认调用
	def process_item(self, item, spider):
		if spider.name == "ccpg":
			title = item['title'][0]
			link = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/'+item['link'][0].replace('./','')
			additem = item['addtime'][0]
			self.conn.execute('insert into ccpg_beijing values(?,?,?,?)',(None,title,link,additem)) 
			return item
		if spider.name == "ccpg_details":
			link = item['link']
			content = item['content']
			self.conn.execute('insert into ccpg_beijing_details values(?,?,?)',(None,link,content)) 
			return item
		return item
			
	def create_table(self):
		if spider.name == "ccpg" or spider.name == "ccpg_details":
			conn=sqlite3.connect(self.dbname)
			conn.execute("""create table ccpg_beijing(id integer primary key autoincrement,title text,link text,addtime text)""")
			conn.execute("""create table ccpg_beijing_details(id integer primary key autoincrement,link text,content text)""")
			conn.commit()
			return conn 
		return None
		
class TutorialPipeline(object):
	def process_item(self, item, spider):
		return item
