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
class hbccgpNoticesSpider(scrapy.Spider):
	name = "hbccgpNotices"
	allowed_domains = ["ccgp-hebei.gov.cn"]
	
	def getlist():
		seq = []
		#70
		for i in range(1,70):
			seq.append("http://www.ccgp-hebei.gov.cn/zfcg/web/getBidingList_"+str(i)+".html")
		return seq;
		
	start_urls = getlist()

	def parse(self,response):
		""""""
		print(response.url)
		req = []
		#onclick="watchContent('567','1');"
		#watchContent(fid,flag)
		#"/zfcg/"+flag+"/bidingAnncDetail_"+fid+".html"
		#<form id="contentform" method="post" action="/zfcg/bidingAnncDetail.html" target="_blank">
		#	<input id="fid" name="fid" type="hidden"/>
		#	<input name="citycode" type="hidden" value="130000000"/>
		#	<input name="cityname" type="hidden" value="省本级"/>
		#</form>

		#table[@id="moredingannctable")]/
		for sel in response.xpath('//tr[contains(@onclick, "watchContent")]'):
			parameter = sel.xpath('@onclick').extract()[0].replace('watchContent(','').replace(');','').replace("'",'').split(',')
			url = "http://www.ccgp-hebei.gov.cn/zfcg/"+parameter[1]+"/bidingAnncDetail_"+parameter[0]+".html"
			title  = sel.xpath(".//td/a[@class='a3']/text()").extract()[0].replace('\\','').replace('/','').replace(':','').replace('?','').replace('*','').replace('<','').replace('>','').replace('|','').replace('"','').replace("'",'')
			r = Request(url, meta={'title': title,'citycode':'130000000','cityname':'省本级'},method="POST",callback=self.parse_details)
			req.append(r)
		return req
		
	def parse_details(self,response):
		""""""
		html = response.xpath('//body').extract()[0]
		filepath = response.meta['title'] + '.html'
		#print(filepath)
		opath = os.path.abspath("./河北采购公告/" + filepath) 
		basedir = os.path.dirname(opath) 
		if not os.path.exists(basedir): 
			os.makedirs(basedir) 
		#print(opath)
		with open(opath, 'w',encoding='utf-8') as f: 
			f.write(html)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
