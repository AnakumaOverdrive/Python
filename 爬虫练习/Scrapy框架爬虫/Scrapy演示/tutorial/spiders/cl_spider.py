#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import ClassifyItem
from scrapy import Request
from scrapy.selector import Selector 
import json

def getUrls():
	arr = []
	for i in range(1,26):
		arr.append("http://cl.koco.pw/thread0806.php?fid=20&search=&page="+str(i))
	return arr

#---------------------------------------------------------------------------
class JdSpider(scrapy.Spider):
	name = "cl"
	allowed_domains = ["cl.koco.pw"]
	start_urls = getUrls()
		
	def parse(self,response):
		for sel in response.xpath('//h3/a[@target="_blank"]'):
			#print(sel.xpath('@href'))
			item = ClassifyItem()
			name = sel.xpath('text()').extract()
			url = sel.xpath('@href').extract()
			if name:
				pass
			else:
				name = sel.xpath('child::font/text()').extract()
				print(name)
				
			item['itemName'] = name[0]
			item['url'] = 'http://cl.koco.pw/' + url[0]
			yield item
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
