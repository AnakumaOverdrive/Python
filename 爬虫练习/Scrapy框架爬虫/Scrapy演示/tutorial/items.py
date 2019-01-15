# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title = scrapy.Field()
	price = scrapy.Field()
	url = scrapy.Field()
	product_id = scrapy.Field()
	number = scrapy.Field()
    
class ClassifyItem(scrapy.Item):
	url = scrapy.Field()
	itemName = scrapy.Field()

class CqgpNoticesItem(scrapy.Item):
	id = scrapy.Field()
	noticeType = scrapy.Field()
	creatorOrgName = scrapy.Field()
	issueTime = scrapy.Field()
	districtName = scrapy.Field()
	title = scrapy.Field()
	projectDirectoryName = scrapy.Field()
	projectPurchaseWay = scrapy.Field()
	buyerName = scrapy.Field()
	agentName = scrapy.Field()
	openBidTime = scrapy.Field()
	
class CqgpNoticesDetailsItem(scrapy.Item):
	title = scrapy.Field()
	projectPurchaseWay = scrapy.Field()
	issueTime = scrapy.Field()
	noticeType = scrapy.Field()
		
class cqgpDisclosuresItem(scrapy.Item):
	id = scrapy.Field()
	creator = scrapy.Field()
	creatorOrgName = scrapy.Field()
	createTime = scrapy.Field()
	title = scrapy.Field()
	buyerName = scrapy.Field()
	publicityTime = scrapy.Field()
	agentName = scrapy.Field()
	approvalName = scrapy.Field()
	state = scrapy.Field()
	auditResult = scrapy.Field()
	
class cqgpDisclosuresDetailsItem(scrapy.Item):
	id = scrapy.Field()
	publicityTime = scrapy.Field()
	title = scrapy.Field()
	attachments = scrapy.Field()
	auditResult = scrapy.Field()

