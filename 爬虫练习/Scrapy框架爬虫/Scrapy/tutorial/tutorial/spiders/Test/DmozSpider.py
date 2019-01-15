import scrapy
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
	#定义spider名字 必须
	name = "dmoz"
	
	#包含了spider允许爬取的域名（domain）列表（列表）。当 OffsiteMiddleware启用时，域名不在列表中的Url不会被跟进
	allowed_domains = ["dmoz11.org"]
	
	#Url列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。
	start_urls = [
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
	]

	#start_requests() 该方法必须返回一个可迭代对象。钙对象包含了Spider用于爬取的第一个Request
	
	#make_requests_from_url(url) 该方法接受Url并返回用户爬取的Request对象。该方法在初始化request时被start_requests()调用，也被用于转化url为request
	
	#当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。
	def parse(self, response):
		self.log('A response from %s just arrived!' % response.url)
		for sel in response.xpath('//ul/li'):
			item = DmozItem()
			item['title'] = sel.xpath('a/text()').extract()
			item['link'] = sel.xpath('a/@href').extract()
			item['desc'] = sel.xpath('text()').extract()
			yield item
	
	#log(message[, level, component]) 使用 scrapy.log.msg() 方法记录(log)message。 log中自动带上该spider的 name 属性。
	
	#closed(reason) 当spider关闭时，该函数被调用。方法提供了一个替代调用signals.connect()来监听 spider_closed 信号的快捷方式。
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	