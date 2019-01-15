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
#河北采购公告
class hbccgpDisclosuresSpider(scrapy.Spider):
	name = "hbccgpDisclosures"
	allowed_domains = ["ccgp-hebei.gov.cn"]
	
	def getlist():
		seq = []
		#63
		for i in range(1,64):
			seq.append("http://www.ccgp-hebei.gov.cn/zfcg/web/getBidWinAnncList_"+str(i)+".html")
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		print(response.url)
		req = []
		#onclick="watchContent('178');"
		#watchContent(fid)
		#"/zfcg/bidWinAnncDetail_"+fid+".html"
		#<form id="contentform" method="post" action="/zfcg/bidWinAnncDetail.html" target="_blank">
		#	<input id="fid" name="fid" type="hidden"/>
		#	<input name="citycode" type="hidden" value="130000000"/>
		#	<input name="cityname" type="hidden" value="省本级"/>
		#</form>


		#table[@id="moredingannctable")]/
		for sel in response.xpath('//tr[contains(@onclick, "watchContent")]'):
			parameter = sel.xpath('@onclick').extract()[0].replace('watchContent(','').replace(');','').replace("'",'')
			url = "http://www.ccgp-hebei.gov.cn/zfcg/bidWinAnncDetail_"+parameter+".html"
			title  = sel.xpath(".//td/a[@class='a3']/text()").extract()[0].replace('\\','').replace('/','').replace(':','').replace('?','').replace('*','').replace('<','').replace('>','').replace('|','').replace('"','').replace("'",'')
			r = Request(url, meta={'title': title,'citycode':'130000000','cityname':'省本级'},method="POST",callback=self.parse_details)
			req.append(r)
		return req
		
	def parse_details(self,response):
		""""""
		html = response.xpath('//body').extract()[0]
		filepath = response.meta['title'] + '.html'
		#print(filepath)
		opath = os.path.abspath("./河北中标结果/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
