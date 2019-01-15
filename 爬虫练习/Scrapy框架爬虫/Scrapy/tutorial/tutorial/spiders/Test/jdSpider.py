#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re

from scrapy import Request
from scrapy.selector import Selector 

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import SitemapSpider
import json

#---------------------------------------------------------------------------
class JdSpider(SitemapSpider):
	name = "jd"
	sitemap_urls = ['http://jandan.net/']

	
	def parse(self,response):
		print('Hi, %s' % response.url)
		self.log('Hi, %s' % response.url)
		pass

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
