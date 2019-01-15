#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import cqgpDisclosuresDetailsItem
from scrapy import Request
from scrapy.selector import Selector 
import json,time
import os, os.path 

#---------------------------------------------------------------------------
class cqgpDisclosuresSpider(scrapy.Spider):
	name = "cqgpDisclosures"
	allowed_domains = ["cqgp.gov.cn"]
	#349
	def getlist():
		seq = []
		for i in range(1,350):
			#https://www.cqgp.gov.cn/gwebsite/api/v1/singles/facade/getsingles?pi=1&ps=20&state=1&timestamp=1476612931140
			seq.append("https://www.cqgp.gov.cn/gwebsite/api/v1/singles/facade/getsingles?pi="+str(i)+"&ps=20&state=1&timestamp=" + str(int(time.time())) +",")
		return seq;
		
	start_urls = getlist()
	
	def parse(self,response):
		print(response.url)
		req = []
		sites = json.loads(response.body_as_unicode())  

		for site in sites['singles']:  
			#https://www.cqgp.gov.cn/gwebsite/api/v1/singles/preview/363034686911639552?timestamp=1476613287470
			next_url = "https://www.cqgp.gov.cn/gwebsite/api/v1/singles/preview/"+site["id"]+"?timestamp=" + str(int(time.time()))
			r = Request(next_url, self.parse_details)
			req.append(r)
			
		return req
		
	def parse_details(self,response):
		"""获取详情页面"""
		sites = json.loads(response.body_as_unicode())  
		html = sites["html"].replace('//n//r','').replace('//t','')
		
		filepath = sites["singles"]["title"] + '.html'
		opath = os.path.abspath("./重庆中标结果/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
			
		#item = cqgpDisclosuresDetailsItem()
		#item["id"] = sites["singles"]["id"]
		#item["publicityTime"] = sites["singles"]["publicityTime"]
		#item["title"] = sites["singles"]["title"]
		#item["attachments"] = sites["singles"]["attachments"]
		#item["auditResult"] = sites["singles"]["auditResult"]
		#yield item
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
