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
#济南中标结果
class jinanccgpDisclosuresSpider(scrapy.Spider):
	name = "jinanccgpDisclosures"
	allowed_domains = ["ccgp-jinan.gov.cn"]
	
	def getlist():
		seq = []
		#1541
		for i in range(1,1542):
			seq.append("http://www.ccgp-jinan.gov.cn/jngp/site/list.jsp?curpage="+str(i)+"&colid=38")
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		print(response.url)
		req = []
		for sel in response.xpath('//a[contains(@href, "/jngp/site/read")]'):
			url = "http://www.ccgp-jinan.gov.cn" + sel.xpath('.//@href').extract()[0]
			title = sel.xpath('.//@title').extract()[0].replace('\\','').replace('/','').replace(':','').replace('?','').replace('*','').replace('<','').replace('>','').replace('|','').replace('"','').replace("'",'')
			#print(url,title)
			r = Request(url, meta={'title': title},method="GET",callback=self.parse_details)
			req.append(r)
		return req
		
	def parse_details(self,response):
		""""""
		html = response.xpath('//body').extract()[0]
		filepath = response.meta['title'] + '.html'
		#print(filepath)
		opath = os.path.abspath("./济南中标结果/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
