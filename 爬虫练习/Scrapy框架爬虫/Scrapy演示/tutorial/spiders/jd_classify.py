#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import ClassifyItem
from scrapy import Request
from scrapy.selector import Selector 
import json

#---------------------------------------------------------------------------
class JdClassifySpider(scrapy.Spider):
	name = "classify"
	allowed_domains = ["jd.com"]
	start_urls = [
		"https://www.jd.com/allSort.aspx"
	]

	def parse(self, response):
		"""获得分类页面"""
		req = []
		item = ClassifyItem()
		for sel in response.xpath('//a'):
			for i in sel.xpath('@href').extract():
				if '//list.jd.com/' in i:
					url = "https:" + i
					itemName = sel.xpath('text()').extract()[0]
					item["url"] = url
					item["itemName"] = itemName
					yield item
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
