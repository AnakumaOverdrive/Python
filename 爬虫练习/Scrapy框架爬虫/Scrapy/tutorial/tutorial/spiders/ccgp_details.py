#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from scrapy import Request
from scrapy.selector import Selector 
from tutorial.items import CcpgDetailItem
import json
import sqlite3

#---------------------------------------------------------------------------

def buildArray():
	conn=sqlite3.connect("Ccpg.db")
	cursor = conn.cursor()
	cursor.execute('select * from ccpg_beijing')
	values = cursor.fetchall()
	links = []
	for val in values:
		links.append(val[2])
	return links
	
	# links = ["http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/t20180103_873512.html"]
	# return links
	
class CcpgDetailspider(scrapy.Spider):
	name = "ccpg_details"
	allowed_domains = [""]
	start_urls = buildArray()
		
	def parse(self,response):
		htmltext = []
		item = CcpgDetailItem()
		item["link"] = response.url
		
		for sel in response.xpath('//div'):
			
			texts = sel.xpath('p/text()').extract()
			if len(texts) > 0:
				for text in texts:
					text = text.replace(' ','').replace('\n','').replace('\t','')
					if len(text) > 0:
						htmltext.append(text)
		item["content"] = ''.join(htmltext)
		return item
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
