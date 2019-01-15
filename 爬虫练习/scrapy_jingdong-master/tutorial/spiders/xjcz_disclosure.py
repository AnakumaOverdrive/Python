#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import ClassifyItem
from scrapy import Request
from scrapy.selector import Selector 
import json
import os, os.path 

#---------------------------------------------------------------------------
#新疆中标结果
class xjczDisclosureSpider(scrapy.Spider):
	name = "xjczDisclosure"
	allowed_domains = ["xjcz.gov.cn"]
	
	def getlist():
		seq = []
		#166
		for i in range(1,167):
			seq.append("http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=16&pagecount="+str(i))
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		print(response.url)
		req = []
		for sel in response.xpath('//a[contains(@href, "/mos/cms/html")]'):
			for i in sel.xpath('@href').extract():
				url = "http://zfcg.xjcz.gov.cn" + i
				title = sel.xpath('text()').extract()[0]
				#print(url,title)
				r = Request(url, meta={'title': title}, callback=self.parse_details)
				req.append(r)
		return req
		#return Request("http://zfcg.xjcz.gov.cn/mos/cms/html/1/15/201510/206878.html", meta={'title': "乌鲁木齐煤矿技工学校专用设备招标公告:(2015)GK-172号"}, callback=self.parse_details)
		
		
	def parse_details(self,response):
		""""""
		html = response.xpath('//div[@id="counts_info"]').extract()[0]
		#print(html)
		filepath = response.meta['title'] + '.html'
		print(filepath)
		opath = os.path.abspath("./新疆中标结果/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
