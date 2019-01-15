# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title = scrapy.Field()
	link = scrapy.Field()
	desc = scrapy.Field()
	
class MyItem(scrapy.Item):
	id = scrapy.Field()
	name = scrapy.Field()
	description = scrapy.Field()
	
class CcpgItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
	addtime = scrapy.Field()

class CcpgDetailItem(scrapy.Item):
	link = scrapy.Field()
	content = scrapy.Field()