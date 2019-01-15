#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector 
import json

#---------------------------------------------------------------------------
class JdSpider(scrapy.Spider):
	name = "product"
	allowed_domains = ["jd.com"]
	start_urls = [
		#"https://list.jd.com/list.html?cat=670,671,2694"	#平板电脑
		#"https://list.jd.com/list.html?cat=670,671,5146"	#平板电脑配件
		#"https://list.jd.com/list.html?cat=670,677,11762"	#组装电脑
		"https://list.jd.com/list.html?cat=670,671,672"		#笔记本
		"https://list.jd.com/list.html?cat=670,671,1105"	#游戏本
	] 
		
		
	def parse11(self,response):
		url = 'https://item.jd.com/3653810.html#comment';
		r =  Request(url, self.parse_product)
		return r
		
	def parse(self,response):
		"""分别获得商品地址和下一页地址"""
		req = []
		#获得下一页地址
		next_list = response.xpath('//a[@class="pn-next"]/@href').extract()
		if next_list:
			next_url = "https://list.jd.com" + next_list[0]
			#print(next_url)
			r = Request(next_url, self.parse)
			req.append(r)
		#获得商品地址
		for sel in response.xpath('//a'):
			for i in sel.xpath('@href').extract():
				if '//item.jd.com/' in i:
					url = "https:" + i
					#print(url)
					r =  Request(url, self.parse_product)
					req.append(r)
		return req
		
	def parse_product(self,response):
		"""商品页获取title,price,product_id"""
		title =response.xpath('//title/text()').extract()[0]
		product_id = response.url.split('/')[-1][:-5]
		
		item = TutorialItem()
		
		item['title'] = title[:title.rindex('【')]
		item['product_id'] =product_id
		item['url'] = response.url

		priceUrl = 'http://p.3.cn/prices/mgets?skuIds=J_' + product_id
		return  Request(priceUrl, meta={'item': item}, callback=self.parsePrice,dont_filter=True)

	def parsePrice(self, response):  
		"""获得商品价格 京东价格是js生成的，我只会这样获取产品价格  
			模拟js访问此网站，获取商品价格，返回的是str 
			类似 [{'p': '128.00', 'm': '188.00', 'id': 'J_10682977360'}]"""
		sel = Selector(text=response.body)  
		try: 
			text = sel.xpath("//text()").extract()[0]
			decodejson = json.loads(text)
			price = decodejson[0]["p"]#京东价
		except Exception as ex:  
			print('Exception: ',ex);   
			price = 0   
		item = response.meta['item']
		item['price'] = price   
		
		evaluateUrl = 'http://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId=' + item['product_id']
		yield Request(evaluateUrl, meta={'item': item}, callback=self.parseEvaluate,dont_filter=True)
	
	def parseEvaluate(self, response):
		"""获得商品评价信息
			模拟js访问此网站，获取商品评价信息，返回的是str 
			类似 {"SkuId":3653810,"ProductId":3653810,"Score1Count":8,"Score2Count":2,"Score3Count":7,
			"Score4Count":36,"Score5Count":624,"ShowCount":371,"CommentCount":677,"AverageScore":5,
			"GoodCount":660,"GoodRate":0.976,"GoodRateShow":98,"GoodRateStyle":146,"GeneralCount":9,
			"GeneralRate":0.013,"GeneralRateShow":1,"GeneralRateStyle":2,"PoorCount":8,"PoorRate":0.011,"PoorRateShow":1,"PoorRateStyle":2}"""
		sel = Selector(text=response.body)  
		try: 
			text = sel.xpath("//text()").extract()[0]
			decodejson = json.loads(text)
			number = decodejson["CommentCount"]#评价数
		except Exception as ex:  
			print('Exception: ',ex);  
			number = 0   
		item = response.meta['item']  
		item['number'] = number   
		yield item

			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
