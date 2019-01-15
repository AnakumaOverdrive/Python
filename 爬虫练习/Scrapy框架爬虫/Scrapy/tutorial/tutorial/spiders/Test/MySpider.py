import scrapy
from tutorial.items import MyItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
	#定义spider名字 必须
	name = "mydmoz"
	
	#包含了spider允许爬取的域名（domain）列表（列表）。当 OffsiteMiddleware启用时，域名不在列表中的Url不会被跟进
	allowed_domains = ["dmoz.org"]
	
	#Url列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。
	start_urls = [
		"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
	]

	#一个包含一个(或多个) Rule 对象的集合(list)。 每个 Rule 对爬取网站的动作定义了特定表现。
	rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

	def parse_item(self, response):
		self.log('Hi, this is an item page! %s' % response.url)
		item = MyItem()
		item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
		item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
		item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
		return item
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	