#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import CqgpNoticesDetailsItem
from scrapy import Request
from scrapy.selector import Selector 
import json,time
import os, os.path 

#---------------------------------------------------------------------------
#重庆采购公告
class cqgpNoticesSpider(scrapy.Spider):
	name = "cqgpNotices"
	allowed_domains = ["cqgp.gov.cn"]
	
	def getlist():
		seq = []
		for i in range(7832,12954):
			seq.append("https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi="+str(i)+"&ps=20&timestamp=" + str(int(time.time())) +",")
		return seq;
		
	start_urls = getlist()
	
	def parse(self,response):
		print(response.url)
		req = []
		sites = json.loads(response.body_as_unicode())  

		for site in sites['notices']:  
			next_url = "https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable/"+site["id"]+"?timestamp=" + str(int(time.time()))
			r = Request(next_url, self.parse_details)
			req.append(r)
			
		return req
		
	def parse_details(self,response):
		"""获取详情页面"""
		sites = json.loads(response.body_as_unicode())  
		html = sites["html"].replace('//n//r','').replace('//t','')
		
		filepath = sites["notice"]["title"] + '.html'
		opath = os.path.abspath("./重庆采购公告/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
			
		item = CqgpNoticesDetailsItem()
		item["title"] = sites["notice"]["title"]
		item["projectPurchaseWay"] = sites["notice"]["projectPurchaseWay"]
		item["issueTime"] = sites["notice"]["issueTime"]
		item["noticeType"] = sites["notice"]["noticeType"]
		yield item
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
