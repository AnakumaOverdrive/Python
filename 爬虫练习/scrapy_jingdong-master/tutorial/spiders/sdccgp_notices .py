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
#山东采购公告
class sdccgpNoticesSpider(scrapy.Spider):
	name = "sdccgpNotices"
	allowed_domains = ["ccgp-shandong.gov.cn"]
	
	def getlist():
		seq = []
		#663
		for i in range(1,664):
			seq.append("http://www.ccgp-shandong.gov.cn/sdgp2014/site/channelall.jsp?curpage="+str(i)+"&colcode=0301&subject=&pdate=")
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		print(response.url)
		req = []
		for sel in response.xpath('//a[contains(@class, "five")]'):
			url = "http://www.ccgp-shandong.gov.cn"+sel.xpath('.//@href').extract()[0]
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
		opath = os.path.abspath("./山东采购公告/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
