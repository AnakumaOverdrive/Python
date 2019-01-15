#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import ClassifyItem
from scrapy import Request
from scrapy.selector import Selector 
import json

#---------------------------------------------------------------------------
class JdSpider(scrapy.Spider):
	name = "cl"
	allowed_domains = ["cl.mscsu.com/"]
	start_urls = [
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=1",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=2",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=3",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=4",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=5",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=6",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=7",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=8",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=9",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=10",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=11",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=12",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=13",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=14",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=15",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=16",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=17",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=18",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=19",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=20",
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=21"
	] 
		
	start_urls2 = [
		"http://cl.mscsu.com/thread0806.php?fid=20&search=&page=21"
	] 
	def parse(self,response):
		"""分别获得商品地址和下一页地址"""
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
			item['url'] = 'http://cl.mscsu.com/' + url[0]
			yield item
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
