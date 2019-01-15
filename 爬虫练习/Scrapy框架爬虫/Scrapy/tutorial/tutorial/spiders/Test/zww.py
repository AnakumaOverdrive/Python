#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import TutorialItem
from scrapy import Request
from scrapy.selector import Selector 
import json

#---------------------------------------------------------------------------

link = 'http://192.168.100.199:10011/api/MobileService/SetNumber?SetNumberPara={%22AssetsId%22:%2200bb7839-5e8f-49f5-a5ca-bc530de9cdc1%22,%22Number%22:%22123123%22,%22Type%22:%221%22,%22UserId%22:%226adefbfb-9829-45c5-9bd4-f7028c7553dc%22}'

def buildArray():
	arr = []
	for i in range(0,10):
		arr.append(link)
	return arr
	
print(buildArray())


class ZwwSpider(scrapy.Spider):
	name = "zww"
	allowed_domains = [""]
	start_urls = buildArray 
		
	def parse(self,response):
		print(response)
		

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
