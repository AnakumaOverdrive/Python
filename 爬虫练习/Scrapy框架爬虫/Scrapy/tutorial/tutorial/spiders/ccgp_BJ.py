#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from scrapy import Request
from scrapy.selector import Selector 
from tutorial.items import CcpgItem
import json

#---------------------------------------------------------------------------
link = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/index%s.html'

def buildArray():
	arr = []
	for i in range(0,1):
		if i== 0:
			arr.append(link % '')
		else:
			arr.append(link % ('_'+ str(i)))
	return arr
	
class Ccpgpider(scrapy.Spider):
	name = "ccpg"
	allowed_domains = [""]
	start_urls = buildArray()
		
	def parse(self,response):
		#self.log('A response from %s just arrived!' % response.url)
		#items = []
		for sel in response.xpath('//ul/li'):
			#item = CcpgItem()
			#item["title"] = sel.xpath('a/text()').extract()
			#item["link"] = sel.xpath('a/@href').extract()
			#item["addtime"] = sel.xpath('span/text()').extract()
			#items.append(item)
			link = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/'+sel.xpath('a/@href').extract()[0].replace('./','')
			print(link)
			r =  Request(link, self.parse_details)
		#return items
			#yield item
			# print(title)
			# print(link)
			# print(desc)
		

	def parse_details(self,response):
		"""获取详情页面"""
		p = response.body
		print(p)
		# title =response.xpath('//title/text()').extract()[0]
		# item = TutorialItem()
		# product_id = response.url.split('/')[-1][:-5]
		# priceUrl = 'http://p.3.cn/prices/mgets?skuIds=J_' + product_id
		# r =  Request(priceUrl, callback=self.parsePrice,dont_filter=True)
		
		# item['title'] = title[:title.rindex('【')]
		# item['product_id'] =product_id
		# item['url'] = response.url
		# r.meta['item'] = item  
		# return r	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
