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
#北京采购公告
class bgpcNoticesSpider(scrapy.Spider):
	name = "bgpcNotices"
	allowed_domains = ["bgpc.gov.cn"]
	
	def getlist():
		seq = []
		for i in range(1,106):
			seq.append("http://www.bgpc.gov.cn/news/news/nt_id/29/page/"+str(i))
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		req = []
		for sel in response.xpath('//a[contains(@href, "news_id")]'):
			for i in sel.xpath('@href').extract():
				url = "http://www.bgpc.gov.cn" + i
				title = sel.xpath('text()').extract()[0]
				#print(url)
				r = Request(url, meta={'title': title}, callback=self.parse_details)
				req.append(r)
		return req
		
	def parse_details(self,response):
		""""""
		html = response.xpath('//div[@id="news_word"]').extract()[0]
		#print(html)
		filepath = response.meta['title'] + '.html'
		opath = os.path.abspath("./北京采购公告/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
