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
#石家庄采购公告
class zgazxxwNoticesSpider(scrapy.Spider):
	name = "zgazxxwNotices"
	allowed_domains = ["zgazxxw.com"]
	
	def getlist():
		seq = []
		#200
		for i in range(0,201):
			seq.append("http://www.zgazxxw.com/he-012008l772-"+str(i)+".html")
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		print(response.url)
		req = []
		for sel in response.xpath('//a[contains(@href, "www.zgazxxw.com/zbpd/zbgg/")]'):
			url = sel.xpath('.//@href').extract()[0]
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
		opath = os.path.abspath("./石家庄采购公告/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
